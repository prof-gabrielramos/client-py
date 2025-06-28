"""
Security utilities and middleware
"""
import functools
import re
from flask import request, jsonify, current_app, session
from werkzeug.exceptions import BadRequest
import bleach
from datetime import datetime, timedelta


class SecurityManager:
    """Security utilities manager"""
    
    # Allowed HTML tags for sanitization
    ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
    ALLOWED_ATTRIBUTES = {}
    
    @staticmethod
    def sanitize_input(text):
        """Sanitize user input to prevent XSS"""
        if not text:
            return text
        
        # Remove potentially dangerous characters
        text = bleach.clean(
            text,
            tags=SecurityManager.ALLOWED_TAGS,
            attributes=SecurityManager.ALLOWED_ATTRIBUTES,
            strip=True
        )
        
        return text.strip()
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate phone number format"""
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Check if it's a valid international format
        if re.match(r'^\+\d{10,15}$', cleaned):
            return cleaned
        
        # Check if it's a valid national format (assuming Brazilian)
        if re.match(r'^\d{10,11}$', cleaned):
            return f"+55{cleaned}"
        
        raise ValueError(f"Invalid phone number format: {phone}")
    
    @staticmethod
    def validate_url(url):
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            raise ValueError(f"Invalid URL format: {url}")
        
        return url
    
    @staticmethod
    def check_rate_limit(key, limit=10, window=60):
        """Simple rate limiting check"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window)
        
        # This is a simple in-memory implementation
        # In production, use Redis or similar
        if not hasattr(current_app, '_rate_limits'):
            current_app._rate_limits = {}
        
        if key not in current_app._rate_limits:
            current_app._rate_limits[key] = []
        
        # Clean old entries
        current_app._rate_limits[key] = [
            timestamp for timestamp in current_app._rate_limits[key]
            if timestamp > window_start
        ]
        
        # Check limit
        if len(current_app._rate_limits[key]) >= limit:
            return False
        
        # Add current request
        current_app._rate_limits[key].append(now)
        return True


def require_auth(f):
    """Authentication decorator"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def validate_json_input(required_fields=None):
    """Decorator to validate JSON input"""
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            # Check required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': f'Missing required fields: {", ".join(missing_fields)}'
                    }), 400
            
            # Sanitize string inputs
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = SecurityManager.sanitize_input(value)
            
            request.validated_json = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def rate_limit(limit=10, window=60):
    """Rate limiting decorator"""
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            key = f"{request.remote_addr}:{f.__name__}"
            
            if not SecurityManager.check_rate_limit(key, limit, window):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': window
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator