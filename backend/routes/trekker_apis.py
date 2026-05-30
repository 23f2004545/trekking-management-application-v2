from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import db
from controller.models import User, Trek, Booking , MedicalRecord
from controller.decorators import trekker_required
from datetime import datetime, timezone
import os

trekker_bp = Blueprint('trekker', __name__)

# ==========================================================================
# 1. PROFILE MANAGEMENT 
# ==========================================================================

@trekker_bp.route('/profile', methods=['GET'])
@jwt_required()
@trekker_required
def get_profile_data():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Formats timestamps to match the UI visual parameters cleanly
    created_formatted = user.created_at.strftime("%B %d, %Y") 
    
    # Calculate a simple human-readable delta for last login matrix tracking
    last_login_str = "Just now"
    if user.last_login_at:
        delta = datetime.now(timezone.utc) - user.last_login_at.replace(tzinfo=timezone.utc)
        if delta.seconds < 60:
            last_login_str = "Seconds ago"
        elif delta.seconds < 3600:
            last_login_str = f"{delta.seconds // 60} minutes ago"
        else:
            last_login_str = user.last_login_at.strftime("%Y-%m-%d %H:%M")

    return make_response(jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "contact": user.contact,
        "is_active": user.is_active,
        "blacklisted": user.blacklisted, # Fallback safety check
        "created_at": created_formatted,
        "last_login_at": last_login_str,
        "profile_pic": user.profile_pic 
    }), 200)


@trekker_bp.route('/profile', methods=['PATCH'])
@jwt_required()
@trekker_required
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form     
    
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
        
    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file and file.filename != '':
            # Secure file names safely to prevent path injection attacks
            filename = f"user_{user.id}_{os.path.basename(file.filename)}"
            save_path = os.path.join('static/' , 'Profile_pics', filename)
            
            # Ensure folder structure exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)

            # Store the serving endpoint static assets path inside the database column
            user.profile_pic = f"/static/Profile_pics/{filename}"
            
    try:
        db.session.commit()
        return make_response(jsonify({
            "message": "Profile metrics modified successfully.",
            "user": {
                "name": user.name, 
                "contact": user.contact, 
                "email": user.email,
                "profile_pic": user.profile_pic
            }
        }), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Database commit failure: {str(e)}"}), 500)


# ==========================================================================
# 2. MEDICAL TELEMETRY MATRIX MANAGEMENT (GET / POST)
# ==========================================================================


@trekker_bp.route('/medical', methods=['GET'])
@jwt_required()
@trekker_required
def get_medical_record():
    user_id = get_jwt_identity()
    record = MedicalRecord.query.filter_by(trekker_id=user_id).first()
    
    if not record:
        return make_response(jsonify({"message": "No medical record found." , "has_data": False}), 404)
        
    return make_response(jsonify({
        "has_data": True,
        "blood_group": record.blood_group,
        "diagonisis": record.diagonisis,
        "allergies": record.allergies,
        "medications": record.medications,
        "emergency_name": record.emergency_name,
        "emergency_phone": record.emergency_contact,
        "emergency_relation": record.emergency_relation,
        "updated_at": record.updated_at.strftime("%b %d, %Y %H:%M") 
    }), 200)


@trekker_bp.route('/medical', methods=['POST'])
@jwt_required()
@trekker_required
def save_medical_record():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    emergency_name = data.get('emergency_name', '').strip()
    emergency_phone = data.get('emergency_phone', '').strip()
    
    if not emergency_name or not emergency_phone:
        return make_response(jsonify({"message": "Emergency contact name and phone integers are mandatory."}), 400)
        
    if len(emergency_phone) != 10 or not emergency_phone.isdigit():
        return make_response(jsonify({"message": "Emergency phone must contain exactly 10 digits."}), 400)

    record = MedicalRecord.query.filter_by(trekker_id=user_id).first()
    
    if not record:
        record = MedicalRecord(
                    trekker_id=user_id,
                    blood_group=data.get('blood_group', '').strip().upper(),
                    diagonisis=data.get('diagonisis', '').strip(),
                    allergies=data.get('allergies', '').strip(),
                    medications=data.get('medications', '').strip(),
                    emergency_name=emergency_name.title(),
                    emergency_contact=emergency_phone,
                    emergency_relation=data.get('emergency_relation', '').strip().title()
                )
        db.session.add(record)
        
    record.blood_group = data.get('blood_group', '').strip().upper()
    record.diagonisis = data.get('diagonisis', '').strip()
    record.allergies = data.get('allergies', '').strip()
    record.medications = data.get('medications', '').strip()
    record.emergency_name = emergency_name.title()
    record.emergency_contact = emergency_phone
    record.emergency_relation = data.get('emergency_relation', '').strip().title()
    
    try:
        db.session.commit()
        return make_response(jsonify({"message": "Medical telemetry metrics committed successfully."}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Database mutation failed: {str(e)}"}), 500)


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