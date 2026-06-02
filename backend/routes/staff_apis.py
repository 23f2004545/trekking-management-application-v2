from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import db
from controller.models import Trek, Booking, User , StaffProfile
from controller.decorators import staff_required
from datetime import datetime, timezone
import os

trek_staff_bp = Blueprint('trek_staff', __name__)

# ==========================================================================
# 1. STAFF DASHBOARD OVERVIEW (Assigned Treks & Trekkers Metrics)
# ==========================================================================

@trek_staff_bp.route('/my-treks', methods=['GET'])
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
# 2. PROFILE MANAGEMENT 
# ==========================================================================

@trek_staff_bp.route('/profile', methods=['GET'])
@jwt_required()
@staff_required
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
    
@trek_staff_bp.route('/profile', methods=['PATCH'])
@jwt_required()
@staff_required
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
# 3. STAFF PROFILE MATRIX MANAGEMENT (GET / POST)
# ==========================================================================

@trek_staff_bp.route('/staff', methods=['GET'])
@jwt_required()
@staff_required
def get_staff_profile():
    user_id = get_jwt_identity()
    record = StaffProfile.query.filter_by(user_id=user_id).first()
    
    if not record:
        return make_response(jsonify({"message": "No staff profile found." , "has_data": False}), 404)
        
    return make_response(jsonify({
        "has_data": True,
        "specialization": record.specialization,
        "experience_years": record.experience_years,
        "certifications": record.certification,
        "status": record.status,
        "emergency_contact": record.emergency_contact,
        "bio": record.bio
        # "updated_at": record.updated_at.strftime("%b %d, %Y %H:%M") 
    }), 200)


@trek_staff_bp.route('/staff', methods=['POST'])
@jwt_required()
@staff_required
def save_staff_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    emergency_contact = data.get('emergency_contact', '').strip()
    
    if not emergency_contact:
        return make_response(jsonify({"message": "Emergency contact is mandatory."}), 400)
        
    if len(emergency_contact) != 10 or not emergency_contact.isdigit():
        return make_response(jsonify({"message": "Emergency phone must contain exactly 10 digits."}), 400)

    record = StaffProfile.query.filter_by(staff_id=user_id).first()
    
    if not record:
        record = StaffProfile(
                    user_id=user_id,
                    specialization=data.get('specialization', '').strip(),
                    experience_years=int(data.get('experience_years', 0)),
                    certification=data.get('certifications', '').strip(),
                    status=data.get('status', '').strip(),
                    emergency_contact=emergency_contact,
                    bio=data.get('bio', '').strip()
                )
        db.session.add(record)
        
    record.specialization = data.get('specialization', '').strip()
    record.experience_years = int(data.get('experience_years', 0))
    record.certification = data.get('certifications', '').strip()
    record.status = data.get('status', '').strip()
    record.emergency_contact = emergency_contact
    record.bio = data.get('bio', '').strip()
    
    try:
        db.session.commit()
        return make_response(jsonify({"message": "Staff profile updated successfully."}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Database mutation failed: {str(e)}"}), 500)


# ==========================================================================
# 3. UPDATE ACTIVE TREK PARAMETERS & STATUS LIFECYCLE
# ==========================================================================
@trek_staff_bp.route('/treks/<int:trek_id>/operations', methods=['PATCH'])
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
# 4. MANAGE & VIEW ACTIVE PARTICIPANT REGISTRATION DETAILS
# ==========================================================================
@trek_staff_bp.route('/treks/<int:trek_id>/participants', methods=['GET'])
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