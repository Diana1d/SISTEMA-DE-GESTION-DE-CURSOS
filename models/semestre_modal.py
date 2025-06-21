from database import db
from datetime import date

class Semestre(db.Model):
    __tablename__ = 'semestres'
    id = db.Column(db.Integer, primary_key=True)
    gestion = db.Column(db.String(20), nullable=False)  # Ej: "2025-1"
    semestre_num = db.Column(db.String(50), nullable=False)  # Ej: "2025-1"
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    
    inscripciones = db.relationship('Inscripcion',back_populates='semestre')
    
    #Pasar los parametros 
    def __init__(self,gestion,semestre_num,fecha_inicio,fecha_fin):
        self.gestion = gestion
        self.semestre_num = semestre_num
        
        # Convertir string vacío a None o parsear fecha
        self.fecha_inicio = date.fromisoformat(fecha_inicio) if fecha_inicio.strip() else None
        self.fecha_fin = date.fromisoformat(fecha_fin) if fecha_fin.strip() else None
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Semestre.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Semestre.query.get(id)
    
    def update(self,gestion=None,semestre_num=None,fecha_inicio=None,fecha_fin=None):
        if  gestion and semestre_num :
            self.gestion = gestion
            self.semestre_num = semestre_num
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin        
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

   