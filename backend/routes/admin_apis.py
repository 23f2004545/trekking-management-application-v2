from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.extensions import bcrypt,db
from controller.models import User,Role,Trek,Booking    
from controller.decorators import admin_required
from datetime import datetime


admin_bp = Blueprint('admin', __name__)

# ==========================================================================
# 1. ADMIN DASHBOARD STATS & OVERVIEW
# ==========================================================================
@admin_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_stats():
        
    stats = {
        "total_treks": Trek.query.count(),
        "total_users": User.query.join(Role).filter(Role.name == 'trekker').count(),
        "total_staff": User.query.join(Role).filter(Role.name == 'trek_staff').count(),
        "total_bookings": Booking.query.count()
    }
    return make_response(jsonify(stats), 200)

# ==========================================================================
# 2. MANAGE TREKKING ROUTES (CRUD)
# ==========================================================================
@admin_bp.route('/treks', methods=['POST'])
@jwt_required()
@admin_required
def create_trek():
        
    data = request.get_json()
    
    # Extract fields based on required system attributes
    name = data.get('name')
    location = data.get('location')
    difficulty = data.get('difficulty') # Easy / Moderate / Hard
    duration = data.get('duration')
    available_slots = data.get('available_slots')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not all([name, location, difficulty, duration, available_slots, start_date_str, end_date_str]):
        return make_response(jsonify({"message": "Missing required fields"}), 400)

    try:
        new_trek = Trek(
            name=name.strip(),
            location=location.strip(),
            difficulty=difficulty,
            duration=int(duration),
            available_slots=int(available_slots),
            status="Pending",  # Initial status lifecycle stage
            start_date=datetime.strptime(start_date_str, "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date_str, "%Y-%m-%d").date()
        )
        db.session.add(new_trek)
        db.session.commit()
        return make_response(jsonify({"message": "Trekking route created successfully", "trek_id": new_trek.id}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Error creating route: {str(e)}"}), 500)


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

    # PUT Method Execution
    data = request.get_json()
    trek.name = data.get('name', trek.name).strip()
    trek.location = data.get('location', trek.location).strip()
    trek.difficulty = data.get('difficulty', trek.difficulty)
    trek.duration = int(data.get('duration', trek.duration))
    trek.available_slots = int(data.get('available_slots', trek.available_slots))
    trek.status = data.get('status', trek.status) # Pending/Approved/Open/Closed/Completed
    
    if data.get('start_date'):
        trek.start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
    if data.get('end_date'):
        trek.end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d").date()

    db.session.commit()
    return make_response(jsonify({"message": "Trekking route updated successfully"}), 200)

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
    name = data.get('name')
    contact = data.get('contact')

    if not all([email, password, name, contact]):
        return make_response(jsonify({"message": "All fields are required"}), 400)

    if User.query.filter_by(email=email).first():
        return make_response(jsonify({"message": "Email already registered"}), 400)

    staff_role = Role.query.filter_by(name='trek_staff').first()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_staff = User(
        name=name.strip().title(),
        email=email.strip().lower(),
        password=hashed_password,
        contact=contact.strip(),
        role=staff_role,
        is_active=True # Active status flag column
    )
    db.session.add(new_staff)
    db.session.commit()
    return make_response(jsonify({"message": "Trek staff account generated successfully"}), 201)


@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['PATCH'])
@jwt_required()
@admin_required
def toggle_user_active_status(user_id):
    """Deactivate or blacklist users and staff by flipping their is_active database field."""
    
    current_user_id = get_jwt_identity()        
    user = User.query.get_or_404(user_id)
    if user.id == int(current_user_id):
        return make_response(jsonify({"message": "Superusers cannot blacklist themselves"}), 400)

    # Flip the activity boolean status flag
    user.is_active = not user.is_active
    db.session.commit()
    
    status_label = "Activated" if user.is_active else "Deactivated/Blacklisted"
    return make_response(jsonify({"message": f"User status changed to {status_label}"}), 200)

# ==========================================================================
# 4. ASSIGN STAFF TO TREKS
# ==========================================================================
@admin_bp.route('/treks/<int:trek_id>/assign-staff', methods=['PATCH'])
@jwt_required()
@admin_required
def assign_staff_to_trek(trek_id):
        
    data = request.get_json()
    staff_id = data.get('staff_id')
    
    trek = Trek.query.get_or_404(trek_id)
    staff_user = User.query.get_or_404(staff_id)

    if staff_user.role.name != 'trek_staff':
        return make_response(jsonify({"message": "Assigned user must possess Trek Staff clearance"}), 400)

    trek.assigned_staff_id = staff_user.id
    db.session.commit()
    return make_response(jsonify({"message": f"Trek successfully assigned to staff: {staff_user.name}"}), 200)

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