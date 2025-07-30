from flask import Blueprint, request, jsonify
from datetime import datetime
from models.support_ticket import SupportTicket
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
        
        # Create new ticket
        ticket = SupportTicket(
            building=data['building'],
            floor=data['floor'],
            department=data['department'],
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
            query = query.filter(SupportTicket.building == building)
        if department:
            query = query.filter(SupportTicket.department == department)
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
        ticket = SupportTicket.query.get_or_404(ticket_id)
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/<int:ticket_id>/status', methods=['PUT'])
def update_ticket_status(ticket_id):
    """Update ticket status with notifications"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        ticket = SupportTicket.query.get_or_404(ticket_id)
        old_status = ticket.status
        ticket.status = new_status
        ticket.notes = notes
        ticket.updated_at = datetime.now()
        
        # Set resolved_at if status is resolved
        if new_status == 'resolved':
            ticket.resolved_at = datetime.now()
        
        db.session.commit()
        
        # Create notification message
        status_messages = {
            'pending': 'Your ticket is pending review',
            'in_progress': 'ICT team is working on your issue',
            'resolved': 'Your issue has been resolved',
            'closed': 'Ticket has been closed'
        }
        
        notification = status_messages.get(new_status, f'Ticket status updated to {new_status}')
        
        return jsonify({
            'message': 'Ticket status updated successfully',
            'ticket_id': ticket.id,
            'status': ticket.status,
            'notification': notification,
            'status_changed': old_status != new_status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/<int:ticket_id>/assign', methods=['PUT'])
def assign_ticket(ticket_id):
    """Assign ticket to ICT staff member"""
    try:
        data = request.get_json()
        assigned_to = data.get('assigned_to')
        
        if not assigned_to:
            return jsonify({'error': 'Assigned_to is required'}), 400
        
        ticket = SupportTicket.query.get_or_404(ticket_id)
        ticket.assigned_to = assigned_to
        ticket.updated_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Ticket assigned successfully',
            'ticket_id': ticket.id,
            'assigned_to': ticket.assigned_to,
            'notification': f'Ticket #{ticket.id} assigned to {assigned_to}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard overview with statistics"""
    try:
        # Get counts by status
        status_counts = {
            'pending': SupportTicket.query.filter_by(status='pending').count(),
            'in_progress': SupportTicket.query.filter_by(status='in_progress').count(),
            'resolved': SupportTicket.query.filter_by(status='resolved').count(),
            'closed': SupportTicket.query.filter_by(status='closed').count()
        }
        
        # Get counts by priority
        priority_counts = {
            'low': SupportTicket.query.filter_by(priority='low').count(),
            'medium': SupportTicket.query.filter_by(priority='medium').count(),
            'high': SupportTicket.query.filter_by(priority='high').count(),
            'urgent': SupportTicket.query.filter_by(priority='urgent').count()
        }
        
        # Get counts by building
        buildings = db.session.query(SupportTicket.building, db.func.count(SupportTicket.id)).group_by(SupportTicket.building).all()
        building_counts = {building: count for building, count in buildings}
        
        # Get recent tickets
        recent_tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).limit(5).all()
        
        return jsonify({
            'status_counts': status_counts,
            'priority_counts': priority_counts,
            'building_counts': building_counts,
            'recent_tickets': [ticket.to_dict() for ticket in recent_tickets],
            'total_tickets': sum(status_counts.values())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 