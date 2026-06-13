class config:
    SECRET_KEY = "secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-production-key"
    
    
    JWT_ACCESS_TOKEN_EXPIRES = 300
    
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 300