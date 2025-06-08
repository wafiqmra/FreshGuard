import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ini_secret_key_rahasia')
    
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')  # IP Public Cloud SQL kamu
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')           # user MySQL kamu di Cloud SQL
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')        # password MySQL kamu di Cloud SQL
    MYSQL_DB = os.getenv('MYSQL_DB', 'freshguard')
    
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
