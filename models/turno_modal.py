from database import db

class Turno(db.Model):
    __tablename__ = 'turnos'
    id = db.Column(db.Integer, primary_key=True)
    tipo_turno = db.Column(db.String(20), nullable=False) 
    
    paralelos = db.relationship('Paralelo',back_populates='turno')
    
    
    
    #Pasar los parametros 
    def __init__(self,tipo_turno):
        self.tipo_turno = tipo_turno
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Turno.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Turno.query.get(id)
    
    def update(self,tipo_turno):
        if  tipo_turno:
            self.tipo_turno = tipo_turno      
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

   