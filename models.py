from mongoengine import Document, StringField, FloatField, DateTimeField
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(Document):
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(Document):
    seat_number = StringField(required=True, unique=True)
    full_name = StringField(required=True)
    birth_date = StringField(required=True)
    math = FloatField(required=True, min_value=0, max_value=100)
    religion = FloatField(required=True, min_value=0, max_value=100)
    history = FloatField(required=True, min_value=0, max_value=100)
    geography = FloatField(required=True, min_value=0, max_value=100)
    english = FloatField(required=True, min_value=0, max_value=100)
    arabic = FloatField(required=True, min_value=0, max_value=100)
    social_studies = FloatField(required=True, min_value=0, max_value=100)
    total_score = FloatField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.total_score = (
            self.math + self.religion + self.history +
            self.geography + self.english + self.arabic +
            self.social_studies
        )
        return super().save(*args, **kwargs)
