import os
import sys
import pytest
from flask_jwt_extended import create_access_token

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app import create_app
from controller.extensions import db, bcrypt
from controller.models import User, Role, StaffProfile


@pytest.fixture(scope="session")
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-jwt-secret-key-that-is-at-least-32-bytes-long",
        "CACHE_TYPE": "NullCache",
        "WTF_CSRF_ENABLED": False,
        "CLOUDINARY_URL": None,
        "CLOUDINARY_CLOUD_NAME": None,
        "CLOUDINARY_API_KEY": None,
        "CLOUDINARY_API_SECRET": None,
    }
    app = create_app(test_config=test_config)
    return app


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        db.create_all()
        # Seed base roles
        for role_name in ["admin", "trek_staff", "trekker"]:
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))
        db.session.commit()

        # Seed standard users
        admin_role = Role.query.filter_by(name="admin").first()
        staff_role = Role.query.filter_by(name="trek_staff").first()
        trekker_role = Role.query.filter_by(name="trekker").first()

        if not User.query.filter_by(email="admin@test.com").first():
            admin_user = User(
                name="Test Admin",
                email="admin@test.com",
                password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
                contact="9876543210",
                profile_pic="/static/Profile_pics/admin.png",
                role=admin_role,
            )
            db.session.add(admin_user)

        if not User.query.filter_by(email="staff@test.com").first():
            staff_user = User(
                name="Test Staff",
                email="staff@test.com",
                password=bcrypt.generate_password_hash("staff123").decode("utf-8"),
                contact="9876543211",
                profile_pic="/static/Profile_pics/trek_staff.png",
                role=staff_role,
            )
            db.session.add(staff_user)
            db.session.flush()
            staff_profile = StaffProfile(
                user_id=staff_user.id,
                specialization="Alpine Guide",
                experience_years=5,
                certification="UIAGM",
                status="Active"
            )
            db.session.add(staff_profile)

        if not User.query.filter_by(email="trekker@test.com").first():
            trekker_user = User(
                name="Test Trekker",
                email="trekker@test.com",
                password=bcrypt.generate_password_hash("trekker123").decode("utf-8"),
                contact="9876543212",
                profile_pic="/static/Profile_pics/trekker.png",
                role=trekker_role,
            )
            db.session.add(trekker_user)

        db.session.commit()

        yield

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_headers(app):
    with app.app_context():
        user = User.query.filter_by(email="admin@test.com").first()
        token = create_access_token(identity=str(user.id))
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def staff_headers(app):
    with app.app_context():
        user = User.query.filter_by(email="staff@test.com").first()
        token = create_access_token(identity=str(user.id))
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def trekker_headers(app):
    with app.app_context():
        user = User.query.filter_by(email="trekker@test.com").first()
        token = create_access_token(identity=str(user.id))
        return {"Authorization": f"Bearer {token}"}
