from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.Text, nullable=True)  # To store base64 encoded avatar
    notes = db.relationship('Note', backref='author', lazy=True)
    playbooks = db.relationship('Playbook', backref='author', lazy=True)
