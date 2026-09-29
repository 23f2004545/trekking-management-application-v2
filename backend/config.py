import os

# Optionally load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key_dev_default")
    
    # Read cloud database URL, falling back to local SQLite
    database_url = os.environ.get("DATABASE_URL") or "sqlite:///database.sqlite3"
    
    # Render / Supabase / Neon compatibility: SQLAlchemy requires postgresql:// instead of legacy postgres://
    if database_url:
        if database_url.startswith("postgres://"):
            # Explicitly bind +psycopg2 to ensure backward compatibility across SQLAlchemy version updates
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif database_url.startswith("postgresql://"):
            # Fix native strings if provided generically by Neon/Render environment fields
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-production-key")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 300))
    
    # Redis & Message Broker Configuration
    REDIS_URL = os.environ.get("REDIS_URL") or os.environ.get("UPSTASH_REDIS_URL")
    if REDIS_URL:
        CACHE_TYPE = os.environ.get("CACHE_TYPE", "RedisCache")
        CACHE_REDIS_URL = REDIS_URL
    else:
        # Graceful local development fallback to in-memory cache when Redis is not running
        CACHE_TYPE = os.environ.get("CACHE_TYPE", "SimpleCache")
        REDIS_URL = "redis://localhost:6379/0"

    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(os.environ.get("CACHE_REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(os.environ.get("CACHE_REDIS_DB", 0))
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300))

    # Base directory and local fallback upload directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "static"))
    
    # Celery Message Broker
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or REDIS_URL
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND") or REDIS_URL
    CELERY_TASK_ALWAYS_EAGER = os.environ.get("CELERY_TASK_ALWAYS_EAGER", "False").lower() in ("true", "1")

    # Cloudinary Cloud Storage (Optional - falls back to local storage if not set)
    CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL", None)
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", None)
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", None)
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", None)

    # Cloud Email / Brevo HTTP API & SMTP Settings
    BREVO_API_KEY = os.environ.get("BREVO_API_KEY", None)
    BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL") or os.environ.get("SMTP_SENDER_EMAIL") or os.environ.get("SMTP_USER") or "nohara1887@gmail.com"
    BREVO_SENDER_NAME = os.environ.get("BREVO_SENDER_NAME") or os.environ.get("SMTP_SENDER_NAME", "Apex Expeditions")

    SMTP_HOST = os.environ.get("SMTP_HOST", "127.0.0.1")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 1025))
    SMTP_USER = os.environ.get("SMTP_USER", None)
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", None)
    SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "False").lower() in ("true", "1")
    SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "False").lower() in ("true", "1")
    # For Brevo and authenticated SMTP, sender email must match verified sender or login email
    SMTP_SENDER_EMAIL = os.environ.get("SMTP_SENDER_EMAIL") or os.environ.get("BREVO_SENDER_EMAIL") or os.environ.get("SMTP_USER") or "nohara1887@gmail.com"
    SMTP_SENDER_NAME = os.environ.get("SMTP_SENDER_NAME") or os.environ.get("BREVO_SENDER_NAME", "Apex Expeditions")