from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import db , cache , bcrypt
from controller.models import *
from controller.decorators import trekker_required
from routes.utils_apis import create_notification , log_system_audit
from datetime import datetime, timezone 
import os , random

trekker_bp = Blueprint('trekker', __name__)


# ==========================================================================
# 1. TREKKER DASHBOARD STATS & GAMIFICATION
# ==========================================================================

@trekker_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_trekker_dashboard_stats():
    user_id = get_jwt_identity()
    current_date = datetime.now(timezone.utc).date()
    user = User.query.get(user_id)
    
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    secured_slots = 0
    completed_paths = 0
    total_altitude = 0.0
    altitude_history = []

    for b in bookings:
        if b.trek.status == 'Open' and b.trek:
            if b.trek.start_date.date() > current_date or (b.trek.start_date.date() <= current_date <= b.trek.end_date.date()):
                secured_slots += 1
            elif b.trek.end_date.date() < current_date:
                completed_paths += 1
                alt = b.trek.max_altitude or 0.0
                total_altitude += alt
                altitude_history.append({
                    "trek_name": b.trek.trek_name,
                    "altitude": alt,
                    "date": b.trek.end_date.strftime("%b %d")
                })
        elif b.trek.status == 'Completed' and b.trek:
            completed_paths += 1
            alt = b.trek.max_altitude or 0.0
            total_altitude += alt
            altitude_history.append({
                "trek_name": b.trek.trek_name,
                "altitude": alt,
                "date": b.trek.end_date.strftime("%b %d")
            })

    # Sort history chronologically for the chart
    altitude_history.reverse()

    # Generate live FOMO simulation data
    recent_activity = [
        {"user": "Aman V.", "trek": "Rohtang Pass", "action": "secured 2 slots"},
        {"user": "Priya S.", "trek": "Hampta Pass", "action": "completed the trail"},
        {"user": "Rahul K.", "trek": "Solang Valley", "action": "booked the final slot!"},
        {"user": "Neha M.", "trek": "Bhrigu Lake", "action": "left a 5-star review"}
    ]
    random.shuffle(recent_activity)

    return make_response(jsonify({
        "secured_slots": secured_slots,
        "completed_paths": completed_paths,
        "total_altitude": int(total_altitude),
        "alerts": "ALL CLEAR",
        "chart_data": altitude_history,
        "fomo_events": recent_activity[:3], # Send 3 random events
        "blacklisted": user.blacklisted 
    }), 200)
    

# ==========================================================================
# 2. PROFILE MANAGEMENT 
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


@trekker_bp.route('/profile', methods=['PATCH' , 'DELETE'])
@jwt_required()
@trekker_required
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    if request.method == 'DELETE':
        user.is_active = not user.is_active
        db.session.commit()
        log_system_audit("Deleted", f"User {user.email} deleted their account", "warning")
        return make_response(jsonify({"message": f"User's account deleted."}), 200)
    
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
# 3. MEDICAL TELEMETRY MATRIX MANAGEMENT (GET / POST)
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
# 4. TREKS MANAGEMENT
# ==========================================================================

