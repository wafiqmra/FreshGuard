import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ini_secret_key_rahasia')
    
    # Konfigurasi MySQL dengan timeout dan SSL
    MYSQL_HOST = '34.69.203.128'
    MYSQL_USER = 'root'  # Ganti dari root ke user khusus
    MYSQL_PASSWORD = 'tubescloud'  # Ganti password
    MYSQL_DB = 'freshguard'
    MYSQL_PORT = 3306
    MYSQL_CONNECT_TIMEOUT = 10
    MYSQL_READ_TIMEOUT = 30
    MYSQL_WRITE_TIMEOUT = 30
    MYSQL_SSL_MODE = 'REQUIRED'  # Wajibkan SSL
    
    # Konfigurasi Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True  # Langsung set boolean
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    import os
from datetime import timedelta

class Config:
    # App Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'ini_secret_key_rahasia')
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # MySQL Configuration with improved settings
    MYSQL_HOST = os.getenv('MYSQL_HOST', '34.69.203.128')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'tubescloud')
    MYSQL_DB = os.getenv('MYSQL_DB', 'freshguard')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_CONNECT_TIMEOUT = 10
    MYSQL_READ_TIMEOUT = 30
    MYSQL_WRITE_TIMEOUT = 30
    MYSQL_POOL_SIZE = 5
    MYSQL_POOL_RECYCLE = 3600
    MYSQL_SSL_MODE = 'REQUIRED'
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size