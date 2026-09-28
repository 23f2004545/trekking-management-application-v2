import os
from unittest.mock import patch
from config import config
from controller.models import db, User, Role, Trek, TrekImage
from datetime import datetime, timezone, timedelta
from scripts.migrate_sqlite_to_pg import normalize_pg_uri


def test_normalize_pg_uri():
    legacy_uri = "postgres://user:pass@ep-xyz.neon.tech/neondb?sslmode=require"
    expected = "postgresql+psycopg2://user:pass@ep-xyz.neon.tech/neondb?sslmode=require"
    assert normalize_pg_uri(legacy_uri) == expected

    native_uri = "postgresql://user:pass@ep-xyz.neon.tech/neondb?sslmode=require"
    assert normalize_pg_uri(native_uri) == expected

    already_driver_uri = "postgresql+psycopg2://user:pass@ep-xyz.neon.tech/neondb"
    assert normalize_pg_uri(already_driver_uri) == already_driver_uri


def test_config_database_url_fallback():
    with patch.dict(os.environ, {"DATABASE_URL": ""}, clear=True):
        from importlib import reload
        import config as cfg_mod
        reload(cfg_mod)
        assert cfg_mod.config.SQLALCHEMY_DATABASE_URI == "sqlite:///database.sqlite3"


def test_model_column_capacity_for_long_urls(app):
    long_cloudinary_url = "https://res.cloudinary.com/demo-account-apex-trekking/image/upload/v1727456789/apex/avatars/user_long_folder_name_nested_very_long_path_to_demonstrate_url_capacity_profile_picture_version_1234567890_abcdefghijklmnopqrstuvwxyz.jpg"
    assert len(long_cloudinary_url) > 200

    with app.app_context():
        trekker_role = Role.query.filter_by(name="trekker").first()
        user = User(
            name="Long URL User",
            email="longurl@test.com",
            password="hashedpassword123",
            contact="1234567890",
            profile_pic=long_cloudinary_url,
            role=trekker_role
        )
        db.session.add(user)
        db.session.commit()

        fetched_user = User.query.filter_by(email="longurl@test.com").first()
        assert fetched_user.profile_pic == long_cloudinary_url

        # Test TrekImage capacity
        now = datetime.now(timezone.utc)
        trek = Trek(
            trek_name="Test Capacity Peak",
            location="Himalayas",
            difficulty="Moderate",
            duration_days=4,
            available_slots=10,
            status="Open",
            start_date=now + timedelta(days=5),
            end_date=now + timedelta(days=9),
            description="Capacity Test",
            max_altitude=4200,
            price_per_person=8000
        )
        db.session.add(trek)
        db.session.commit()

        trek_img = TrekImage(trek_id=trek.trek_id, image_url=long_cloudinary_url)
        db.session.add(trek_img)
        db.session.commit()

        fetched_img = TrekImage.query.filter_by(trek_id=trek.trek_id).first()
        assert fetched_img.image_url == long_cloudinary_url
