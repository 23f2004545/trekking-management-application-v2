from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from controller.extensions import bcrypt,db,cache
from controller.models import User,Role
from datetime import datetime, timezone
from tasks import send_otp_email
from services.cloudinary_service import upload_image
from services.demo_service import is_demo_user
import os , re , random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    
    # Check if user exists and password hash matches
    if user and bcrypt.check_password_hash(user.password, data.get("password")):
        
        if not user.is_active:
           return make_response(jsonify({"message": "Account Deactivated"}), 403)
       
        if user.role.name == 'trek_staff' and user.blacklisted:
            return make_response(jsonify({"message": "Account Restricted by Administration"}), 403)
    
        # Create the token using the user's ID as the "subject" (sub)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()
        
        
        return make_response(jsonify({"access_token": access_token, "refresh_token": refresh_token, "role": user.role.name , "name": user.name , "profile_pic": user.profile_pic}), 200)

    return make_response(jsonify({"message": "Invalid email or password"}), 401)


@auth_bp.route('/demo-login', methods=['POST'])
def demo_login():
    """
    Instant Access Demo Login:
    Validates role, dynamically auto-reseeds demo dataset if needed,
    and returns JWT credentials tagged with is_demo: True.
    """
    from services.demo_service import seed_or_reset_demo_data
    
    data = request.get_json() or {}
    role = data.get('role', 'admin')
    if role in ['staff', 'guide']:
        role = 'trek_staff'

    if role not in ['admin', 'trek_staff', 'trekker']:
        return make_response(jsonify({"message": "Invalid demo role requested."}), 400)

    try:
        user = seed_or_reset_demo_data(target_role=role)
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()

        access_token = create_access_token(identity=str(user.id), additional_claims={"is_demo": True})
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims={"is_demo": True})

        return make_response(jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role.name,
            "name": user.name,
            "profile_pic": user.profile_pic,
            "is_demo": True,
            "message": f"Welcome to Apex Expeditions Demo Portal as {user.role.name.title()}!"
        }), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": f"Demo auto-reseed failure: {str(e)}"}), 500)



@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return make_response(jsonify({"access_token": new_access_token}), 200)


@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    
    return make_response(jsonify({"message": "User logged out successfully"}), 200)


@auth_bp.route('/register', methods=['POST'])
def register():
    
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    contact = request.form.get('contact')

        
    profile_pic = None 
    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file and file.filename != '':
            profile_pic = upload_image(file, folder="apex/avatars", filename_prefix="user", local_subfolder="Profile_pics")
        
    # Fallback if no image uploaded
    if not profile_pic:
        profile_pic = "/static/Profile_pics/trekker.png"
        
        
    name = name.strip().title() 
    
    
    # BACKEND VALIDATION LAYER 
    if not name or not email or not password or not contact :
        return make_response(jsonify({"message": "All fields are required"}), 400)

    # Regex for standard email format
    pattern = r'^[\w\.-]+@[\w\.-]+\.[\w]{2,}$'
    if re.match(pattern, email) is  None:
        return make_response(jsonify({"message": "Invalid email format"}), 400)
    
    if not name.replace(" ", "").isalpha():
        return make_response(jsonify({"message": "Name must contain only alphabetic characters and spaces"}), 400)
    
    if not(contact.isdigit() and len(contact) == 10):
        return make_response(jsonify({"message": "Contact number must be exactly 10 digits"}), 400)
    
    if len(password) < 8:
        return make_response(jsonify({"message": "Password must be at least 8 characters long"}), 400)
    
    # Check if user with the same email already exists
    if User.query.filter_by(email=email).first():
        return make_response(jsonify({"message": "Email already registered"}), 400)
    
    # Hash the password before storing
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    role = Role.query.filter_by(name='trekker').first()
    
    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        contact=contact,
        profile_pic=profile_pic,
        role=role
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return make_response(jsonify({"message": "User registered successfully"}), 201)


@auth_bp.route('/request-login-otp', methods=['POST'])
def request_login_otp():
    """Generates an OTP for passwordless login."""
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # We return a generic message to prevent 'Email Enumeration' hacking
        return make_response(jsonify({"message": "If this email exists, an OTP has been sent."}), 200)
        
    if not user.is_active:
        return make_response(jsonify({"message": "Account suspended."}), 403)

    otp_code = str(random.randint(100000, 999999))
    cache.set(f"login_otp_{email}", otp_code, timeout=300) # 5 minutes TTL
    
    demo_delivery_email = None
    if is_demo_user(user):
        demo_delivery_email = data.get('demo_delivery_email')
    
    send_otp_email.delay(user.email, user.name, otp_code, demo_delivery_email=demo_delivery_email)
    
    return make_response(jsonify({"message": "If this email exists, an OTP has been sent."}), 200)


@auth_bp.route('/verify-login-otp', methods=['POST'])
def verify_login_otp():
    """Validates the OTP and instantly logs the user in."""
    email = request.json.get('email')
    submitted_otp = request.json.get('otp')
    
    stored_otp = cache.get(f"login_otp_{email}")
    
    if not stored_otp or str(stored_otp) != str(submitted_otp):
        return make_response(jsonify({"message": "Invalid or expired OTP."}), 401)
        
    user = User.query.filter_by(email=email).first()
    
    # OTP is valid! Log them in.
    cache.delete(f"login_otp_{email}") # Destroy OTP
    
    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()
    
    # Generate identical payload to your normal /login route
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return make_response(jsonify({
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "role": user.role.name, 
        "name": user.name, 
        "profile_pic": user.profile_pic
    }), 200)
