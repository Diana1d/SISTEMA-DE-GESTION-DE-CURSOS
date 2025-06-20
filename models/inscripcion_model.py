from database import db

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True)
    paralelo_id = db.Column(db.Integer, db.ForeignKey('paralelos.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)

    paralelos = db.relationship('Paralelo', back_populates='inscripciones')
    estudiante = db.relationship('Estudiante',back_populates='inscripciones')
    
    #Pasar los parametros 
    def __init__(self,paralelo_id, estudiante_id):
        self.paralelo_id = paralelo_id
        self.estudiante_id = estudiante_id
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Inscripcion.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Inscripcion.query.get(id)
    
    def update(self,paralelo_id=None, estudiante_id=None):
        if  paralelo_id and estudiante_id :
            self.paralelo_id = paralelo_id   
            self.estudiante_id = estudiante_id           
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    