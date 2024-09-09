from app import db
from sqlalchemy import func

class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column("pk_transaction", db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    chest_pain_type = db.Column(db.Integer)
    resting_bp = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    fasting_bs = db.Column(db.Integer)
    resting_ecg = db.Column(db.Integer)
    max_hr = db.Column(db.Integer)
    exercise_angina = db.Column(db.Integer)
    oldpeak = db.Column(db.Integer)
    st_slope = db.Column(db.Integer)
    heart_disease = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())