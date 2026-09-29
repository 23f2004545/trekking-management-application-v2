import os
from flask import Flask 
from controller.extensions import db, jwt, bcrypt, cache
from controller.models import User, Role
from config import config
from flask_cors import CORS
from sqlalchemy import text

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # jwt_data["sub"] contains whatever identity you put in the token when you created it
    identity = jwt_data["sub"] 
    return User.query.get(int(identity)) # This will print None since it's outside of a request context, but it confirms the function is registered.

from routes.auth_apis import auth_bp
from routes.admin_apis import admin_bp
from routes.staff_apis import trek_staff_bp
from routes.trekker_apis import trekker_bp
from routes.utils_apis import utils_bp

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    if test_config:
        app.config.update(test_config)
    
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    
    with app.app_context():
        db.create_all()

        # PostgreSQL schema self-healing & sequence synchronization
        if db.engine.name == 'postgresql':
            try:
                db.session.execute(text("""
                    DO $$
                    BEGIN
                        IF EXISTS (
                            SELECT 1 FROM information_schema.table_constraints tc
                            JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
                            WHERE tc.table_name = 'trek' 
                              AND tc.constraint_type = 'FOREIGN KEY'
                              AND ccu.table_name = 'staff_profile'
                              AND tc.constraint_name = 'trek_assigned_staff_id_fkey'
                        ) THEN
                            ALTER TABLE trek DROP CONSTRAINT IF EXISTS trek_assigned_staff_id_fkey;
                            ALTER TABLE trek ADD CONSTRAINT trek_assigned_staff_id_fkey FOREIGN KEY (assigned_staff_id) REFERENCES "user"(id) ON DELETE SET NULL;
                        END IF;
                    END $$;
                """))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                app.logger.warning(f"PostgreSQL FK fix notice: {e}")

            # Resync primary key sequences in case demo seeding / inserts used explicit IDs
            tables_to_sync = [
                ('user', 'id'),
                ('role', 'id'),
                ('staff_profile', 'staff_id'),
                ('trek', 'trek_id'),
                ('booking', 'booking_id'),
                ('feedback', 'feedback_id'),
                ('support_ticket', 'ticket_id'),
                ('medical_record', 'record_id'),
                ('review', 'review_id'),
                ('dispatch_ticket', 'ticket_id')
            ]
            for tbl, col in tables_to_sync:
                try:
                    db.session.execute(text(f"""
                        SELECT setval(pg_get_serial_sequence('"{tbl}"', '{col}'), COALESCE((SELECT MAX({col}) + 1 FROM "{tbl}"), 1), false);
                    """))
                    db.session.commit()
                except Exception:
                    db.session.rollback()
        
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

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(trek_staff_bp, url_prefix='/api/trek_staff')
    app.register_blueprint(trekker_bp, url_prefix='/api/trekker')
    app.register_blueprint(utils_bp, url_prefix='/api/utils')

    return app

app = create_app()

cors_origins_env = os.environ.get("CORS_ORIGINS")
if cors_origins_env:
    allowed_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
else:
    frontend_url = os.environ.get("FRONTEND_URL")
    if frontend_url:
        allowed_origins = [frontend_url.rstrip("/"), "http://localhost:5173", "http://127.0.0.1:5000", "http://localhost:5000"]
    else:
        allowed_origins = "*"

CORS(app, origins=allowed_origins, supports_credentials=True)

if __name__ == '__main__':
    app.run(debug=True)