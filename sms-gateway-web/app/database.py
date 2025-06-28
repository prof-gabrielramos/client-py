"""
Database initialization and utilities
"""
from flask import current_app
from .models import db, User
import os


def init_db(app):
    """Initialize database"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)
            db.session.commit()
            current_app.logger.info('Default admin user created')


def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        return db.session
    except Exception as e:
        current_app.logger.error(f"Database connection error: {e}")
        raise


class DatabaseManager:
    """Database operations manager"""
    
    @staticmethod
    def safe_execute(query, params=None):
        """Execute query safely with proper error handling"""
        try:
            if params:
                result = db.session.execute(query, params)
            else:
                result = db.session.execute(query)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Database query error: {e}")
            raise
    
    @staticmethod
    def paginate_query(query, page, per_page, error_out=False):
        """Paginate query with error handling"""
        try:
            return query.paginate(
                page=page,
                per_page=per_page,
                error_out=error_out
            )
        except Exception as e:
            current_app.logger.error(f"Pagination error: {e}")
            raise