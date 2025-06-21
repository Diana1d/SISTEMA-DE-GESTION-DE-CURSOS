from database import db

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semestres.id'), nullable=False)
    paralelo_id = db.Column(db.Integer, db.ForeignKey('paralelos.id'), nullable=False)
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)
   
    curso = db.relationship('Curso',back_populates='inscripciones')
    estudiante = db.relationship('Estudiante',back_populates='inscripciones')
    semestre = db.relationship('Semestre', back_populates='inscripciones')
    paralelo = db.relationship('Paralelo', back_populates='inscripciones')
    turno = db.relationship('Turno',back_populates='inscripciones')
    
    #Pasar los parametros 
    def __init__(self,curso_id,estudiante_id,semestre_id,paralelo_id, turno_id):
        self.curso_id =curso_id
        self.estudiante_id = estudiante_id
        self.semestre_id =semestre_id
        self.paralelo_id = paralelo_id
        self.turno_id = turno_id
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Inscripcion.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Inscripcion.query.get(id)
    
    def update(self,curso_id=None,estudiante_id=None,semestre_id=None,paralelo_id=None, turno_id=None):
        if  paralelo_id and estudiante_id :
            self.paralelo_id = paralelo_id   
            self.estudiante_id = estudiante_id           
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    