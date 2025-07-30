from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from models.support_ticket import SupportTicket
from models.department import Department
from models.building import Building
from models.floor import Floor
from datetime import datetime
import secrets
import string
import jwt
import os
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user or not current_user.active:
                return jsonify({'message': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to require ADMIN role"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.has_permission('ADMIN'):
            return jsonify({'message': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def agent_or_admin_required(f):
    """Decorator to require agent or admin role"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.has_permission('ADMIN') and not current_user.has_permission('AGENT'):
            return jsonify({'message': 'Agent or admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Ticket Management
@admin_bp.route('/admin/tickets', methods=['GET'])
@token_required
@agent_or_admin_required
def get_tickets(current_user):
    """Get all tickets with filtering and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        department_id = request.args.get('department_id', type=int)
        building_id = request.args.get('building_id', type=int)
        assigned_to_id = request.args.get('assigned_to_id', type=int)
        
        query = SupportTicket.query
        
        if status:
            query = query.filter(SupportTicket.status == status)
        if department_id:
            query = query.filter(SupportTicket.department_id == department_id)
        if building_id:
            query = query.filter(SupportTicket.building_id == building_id)
        if assigned_to_id:
            query = query.filter(SupportTicket.assigned_to_id == assigned_to_id)
        
        tickets = query.order_by(SupportTicket.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'tickets': [ticket.to_dict() for ticket in tickets.items],
            'total': tickets.total,
            'pages': tickets.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/tickets/<int:ticket_id>/status', methods=['PATCH'])
@token_required
@agent_or_admin_required
def update_ticket_status(current_user, ticket_id):
    """Update ticket status"""
    try:
        ticket = SupportTicket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        data = request.get_json()
        new_status = data.get('status')
        notes = data.get('notes')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        valid_statuses = ['pending', 'in_progress', 'resolved', 'closed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400
        
        ticket.status = new_status
        if notes:
            ticket.notes = notes
        
        if new_status == 'resolved':
            ticket.resolved_at = datetime.utcnow()
        
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Ticket status updated successfully',
            'ticket': ticket.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Department Management
@admin_bp.route('/admin/departments', methods=['GET'])
@token_required
@admin_required
def get_departments(current_user):
    """Get all departments"""
    try:
        departments = Department.query.all()
        return jsonify({
            'departments': [dept.to_dict() for dept in departments]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/departments', methods=['POST'])
@token_required
@admin_required
def create_department(current_user):
    """Create a new department"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Department name is required'}), 400
        
        # Check if department already exists
        existing = Department.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Department already exists'}), 400
        
        department = Department(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(department)
        db.session.commit()
        
        return jsonify({
            'message': 'Department created successfully',
            'department': department.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Building Management
@admin_bp.route('/admin/buildings', methods=['GET'])
@token_required
@admin_required
def get_buildings(current_user):
    """Get all buildings"""
    try:
        buildings = Building.query.all()
        return jsonify({
            'buildings': [building.to_dict() for building in buildings]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Floor Management
@admin_bp.route('/admin/floors', methods=['GET'])
@token_required
@admin_required
def get_floors(current_user):
    """Get all floors"""
    try:
        building_id = request.args.get('building_id', type=int)
        
        if building_id:
            floors = Floor.query.filter_by(building_id=building_id).all()
        else:
            floors = Floor.query.all()
        
        return jsonify({
            'floors': [floor.to_dict() for floor in floors]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User Management
@admin_bp.route('/admin/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    """Get all users"""
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users', methods=['POST'])
@token_required
@admin_required
def create_user(current_user):
    """Create a new user"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Check if user already exists
        existing = User.query.filter_by(username=data['username']).first()
        if existing:
            return jsonify({'error': 'Username already exists'}), 400
        
        # Generate random password if not provided
        password = data.get('password') or ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        
        user = User(
            username=data['username'],
            role=data.get('role', 'VIEWER'),
            department_id=data.get('department_id'),
            active=data.get('active', True),
            must_change_password=data.get('must_change_password', True)
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict(),
            'temporary_password': password if data.get('password') is None else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
@token_required
@admin_required
def reset_user_password(current_user, user_id):
    """Reset user password"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate new random password
        new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        user.set_password(new_password)
        user.must_change_password = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Password reset successfully',
            'new_password': new_password
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 