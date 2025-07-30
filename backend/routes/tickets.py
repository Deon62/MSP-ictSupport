from flask import Blueprint, request, jsonify
from datetime import datetime
from models.support_ticket import SupportTicket
from models.building import Building
from models.department import Department
from models.floor import Floor
from database import db

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets', methods=['POST'])
def create_ticket():
    """Create a new support ticket"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['building', 'floor', 'department', 'issue_type', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Handle building (can be ID or name)
        building_id = None
        if isinstance(data['building'], int):
            building_id = data['building']
        else:
            building = Building.query.filter_by(name=data['building']).first()
            if building:
                building_id = building.id
            else:
                return jsonify({'error': f'Building not found: {data["building"]}'}), 400
        
        # Handle department (can be ID or name)
        department_id = None
        if isinstance(data['department'], int):
            department_id = data['department']
        else:
            department = Department.query.filter_by(name=data['department']).first()
            if department:
                department_id = department.id
            else:
                return jsonify({'error': f'Department not found: {data["department"]}'}), 400
        
        # Handle floor (can be ID or name)
        floor_id = None
        if isinstance(data['floor'], int):
            floor_id = data['floor']
        else:
            floor = Floor.query.filter_by(building_id=building_id, label=data['floor']).first()
            if floor:
                floor_id = floor.id
            else:
                return jsonify({'error': f'Floor not found: {data["floor"]} in building {data["building"]}'}), 400
        
        # Create new ticket
        ticket = SupportTicket(
            building_id=building_id,
            floor_id=floor_id,
            department_id=department_id,
            issue_type=data['issue_type'],
            description=data['description'],
            contact_person=data.get('contact_person', ''),
            phone_number=data.get('phone_number', ''),
            priority=data.get('priority', 'medium')
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'message': 'Ticket created successfully',
            'ticket_id': ticket.id,
            'status': 'pending',
            'notification': f'Ticket #{ticket.id} created successfully. You will be notified when status changes.'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets with enhanced filtering and search"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        building = request.args.get('building')
        department = request.args.get('department')
        priority = request.args.get('priority')
        search = request.args.get('search')  # Search in description and contact person
        
        query = SupportTicket.query
        
        if status:
            query = query.filter(SupportTicket.status == status)
        if building:
            # Handle both building name and ID
            if building.isdigit():
                query = query.filter(SupportTicket.building_id == int(building))
            else:
                building_obj = Building.query.filter_by(name=building).first()
                if building_obj:
                    query = query.filter(SupportTicket.building_id == building_obj.id)
        if department:
            # Handle both department name and ID
            if department.isdigit():
                query = query.filter(SupportTicket.department_id == int(department))
            else:
                dept_obj = Department.query.filter_by(name=department).first()
                if dept_obj:
                    query = query.filter(SupportTicket.department_id == dept_obj.id)
        if priority:
            query = query.filter(SupportTicket.priority == priority)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    SupportTicket.description.ilike(search_term),
                    SupportTicket.contact_person.ilike(search_term),
                    SupportTicket.issue_type.ilike(search_term)
                )
            )
        
        tickets = query.order_by(SupportTicket.created_at.desc()).all()
        
        # Add notification count for pending tickets
        pending_count = SupportTicket.query.filter_by(status='pending').count()
        in_progress_count = SupportTicket.query.filter_by(status='in_progress').count()
        
        return jsonify({
            'tickets': [ticket.to_dict() for ticket in tickets],
            'summary': {
                'total': len(tickets),
                'pending': pending_count,
                'in_progress': in_progress_count,
                'resolved': SupportTicket.query.filter_by(status='resolved').count(),
                'closed': SupportTicket.query.filter_by(status='closed').count()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket by ID"""
    try:
        ticket = SupportTicket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        return jsonify({'ticket': ticket.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/<int:ticket_id>/status', methods=['PUT'])
def update_ticket_status(ticket_id):
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

@tickets_bp.route('/tickets/<int:ticket_id>/assign', methods=['PUT'])
def assign_ticket(ticket_id):
    """Assign ticket to a user"""
    try:
        ticket = SupportTicket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        data = request.get_json()
        assigned_to_id = data.get('assigned_to_id')
        
        if not assigned_to_id:
            return jsonify({'error': 'Assigned user ID is required'}), 400
        
        ticket.assigned_to_id = assigned_to_id
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Ticket assigned successfully',
            'ticket': ticket.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard statistics"""
    try:
        # Get counts by status
        status_counts = {
            'pending': SupportTicket.query.filter_by(status='pending').count(),
            'in_progress': SupportTicket.query.filter_by(status='in_progress').count(),
            'resolved': SupportTicket.query.filter_by(status='resolved').count(),
            'closed': SupportTicket.query.filter_by(status='closed').count(),
            'cancelled': SupportTicket.query.filter_by(status='cancelled').count()
        }
        
        # Get counts by priority
        priority_counts = {
            'low': SupportTicket.query.filter_by(priority='low').count(),
            'medium': SupportTicket.query.filter_by(priority='medium').count(),
            'high': SupportTicket.query.filter_by(priority='high').count(),
            'urgent': SupportTicket.query.filter_by(priority='urgent').count()
        }
        
        # Get recent tickets
        recent_tickets = SupportTicket.query.order_by(
            SupportTicket.created_at.desc()
        ).limit(5).all()
        
        return jsonify({
            'status_counts': status_counts,
            'priority_counts': priority_counts,
            'recent_tickets': [ticket.to_dict() for ticket in recent_tickets],
            'total_tickets': sum(status_counts.values())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """Delete a ticket"""
    try:
        ticket = SupportTicket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        db.session.delete(ticket)
        db.session.commit()
        
        return jsonify({
            'message': 'Ticket deleted successfully',
            'ticket_id': ticket_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 