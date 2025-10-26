from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

db = SQLAlchemy()
sess = Session()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'Hello python'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///kaveri_ai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    
    db.init_app(app)
    sess.init_app(app)
    
    register_blueprints(app)
    
    with app.app_context():
        db.create_all()
    
    return app

def register_blueprints(app):
    from app.routes.auth import auth_bp
    from app.routes.assignment import ass_bp
    from app.routes.dashboard import dash_bp
    from app.routes.content import content_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(ass_bp, url_prefix='/assessment')
    app.register_blueprint(dash_bp, url_prefix='/dashboard') 
    app.register_blueprint(content_bp, url_prefix='/content')
    
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('intro.html')