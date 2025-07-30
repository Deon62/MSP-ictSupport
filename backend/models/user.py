from datetime import datetime
from database import db
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='VIEWER')  # ADMIN, AGENT, VIEWER
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    active = db.Column(db.Boolean, default=True)
    must_change_password = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    # Relationship
    department = db.relationship('Department', backref='users')
    
    def set_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def generate_token(self):
        """Generate JWT token for user session"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'role': self.role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY', 'your-secret-key'), algorithm='HS256')
    
    def is_locked(self):
        """Check if account is locked due to failed login attempts"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False
    
    def record_failed_login(self):
        """Record failed login attempt and lock account if necessary"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=5)
    
    def reset_failed_attempts(self):
        """Reset failed login attempts on successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()
    
    def has_permission(self, required_role):
        """Check if user has required role permission"""
        role_hierarchy = {
            'ADMIN': ['ADMIN', 'AGENT', 'VIEWER'],
            'AGENT': ['AGENT', 'VIEWER'],
            'VIEWER': ['VIEWER']
        }
        return required_role in role_hierarchy.get(self.role, [])
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'active': self.active,
            'must_change_password': self.must_change_password,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}: {self.role}>' 