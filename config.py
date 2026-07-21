import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-premium-key-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'stock_management.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Optional extensions for a production system
    # MAIL_SERVER = ...
