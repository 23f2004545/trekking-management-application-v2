class config:
    SECRET_KEY = "secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-production-key"
    
    # Optional: How long should an access token live? (e.g., 1 hour)
    JWT_ACCESS_TOKEN_EXPIRES = 36000