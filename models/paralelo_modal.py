from database import db

class Paralelo(db.Model):
    __tablename__ = 'paralelos'
    id = db.Column(db.Integer, primary_key=True)
    paralelo = db.Column(db.String(20), nullable=False)  # Ej: "A", "B"
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semestres.id'), nullable=False)
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)
    
    curso = db.relationship('Curso',back_populates='paralelos')
    semestre = db.relationship('Semestre', back_populates='paralelos')
    turno = db.relationship('Turno',back_populates='paralelos')
    inscripciones = db.relationship('Inscripcion',back_populates='paralelos')
    
    #Pasar los parametros 
    def __init__(self,paralelo,curso_id,semestre_id,turno_id):
        self.paralelo = paralelo
        self.curso_id = curso_id
        self.semestre_id = semestre_id
        self.turno_id = turno_id
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Paralelo.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Paralelo.query.get(id)
    
    def update(self,paralelo=None,curso_id=None,semestre_id=None,turno_id=None):
        if  paralelo and curso_id and semestre_id and turno_id :
            self.paralelo = paralelo   
            self.curso_id = curso_id
            self.semestre_id = semestre_id
            self.turno_id = turno_id        
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

   