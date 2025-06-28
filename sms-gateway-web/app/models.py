"""
Database models with proper indexing and relationships
"""
import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    """Message model with proper indexing"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(255), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    recipients = db.Column(db.Text, nullable=False)  # JSON string
    state = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('messages', lazy=True))
    
    @property
    def recipients_list(self):
        """Get recipients as list"""
        try:
            return json.loads(self.recipients)
        except (json.JSONDecodeError, TypeError):
            return []
    
    @recipients_list.setter
    def recipients_list(self, value):
        """Set recipients from list"""
        self.recipients = json.dumps(value)


class Contact(db.Model):
    """Contact model"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False, unique=True, index=True)
    group_name = db.Column(db.String(100), index=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('contacts', lazy=True))


class Webhook(db.Model):
    """Webhook model"""
    __tablename__ = 'webhooks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    events = db.Column(db.Text, nullable=False)  # JSON string
    headers = db.Column(db.Text)  # JSON string
    enabled = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('webhooks', lazy=True))
    
    @property
    def events_list(self):
        """Get events as list"""
        try:
            return json.loads(self.events)
        except (json.JSONDecodeError, TypeError):
            return []
    
    @events_list.setter
    def events_list(self, value):
        """Set events from list"""
        self.events = json.dumps(value)
    
    @property
    def headers_dict(self):
        """Get headers as dict"""
        try:
            return json.loads(self.headers) if self.headers else {}
        except (json.JSONDecodeError, TypeError):
            return {}
    
    @headers_dict.setter
    def headers_dict(self, value):
        """Set headers from dict"""
        self.headers = json.dumps(value) if value else None