import os
import io
from unittest.mock import patch
from werkzeug.datastructures import FileStorage
from services.cloudinary_service import is_cloudinary_configured, upload_image


def test_is_cloudinary_configured_falsy():
    with patch.dict(os.environ, {
        "CLOUDINARY_URL": "",
        "CLOUDINARY_CLOUD_NAME": "",
        "CLOUDINARY_API_KEY": "",
        "CLOUDINARY_API_SECRET": ""
    }, clear=True):
        assert is_cloudinary_configured() is False


def test_is_cloudinary_configured_with_url():
    with patch.dict(os.environ, {"CLOUDINARY_URL": "cloudinary://123:abc@testcloud"}):
        assert is_cloudinary_configured() is True


def test_is_cloudinary_configured_with_keys():
    with patch.dict(os.environ, {
        "CLOUDINARY_CLOUD_NAME": "test_cloud",
        "CLOUDINARY_API_KEY": "12345",
        "CLOUDINARY_API_SECRET": "secret_abc"
    }):
        assert is_cloudinary_configured() is True


def test_upload_image_cloudinary_mocked(app):
    fake_file = FileStorage(
        stream=io.BytesIO(b"fake image bytes"),
        filename="test_avatar.jpg",
        content_type="image/jpeg",
    )

    expected_url = "https://res.cloudinary.com/testcloud/image/upload/v12345/apex/avatars/test_avatar.jpg"

    with app.app_context():
        with patch("services.cloudinary_service.is_cloudinary_configured", return_value=True), \
             patch("services.cloudinary_service.setup_cloudinary", return_value=True), \
             patch("cloudinary.uploader.upload", return_value={"secure_url": expected_url}):

            result_url = upload_image(fake_file, folder="apex/avatars", filename_prefix="user")
            assert result_url == expected_url


def test_upload_image_local_fallback(app):
    fake_file = FileStorage(
        stream=io.BytesIO(b"fake image bytes local fallback"),
        filename="local_avatar.png",
        content_type="image/png",
    )

    with app.app_context():
        with patch("services.cloudinary_service.is_cloudinary_configured", return_value=False):
            result_url = upload_image(fake_file, folder="apex/avatars", filename_prefix="trekker", local_subfolder="Profile_pics")
            assert result_url.startswith("/static/Profile_pics/")
            assert "local_avatar.png" in result_url

            # Clean up test file from static folder
            rel_path = result_url.lstrip("/")
            full_path = os.path.join(app.config.get("BASE_DIR", "backend"), rel_path)
            if os.path.exists(full_path):
                os.remove(full_path)


def test_upload_image_empty_file(app):
    with app.app_context():
        assert upload_image(None) is None
        empty_fs = FileStorage(stream=io.BytesIO(b""), filename="")
        assert upload_image(empty_fs) is None
