

from database import db


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
    
    def __repr__(self):
        return f'<Department {self.name}>' 