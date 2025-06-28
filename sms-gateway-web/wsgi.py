"""
WSGI entry point for production deployment
"""
import os
import logging
from app import create_app
from app.config import config

# Get configuration from environment
config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config[config_name])

# Setup logging for production
if config_name == 'production':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    app.run()