from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import db
from controller.models import Trek, Booking, User
from controller.decorators import staff_required

staff_bp = Blueprint('staff', __name__)

# ==========================================================================
# 1. STAFF DASHBOARD OVERVIEW (Assigned Treks & Trekkers Metrics)
# ==========================================================================
@staff_bp.route('/my-treks', methods=['GET'])
@jwt_required()
@staff_required
def get_assigned_treks():
    """Fetch only the treks assigned to the logged-in staff member along with registration metrics."""
    staff_id = int(get_jwt_identity())
    
    assigned_treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()
    
    results = []
    for trek in assigned_treks:
        # Count active participant bookings attached to this specific trek row
        registered_count = Booking.query.filter_by(trek_id=trek.id).filter(Booking.status != 'Cancelled').count()
        
        results.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status, # Pending / Approved / Open / Closed / Completed
            "start_date": trek.start_date.strftime("%Y-%m-%d"),
            "end_date": trek.end_date.strftime("%Y-%m-%d"),
            "registered_trekkers_count": registered_count
        })
        
    return make_response(jsonify(results), 200)

# ==========================================================================
# 2. UPDATE ACTIVE TREK PARAMETERS & STATUS LIFECYCLE
# ==========================================================================
@staff_bp.route('/treks/<int:trek_id>/operations', methods=['PATCH'])
@jwt_required()
@staff_required
def update_trek_operations(trek_id):
    """Allows assigned staff to adjust slots, toggle status boundaries (Open/Closed), or transition the trek lifecycle."""
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get_or_404(trek_id)
    
    # ISOLATION PRIVILEGE GUARD: Ensure only the assigned staff can modify this trek record
    if trek.assigned_staff_id != staff_id:
        return make_response(jsonify({"message": "Operation Denied: You are not assigned to manage this trek route."}), 403)
        
    data = request.get_json()
    
    # 1. Optional Slot Adjustment
    if 'available_slots' in data:
        trek.available_slots = int(data.get('available_slots'))
        
    # 2. Optional Status Updates (Open / Closed / Ongoing / Completed)
    if 'status' in data:
        new_status = data.get('status')
        # Simple constraint check
        if new_status in ["Pending", "Approved", "Open", "Closed", "Completed"]:
            trek.status = new_status
        else:
            return make_response(jsonify({"message": "Invalid tracking status state configuration."}), 400)
            
    try:
        db.session.commit()
        return make_response(jsonify({"message": f"Trek parameters for '{trek.name}' updated successfully."}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Database mutation failed: {str(e)}"}), 500)

# ==========================================================================
# 3. MANAGE & VIEW ACTIVE PARTICIPANT REGISTRATION DETAILS
# ==========================================================================
@staff_bp.route('/treks/<int:trek_id>/participants', methods=['GET'])
@jwt_required()
@staff_required
def get_trek_participants(trek_id):
    """Retrieve the explicit details of all registered trekkers signed up for an assigned tracking coordinate."""
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get_or_404(trek_id)
    
    if trek.assigned_staff_id != staff_id:
        return make_response(jsonify({"message": "Operation Denied: You are not assigned to manage this trek route."}), 403)
        
    # Fetch all active bookings bound to this trek ID code
    bookings = Booking.query.filter_by(trek_id=trek.id).filter(Booking.status != 'Cancelled').all()
    
    participant_list = []
    for b in bookings:
        participant_list.append({
            "booking_id": b.id,
            "booking_date": b.booking_date.strftime("%Y-%m-%d"),
            "booking_status": b.status, # Booked / Completed
            "trekker_id": b.user.id,
            "trekker_name": b.user.name,
            "trekker_email": b.user.email,
            "trekker_contact": b.user.contact
        })
        
    return make_response(jsonify({
        "trek_name": trek.name,
        "participants": participant_list
    }), 200)