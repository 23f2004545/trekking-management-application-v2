import os
import time
from werkzeug.utils import secure_filename
from flask import current_app

try:
    import cloudinary
    import cloudinary.uploader
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False


def is_cloudinary_configured():
    """
    Determines whether valid Cloudinary configuration is present in environment or current_app config.
    """
    cloudinary_url = os.environ.get("CLOUDINARY_URL")
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    if CLOUDINARY_AVAILABLE:
        if cloudinary_url:
            return True
        if cloud_name and api_key and api_secret:
            return True

    return False


def setup_cloudinary():
    """Initializes Cloudinary configuration if parameters exist."""
    if not CLOUDINARY_AVAILABLE:
        return False

    cloudinary_url = os.environ.get("CLOUDINARY_URL")
    if cloudinary_url:
        cloudinary.config(cloudinary_url=cloudinary_url)
        return True

    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    if cloud_name and api_key and api_secret:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        return True

    return False


def upload_image(file_storage, folder="general", filename_prefix=None, local_subfolder=None):
    """
    Uploads an image with automatic production cloud / local filesystem fallback.
    Isolates media inside the 'apex_trek_portfolio' root folder.

    Args:
        file_storage: Werkzeug FileStorage object or file-like object.
        folder: Subfolder name (e.g. 'avatars', 'treks', 'tickets'). Defaults to 'general'.
        filename_prefix: Optional string prefix to prepend to saved filename.
        local_subfolder: Local static subfolder for fallback (e.g. 'Profile_pics' or 'Treks').

    Returns:
        str: Public Cloudinary HTTPS URL or local '/static/<subfolder>/<filename>' URL.
    """
    if not file_storage or not getattr(file_storage, "filename", None):
        return None

    orig_filename = secure_filename(file_storage.filename) or "image.png"

    # 1. Attempt Cloudinary upload if configured
    if is_cloudinary_configured() and setup_cloudinary():
        try:
            if hasattr(file_storage, "seek"):
                file_storage.seek(0)

            # 🔥 STRENGTHENED ISOLATION:
            # Combines the isolated app root namespace with whatever subfolder is passed down.
            # Resulting paths: 'apex_trek_portfolio/avatars', 'apex_trek_portfolio/treks', etc.
            target_cloud_folder = f"apex_trek_portfolio/{folder}"

            upload_result = cloudinary.uploader.upload(
                file_storage,
                folder=target_cloud_folder,
                resource_type="image",
                use_filename=True,
                unique_filename=True
            )
            secure_url = upload_result.get("secure_url")
            if secure_url:
                return secure_url
        except Exception as e:
            if current_app:
                current_app.logger.warning(f"Cloudinary upload failed, falling back to local: {e}")
            else:
                print(f"[Cloudinary Warning] Upload failed, falling back to local: {e}")

    # 2. Local Filesystem Fallback (Unchanged structural integrity)
    subfolder = local_subfolder or ("Profile_pics" if "avatar" in folder or "user" in folder else "Treks")

    if current_app and "BASE_DIR" in current_app.config:
        base_static_dir = os.path.join(current_app.config["BASE_DIR"], "static")
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_static_dir = os.path.abspath(os.path.join(current_dir, "..", "static"))

    save_dir = os.path.join(base_static_dir, subfolder)
    os.makedirs(save_dir, exist_ok=True)

    timestamp = int(time.time())
    if filename_prefix:
        final_filename = f"{filename_prefix}_{timestamp}_{orig_filename}"
    else:
        final_filename = f"{timestamp}_{orig_filename}"

    save_path = os.path.join(save_dir, final_filename)
    if hasattr(file_storage, "seek"):
        file_storage.seek(0)
    file_storage.save(save_path)

    return f"/static/{subfolder}/{final_filename}"
