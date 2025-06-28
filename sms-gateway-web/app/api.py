"""
API blueprint with security and validation
"""
from flask import Blueprint, request, jsonify, session, current_app
import json
import logging
from datetime import datetime

from .models import db, Message, Contact, Webhook, User
from .security import require_auth, validate_json_input, rate_limit, SecurityManager
from .sms_client import SMSGatewayClient

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api_bp.route('/send', methods=['POST'])
@require_auth
@rate_limit(limit=10, window=60)  # 10 SMS per minute
@validate_json_input(['message', 'phone_numbers'])
def send_sms():
    """Send SMS with security validation"""
    try:
        data = request.validated_json
        user_id = session.get('user_id')
        
        # Validate and sanitize inputs
        message_text = SecurityManager.sanitize_input(data['message'])
        if len(message_text) > 1600:
            return jsonify({'error': 'Message too long (max 1600 characters)'}), 400
        
        # Validate phone numbers
        phone_numbers = []
        for phone in data['phone_numbers']:
            try:
                validated_phone = SecurityManager.validate_phone_number(phone)
                phone_numbers.append(validated_phone)
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        
        if len(phone_numbers) > 10:  # Limit bulk sending
            return jsonify({'error': 'Maximum 10 recipients per message'}), 400
        
        # Send SMS
        client = SMSGatewayClient()
        result = client.send_sms(
            phone_numbers=phone_numbers,
            message=message_text,
            with_delivery_report=data.get('with_delivery_report', True),
            sim_number=data.get('sim_number'),
            ttl=data.get('ttl')
        )
        
        # Store in database
        message = Message(
            id=result['id'],
            content=message_text,
            recipients=json.dumps(phone_numbers),
            state=result['state'],
            user_id=user_id
        )
        db.session.add(message)
        db.session.commit()
        
        logger.info(f"SMS sent by user {session.get('username')} to {len(phone_numbers)} recipients")
        
        return jsonify({
            'id': result['id'],
            'state': result['state'],
            'recipients': phone_numbers
        })
        
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")
        return jsonify({'error': 'Failed to send SMS'}), 500


@api_bp.route('/messages', methods=['GET'])
@require_auth
@rate_limit(limit=30, window=60)
def get_messages():
    """Get messages with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 25, type=int), 100)  # Max 100 per page
        
        user_id = session.get('user_id')
        
        # Query with proper filtering
        query = Message.query.filter_by(user_id=user_id).order_by(Message.created_at.desc())
        
        # Apply filters
        state_filter = request.args.get('state')
        if state_filter:
            query = query.filter(Message.state == state_filter)
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        messages = []
        for message in pagination.items:
            messages.append({
                'id': message.id,
                'content': message.content[:100] + '...' if len(message.content) > 100 else message.content,
                'recipients': message.recipients_list,
                'state': message.state,
                'created_at': message.created_at.isoformat()
            })
        
        return jsonify({
            'messages': messages,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        return jsonify({'error': 'Failed to fetch messages'}), 500


@api_bp.route('/contacts', methods=['GET', 'POST'])
@require_auth
@rate_limit(limit=20, window=60)
def manage_contacts():
    """Manage contacts with validation"""
    user_id = session.get('user_id')
    
    if request.method == 'GET':
        try:
            contacts = Contact.query.filter_by(user_id=user_id).order_by(Contact.name).all()
            
            return jsonify([{
                'id': contact.id,
                'name': contact.name,
                'phone': contact.phone,
                'group_name': contact.group_name,
                'notes': contact.notes
            } for contact in contacts])
            
        except Exception as e:
            logger.error(f"Error fetching contacts: {e}")
            return jsonify({'error': 'Failed to fetch contacts'}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            # Validate required fields
            name = SecurityManager.sanitize_input(data.get('name', ''))
            phone = data.get('phone', '')
            
            if not name or not phone:
                return jsonify({'error': 'Name and phone are required'}), 400
            
            # Validate phone number
            try:
                validated_phone = SecurityManager.validate_phone_number(phone)
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            
            # Check for duplicates
            existing = Contact.query.filter_by(phone=validated_phone, user_id=user_id).first()
            if existing:
                return jsonify({'error': 'Contact with this phone number already exists'}), 400
            
            # Create contact
            contact = Contact(
                name=name,
                phone=validated_phone,
                group_name=SecurityManager.sanitize_input(data.get('group_name', '')),
                notes=SecurityManager.sanitize_input(data.get('notes', '')),
                user_id=user_id
            )
            
            db.session.add(contact)
            db.session.commit()
            
            logger.info(f"Contact created by user {session.get('username')}: {name}")
            
            return jsonify({
                'id': contact.id,
                'name': contact.name,
                'phone': contact.phone
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating contact: {e}")
            return jsonify({'error': 'Failed to create contact'}), 500


@api_bp.route('/test-connection', methods=['POST'])
@require_auth
@rate_limit(limit=5, window=60)
def test_connection():
    """Test SMS gateway connection"""
    try:
        data = request.get_json()
        gateway_url = data.get('gateway_url')
        
        if not gateway_url:
            return jsonify({'error': 'Gateway URL is required'}), 400
        
        # Validate URL
        try:
            SecurityManager.validate_url(gateway_url)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Test connection
        client = SMSGatewayClient(base_url=gateway_url)
        success = client.test_connection()
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Connection failed'})
            
    except Exception as e:
        logger.error(f"Error testing connection: {e}")
        return jsonify({'success': False, 'error': 'Connection test failed'}), 500


@api_bp.route('/health', methods=['GET'])
@rate_limit(limit=60, window=60)
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': current_app.config.get('VERSION', '1.0.0')
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': 'Database connection failed'
        }), 503