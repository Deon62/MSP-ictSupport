

from database import db


class Building(db.Model):
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200))
    floors = db.Column(db.Integer)
    description = db.Column(db.Text)
    contact_person = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'floors': self.floors,
            'description': self.description,
            'contact_person': self.contact_person,
            'phone_number': self.phone_number
        }
    
    def __repr__(self):
        return f'<Building {self.name}>' 