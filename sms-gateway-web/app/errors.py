"""
Error handling and logging
"""
import logging
import traceback
from flask import jsonify, render_template, request, current_app
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        current_app.logger.warning(f"Bad request: {error}")
        if request.is_json:
            return jsonify({'error': 'Bad request'}), 400
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized errors"""
        current_app.logger.warning(f"Unauthorized access: {error}")
        if request.is_json:
            return jsonify({'error': 'Unauthorized'}), 401
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden errors"""
        current_app.logger.warning(f"Forbidden access: {error}")
        if request.is_json:
            return jsonify({'error': 'Forbidden'}), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        current_app.logger.info(f"Page not found: {request.url}")
        if request.is_json:
            return jsonify({'error': 'Not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle rate limit errors"""
        current_app.logger.warning(f"Rate limit exceeded: {request.remote_addr}")
        if request.is_json:
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.'
            }), 429
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        current_app.logger.error(f"Internal server error: {error}")
        current_app.logger.error(traceback.format_exc())
        
        if request.is_json:
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unexpected exceptions"""
        if isinstance(error, HTTPException):
            return error
        
        current_app.logger.error(f"Unhandled exception: {error}")
        current_app.logger.error(traceback.format_exc())
        
        if request.is_json:
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }), 500
        return render_template('errors/500.html'), 500


def setup_logging(app):
    """Setup application logging"""
    if not app.debug and not app.testing:
        # File logging
        if app.config.get('LOG_FILE'):
            file_handler = logging.FileHandler(app.config['LOG_FILE'])
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
        # Console logging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        console_handler.setLevel(logging.INFO)
        app.logger.addHandler(console_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('SMS Gateway Web startup')