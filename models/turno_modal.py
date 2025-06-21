from database import db

class Turno(db.Model):
    __tablename__ = 'turnos'
    id = db.Column(db.Integer, primary_key=True)
    tipo_turno = db.Column(db.String(20), nullable=False) 
    
    inscripciones = db.relationship('Inscripcion',back_populates='turno')
        
    @staticmethod        
    def get_all():
        return Turno.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Turno.query.get(id)
    

    

   