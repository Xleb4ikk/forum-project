from flask import Flask
from app.models.db_models import db
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize admin panel
    from app.admin import init_admin
    init_admin(app)
    
    # Register admin routes
    from app.admin.routes import admin_bp, init_first_admin
    app.register_blueprint(admin_bp)
    
    # Register main blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create tables and initialize admin user on first run
    with app.app_context():
        db.create_all()
        init_first_admin()
    
    return app 