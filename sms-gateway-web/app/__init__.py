"""
SMS Gateway Web Application
Refatorado para arquitetura modular
"""
import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

from .config import Config
from .database import init_db
from .auth import auth_bp
from .api import api_bp
from .main import main_bp
from .models import db


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Security extensions
    csrf = CSRFProtect(app)
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Security headers
    Talisman(app, force_https=app.config.get('FORCE_HTTPS', False))
    
    # Initialize database
    db.init_app(app)
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)
    
    # Error handlers
    from .errors import register_error_handlers
    register_error_handlers(app)
    
    return app