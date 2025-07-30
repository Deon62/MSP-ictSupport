from models.building import Building
from models.department import Department
from models.support_ticket import SupportTicket
from database import db

def initialize_sample_data():
    """Initialize sample data for the ICT Support System"""
    
    # Check if data already exists
    if Building.query.first() is not None:
        print("Sample data already exists. Skipping initialization.")
        return
    
    # Create sample buildings
    buildings = [
        {
            'name': 'Teleposta Tower',
            'address': 'Kenya Road, Nairobi',
            'floors': 27,
            'description': 'Main building with 27 floors - largest building',
            'contact_person': 'John Kamau',
            'phone_number': '+254-700-123-456'
        },
        {
            'name': 'Annex Building A',
            'address': 'Haile Selassie Avenue, Nairobi',
            'floors': 8,
            'description': 'Annex building with administrative offices',
            'contact_person': 'Mary Wanjiku',
            'phone_number': '+254-700-123-457'
        },
        {
            'name': 'Annex Building B',
            'address': 'Moi Avenue, Nairobi',
            'floors': 12,
            'description': 'Secondary annex building',
            'contact_person': 'Peter Otieno',
            'phone_number': '+254-700-123-458'
        },
        {
            'name': 'Regional Office',
            'address': 'Nakuru Highway, Nairobi',
            'floors': 5,
            'description': 'Regional operations center',
            'contact_person': 'Sarah Muthoni',
            'phone_number': '+254-700-123-459'
        }
    ]
    
    for building_data in buildings:
        building = Building(**building_data)
        db.session.add(building)
    
    # Create sample departments
    departments = [
        {
            'name': 'ICT Department',
            'building': 'Teleposta Tower',
            'floor': '15',
            'description': 'Information and Communication Technology',
            'contact_person': 'David Kimani',
            'phone_number': '+254-700-123-460'
        },
        {
            'name': 'Human Resources',
            'building': 'Teleposta Tower',
            'floor': '8',
            'description': 'Human Resources and Administration',
            'contact_person': 'Grace Njeri',
            'phone_number': '+254-700-123-461'
        },
        {
            'name': 'Finance Department',
            'building': 'Teleposta Tower',
            'floor': '12',
            'description': 'Finance and Accounting',
            'contact_person': 'James Kiprop',
            'phone_number': '+254-700-123-462'
        },
        {
            'name': 'Customer Service',
            'building': 'Annex Building A',
            'floor': '3',
            'description': 'Customer Support and Relations',
            'contact_person': 'Alice Ochieng',
            'phone_number': '+254-700-123-463'
        },
        {
            'name': 'Operations',
            'building': 'Annex Building B',
            'floor': '6',
            'description': 'Operations and Logistics',
            'contact_person': 'Robert Mwangi',
            'phone_number': '+254-700-123-464'
        },
        {
            'name': 'Legal Department',
            'building': 'Teleposta Tower',
            'floor': '20',
            'description': 'Legal Affairs and Compliance',
            'contact_person': 'Patricia Akinyi',
            'phone_number': '+254-700-123-465'
        },
        {
            'name': 'Marketing',
            'building': 'Annex Building A',
            'floor': '5',
            'description': 'Marketing and Communications',
            'contact_person': 'Michael Odhiambo',
            'phone_number': '+254-700-123-466'
        },
        {
            'name': 'Research & Development',
            'building': 'Teleposta Tower',
            'floor': '25',
            'description': 'Research and Development Division',
            'contact_person': 'Dr. Elizabeth Wambui',
            'phone_number': '+254-700-123-467'
        }
    ]
    
    for dept_data in departments:
        department = Department(**dept_data)
        db.session.add(department)
    
    # Create sample support tickets
    sample_tickets = [
        {
            'building': 'Teleposta Tower',
            'floor': '15',
            'department': 'ICT Department',
            'issue_type': 'WiFi Connectivity',
            'description': 'WiFi connection is very slow on the 15th floor. Need assistance to improve network speed.',
            'contact_person': 'David Kimani',
            'phone_number': '+254-700-123-460',
            'priority': 'high',
            'status': 'pending'
        },
        {
            'building': 'Annex Building A',
            'floor': '3',
            'department': 'Customer Service',
            'issue_type': 'Printer Issues',
            'description': 'Printer in customer service office is not printing. Shows error message "Paper Jam" but no paper is stuck.',
            'contact_person': 'Alice Ochieng',
            'phone_number': '+254-700-123-463',
            'priority': 'medium',
            'status': 'in_progress'
        },
        {
            'building': 'Teleposta Tower',
            'floor': '8',
            'department': 'Human Resources',
            'issue_type': 'Projector Setup',
            'description': 'Need help setting up projector in boardroom for presentation tomorrow morning.',
            'contact_person': 'Grace Njeri',
            'phone_number': '+254-700-123-461',
            'priority': 'medium',
            'status': 'pending'
        },
        {
            'building': 'Annex Building B',
            'floor': '6',
            'department': 'Operations',
            'issue_type': 'Computer Hardware',
            'description': 'Computer screen is showing blue screen error. Need urgent replacement or repair.',
            'contact_person': 'Robert Mwangi',
            'phone_number': '+254-700-123-464',
            'priority': 'urgent',
            'status': 'pending'
        },
        {
            'building': 'Teleposta Tower',
            'floor': '12',
            'department': 'Finance Department',
            'issue_type': 'Software Installation',
            'description': 'Need Microsoft Excel updated to latest version for financial reporting.',
            'contact_person': 'James Kiprop',
            'phone_number': '+254-700-123-462',
            'priority': 'low',
            'status': 'resolved'
        }
    ]
    
    for ticket_data in sample_tickets:
        ticket = SupportTicket(**ticket_data)
        db.session.add(ticket)
    
    # Commit all changes
    try:
        db.session.commit()
        print("Sample data initialized successfully!")
        print(f"Created {len(buildings)} buildings")
        print(f"Created {len(departments)} departments")
        print(f"Created {len(sample_tickets)} sample tickets")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing sample data: {e}") 