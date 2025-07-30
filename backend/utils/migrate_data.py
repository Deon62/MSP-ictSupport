from database import db
from models.support_ticket import SupportTicket
from models.building import Building
from models.department import Department
from models.floor import Floor

def migrate_ticket_data():
    """Migrate existing ticket data to use foreign keys"""
    try:
        print("Starting data migration...")
        
        # Get all tickets
        tickets = SupportTicket.query.all()
        
        for ticket in tickets:
            # Migrate building
            if hasattr(ticket, 'building') and isinstance(ticket.building, str):
                building = Building.query.filter_by(name=ticket.building).first()
                if building:
                    ticket.building_id = building.id
                    print(f"✓ Migrated building for ticket {ticket.id}: {ticket.building}")
                else:
                    # Create building if it doesn't exist
                    building = Building(name=ticket.building)
                    db.session.add(building)
                    db.session.flush()  # Get the ID
                    ticket.building_id = building.id
                    print(f"✓ Created and migrated building for ticket {ticket.id}: {ticket.building}")
            
            # Migrate department
            if hasattr(ticket, 'department') and isinstance(ticket.department, str):
                department = Department.query.filter_by(name=ticket.department).first()
                if department:
                    ticket.department_id = department.id
                    print(f"✓ Migrated department for ticket {ticket.id}: {ticket.department}")
                else:
                    # Create department if it doesn't exist
                    department = Department(name=ticket.department)
                    db.session.add(department)
                    db.session.flush()  # Get the ID
                    ticket.department_id = department.id
                    print(f"✓ Created and migrated department for ticket {ticket.id}: {ticket.department}")
            
            # Migrate floor
            if hasattr(ticket, 'floor') and isinstance(ticket.floor, str):
                # Find floor in the building
                if hasattr(ticket, 'building_id') and ticket.building_id:
                    floor = Floor.query.filter_by(
                        building_id=ticket.building_id,
                        label=ticket.floor
                    ).first()
                    
                    if floor:
                        ticket.floor_id = floor.id
                        print(f"✓ Migrated floor for ticket {ticket.id}: {ticket.floor}")
                    else:
                        # Create floor if it doesn't exist
                        floor = Floor(
                            building_id=ticket.building_id,
                            label=ticket.floor,
                            display_name=ticket.floor
                        )
                        db.session.add(floor)
                        db.session.flush()  # Get the ID
                        ticket.floor_id = floor.id
                        print(f"✓ Created and migrated floor for ticket {ticket.id}: {ticket.floor}")
        
        # Commit all changes
        db.session.commit()
        print("✓ Data migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error during migration: {str(e)}")
        db.session.rollback()
        return False

def cleanup_old_columns():
    """Remove old string columns after migration (run this after confirming migration worked)"""
    try:
        # This would require dropping and recreating the table
        # For now, we'll keep the old columns for backward compatibility
        print("Note: Old columns preserved for backward compatibility")
        return True
    except Exception as e:
        print(f"✗ Error cleaning up old columns: {str(e)}")
        return False

if __name__ == "__main__":
    from app import app
    with app.app_context():
        migrate_ticket_data() 