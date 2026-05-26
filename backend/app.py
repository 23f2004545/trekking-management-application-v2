from flask import Flask 
from controller.extensions import db, jwt, bcrypt
from controller.models import User, Role
from config import config
from flask_cors import CORS


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # jwt_data["sub"] contains whatever identity you put in the token when you created it
    identity = jwt_data["sub"] 
    return User.query.get(int(identity)) # This will print None since it's outside of a request context, but it confirms the function is registered.

from routes.auth_apis import auth_bp
from routes.admin_apis import admin_bp
from routes.staff_apis import staff_bp
from routes.trekker_apis import trekker_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            
        trek_staff_role = Role.query.filter_by(name='trek_staff').first()
        if not trek_staff_role:
            trek_staff_role = Role(name='trek_staff')
            db.session.add(trek_staff_role)
            
        trekker_role = Role.query.filter_by(name='trekker').first()
        if not trekker_role:
            trekker_role = Role(name='trekker')
            db.session.add(trekker_role)
            
        admin = User.query.filter_by(name='admin').first()
        if not admin:
            admin = User(
                name='admin',
                email='admin@gmail.com',
                password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                contact='1234567890',
                profile_pic="/static/Profile_pics/admin.png",
                role=admin_role,
            )
            db.session.add(admin)

        db.session.commit()

    return app

app = create_app()
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5000"])

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(staff_bp, url_prefix='/api/staff')
app.register_blueprint(trekker_bp, url_prefix='/api/trekker')

if __name__ == '__main__':
    app.run(debug=True)