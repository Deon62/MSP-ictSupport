from flask import Blueprint, request, jsonify
from models.user import User
from database import db
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

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

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if not user.active:
        return jsonify({'message': 'Account is deactivated'}), 401
    
    if user.is_locked():
        return jsonify({'message': 'Account is temporarily locked due to failed login attempts'}), 401
    
    if not user.check_password(data['password']):
        user.record_failed_login()
        db.session.commit()
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Successful login
    user.reset_failed_attempts()
    db.session.commit()
    
    token = user.generate_token()
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict(),
        'must_change_password': user.must_change_password
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """Change user password endpoint"""
    data = request.get_json()
    
    if not data or not data.get('current_password') or not data.get('new_password'):
        return jsonify({'message': 'Current password and new password required'}), 400
    
    if not current_user.check_password(data['current_password']):
        return jsonify({'message': 'Current password is incorrect'}), 400
    
    # Validate new password strength
    new_password = data['new_password']
    if len(new_password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400
    
    current_user.set_password(new_password)
    current_user.must_change_password = False
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user information"""
    return jsonify({
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logout endpoint (client should discard token)"""
    return jsonify({'message': 'Logout successful'}), 200 