@trekker_bp.route('/treks', methods=['GET'])
@jwt_required()
@trekker_required
@cache.cached(timeout=300, query_string=True) # Cache this endpoint for 5 minutes to optimize performance
def get_all_treks():
    
    query_pipeline = Trek.query.filter_by(status='Open')
    treks = Trek.query.filter_by(status='Open').order_by(Trek.created_at.desc()).all()
    
    results = []
    for t in treks:
        # Resolve assigned guide properties safely
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
    user = User.query.get(user_id)
    
    if not trek_id:
        return make_response(jsonify({"message": "Trek identification coordinate required."}), 400)
        
    # Query target route under a database session state lock if executing concurrent scales
    trek = Trek.query.get_or_404(trek_id)
    
    # Validate User is not blacklisted 
    if user.blacklisted:
        return make_response(jsonify({"message": "Booking denied: ACCOUNT BLACKLISTED "}), 400)
    
    # Validate trek lifecycle status boundary condition
    if trek.status != 'Open':
        return make_response(jsonify({"message": "Booking denied: This route ecosystem is currently closed or completed."}), 400)
        
    # Prevent duplicate active bookings for the same trek by the same user
    existing_active_booking = Booking.query.filter_by(user_id=user_id, trek_id=trek_id).filter(Booking.status == 'Booked').first()
    if existing_active_booking:
        return make_response(jsonify({"message": "Booking denied: You already hold a secured active slot for this expedition."}), 400)
        
    # Prevent overbooking beyond physical route capacity constraints
    if trek.available_slots <= 0:
        return make_response(jsonify({"message": "Booking denied: Base camp slots are completely full."}), 400)
    
    number_of_persons = data.get('adults') + data.get('children') + data.get('seniors')
    
    if number_of_persons > trek.available_slots:
        return make_response(jsonify({"message": "Booking denied: Not enough slots available."}), 400)
        
    try:
        # Deduct slot reservation dynamically
        trek.available_slots -= int(number_of_persons)
        
        new_booking = Booking(
            user_id=user_id,
            trek_id=trek_id,
            booking_date=datetime.now(timezone.utc),
            status='Booked' ,# Default state tracking label
            number_of_persons=number_of_persons,
            payment_method=data.get('payment_method'),
            total_amount=trek.price_per_person * number_of_persons,
            instructions=data.get('medical_instructions'),
            snapshot_start_date = trek.start_date,
            snapshot_end_date = trek.end_date,
            snapshot_duration_days = trek.duration_days, 
            snapshot_staff = trek.assigned_staff_id
        )
        
        db.session.add(new_booking)
        db.session.commit()
        create_notification(user.id, f"Successfully secured a slot for {trek.trek_name} trek", "success")
        return make_response(jsonify({"message": "Base camp slot secured successfully! Expedition booked.", "booking_id": new_booking.booking_id}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Transaction aborted: {str(e)}"}), 500)
    
    
@trekker_bp.route('/cancel_booking/<int:id>', methods=['PATCH'])
@jwt_required()
@trekker_required
def cancel_booking(id):
    
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    booking = Booking.query.get_or_404(id)
    booking.status = 'Cancelled'
    booking.payment_status = 'Refunded'
    booking.cancelled_at = datetime.now(timezone.utc)
    booking.updated_at = datetime.now(timezone.utc)
    booking.trek.available_slots -= booking.number_of_persons
    db.session.commit()
    
    log_system_audit("Cancelled", f"Booking cancelled by user {user.email}", "danger")
    return make_response(jsonify({"message": "Booking Cancelled"}), 200)

# ==========================================================================
# 4. TRACK ACTIVE BOOKINGS & HISTORICAL RECORDS
# ==========================================================================

@trekker_bp.route('/bookings', methods=['GET'])
@jwt_required()
@trekker_required
def get_bookings():
    """Retrieve personal booking records dynamically calculated for timeline states."""
    user_id = get_jwt_identity()
    user_bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()
    current_date = datetime.now(timezone.utc).date()
    
    treks = Trek.query.filter_by(status='Open').order_by(Trek.created_at.desc()).all()
    
    results = []
    for b in user_bookings:
        # Lifecycle Tracking Logic
        if b.trek.status == 'Completed':
            continue
        
        calc_status = b.status
        if b.status == 'Booked' and b.trek :
            if current_date < b.trek.start_date.date():
                calc_status = 'Upcoming'
            elif b.trek.start_date.date() <= current_date <= b.trek.end_date.date():
                calc_status = 'Ongoing'
            else:
                calc_status = 'Completed'
                
        if calc_status == 'Completed':
            continue

        # Extract First Trek Image
        trek_img = ""
        if b.trek and b.trek.images:
            trek_img = b.trek.images[0].image_url

        # Resolve Assigned Staff Guide
        staff_data = {"name": "Unassigned", "email": "N/A", "contact": "N/A"}
        if b.trek and b.trek.assigned_staff_id:
            staff_user = User.query.get(b.trek.assigned_staff_id)
            if staff_user:
                staff_data = {
                    "name": staff_user.name, 
                    "email": staff_user.email, 
                    "contact": staff_user.contact
                }

        results.append({
            "booking_id": b.booking_id,
            "trek_name": b.trek.trek_name if b.trek else "Deleted Route",
            "booking_date": b.booking_date.strftime("%B %d, %Y"),
            "booking_status": calc_status,
            "payment_status": b.payment_status,
            "duration_days": b.trek.duration_days if b.trek else 0,
            "total_people": b.number_of_persons,
            "trek_image": trek_img,
            "staff": staff_data
        })
        
    return make_response(jsonify(results), 200)

@trekker_bp.route('/history', methods=['GET'])
@jwt_required()
@trekker_required
def get_completed_history():
    user_id = get_jwt_identity()
    current_date = datetime.now(timezone.utc).date()
    
    user_bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()
    
    results = []
    for b in user_bookings:
        # Filter: Only process Completed routes
        is_past_date = b.trek and b.trek.end_date.date() < current_date
        if b.trek.status == 'Completed' or (b.status == 'Booked' and is_past_date):
            
            # Check for existing feedback
            user_review = Review.query.filter_by(user_id=user_id, trek_id=b.trek_id).first()
            reviews = Review.query.filter_by(trek_id=b.trek_id).all() 
            
            staff_rating_avg = None
            trek_rating_avg = None
            
            if hasattr(b.trek, 'reviews') and b.trek.reviews:
                trek_rating_avg = round(sum([r.trek_rating for r in b.trek.reviews]) / len(b.trek.reviews))

            if reviews :
                staff_rating_avg = round(sum([r.staff_rating for r in reviews]) / len(reviews))
            
            gallery = [img.image_url for img in b.trek.images] if b.trek.images else []
            
            price = b.total_amount / b.number_of_persons
            
            
            staff_info = {"name": "Unknown", "profile_pic": "" , "specialization" : "General Mountaineering" , "certification" : "Basic Certified" ,"experience_years": None, "status" : "Active" , "staff_rating_avg" : staff_rating_avg }
            if b.snapshot_staff and b.trek.assigned_staff:
                staff_user = User.query.get(b.snapshot_staff)
                if staff_user:
                    staff_info = {"name": staff_user.name, "profile_pic": staff_user.profile_pic ,"specialization": staff_user.staff_profile.specialization, "certification": staff_user.staff_profile.certification, "experience": staff_user.staff_profile.experience_years , "status" : staff_user.staff_profile.status , "staff_rating_avg" : staff_rating_avg}

            results.append({
                "booking_id": b.booking_id,
                "booking_date": b.booking_date.strftime("%B %d, %Y"),
                "total_trekkers": b.number_of_persons,
                "total_amount_paid": b.total_amount,
                "payment_type": b.payment_method,
                "payment_status": b.payment_status,
                "booking_created_at": b.created_at.strftime("%Y-%m-%d %H:%M"),
                
                # TrekDetail Component Mapping
                "trek_id": b.trek.trek_id,
                "trek_name": b.trek.trek_name,
                "location": b.trek.location,
                "difficulty": b.trek.difficulty,
                "duration_days": b.snapshot_duration_days,
                "status": "Completed",
                "max_altitude": getattr(b.trek, 'max_altitude', 0),
                "price_per_person":price,
                "description": b.trek.description,
                "images": gallery,
                "trek_avg": trek_rating_avg ,             
                "staff": staff_info,
                "profile" : staff_user.profile_pic ,
                "start_date" : b.snapshot_start_date.strftime("%Y-%m-%d"),
                "end_date" : b.snapshot_end_date.strftime("%Y-%m-%d"),
                
                # Review Component Mapping
                "review_submitted": True if user_review else False,
                "existing_trek_review": {"stars": user_review.trek_rating, "comment": user_review.trek_experience} if user_review else None,
                "existing_staff_review": {"stars": user_review.staff_rating, "comment": user_review.staff_experience} if user_review else None
            })
    return make_response(jsonify(results), 200)

# ==========================================================================
# 5. SUBMIT POST-TRIP EVALUATION
# ==========================================================================
@trekker_bp.route('/reviews', methods=['POST'])
@jwt_required()
def submit_trek_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    trek_id = data.get('trek_id')
    
    existing = Review.query.filter_by(user_id=user_id, trek_id=trek_id).first()
    if existing:
        return make_response(jsonify({"message": "Evaluation already logged for this path."}), 400)
        
    try:
        new_review = Review(
            user_id=user_id,
            trek_id=trek_id,
            staff_id=data.get('staff_id'),
            trek_rating=data.get('trek_rating'),
            staff_rating=data.get('staff_rating'),
            trek_experience=data.get('trek_comment'),
            staff_experience=data.get('staff_comment')
        )
        db.session.add(new_review)
        db.session.commit()
        return make_response(jsonify({"message": "Review matrix synchronized with database."}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": str(e)}), 500)
    

# ==========================================================================
# 6. Exporting History
# ==========================================================================

@trekker_bp.route('/export-history', methods=['POST'])
@jwt_required()
@trekker_required
def trigger_csv_export():
    """Triggers the async Celery worker to generate a CSV."""
    from tasks import export_history_csv
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Use .delay() to send it to Redis/Celery without blocking Flask
    export_history_csv.delay(user_id, user.email, user.name)
    create_notification(user.id, "Your CSV data has been exported and emailed.", "info")
    
    return make_response(jsonify({
        "message": "Export initiated! Your CSV will be emailed to you shortly."
    }), 202)
    


# ==========================================================================
# 7. Password Reset via OTP Workflow
# ==========================================================================

@trekker_bp.route('/request-password-otp', methods=['POST'])
@jwt_required()
@trekker_required
def request_password_otp():
    """Generates a 6-digit OTP, stores it in Redis for 5 mins, and emails it via Celery."""
    from tasks import send_otp_email
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Generate 6 digit string
    otp_code = str(random.randint(100000, 999999))
    
    # Save to Redis Cache with a 300 second (5 min) Time-To-Live
    cache.set(f"password_otp_{user_id}", otp_code, timeout=300)
    
    # Trigger Celery to send email asynchronously
    send_otp_email.delay(user.email, user.name, otp_code)
    
    return make_response(jsonify({"message": "OTP generated and dispatched to your email."}), 200)


@trekker_bp.route('/reset-password', methods=['PATCH'])
@jwt_required()
@trekker_required
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