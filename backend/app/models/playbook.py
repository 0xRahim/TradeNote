from app import db
from datetime import datetime

class Playbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playbook_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    entry_model = db.Column(db.String(50), nullable=False)
    trade_model = db.Column(db.String(50), nullable=False)
    setup_grade = db.Column(db.String(10), nullable=False)
    confluences = db.Column(db.JSON)
    rules = db.Column(db.JSON)
    confirmations = db.Column(db.JSON)
    invalidations = db.Column(db.JSON)
    roadmap = db.Column(db.JSON)
    tags = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
