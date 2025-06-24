from database import db
from models.estudiante_model import Estudiante
from models.curso_model import Curso

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semestres.id'), nullable=False)
    paralelo_id = db.Column(db.Integer, db.ForeignKey('paralelos.id'), nullable=False)
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)
    activo = True
    #activo = db.Column(db.Boolean, default=True,nullable=False)
   
    #curso = db.relationship('Curso', back_populates='inscripciones')
    curso = db.relationship('Curso', back_populates='inscripciones', lazy='joined')
    estudiante = db.relationship('Estudiante', back_populates='inscripciones', lazy='joined')
    semestre = db.relationship('Semestre', back_populates='inscripciones')
    paralelo = db.relationship('Paralelo', back_populates='inscripciones')
    turno = db.relationship('Turno', back_populates='inscripciones')
    estudiante = db.relationship('Estudiante', back_populates='inscripciones')
    
    def __init__(self, curso_id, estudiante_id, semestre_id, paralelo_id, turno_id,activo):
        self.curso_id = curso_id
        self.estudiante_id = estudiante_id
        self.semestre_id = semestre_id
        self.paralelo_id = paralelo_id
        self.turno_id = turno_id
        self.activo = activo
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Inscripcion.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Inscripcion.query.get(id)
    
    def update(self, curso_id=None, estudiante_id=None, semestre_id=None, paralelo_id=None, turno_id=None,activo=None):
        if curso_id and estudiante_id and semestre_id and paralelo_id and turno_id :
            self.curso_id =curso_id
            self.estudiante_id = estudiante_id
            self.semestre_id =semestre_id
            self.paralelo_id = paralelo_id
            self.turno_id = turno_id 
            
        if activo is not None:
            self.activo = activo        
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def existe_inscripcion(cls, estudiante_id, curso_id):
        return db.session.query(cls).filter(
            cls.estudiante_id == estudiante_id,
            cls.curso_id == curso_id
        ).first() is not None

    @staticmethod
    def get_estudiantes_by_curso(curso_id):
        """Obtiene todos los estudiantes inscritos en un curso específico con sus usuarios"""
        return Estudiante.query.options(db.joinedload(Estudiante.usuario)).join(Inscripcion).filter(
            Inscripcion.curso_id == curso_id
        ).all()
        
    @staticmethod
    def get_cursos_by_estudiante(estudiante_id):
        return Curso.query.join(Inscripcion).filter(Inscripcion.estudiante_id == estudiante_id).all()
    
    @staticmethod
    def get_curso_by_estudiante(estudiante_id, curso_id):
        return Curso.query.join(Inscripcion).filter(
            Inscripcion.estudiante_id == estudiante_id,
            Inscripcion.curso_id == curso_id
        ).first()