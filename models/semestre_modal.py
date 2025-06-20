from database import db

class Semestre(db.Model):
    __tablename__ = 'semestres'
    id = db.Column(db.Integer, primary_key=True)
    gestion = db.Column(db.String(20), nullable=False)  # Ej: "2025-1"
    semestre_num = db.Column(db.String(50), nullable=False)  # Ej: "2025-1"
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    
    paralelos = db.relationship('Paralelo',back_populates='semestre')
    
    #Pasar los parametros 
    def __init__(self,gestion,semestre_num,fecha_inicio,fecha_fin):
        self.gestion = gestion
        self.semestre_num = semestre_num
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Semestre.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Semestre.query.get(id)
    
    def update(self,gestion,semestre_num,fecha_inicio,fecha_fin):
        if  gestion and semestre_num and fecha_inicio and fecha_fin :
            self.gestion = gestion
            self.semestre_num = semestre_num
            self.fecha_inicio = fecha_inicio
            self.fecha_fin = fecha_fin        
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

   