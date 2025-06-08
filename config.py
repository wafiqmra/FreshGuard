import os

class Config:
    # Secret key Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'ini_secret_key_rahasia')

    # Konfigurasi Database - koneksi via Unix socket (Cloud SQL Proxy)
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'freshguard')
    
    # Path ke Unix socket Cloud SQL (ganti host jadi unix_socket saat connect)
    MYSQL_UNIX_SOCKET = '/cloudsql/turnkey-chimera-460001-p0:us-central1:freshguard-uas'

    # Konfigurasi email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # masukkan di environment variable
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # masukkan di environment variable
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  # masukkan di environment variable

    # Path ke credentials GCP
    GOOGLE_APPLICATION_CREDENTIALS = '/key.json'
