import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tawjihi-secret-key-2023'
    MONGODB_SETTINGS = {
        'db': 'tawjihi_db',
        'host': 'mongodb+srv://tncxzml:CPsMBvK4w47HOsU0@cardify.05dzz.mongodb.net/',
    }
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)