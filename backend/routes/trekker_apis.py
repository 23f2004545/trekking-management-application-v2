from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import db
from controller.models import User, Trek, Booking
from controller.decorators import trekker_required
from datetime import datetime, timezone

trekker_bp = Blueprint('trekker', __name__)

# ==========================================================================
# 1. PROFILE MANAGEMENT (Targeted Field Mutations)
# ==========================================================================
@trekker_bp.route('/profile', methods=['PATCH'])
@jwt_required()
@trekker_required
def update_profile():
    """Allows a trekker to update single fields like name or contact reactively."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    
    if 'name' in data:
        name_val = data.get('name').strip().title()
        if name_val.replace(" ", "").isalpha():
            user.name = name_val
        else:
            return make_response(jsonify({"message": "Name must contain only alphabetic characters."}), 400)
            
    if 'contact' in data:
        contact_val = data.get('contact').strip()
        if contact_val.isdigit() and len(contact_val) == 10:
            user.contact = contact_val
        else:
            return make_response(jsonify({"message": "Contact number must be exactly 10 digits."}), 400)
            
    db.session.commit()
    return make_response(jsonify({
        "message": "Profile updated successfully.",
        "user": {"name": user.name, "contact": user.contact, "email": user.email}
    }), 200)

# ==========================================================================
# 2. DISCOVER, SEARCH, & FILTER OPEN TREKS
# ==========================================================================
@trekker_bp.route('/treks', methods=['GET'])
@jwt_required()
@trekker_required
def get_discoverable_treks():
    """Fetch approved/open treks with optional parameters for difficulty, location, and duration."""
    # Trekkers should primarily discover treks that are explicitly marked as 'Open'
    query_pipeline = Trek.query.filter_by(status='Open')
    
    # Extract query filter arguments
    difficulty = request.args.get('difficulty') # Easy / Moderate / Hard
    location = request.args.get('location')
    max_duration = request.args.get('duration') # Max days slider/input

    if difficulty:
        query_pipeline = query_pipeline.filter_by(difficulty=difficulty)
    if location:
        query_pipeline = query_pipeline.filter(Trek.location.ilike(f"%{location}%"))
    if max_duration:
        query_pipeline = query_pipeline.filter(Trek.duration <= int(max_duration))
        
    treks = query_pipeline.all()
    
    results = [{
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration": t.duration,
        "available_slots": t.available_slots,
        "start_date": t.start_date.strftime("%Y-%m-%d"),
        "end_date": t.end_date.strftime("%Y-%m-%d")
    } for t in treks]
    
    return make_response(jsonify(results), 200)

# ==========================================================================
# 3. CORE SECURE BOOKING SYSTEM & CRITICAL VALIDATIONS
# ==========================================================================
@trekker_bp.route('/bookings', methods=['POST'])
@jwt_required()
@trekker_required
def book_trek_slot():
    """Creates a booking record with atomic validation safeguards against overbooking/duplicates."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    trek_id = data.get('trek_id')
    
    if not trek_id:
        return make_response(jsonify({"message": "Trek identification coordinate required."}), 400)
        
    # Query target route under a database session state lock if executing concurrent scales
    trek = Trek.query.get_or_404(trek_id)
    
    # GUARD 1: Validate trek lifecycle status boundary condition
    if trek.status != 'Open':
        return make_response(jsonify({"message": "Booking denied: This route ecosystem is currently closed or completed."}), 400)
        
    # GUARD 2: Prevent duplicate active bookings for the same trek by the same user
    existing_active_booking = Booking.query.filter_by(user_id=user_id, trek_id=trek_id).filter(Booking.status == 'Booked').first()
    if existing_active_booking:
        return make_response(jsonify({"message": "Booking denied: You already hold a secured active slot for this expedition."}), 400)
        
    # GUARD 3: Prevent overbooking beyond physical route capacity constraints
    if trek.available_slots <= 0:
        return make_response(jsonify({"message": "Booking denied: Base camp slots are completely full."}), 400)
        
    try:
        # Deduct slot reservation dynamically
        trek.available_slots -= 1
        
        new_booking = Booking(
            user_id=user_id,
            trek_id=trek_id,
            booking_date=datetime.now(timezone.utc),
            status='Booked' # Default state tracking label
        )
        
        db.session.add(new_booking)
        db.session.commit()
        return make_response(jsonify({"message": "Base camp slot secured successfully! Expedition booked.", "booking_id": new_booking.id}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Transaction aborted: {str(e)}"}), 500)

# ==========================================================================
# 4. TRACK ACTIVE BOOKINGS & HISTORICAL RECORDS
# ==========================================================================
@trekker_bp.route('/bookings/history', methods=['GET'])
@jwt_required()
@trekker_required
def get_user_trekking_history():
    """Retrieve only the personal historical trekking database lines for the logged-in trekker user."""
    user_id = get_jwt_identity()
    
    # Pull all records attached to this single trekker account mapping
    user_bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()
    
    history_cards = []
    for b in user_bookings:
        # Cross-reference the master trek lifecycle status to determine user visibility parameters
        history_cards.append({
            "booking_id": b.id,
            "booking_date": b.booking_date.strftime("%Y-%m-%d"),
            "booking_status": b.status, # Booked / Cancelled / Completed
            "trek_id": b.trek.id,
            "trek_name": b.trek.name,
            "location": b.trek.location,
            "duration": b.trek.duration,
            "difficulty": b.trek.difficulty,
            "trek_status": b.trek.status # Shows if it's currently Ongoing / Completed on the trail
        })
        
    return make_response(jsonify(history_cards), 200)


@trekker_bp.route('/bookings/<int:booking_id>/cancel', methods=['PATCH'])
@jwt_required()
@trekker_required
def cancel_trek_booking(booking_id):
    """Allows users to safely cancel an active reservation and restore available slot counts."""
    user_id = int(get_jwt_identity())
    booking = Booking.query.get_or_404(booking_id)
    
    # ISOLATION PRIVILEGE GUARD
    if booking.user_id != user_id:
        return make_response(jsonify({"message": "Access Denied: Cannot cancel another trekker's payload."}), 403)
        
    if booking.status != 'Booked':
        return make_response(jsonify({"message": "This record is already finalized or cancelled."}), 400)
        
    try:
        booking.status = 'Cancelled'
        # Restore slot capacity value dynamically back to the parent trek map entity row
        booking.trek.available_slots += 1
        
        db.session.commit()
        return make_response(jsonify({"message": "Expedition registration cancelled successfully. Slots returned."}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Cancellation transaction error: {str(e)}"}), 500)