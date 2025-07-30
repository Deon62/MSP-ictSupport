#!/usr/bin/env python3
"""
Database seeding utilities
"""
from database import db
from models.user import User
from models.building import Building
from models.department import Department
from models.floor import Floor
import bcrypt
from datetime import datetime

def seed_database():
    """Seed the database with initial data"""
    try:
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='ict_support').first()
        if not admin_user:
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
        
        # Check if buildings already exist
        if Building.query.count() == 0:
            # Create buildings
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
                buildings[building_data['name']] = building
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
        
        # Check if departments already exist
        if Department.query.count() == 0:
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
        print("✅ Database seeding completed!")
        
    except Exception as e:
        print(f"✗ Error seeding database: {str(e)}")
        db.session.rollback()
        raise

def reset_database():
    """Reset the database (for development)"""
    try:
        # Drop all tables
        db.drop_all()
        print("✓ Dropped all tables")
        
        # Create all tables
        db.create_all()
        print("✓ Created all tables")
        
        # Seed the database
        return seed_database()
        
    except Exception as e:
        print(f"✗ Error resetting database: {str(e)}")
        return False

if __name__ == "__main__":
    # This can be run directly to seed the database
    from app import app
    with app.app_context():
        seed_database() 