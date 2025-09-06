from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure the database
    db_path = os.path.expanduser('~/TradeNote/tradenote.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['UPLOAD_FOLDER'] = os.path.expanduser('~/TradeNote/uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


    db.init_app(app)

    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from .models.user import User
        from .models.note import Note
        from .models.trade import Trade
        from .models.playbook import Playbook

        db.create_all()

        # Register Blueprints
        from .routes.auth import auth_bp
        from .routes.notes import notes_bp
        from .routes.events import events_bp
        from .routes.trades import trades_bp
        from .routes.playbooks import playbooks_bp

        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(notes_bp, url_prefix='/notes')
        app.register_blueprint(events_bp, url_prefix='/')
        app.register_blueprint(trades_bp, url_prefix='/trades')
        app.register_blueprint(playbooks_bp, url_prefix='/playbooks')


    return app
