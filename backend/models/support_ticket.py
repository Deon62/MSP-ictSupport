from datetime import datetime
from database import db

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