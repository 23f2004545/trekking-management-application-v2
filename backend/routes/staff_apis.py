from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import db,cache,bcrypt
from controller.models import Trek, Booking, User , StaffProfile ,TrekImage 
from controller.decorators import staff_required
from routes.utils_apis import create_notification , log_system_audit
from datetime import datetime, timezone
from sqlalchemy import func,case
from services.cloudinary_service import upload_image
from services.demo_service import is_demo_user, is_demo_target
import os , random


trek_staff_bp = Blueprint('trek_staff', __name__)

# ==========================================================================
# 1. STAFF DASHBOARD OVERVIEW (Assigned Treks & Trekkers Metrics)
# ==========================================================================

@trek_staff_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@staff_required
def get_staff_dashboard_stats():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    staff = user.staff_profile
    if not staff:
        return make_response(jsonify({"message": "Staff profile constraints not found."}), 403)
    
    is_onboarded = staff.emergency_contact != "1234567890"

    current_date = datetime.now(timezone.utc).date()
    
    # Isolate treks assigned explicitly to this guide
    assigned_treks = Trek.query.filter_by(assigned_staff_id=staff.user_id).all()
    assigned_trek_ids = [t.trek_id for t in assigned_treks]
    
    # Calculate active parameters
    active_routes_count = len([t for t in assigned_treks if t.status in ['Open', 'Ongoing']])
    
    # Calculate upcoming explorers across all assigned treks
    upcoming_explorers = db.session.query(func.sum(Booking.number_of_persons))\
        .filter(Booking.trek_id.in_(assigned_trek_ids), Booking.status == 'Booked').scalar() or 0

    # Determine the very next departure date
    upcoming_treks = [t for t in assigned_treks if t.start_date.date() >= current_date]
    upcoming_treks.sort(key=lambda x: x.start_date.date())
    next_deployment = upcoming_treks[0].start_date.strftime("%b %d, %Y") if upcoming_treks else "No pending deployments"

    # Grab a quick summary of active/upcoming treks for the dashboard view
    active_roster = []
    for t in upcoming_treks[:4]:  # Top 4 most immediate
        booked_count = db.session.query(func.sum(Booking.number_of_persons))\
            .filter_by(trek_id=t.trek_id, status='Booked').scalar() or 0
            
        active_roster.append({
            "trek_id": t.trek_id,
            "name": t.trek_name,
            "status": t.status,
            "start_date": t.start_date.strftime("%b %d"),
            "registered_count": booked_count,
            "capacity": t.available_slots + booked_count # Total capacity computation
        })

    return make_response(jsonify({
        "is_onboarded": is_onboarded,
        "active_routes": active_routes_count,
        "total_explorers": upcoming_explorers,
        "next_deployment": next_deployment,
        "active_roster": active_roster,
        "blacklisted": user.blacklisted
    }), 200)

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
            new_url = upload_image(file, folder="apex/avatars", filename_prefix=f"staff_{user.id}", local_subfolder="Profile_pics")
            if new_url:
                user.profile_pic = new_url
            
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
    
    if record.specialization == "Pending":
        return make_response(jsonify({"has_data": False}), 200)
        
    return make_response(jsonify({
        "has_data": True,
        "specialization": record.specialization,
        "experience_years": record.experience_years,
        "certifications": record.certification,
        "status": record.status,
        "emergency_contact": record.emergency_contact,
        "bio": record.bio,
        "updated_at" : record.updated_at.strftime("%b %d, %Y %H:%M")
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

    record = StaffProfile.query.filter_by(user_id=user_id).first()
    
    if not record:
        record = StaffProfile(
                    user_id=user_id,
                    specialization=data.get('specialization', '').strip(),
                    experience_years=int(data.get('experience_years', 0)),
                    certification=data.get('certifications', '').strip(),
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
# 3. MANAGE ASSIGNED ROUTES & STATUS LIFECYCLES
# ==========================================================================
@trek_staff_bp.route('/treks', methods=['GET'])
@jwt_required()
@staff_required
def get_staff_assigned_treks():
    
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    staff = user.staff_profile
    if not staff:
        return make_response(jsonify({"message": "Staff profile constraints not found."}), 403)

    # Priority Sorting: Ongoing (1) -> Open (2) -> Pending (3) -> Completed (4) -> Cancelled (5)
    status_priority = case(
        (Trek.status == 'Ongoing', 1),
        (Trek.status == 'Open', 2),
        (Trek.status == 'Pending', 3),
        (Trek.status == 'Completed', 4),
        (Trek.status == 'Cancelled', 5),
        else_=6
    )

    treks = Trek.query.filter_by(assigned_staff_id=staff.user_id)\
        .order_by(status_priority, Trek.start_date.asc()).all()

    results = []
    for t in treks:
        
        staff_user = User.query.get(t.assigned_staff_id) if t.assigned_staff_id else None
        images = TrekImage.query.filter_by(trek_id=t.trek_id).all()
        
        results.append({
            "trek_id": t.trek_id,
            "trek_name": t.trek_name,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration_days": t.duration_days ,
            "available_slots": t.available_slots,
            "status": t.status,
            "start_date": t.start_date.strftime("%Y-%m-%d") ,
            "end_date": t.end_date.strftime("%Y-%m-%d") ,
            "max_altitude": getattr(t, 'max_altitude', 0.0),
            "price_per_person": getattr(t, 'price_per_person', 0.0),
            "description": getattr(t, 'description', ""),
            "created_at": t.created_at.strftime("%Y-%m-%d") ,
            "updated_at": t.updated_at.strftime("%Y-%m-%d") ,
            "image_url": images[0].image_url if images else "/static/Treks/default_trek.jpeg",
            "assigned_staff": {
                "id": staff_user.id if staff_user else None,
                "name": staff_user.name if staff_user else "Unassigned Guide"
            }
        })
        
    return make_response(jsonify(results), 200)


@trek_staff_bp.route('/treks/<int:trek_id>/update-field-data', methods=['PATCH'])
@jwt_required()
@staff_required
def update_trek_field_data(trek_id):
    
    from tasks import dispatch_cancellation_email , dispatch_completion_email
    
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    staff = user.staff_profile
    if not staff:
        return make_response(jsonify({"message": "Staff profile constraints not found."}), 403)
    
    trek = Trek.query.get_or_404(trek_id)

    # Security Guard: Prevent cross-staff manipulation
    if trek.assigned_staff_id != staff.user_id:
        return make_response(jsonify({"message": "Unauthorized: Route belongs to another guide."}), 403)

    if is_demo_user(user) and not is_demo_target(trek):
        return make_response(jsonify({
            "message": "[SIMULATED] Field update executed in simulation mode. Live route data was preserved.",
            "simulated": True
        }), 200)

    data = request.get_json()
    status_changed = False
    new_status = data.get('status')
    abort_reason = data.get('cancellation_reason')
    
    # Update Lifecycle Status
    if new_status:
        allowed_statuses = ['Open', 'Ongoing', 'Closed', 'Completed' , 'Cancelled']
        if new_status in allowed_statuses and trek.status != new_status:
            trek.status = new_status
            status_changed = True

            
    # Update Live Slot Capacities (e.g., if a tent breaks or weather limits capacity)
    if 'available_slots' in data:
        trek.available_slots = int(data['available_slots'])
        
    # Update Trail Description (To provide live field notes/warnings)
    if 'description' in data:
        trek.description = data['description'].strip()

    trek.updated_at = db.func.current_timestamp()

    if status_changed:
        # All currently active bookings for this specific trek
        active_bookings = Booking.query.filter_by(trek_id=trek.trek_id, status='Booked').all()
        if new_status == 'Cancelled':
                trek.available_slots = 25
                db.session.commit()
                log_system_audit("CANCEL", f"Trek #{trek_id} halted by Staff {user.email}.", "danger")
        for booking in active_bookings:
            if new_status == 'Completed':
                booking.status = 'Completed'
                booking.updated_at = datetime.now(timezone.utc)
                # Fire Completion Email
                if not is_demo_user(user):
                    dispatch_completion_email.delay(
                        booking.user.email, 
                        booking.user.name, 
                        trek.trek_name, 
                        trek.duration_days, 
                        trek.max_altitude
                    )
                
            elif new_status == 'Cancelled':
                booking.status = 'Cancelled'
                booking.payment_status = 'Refunded' # Trigger refund pipeline state
                trek.cancellation_reason = f"Guide : {abort_reason}"
                trek.cancelled_at = datetime.now(timezone.utc)
                booking.updated_at = datetime.now(timezone.utc)
                # Fire Cancellation Email
                if not is_demo_user(user):
                    dispatch_cancellation_email.delay(
                        booking.user.email, 
                        booking.user.name, 
                        trek.trek_name, 
                        trek.duration_days, 
                        abort_reason, 
                        "Field Commander" 
                    )
                create_notification(booking.user_id, f"Your trek ({trek.trek_name}) has been CANCELLED by Staff", "danger")

    try:
        db.session.commit()
        admin = User.query.filter_by(name='admin').first()
        create_notification(admin.id, f"{user.name} has modified TREK : {trek.trek_name}", "warning")
        try:
            cache.clear()
        except Exception:
            pass
        return make_response(jsonify({
            "message": "Field operational parameters synchronized.", 
            "new_status": trek.status
        }), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Transaction aborted: {str(e)}"}), 500)


# ==========================================================================
# 4. TACTICAL PARTICIPANT MANIFEST
# ==========================================================================

@trek_staff_bp.route('/participants', methods=['GET'])
@jwt_required()
@staff_required
def get_trail_manifests():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    staff = user.staff_profile
    if not staff:
        return make_response(jsonify({"message": "Staff profile constraints not found."}), 403)
    
    # Fetch active bookings for treks assigned to this staff member
    bookings = Booking.query.join(Trek).filter(
        Trek.assigned_staff_id == staff.user_id,
        Booking.status == 'Booked',
        Trek.status.in_(['Open', 'Ongoing'])
    ).order_by(Trek.start_date.asc()).all()

    # Group payload logically by Trek ID so the frontend can filter easily
    manifest = {}
    for b in bookings:
        t_id = b.trek_id
        if t_id not in manifest:
            manifest[t_id] = {
                "trek_name": b.trek.trek_name,
                "start_date": b.trek.start_date.strftime("%b %d, %Y"),
                "status": b.trek.status,
                "explorers": []
            }
        
        manifest[t_id]["explorers"].append({
            "booking_id": b.booking_id,
            "name": b.user.name,
            "contact": b.user.contact,
            "headcount": b.number_of_persons,
            "medical_notes": getattr(b, 'instructions', None) or "No special instructions logged.", # Reusing text field for payload demonstration
            "payment_status": b.payment_status,
            "medical_record_exists": True if b.user.medical_record else False,
            "emergency_name": b.user.medical_record.emergency_name if b.user.medical_record else 'N/A' ,
            "emergency_contact": b.user.medical_record.emergency_contact if b.user.medical_record else 'N/A' ,
            "blood_group": b.user.medical_record.blood_group if b.user.medical_record else 'N/A',
            "allergies" : b.user.medical_record.allergies if b.user.medical_record else None,
            "medications" : b.user.medical_record.medications if b.user.medical_record else None
        })
                
    # Convert grouped dict to an array list
    return make_response(jsonify(list(manifest.values())), 200)


# ==========================================================================
# 5. Password Reset via OTP Workflow
# ==========================================================================

@trek_staff_bp.route('/request-password-otp', methods=['POST'])
@jwt_required()
@staff_required
def request_password_otp():
    """Generates a 6-digit OTP, stores it in Redis for 5 mins, and emails it via Celery."""
    from tasks import send_otp_email
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    data = request.get_json(silent=True) or {}
    demo_delivery_email = None
    if is_demo_user(user):
        demo_delivery_email = data.get('demo_delivery_email')

    # Generate 6 digit string
    otp_code = str(random.randint(100000, 999999))
    
    # Save to Redis Cache with a 300 second (5 min) Time-To-Live
    cache.set(f"password_otp_{user_id}", otp_code, timeout=300)
    
    # Trigger Celery to send email asynchronously
    send_otp_email.delay(user.email, user.name, otp_code, demo_delivery_email=demo_delivery_email)
    
    return make_response(jsonify({"message": "OTP generated and dispatched to your email."}), 200)


@trek_staff_bp.route('/reset-password', methods=['PATCH'])
@jwt_required()
@staff_required
def reset_password_with_otp():
    """Validates the Redis OTP and updates the password."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    submitted_otp = data.get('otp')
    new_password = data.get('new_password')
    
    if not submitted_otp or not new_password:
        return make_response(jsonify({"message": "OTP and New Password are required."}), 400)
        
    # Retrieve OTP from Redis
    stored_otp = cache.get(f"password_otp_{user_id}")
    
    if not stored_otp:
        return make_response(jsonify({"message": "OTP has expired or was not requested."}), 400)
        
    if str(stored_otp) != str(submitted_otp):
        return make_response(jsonify({"message": "Invalid OTP code provided."}), 400)
        
    # OTP is valid! Hash new password and save
    user = User.query.get(user_id)
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    create_notification(user.id, "Your security key was successfully updated.", "success")
    
    # Crucial: Delete the OTP from Redis so it cannot be reused
    cache.delete(f"password_otp_{user_id}")
    
    return make_response(jsonify({"message": "Security key successfully updated."}), 200)
