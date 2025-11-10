# src/config/config.py
import os
from datetime import timedelta

class Config:
    """Base configuration for Auth Service"""
    
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # API Configuration
    API_TITLE = 'Auth Service API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    SERVICE_NAME = 'auth'
    SERVICE_VERSION = '1.0.0'
    
    # MySQL Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+mysqldb://root:password@localhost:3306/auth_service'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-me-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Security Headers
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',') or ['http://localhost:3000']
    
    # Logging (AWS CloudWatch compatible)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    # External Services
    MONITORING_SERVICE_URL = os.environ.get('MONITORING_SERVICE_URL', 'http://dashboard:5001')
    
    # Rate Limiting (important for auth endpoints)
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = "200 per hour"
    RATELIMIT_LOGIN = "5 per minute"
    
    # Redis Cache for token blacklist/sessions
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Message Queue for async tasks (password reset emails, etc.)
    RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
    
    # AWS Specific Configuration
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    
    # AWS Services (if used for SES, SNS, etc.)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    
    # Email Service (for password resets)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'email-smtp.us-east-1.amazonaws.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    
    # Application Settings
    PASSWORD_RESET_TIMEOUT = int(os.environ.get('PASSWORD_RESET_TIMEOUT', '3600'))  # 1 hour
    MAX_LOGIN_ATTEMPTS = int(os.environ.get('MAX_LOGIN_ATTEMPTS', '5'))
    ACCOUNT_LOCKOUT_DURATION = int(os.environ.get('ACCOUNT_LOCKOUT_DURATION', '1800'))  # 30 minutes


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Development MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+mysqldb://root:mysqlpassword123@localhost:3306/auth_dev'
    )
    
    # Development-specific security (less strict)
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    
    # Verbose logging
    LOG_LEVEL = 'DEBUG'
    
    # Longer tokens for development convenience
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Simple cache for development
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 60


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Test database
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://test:test@localhost:3306/auth_test'
    
    # Fast token expiration for tests
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    
    # Mock external services
    MONITORING_SERVICE_URL = 'http://mock-monitoring:5002'
    
    # Simple cache for tests
    CACHE_TYPE = 'SimpleCache'
    
    # Disable rate limiting in tests
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production configuration optimized for AWS"""
    DEBUG = False
    TESTING = False
    
    # Production MySQL (RDS compatible)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqldb://user:password@production-db.abc123.us-east-1.rds.amazonaws.com:3306/auth_prod'
    )
    
    # Enhanced connection pooling for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'pool_size': 20,
        'max_overflow': 30,
        'pool_timeout': 30,
    }
    
    # Strict security
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    # Shorter token expiration for security
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    
    # Strict CORS in production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # AWS-specific production settings
    PREFERRED_URL_SCHEME = 'https'


class DockerConfig(DevelopmentConfig):
    """Docker-specific configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+mysqldb://root:mysqlpassword123@mysql-db:3306/orchestratorAuth'
    )
    
    # Docker service discovery
    DASHBOARD_SERVICE_URL = os.environ.get('DASHBOARD_SERVICE_URL', 'http://dashboard:5001')
    #RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
    #CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')


class AWSEC2Config(ProductionConfig):
    """AWS EC2 specific configuration"""
    
    # Use RDS endpoint directly
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqldb://user:password@auth-db.abc123.us-east-1.rds.amazonaws.com:3306/auth_prod'
    )
    
    # Use ElastiCache Redis
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://auth-cache.abc123.0001.use1.cache.amazonaws.com:6379/0')
    
    # AWS-specific service URLs
    MONITORING_SERVICE_URL = os.environ.get('MONITORING_SERVICE_URL', 'http://internal-monitoring-elb-123456.us-east-1.elb.amazonaws.com')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'aws': AWSEC2Config,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'docker ')
    return config.get(env, config['docker'])