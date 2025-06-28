"""
Authentication blueprint with security best practices
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

from .models import db, User
from .security import rate_limit, SecurityManager

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limit(limit=5, window=300)  # 5 attempts per 5 minutes
def login():
    """Secure login with rate limiting"""
    if request.method == 'POST':
        username = SecurityManager.sanitize_input(request.form.get('username', ''))
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            logger.warning(f"Login attempt with missing credentials from {request.remote_addr}")
            return render_template('auth/login.html')
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if user and user.is_active and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            
            # Update last login
            user.last_login = db.func.now()
            db.session.commit()
            
            logger.info(f"Successful login for user {username} from {request.remote_addr}")
            flash('Login successful', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            logger.warning(f"Failed login attempt for user {username} from {request.remote_addr}")
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """Secure logout"""
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f"User {username} logged out from {request.remote_addr}")
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@rate_limit(limit=3, window=300)  # 3 attempts per 5 minutes
def change_password():
    """Change password with security validation"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        user = User.query.get(session['user_id'])
        
        # Validate current password
        if not user.check_password(current_password):
            flash('Current password is incorrect', 'error')
            return render_template('auth/change_password.html')
        
        # Validate new password
        if len(new_password) < 8:
            flash('New password must be at least 8 characters long', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('auth/change_password.html')
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        logger.info(f"Password changed for user {user.username}")
        flash('Password changed successfully', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/change_password.html')