import io
from unittest.mock import patch
from controller.models import db, User, Trek, TrekImage
from datetime import datetime, timezone, timedelta


def test_register_with_profile_pic_upload(client, app):
    fake_avatar = (io.BytesIO(b"dummy image data"), "avatar.jpg")
    mock_url = "https://res.cloudinary.com/testcloud/image/upload/v1/apex/avatars/new_trekker.jpg"

    with patch("services.cloudinary_service.is_cloudinary_configured", return_value=True), \
         patch("services.cloudinary_service.setup_cloudinary", return_value=True), \
         patch("cloudinary.uploader.upload", return_value={"secure_url": mock_url}):

        response = client.post(
            "/api/auth/register",
            data={
                "name": "Alex Explorer",
                "email": "alex@test.com",
                "password": "Password123",
                "contact": "9876543299",
                "profile_pic": fake_avatar,
            },
            content_type="multipart/form-data"
        )
        assert response.status_code == 201

        with app.app_context():
            user = User.query.filter_by(email="alex@test.com").first()
            assert user is not None
            assert user.profile_pic == mock_url


def test_staff_profile_pic_update(client, staff_headers, app):
    fake_avatar = (io.BytesIO(b"updated staff avatar"), "staff_new.jpg")
    mock_url = "https://res.cloudinary.com/testcloud/image/upload/v1/apex/avatars/staff_updated.jpg"

    with patch("services.cloudinary_service.is_cloudinary_configured", return_value=True), \
         patch("services.cloudinary_service.setup_cloudinary", return_value=True), \
         patch("cloudinary.uploader.upload", return_value={"secure_url": mock_url}):

        response = client.patch(
            "/api/trek_staff/profile",
            headers=staff_headers,
            data={
                "name": "Updated Staff Name",
                "contact": "9876543211",
                "profile_pic": fake_avatar,
            },
            content_type="multipart/form-data"
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.filter_by(email="staff@test.com").first()
            assert user.profile_pic == mock_url


def test_trekker_profile_pic_update(client, trekker_headers, app):
    fake_avatar = (io.BytesIO(b"updated trekker avatar"), "trekker_new.jpg")
    mock_url = "https://res.cloudinary.com/testcloud/image/upload/v1/apex/avatars/trekker_updated.jpg"

    with patch("services.cloudinary_service.is_cloudinary_configured", return_value=True), \
         patch("services.cloudinary_service.setup_cloudinary", return_value=True), \
         patch("cloudinary.uploader.upload", return_value={"secure_url": mock_url}):

        response = client.patch(
            "/api/trekker/profile",
            headers=trekker_headers,
            data={
                "name": "Updated Trekker Name",
                "contact": "9876543212",
                "profile_pic": fake_avatar,
            },
            content_type="multipart/form-data"
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.filter_by(email="trekker@test.com").first()
            assert user.profile_pic == mock_url


def test_admin_trek_create_and_update_with_gallery_upload(client, admin_headers, app):
    # 1. Create a trek with 4 gallery files
    gallery_files = [
        (io.BytesIO(f"img {i}".encode()), f"gallery_{i}.jpg") for i in range(4)
    ]
    mock_urls = [
        f"https://res.cloudinary.com/testcloud/image/upload/v1/apex/treks/img_{i}.jpg"
        for i in range(4)
    ]

    upload_mock_iter = iter([{"secure_url": url} for url in mock_urls])

    now = datetime.now(timezone.utc)
    start_str = (now + timedelta(days=10)).strftime("%Y-%m-%d")
    end_str = (now + timedelta(days=15)).strftime("%Y-%m-%d")

    with patch("services.cloudinary_service.is_cloudinary_configured", return_value=True), \
         patch("services.cloudinary_service.setup_cloudinary", return_value=True), \
         patch("cloudinary.uploader.upload", side_effect=lambda *args, **kwargs: next(upload_mock_iter)):

        data = {
            "name": "Rohtang Ridge Pass",
            "location": "Manali, Himachal Pradesh",
            "difficulty": "Moderate",
            "duration_days": 5,
            "available_slots": 12,
            "max_altitude": 4000,
            "price_per_person": 7500,
            "start_date": start_str,
            "end_date": end_str,
            "description": "High altitude pass trek.",
            "trek_gallery": gallery_files
        }

        response = client.post(
            "/api/admin/treks",
            headers=admin_headers,
            data=data,
            content_type="multipart/form-data"
        )
        assert response.status_code == 201
        res_json = response.get_json()
        trek_id = res_json["trek_id"]

        with app.app_context():
            images = TrekImage.query.filter_by(trek_id=trek_id).all()
            assert len(images) == 4
            for img in images:
                assert img.image_url in mock_urls

    # 2. Update the trek with 4 replacement gallery files
    new_gallery_files = [
        (io.BytesIO(f"new img {i}".encode()), f"new_gallery_{i}.jpg") for i in range(4)
    ]
    new_mock_urls = [
        f"https://res.cloudinary.com/testcloud/image/upload/v2/apex/treks/new_img_{i}.jpg"
        for i in range(4)
    ]
    new_upload_mock_iter = iter([{"secure_url": url} for url in new_mock_urls])

    with patch("services.cloudinary_service.is_cloudinary_configured", return_value=True), \
         patch("services.cloudinary_service.setup_cloudinary", return_value=True), \
         patch("cloudinary.uploader.upload", side_effect=lambda *args, **kwargs: next(new_upload_mock_iter)):

        update_data = {
            "name": "Rohtang Ridge Pass Extended",
            "location": "Manali, Himachal Pradesh",
            "difficulty": "Hard",
            "duration_days": 6,
            "available_slots": 10,
            "max_altitude": 4200,
            "price_per_person": 8500,
            "start_date": start_str,
            "end_date": end_str,
            "description": "Extended pass trek.",
            "trek_gallery": new_gallery_files
        }

        update_response = client.put(
            f"/api/admin/treks/{trek_id}",
            headers=admin_headers,
            data=update_data,
            content_type="multipart/form-data"
        )
        assert update_response.status_code == 200

        with app.app_context():
            updated_images = TrekImage.query.filter_by(trek_id=trek_id).all()
            assert len(updated_images) == 4
            for img in updated_images:
                assert img.image_url in new_mock_urls
