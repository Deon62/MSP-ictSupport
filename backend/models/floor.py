from database import db

class Floor(db.Model):
    __tablename__ = 'floors'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    label = db.Column(db.String(50), nullable=False)  # "1", "2", "Background Floor", "Ground Floor"
    description = db.Column(db.Text)
    
    # Relationship
    building = db.relationship('Building', backref='floors')
    
    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'building_name': self.building.name if self.building else None,
            'label': self.label,
            'description': self.description
        }
    
    def __repr__(self):
        return f'<Floor {self.label} in {self.building.name if self.building else "Unknown Building"}>' 