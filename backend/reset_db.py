#!/usr/bin/env python3
"""
Simple database reset script
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import jwt
from datetime import datetime, timedelta

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ict_support.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models with correct schema
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='VIEWER')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    active = db.Column(db.Boolean, default=True)
    must_change_password = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'department_id': self.department_id,
            'active': self.active,
            'must_change_password': self.must_change_password,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Building(db.Model):
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    contact_person = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'contact_person': self.contact_person,
            'phone_number': self.phone_number
        }

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    contact_person = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'contact_person': self.contact_person,
            'phone_number': self.phone_number
        }

class Floor(db.Model):
    __tablename__ = 'floors'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'label': self.label,
            'description': self.description
        }

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floors.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    issue_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_person = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, resolved, closed
    assigned_to = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5 star rating
    rating_comment = db.Column(db.Text)  # Optional comment with rating
    rated_at = db.Column(db.DateTime)  # When the rating was submitted
    
    # Relationships
    building = db.relationship('Building', backref='tickets')
    floor = db.relationship('Floor', backref='tickets')
    department = db.relationship('Department', backref='tickets')
    
    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'building_name': self.building.name if self.building else None,
            'floor_id': self.floor_id,
            'floor_label': self.floor.label if self.floor else None,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'issue_type': self.issue_type,
            'description': self.description,
            'contact_person': self.contact_person,
            'phone_number': self.phone_number,
            'priority': self.priority,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'notes': self.notes,
            'rating': self.rating,
            'rating_comment': self.rating_comment,
            'rated_at': self.rated_at.isoformat() if self.rated_at else None
        }

def reset_database():
    """Reset the database completely"""
    print("🗑️  Resetting database...")
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("✓ Dropped all existing tables")
        
        # Create all tables with new schema
        db.create_all()
        print("✓ Created all tables with new schema")
        
        # Seed the database
        seed_database()
        
        print("✅ Database reset completed successfully!")

def seed_database():
    """Seed the database with initial data"""
    print("\n🌱 Seeding database...")
    
    try:
        # Create default admin user
        admin_user = User(
            username='ict_support',
            role='ADMIN',
            active=True,
            must_change_password=True
        )
        admin_user.set_password('Ict@support')
        db.session.add(admin_user)
        print("✓ Created admin user: ict_support")
        
        # Create buildings first
        buildings_data = [
            {"name": "Uchumi House", "description": "Uchumi House building"},
            {"name": "KICC", "description": "KICC building"},
            {"name": "Harambee House", "description": "Harambee House building"},
            {"name": "Teleposta", "description": "Teleposta building"}
        ]
        
        buildings = {}
        for building_data in buildings_data:
            building = Building(**building_data)
            db.session.add(building)
            print(f"✓ Created building: {building_data['name']}")
        
        # Commit buildings to get their IDs
        db.session.commit()
        
        # Now get the buildings with their IDs
        for building_data in buildings_data:
            building = Building.query.filter_by(name=building_data['name']).first()
            if building:
                buildings[building_data['name']] = building
        
        # Create floors for each building
        floor_labels = [str(i) for i in range(1, 28)] + ["Background Floor", "Ground Floor"]
        
        for building_name, building in buildings.items():
            for label in floor_labels:
                floor = Floor(
                    building_id=building.id,
                    label=label,
                    description=f"Floor {label} in {building_name}"
                )
                db.session.add(floor)
            print(f"✓ Created {len(floor_labels)} floors for {building_name}")
        
        # Create departments
        departments_data = [
            {"name": "Human Resource", "description": "Human Resource department"},
            {"name": "Internal Audit", "description": "Internal Audit department"},
            {"name": "Guidance and Counselling", "description": "Guidance and Counselling department"},
            {"name": "Accounts", "description": "Accounts department"},
            {"name": "Library", "description": "Library department"},
            {"name": "Treasury", "description": "Treasury department"}
        ]
        
        for dept_data in departments_data:
            department = Department(**dept_data)
            db.session.add(department)
            print(f"✓ Created department: {dept_data['name']}")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Database seeding completed successfully!")
        
        # Verify the data
        verify_database()
        
    except Exception as e:
        print(f"✗ Error seeding database: {str(e)}")
        db.session.rollback()
        raise

def verify_database():
    """Verify that all data was created correctly"""
    print("\n🔍 Verifying database...")
    
    try:
        # Check users
        user_count = User.query.count()
        print(f"✓ Users: {user_count}")
        
        # Check buildings
        building_count = Building.query.count()
        print(f"✓ Buildings: {building_count}")
        
        # Check floors
        floor_count = Floor.query.count()
        print(f"✓ Floors: {floor_count}")
        
        # Check departments
        dept_count = Department.query.count()
        print(f"✓ Departments: {dept_count}")
        
        # Check admin user
        admin = User.query.filter_by(username='ict_support').first()
        if admin:
            print(f"✓ Admin user: {admin.username} (Role: {admin.role})")
        else:
            print("✗ Admin user not found!")
        
        print("✅ Database verification completed!")
        
    except Exception as e:
        print(f"✗ Error verifying database: {str(e)}")

def main():
    """Main function"""
    print("🔄 ICT Support System - Database Reset")
    print("=" * 50)
    
    try:
        reset_database()
        print("\n🎉 Database reset completed successfully!")
        print("\nNext steps:")
        print("1. Start the server: python app.py")
        print("2. Test the system: python ../test_system.py")
        print("3. Access admin: http://localhost:5000/admin")
        print("4. Login with: ict_support / Ict@support")
        
    except Exception as e:
        print(f"\n✗ Database reset failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 