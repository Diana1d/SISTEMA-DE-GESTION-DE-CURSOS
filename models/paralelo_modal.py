from database import db

class Paralelo(db.Model):
    __tablename__ = 'paralelos'
    id = db.Column(db.Integer, primary_key=True)
    paralelo = db.Column(db.String(20), nullable=False)  # Ej: "A", "B"
    
    inscripciones = db.relationship('Inscripcion',back_populates='paralelo')
    
    @staticmethod        
    def get_all():
        return Paralelo.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Paralelo.query.get(id)
  