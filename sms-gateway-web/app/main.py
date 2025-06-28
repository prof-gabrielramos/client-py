"""
Main blueprint with optimized routes
"""
from flask import Blueprint, render_template, request, session, jsonify
import logging

from .models import db, Message, Contact
from .security import require_auth
from .cache import cached, cache_key_for_user
from .performance import PerformanceMonitor

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@main_bp.route('/')
@require_auth
@PerformanceMonitor.monitor_request_time
@cached(ttl=60, key_prefix='dashboard')
def dashboard():
    """Optimized dashboard with caching"""
    try:
        user_id = session.get('user_id')
        
        # Get message statistics
        stats_query = db.session.query(
            Message.state,
            db.func.count(Message.id).label('count')
        ).filter_by(user_id=user_id).group_by(Message.state)
        
        stats = {state: count for state, count in stats_query.all()}
        
        # Get recent messages (limited to 10)
        recent_messages = Message.query.filter_by(user_id=user_id)\
            .order_by(Message.created_at.desc())\
            .limit(10)\
            .all()
        
        return render_template(
            'main/dashboard.html',
            stats=stats,
            recent_messages=recent_messages
        )
        
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('main/dashboard.html', stats={}, recent_messages=[])


@main_bp.route('/send')
@require_auth
@PerformanceMonitor.monitor_request_time
def send_page():
    """Send SMS page with contact optimization"""
    try:
        user_id = session.get('user_id')
        
        # Get contacts (limited to 20 for performance)
        contacts = Contact.query.filter_by(user_id=user_id)\
            .order_by(Contact.name)\
            .limit(20)\
            .all()
        
        return render_template('main/send.html', contacts=contacts)
        
    except Exception as e:
        logger.error(f"Send page error: {e}")
        return render_template('main/send.html', contacts=[])


@main_bp.route('/messages')
@require_auth
@PerformanceMonitor.monitor_request_time
def messages():
    """Messages page with optimized pagination"""
    try:
        user_id = session.get('user_id')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 25, type=int), 100)
        
        # Optimized query with proper indexing
        query = Message.query.filter_by(user_id=user_id)\
            .order_by(Message.created_at.desc())
        
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
        
        return render_template(
            'main/messages.html',
            messages=pagination.items,
            pagination=pagination
        )
        
    except Exception as e:
        logger.error(f"Messages page error: {e}")
        return render_template('main/messages.html', messages=[], pagination=None)


@main_bp.route('/contacts')
@require_auth
@PerformanceMonitor.monitor_request_time
def contacts():
    """Contacts page with search optimization"""
    try:
        user_id = session.get('user_id')
        search = request.args.get('search', '').strip()
        
        query = Contact.query.filter_by(user_id=user_id)
        
        if search:
            query = query.filter(
                db.or_(
                    Contact.name.ilike(f'%{search}%'),
                    Contact.phone.ilike(f'%{search}%')
                )
            )
        
        contacts = query.order_by(Contact.name).limit(100).all()
        
        return render_template('main/contacts.html', contacts=contacts)
        
    except Exception as e:
        logger.error(f"Contacts page error: {e}")
        return render_template('main/contacts.html', contacts=[])


@main_bp.route('/settings')
@require_auth
@PerformanceMonitor.monitor_request_time
def settings():
    """Settings page"""
    return render_template('main/settings.html')


@main_bp.route('/metrics')
@require_auth
def metrics():
    """System metrics endpoint (admin only)"""
    try:
        # In production, add admin role check
        metrics = PerformanceMonitor.get_system_metrics()
        return jsonify(metrics)
        
    except Exception as e:
        logger.error(f"Metrics error: {e}")
        return jsonify({'error': 'Failed to get metrics'}), 500