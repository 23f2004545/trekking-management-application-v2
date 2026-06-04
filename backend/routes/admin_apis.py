from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import bcrypt,db
from controller.models import * 
from controller.decorators import admin_required
from datetime import datetime, timezone , timedelta
from sqlalchemy import func
import os


admin_bp = Blueprint('admin', __name__)

# ==========================================================================
# 1. ADMIN DASHBOARD STATS & OVERVIEW
# ==========================================================================

@admin_bp.route('/profile', methods=['GET'])
@jwt_required()
@admin_required
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

@admin_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_stats():
    """Compiles operational counters, ratings insights, and graphing trends."""
    
    # 1. CORE COUNTERS (Fallback to 0 naturally if empty)
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()
    
    # Count specific roles safely using relationships
    total_staff = User.query.filter(User.role.has(name='trek_staff')).count()
    total_trekkers = User.query.filter(User.role.has(name='trekker')).count()

    # 2. POPULAR TREKS (Top 3 by booking volume)
    popular_treks_query = db.session.query(
        Trek.trek_name, func.count(Booking.booking_id).label('booking_count')
    ).join(Booking, Booking.trek_id == Trek.trek_id)\
     .group_by(Trek.trek_id)\
     .order_by(func.count('booking_count').desc()).limit(3).all()
     
    popular_treks = [{"name": row[0], "bookings": row[1]} for row in popular_treks_query]

    # 3. RATING INSIGHTS (Averages & Top Performers)
    # Global Average Trek Rating
    avg_rating_raw = db.session.query(func.avg(Review.trek_rating)).scalar()
    global_avg_rating = round(avg_rating_raw, 1) if avg_rating_raw else 0.0

    # Highest Rated Trek
    top_trek_query = db.session.query(
        Trek.trek_name, func.avg(Review.trek_rating).label('avg')
    ).join(Review, Review.trek_id == Trek.trek_id)\
     .group_by(Trek.trek_id)\
     .order_by(func.avg('avg').desc()).first()
     
    top_trek = {"name": top_trek_query[0], "rating": round(top_trek_query[1], 1)} if top_trek_query else None

    # Highest Rated Staff Guide
    top_staff_query = db.session.query(
        User.name, func.avg(Review.staff_rating).label('avg')
    ).join(StaffProfile, StaffProfile.user_id == User.id)\
     .join(Review, Review.staff_id == StaffProfile.staff_id)\
     .group_by(User.id).order_by(func.avg('avg').desc()).first()

    top_staff = {"name": top_staff_query[0], "rating": round(top_staff_query[1], 1)} if top_staff_query else None

    # 4. BOOKING TRENDS (Last 6 Months)
    booking_trends = []
    current_date = datetime.now(timezone.utc)
    
    # Walk backwards 5 months + current month
    for i in range(5, -1, -1):
        target_date = current_date - timedelta(days=i*30)
        month_label = target_date.strftime("%b %Y")
        
        # Count bookings for this specific month/year
        monthly_count = Booking.query.filter(
            func.extract('month', Booking.created_at) == target_date.month,
            func.extract('year', Booking.created_at) == target_date.year
        ).count()
        
        booking_trends.append({"month": month_label, "count": monthly_count})

    # Total summation check to see if we have ANY data to chart
    has_chart_data = sum([t['count'] for t in booking_trends]) > 0

    return make_response(jsonify({
        "counters": {
            "treks": total_treks,
            "trekkers": total_trekkers,
            "staff": total_staff,
            "bookings": total_bookings
        },
        "insights": {
            "global_avg_rating": global_avg_rating,
            "top_trek": top_trek,
            "top_staff": top_staff
        },
        "charts": {
            "has_data": has_chart_data,
            "trends": booking_trends,
            "popular": popular_treks
        }
    }), 200)

# ==========================================================================
# 2. MANAGE TREKKING ROUTES (CRUD)
# ==========================================================================

@admin_bp.route('/treks', methods=['GET'])
@jwt_required()
@admin_required
def get_all_treks():
    treks = Trek.query.order_by(Trek.created_at.desc()).all()
    
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
            "image_url": images[0].image_url if images else "/static/Treks/default_trek.jpg",
            "assigned_staff": {
                "id": staff_user.id if staff_user else None,
                "name": staff_user.name if staff_user else "Unassigned Guide"
            }
        })
        
    return make_response(jsonify(results), 200)



