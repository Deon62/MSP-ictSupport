from datetime import datetime
from database import db

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'building': self.building,
            'floor': self.floor,
            'department': self.department,
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
            'notification': self._get_notification_message()
        }
    
    def _get_notification_message(self):
        """Get notification message based on status"""
        status_messages = {
            'pending': 'Your ticket is pending review',
            'in_progress': 'ICT team is working on your issue',
            'resolved': 'Your issue has been resolved',
            'closed': 'Ticket has been closed'
        }
        return status_messages.get(self.status, f'Ticket status: {self.status}')
    
    def __repr__(self):
        return f'<SupportTicket {self.id}: {self.issue_type} - {self.status}>' 