@admin_bp.route('/treks', methods=['POST'])
@jwt_required()
@admin_required
def create_trek():
    
    data = request.form
    
    name = data.get('name')
    location = data.get('location')
    difficulty = data.get('difficulty')
    duration = data.get('duration_days') or data.get('duration')
    available_slots = data.get('available_slots')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    max_altitude = data.get('max_altitude', 0)
    price = data.get('price_per_person', 0)
    description = data.get('description', '')
    assigned_staff_id = data.get('assigned_staff_id')

    if not all([name, location, difficulty, duration, available_slots, start_date_str, end_date_str]):
        return make_response(jsonify({"message": "Missing non-optional tracking fields."}), 400)
    
    # assigned_staff = User.query.get(assigned_staff_id) if assigned_staff_id and assigned_staff_id != 'null' else 1
    
    staff_id = None
    if assigned_staff_id and assigned_staff_id != 'null' and assigned_staff_id != 'undefined':
        staff_id = int(assigned_staff_id)
    
    try:
        new_trek = Trek(
            trek_name=name.strip(),
            location=location.strip(),
            difficulty=difficulty,
            duration_days=int(duration),
            available_slots=int(available_slots),
            status=data.get('status', 'Pending'),
            start_date=datetime.strptime(start_date_str, "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date_str, "%Y-%m-%d").date(),
            description=description.strip(),
            max_altitude=float(max_altitude),
            price_per_person=float(price),
            assigned_staff_id=staff_id 
        )
        db.session.add(new_trek)
        db.session.flush()  
        
        # 📸 PROCESS MULTIPLE UPLOADS LOOP (Max 4 elements)
        if 'trek_gallery' in request.files:
            uploaded_files = request.files.getlist('trek_gallery')
            for index, file in enumerate(uploaded_files[:4]):
                if file and file.filename != '':
                    timestamp = int(datetime.now(timezone.utc).timestamp())
                    filename = f"trek_{new_trek.trek_id}_img{index}_{timestamp}_{os.path.basename(file.filename)}"
                    save_path = os.path.join('static/', 'Treks', filename)
                    
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    file.save(save_path)
                    
                    # Commit row line to the child trek_images table
                    new_image = TrekImage(
                        trek_id=new_trek.trek_id,
                        image_url=f"/static/Treks/{filename}"
                    )
                    db.session.add(new_image)

        db.session.commit()
            
        db.session.commit()
        return make_response(jsonify({"message": "Expedition coordinate mapping generated successfully.", "trek_id": new_trek.trek_id}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Database transaction aborted: {str(e)}"}), 500)

@admin_bp.route('/treks/<int:trek_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@admin_required
def manage_trek_by_id(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    if request.method == 'DELETE':
        try:
            db.session.delete(trek)
            db.session.commit()
            return make_response(jsonify({"message": "Trekking route removed successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"Database dependency error: {str(e)}"}), 400)

    # PUT Method Execution (Upgraded to support multi-part form payloads)
    data = request.form if request.form else request.get_json()
    
    try:
        trek.trek_name = data.get('trek_name', trek.trek_name).strip()
        trek.location = data.get('location', trek.location).strip()
        trek.difficulty = data.get('difficulty', trek.difficulty)
        trek.duration_days = int(data.get('duration_days', trek.duration_days))
        trek.available_slots = int(data.get('available_slots', trek.available_slots))
        trek.description = data.get('description', trek.description).strip()
        trek.max_altitude = float(data.get('max_altitude', trek.max_altitude))
        trek.price_per_person = float(data.get('price_per_person', trek.price_per_person))
        
        # Change status of all related bookings 
        
        status_changed = False
        new_status = data.get('status')
        
        if new_status:
            allowed_statuses = ['Open', 'Ongoing', 'Closed', 'Completed', 'Cancelled']
            if new_status in allowed_statuses and trek.status != new_status:
                trek.status = new_status
                status_changed = True
                
        if status_changed:
        # All currently active bookings for this specific trek
            active_bookings = Booking.query.filter_by(trek_id=trek.trek_id, status='Booked').all()
            
            for booking in active_bookings:
                if new_status == 'Completed':
                    booking.status = 'Completed'
                    booking.updated_at = datetime.now(timezone.utc)
                    
                elif new_status == 'Cancelled':
                    booking.status = 'Cancelled'
                    booking.payment_status = 'Refunded' # Trigger refund pipeline state
                    booking.cancellation_reason = "Route operations halted by field administration."
                    booking.cancelled_at = datetime.now(timezone.utc)
                    booking.updated_at = datetime.now(timezone.utc)
                    
        
        staff_id = data.get('assigned_staff_id')
        trek.assigned_staff_id = int(staff_id) if staff_id and staff_id != 'null' else None
        
        if data.get('start_date'):
            trek.start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
        if data.get('end_date'):
            trek.end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d").date()
            
        trek.updated_at = datetime.now(timezone.utc)

        # 📸 DYNAMIC GALLERY REPLACEMENT LAYER
        if 'trek_gallery' in request.files:
            uploaded_files = request.files.getlist('trek_gallery')
            if uploaded_files and uploaded_files[0].filename != '':
                # Safely clear historical child references out of database lines
                TrekImage.query.filter_by(trek_id=trek.trek_id).delete()
                
                for index, file in enumerate(uploaded_files[:4]):
                    timestamp = int(datetime.now(timezone.utc).timestamp())
                    filename = f"trek_update_{trek.trek_id}_img{index}_{timestamp}_{os.path.basename(file.filename)}"
                    save_path = os.path.join('static/', 'Treks', filename)
                    file.save(save_path)
                    
                    new_image = TrekImage(trek_id=trek.trek_id, image_url=f"/static/Treks/{filename}")
                    db.session.add(new_image)

        db.session.commit()
        return make_response(jsonify({"message": "Trekking route updated successfully"}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Database mutation failed: {str(e)}"}), 500)


@admin_bp.route('/treks/<int:trek_id>/details', methods=['GET'])
@jwt_required()
# @admin_required
def trek_details(trek_id):

    trek = Trek.query.get_or_404(trek_id)
    
    # 1. Gather all gallery paths from our fresh child image table
    gallery_images = [img.image_url for img in trek.images]


    # 2. Extract Assigned Staff Guide Profile
    staff_user = User.query.get(trek.assigned_staff_id) if trek.assigned_staff_id else None
    reviews = Review.query.filter_by(trek_id=trek_id).all()
    
    # 3. Compile Separate Reviews (Trek vs Staff) from feedback metrics tables
    # (Assuming columns exist or fallback to blank lists until Milestone 6 execution)
    trek_reviews_list = [
        # {
        #     "id": 1, 
        #     "trekker": "Aarav Patel", 
        #     "stars": 5, 
        #     "comment": "Breathtaking views and a well-marked trail. Highly recommend!"
        # },
        # {
        #     "id": 2, 
        #     "trekker": "Priya Sharma", 
        #     "stars": 4, 
        #     "comment": "Beautiful trek, but the final ascent was tougher than expected."
        # },
        # {
        #     "id": 2, 
        #     "trekker": "Priya Sharma", 
        #     "stars": 4, 
        #     "comment": "Beautiful trek, but the final ascent was tougher than expected."
        # },
        # {
        #     "id": 2, 
        #     "trekker": "Priya Sharma", 
        #     "stars": 4, 
        #     "comment": "Beautiful trek, but the final ascent was tougher than expected."
        # },
        # {
        #     "id": 3, 
        #     "trekker": "Rohan Gupta", 
        #     "stars": 5, 
        #     "comment": "An unforgettable experience. The sunrise from the summit was magical."
        # }
    ]
    staff_reviews_list = [
        # {
        #     "id": 101, 
        #     "trekker": "Aarav Patel", 
        #     "stars": 5, 
        #     "comment": "Our guide was incredibly patient and knowledgeable about the local flora."
        # },
        # {
        #     "id": 102, 
        #     "trekker": "Sneha Desai", 
        #     "stars": 3, 
        #     "comment": "Friendly staff, but dinner was served a bit late on the second night."
        # },
        # {
        #     "id": 102, 
        #     "trekker": "Sneha Desai", 
        #     "stars": 3, 
        #     "comment": "Friendly staff, but dinner was served a bit late on the second night."
        # },
        # {
        #     "id": 102, 
        #     "trekker": "Sneha Desai", 
        #     "stars": 3, 
        #     "comment": "Friendly staff, but dinner was served a bit late on the second night."
        # }
    ]
    staff_rating_avg = None
    trek_rating_avg = None
    
    if hasattr(trek, 'reviews') and trek.reviews:
        trek_reviews_list = [{
            "id": r.id, "trekker": r.author.name, "stars": r.trek_rating, "comment": r.trek_experience or 'No review provided'
        } for r in trek.reviews]
        trek_rating_avg = round(sum([r.trek_rating for r in trek.reviews]) / len(trek.reviews))

    if reviews :
        staff_reviews_list = [{
            "id": r.id, "trekker": r.author.name, "stars": r.staff_rating, "comment": r.staff_experience or 'No review provided'
        } for r in reviews]
        staff_rating_avg = round(sum([r.staff_rating for r in reviews]) / len(reviews))

    payload = {
        "trek_id": trek.trek_id,
        "trek_name": trek.trek_name,
        "location": trek.location,
        "difficulty": trek.difficulty,
        "duration_days": trek.duration_days if hasattr(trek, 'duration_days') else getattr(trek, 'duration_days', 0),
        "available_slots": trek.available_slots,
        "status": trek.status,
        "start_date": trek.start_date.strftime("%Y-%m-%d") if trek.start_date else "",
        "end_date": trek.end_date.strftime("%Y-%m-%d") if trek.end_date else "",
        "description": trek.description or "No baseline overview provided.",
        "max_altitude": getattr(trek, 'max_altitude', 0.0),
        "price_per_person": getattr(trek, 'price_per_person', 0.0),
        "created_at": trek.created_at.strftime("%B %d, %Y") if trek.created_at else "N/A",
        "updated_at": trek.updated_at.strftime("%B %d, %Y") if hasattr(trek, 'updated_at') and trek.updated_at else "N/A",
        "images": gallery_images,
        "trek_rating_avg": trek_rating_avg ,
        "trek_reviews": trek_reviews_list,
        "staff": {
            "id" : staff_user.id,
            "name": staff_user.name if staff_user else "Unassigned Guide Leader",
            "experience": staff_user.staff_profile.experience_years if staff_user and staff_user.staff_profile else None,
            "status": staff_user.staff_profile.status if staff_user and staff_user.staff_profile else "Active",
            "specialization": staff_user.staff_profile.specialization if staff_user and staff_user.staff_profile else "General Mountaineering",
            "certification": staff_user.staff_profile.certification if staff_user and staff_user.staff_profile else "Basic Certified",
            "profile_pic": staff_user.profile_pic if staff_user else '/static/Profile_pics/trek_staff.png',
            "staff_rating_avg": staff_rating_avg ,
            "staff_reviews": staff_reviews_list
        }
    }
    return make_response(jsonify(payload), 200)

# ==========================================================================
# 3. ADD AND MANAGE TREK STAFF / USER BLACKLISTS
# ==========================================================================

@admin_bp.route('/staff', methods=['POST'])
@jwt_required()
@admin_required
def add_trek_staff():
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return make_response(jsonify({"message": "All fields are required"}), 400)

    if User.query.filter_by(email=email).first():
        return make_response(jsonify({"message": "Email already registered"}), 400)

    staff_role = Role.query.filter_by(name='trek_staff').first()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_staff = User(
        name='Staff',
        email=email.strip().lower(),
        password=hashed_password,
        contact='123456780',
        profile_pic='/static/Profile_pics/trek_staff.png',
        role=staff_role
    )
    
    db.session.add(new_staff)
    id = User.query.filter_by(email=email).first().id
    
    # Dummy staff profile with default values to satisfy non-nullable constraints and allow future updates
    new_staff_profile = StaffProfile(
        user_id=id,
        specialization='Pending',
        certification='Pending',
        experience_years='0',
        status='Active',
        emergency_contact='1234567890',
        bio='Pending'
    )
    
    db.session.add(new_staff_profile)
    db.session.commit()
    return make_response(jsonify({"message": "Trek staff account generated successfully"}), 201)


# @admin_bp.route('/users/<int:user_id>/toggle-status', methods=['PATCH'])
# @jwt_required()
# @admin_required
# def toggle_user_active_status(user_id):
#     """Deactivate or blacklist users and staff by flipping their is_active database field."""
    
#     current_user_id = get_jwt_identity()        
#     user = User.query.get_or_404(user_id)
#     if user.id == int(current_user_id):
#         return make_response(jsonify({"message": "Superusers cannot blacklist themselves"}), 400)

#     # Flip the activity boolean status flag
#     user.is_active = not user.is_active
#     db.session.commit()
    
#     status_label = "Activated" if user.is_active else "Deactivated/Blacklisted"
#     return make_response(jsonify({"message": f"User status changed to {status_label}"}), 200)

@admin_bp.route('/staff', methods=['GET'])
@jwt_required()
@admin_required
def get_all_staff():

    staff_role = Role.query.filter_by(name='trek_staff').first()
    if not staff_role:
        return make_response(jsonify([]), 200)
        
    staff_members = User.query.filter_by(role=staff_role).all()
    
    results = []
    for s in staff_members:
        results.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "contact": s.contact,
            "is_active": s.is_active,
            "blacklisted": getattr(s, 'blacklisted', False),
            "specialization": getattr(s.staff_profile, 'specialization', "General Mountaineering"),
            "certification": getattr(s.staff_profile, 'certification', "Basic Certified"),
            "experience": getattr(s.staff_profile, 'experience', "2+ Years"),
            "last_login_at": s.last_login_at.strftime("%b %d, %I:%M %p") if s.last_login_at else "Offline Logs",
            "profile_pic": s.profile_pic or "/static/Profile_pics/trek_staff.png"
        })
    return make_response(jsonify(results), 200)


@admin_bp.route('/staff/<int:staff_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_single_staff_profile(staff_id):
    staff = User.query.get_or_404(staff_id)
    return make_response(jsonify({
        "id": staff.id,
        "name": staff.name,
        "email": staff.email,
        "contact": staff.contact,
        "is_active": staff.is_active,
        "blacklisted": getattr(staff, 'blacklisted', False),
        "created_at": staff.created_at.strftime("%B %d, %Y") if staff.created_at else "N/A",
        "last_login_at": staff.last_login_at.strftime("%I:%M %p") if staff.last_login_at else "Never",
        "profile_pic": staff.profile_pic or "/static/Profile_pics/trek_staff.png",
        "specialization": getattr(staff.staff_profile, 'specialization', "Glacier Survival"),
        "certification": getattr(staff.staff_profile, 'certification', "NIM Advanced"),
        "experience": getattr(staff.staff_profile, 'experience', "5 Years")
    }), 200)


@admin_bp.route('/users/<int:user_id>/toggle-blacklist', methods=['PATCH'])
@jwt_required()
@admin_required
def toggle_user_blacklist_status(user_id):
    """Flips the blacklisted attribute state flag to restrict ecosystem logins."""
    user = User.query.get_or_404(user_id)
    
    # Check if column parameter attribute exists inside your models.py
    if hasattr(user, 'blacklisted'):
        user.blacklisted = not user.blacklisted
        db.session.commit()
        status_txt = "Blacklisted" if user.blacklisted else "Whitelisted"
        return make_response(jsonify({"message": f"User account credentials flagged as {status_txt}."}), 200)
        
    return make_response(jsonify({"message": "Model column definition missing block attributes."}), 500)


# ==========================================================================
# 4. ASSIGN OR INTERCHANGE STAFF OPERATIONS GATEWAY
# ==========================================================================

@admin_bp.route('/assign-staff-override', methods=['PATCH'])
@jwt_required()
@admin_required
def assign_staff_override():

    data = request.get_json()
    trek_id = data.get('trek_id')
    staff_id = data.get('staff_id')
    force_switch = data.get('force_switch', False)

    if not trek_id or not staff_id:
        return make_response(jsonify({"message": "Trek ID and Staff ID are mandatory parameters."}), 400)

    trek = Trek.query.get_or_404(trek_id)
    new_staff = User.query.get_or_404(staff_id)

    if new_staff.role.name != 'trek_staff':
        return make_response(jsonify({"message": "Target user lacks verified guide credentials."}), 400)

    # Intersection Alert Trigger Check: Evaluate if route already possesses an assignment
    if trek.assigned_staff_id and trek.assigned_staff_id != new_staff.id and not force_switch:
        old_staff = User.query.get(trek.assigned_staff_id)
        return make_response(jsonify({
            "collision": True,
            "old_staff_name": old_staff.name if old_staff else "Another Guide",
            "new_staff_name": new_staff.name,
            "trek_name": trek.trek_name
        }), 200)

    try:
        trek.assigned_staff_id = new_staff.id
        db.session.commit()
        return make_response(jsonify({"message": f"Trek '{trek.trek_name}' successfully routed to {new_staff.name}."}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Mutation failed: {str(e)}"}), 500)

# ==========================================================================
# 5. SEARCH & AUDIT CORE ENGINE (Treks, Staff, Users, Bookings)
# ==========================================================================
@admin_bp.route('/search', methods=['GET'])
@jwt_required()
@admin_required
def global_admin_search():
        
    target = request.args.get('target', 'treks') # Default search domain targets treks
    query = request.args.get('query', '')

    results = []
    
    if target == 'treks':
        # Search by ID integer or Name string matching patterns
        trek_query = Trek.query
        if query.isdigit():
            trek_query = trek_query.filter(Trek.id == int(query))
        elif query:
            trek_query = trek_query.filter(Trek.name.ilike(f"%{query}%") | Trek.location.ilike(f"%{query}%"))
        
        results = [{
            "id": t.id, "name": t.name, "location": t.location, 
            "difficulty": t.difficulty, "slots": t.available_slots, "status": t.status
        } for t in trek_query.all()]

    elif target in ['staff', 'users']:
        role_target = 'trek_staff' if target == 'staff' else 'trekker'
        user_query = User.query.join(Role).filter(Role.name == role_target)
        
        if query.isdigit():
            user_query = user_query.filter(User.id == int(query))
        elif query:
            user_query = user_query.filter(User.name.ilike(f"%{query}%") | User.email.ilike(f"%{query}%"))
            
        results = [{
            "id": u.id, "name": u.name, "email": u.email, 
            "contact": u.contact, "is_active": u.is_active
        } for u in user_query.all()]

    elif target == 'bookings':
        booking_query = Booking.query
        if query.isdigit():
            booking_query = booking_query.filter((Booking.id == int(query)) | (Booking.user_id == int(query)))
            
        results = [{
            "booking_id": b.id, "user_name": b.user.name, "trek_name": b.trek.name,
            "date": b.booking_date.strftime("%Y-%m-%d"), "status": b.status
        } for b in booking_query.all()]

    return make_response(jsonify(results), 200)


# ==========================================================================
# 6. ADD AND MANAGE TREKKER / USER BLACKLISTS
# ==========================================================================

@admin_bp.route('/trekkers', methods=['GET'])
@jwt_required()
@admin_required
def get_all_trekkers():

    trekkers_role = Role.query.filter_by(name='trekker').first()
    if not trekkers_role:
        return make_response(jsonify([]), 200)
        
    trekkers = User.query.filter_by(role=trekkers_role).all()
    
    results = []
    for t in trekkers:
        results.append({
            "id": t.id,
            "name": t.name,
            "email": t.email,
            "contact": t.contact,
            "is_active": t.is_active,
            "blacklisted": getattr(t, 'blacklisted', False),
            "emergency_contact": getattr(t.medical_record, 'emergency_contact', "None"),
            "emergency_relation": getattr(t.medical_record, 'emergency_relation', "None"),
            "emergency_name": getattr(t.medical_record, 'emergency_name', "None"),
            "last_login_at": t.last_login_at.strftime("%b %d, %I:%M %p") if t.last_login_at else "Offline Logs",
            "profile_pic": t.profile_pic or "/static/Profile_pics/trekker.png"
        })
    return make_response(jsonify(results), 200)


@admin_bp.route('/trekker/<int:trekker_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_single_trekker_profile(trekker_id):
    trekker = User.query.get_or_404(trekker_id)
    return make_response(jsonify({
        "id": trekker.id,
        "name": trekker.name,
        "email": trekker.email,
        "contact": trekker.contact,
        "is_active": trekker.is_active,
        "blacklisted": getattr(trekker, 'blacklisted', False),
        "created_at": trekker.created_at.strftime("%B %d, %Y") if trekker.created_at else "N/A",
        "last_login_at": trekker.last_login_at.strftime("%I:%M %p") if trekker.last_login_at else "Never",
        "profile_pic": trekker.profile_pic or "/static/Profile_pics/trekker.png",
        "emergency_contact": getattr(trekker.medical_record, 'emergency_contact', "None"),
        "emergency_relation": getattr(trekker.medical_record, 'emergency_relation', "None"),
        "emergency_name": getattr(trekker.medical_record, 'emergency_name', "None"),
        "medications" : getattr(trekker.medical_record, 'medications', "None"),
        "allergies": getattr(trekker.medical_record, 'allergies', "None"),  
        "diagnosis": getattr(trekker.medical_record, 'diagnosis', "None"),
        "blood_group": getattr(trekker.medical_record, 'blood_group', "None")
    }), 200)
    
    
# ==========================================================================
# 7. BOOKING LOGS & TREKKER REVIEWS AUDIT
# ==========================================================================
@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
@admin_required
def get_all_global_bookings():
    """Compiles global reservation logs with calculated timeline status metrics."""
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    current_date = datetime.now(timezone.utc).date()
    
    results = []
    for b in bookings:
        # Resolve real-time lifecycle tracking labels based on schedule bounds
        calculated_status = b.status # Default fallback status: Booked / Cancelled
        
        if b.status == 'Booked' and b.trek:
            if current_date < b.trek.start_date.date():
                calculated_status = 'Upcoming'
            elif b.trek.start_date.date() <= current_date <= b.trek.end_date.date():
                calculated_status = 'Ongoing'
            else:
                calculated_status = 'Completed'

        results.append({
            "booking_id": b.booking_id,
            "booking_date": b.booking_date.strftime("%Y-%m-%d"),
            "booking_status": calculated_status, 
            "trek_name": b.trek.trek_name if b.trek else " PURGED ROUTE",
            "trekker": {
                "name": b.user.name if b.user else "Deleted Explorer",
                "profile_pic": b.user.profile_pic if b.user else ""
            }
        })
    return make_response(jsonify(results), 200)


@admin_bp.route('/bookings/<int:booking_id>/details', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_booking_deep_details(booking_id):
    
    b = Booking.query.get_or_404(booking_id)
    current_date = datetime.now(timezone.utc).date()
    
    calculated_status = b.status
    if b.status == 'Booked' and b.trek:
        if current_date < b.trek.start_date.date(): calculated_status = 'Upcoming'
        elif b.trek.start_date.date() <= current_date <= b.trek.end_date.date(): calculated_status = 'Ongoing'
        else: calculated_status = 'Completed'

    # Pull direct assigned guide details safely
    staff_user = User.query.get(b.trek.assigned_staff_id) if b.trek and b.trek.assigned_staff_id else None
    
    # Query distinct reviewer lines matching this unique transaction node
    review = Review.query.filter_by(user_id=b.user_id, trek_id=b.trek_id).first()

    payload = {
        "booking_id": b.booking_id,
        "booking_date": b.booking_date.strftime("%B %d, %Y"),
        "booking_status": calculated_status,
        "cancelled_date": "2026-05-28" if b.status == 'Cancelled' else None, # Example tracking placeholder
        "cancelled_reason": "Route environmental warnings / high windfall advisory." if b.status == 'Cancelled' else None,
        "trek": {
            "name": b.trek.trek_name if b.trek else "Unknown Pass",
            "location": b.trek.location if b.trek else "Grid offline",
            "difficulty": b.trek.difficulty if b.trek else "Moderate",
            "schedule": f"{b.trek.start_date.date()} to {b.trek.end_date.date()}" if b.trek else "N/A",
            "altitude": getattr(b.trek, 'max_altitude', 0.0),
            "price": getattr(b.trek, 'price_per_person', 0.0)
        },
        "trekker": {
            "name": b.user.name, "email": b.user.email, "contact": b.user.contact,
            "profile_pic": b.user.profile_pic or ""
        },
        "staff": {
            "name": staff_user.name if staff_user else "Unassigned Guide",
            "email": staff_user.email if staff_user else "N/A",
            "contact": staff_user.contact if staff_user else "N/A",
            "profile_pic": staff_user.profile_pic if staff_user else ""
        },
        "review": {
            "exists": True if review else False,
            "trek_stars": review.trek_rating if review else 0,
            "staff_stars": review.staff_rating if review else 0,
            "trek_text": review.trek_experience if review else "",
            "staff_text": review.staff_experience if review else ""
        }
    }
    return make_response(jsonify(payload), 200)