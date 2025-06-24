from database import db
from flask import render_template
from models.evaluacion_model import Evaluacion
from models.estudiante_model import Estudiante
from sqlalchemy import func

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    evaluacion_id = db.Column(db.Integer, db.ForeignKey('evaluaciones.id'), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)
    comentarios = db.Column(db.Text)

    estudiante = db.relationship('Estudiante', backref='calificaciones')
    evaluacion = db.relationship('Evaluacion', backref='calificaciones')

    def __init__(self, estudiante_id, evaluacion_id, nota, fecha_registro, comentarios=None):
        self.estudiante_id = estudiante_id
        self.evaluacion_id = evaluacion_id
        self.nota = nota
        self.fecha_registro = fecha_registro
        self.comentarios = comentarios

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Calificacion.query.all()

    @staticmethod
    def get_by_id(id):
        return Calificacion.query.get(id)

    @staticmethod
    def get_by_estudiante(estudiante_id):
        return Calificacion.query.filter_by(estudiante_id=estudiante_id).all()

    @staticmethod
    def get_by_evaluacion(evaluacion_id):
        return Calificacion.query.filter_by(evaluacion_id=evaluacion_id).all()
    
    @staticmethod
    def get_by_estudiante_and_curso(estudiante_id, curso_id):
        return Calificacion.query.join(Evaluacion).filter(
            Calificacion.estudiante_id == estudiante_id,
            Evaluacion.curso_id == curso_id
        ).all()
        
    @staticmethod
    def calcular_promedio_curso(curso_id, estudiante_id=None):
        # Consulta que une Calificacion -> Evaluacion -> Curso
        query = db.session.query(
            func.avg(Calificacion.nota).label('promedio')
        ).join(
            Evaluacion,
            Calificacion.evaluacion_id == Evaluacion.id
        ).filter(
            Evaluacion.curso_id == curso_id
        )
        
        if estudiante_id:
            query = query.filter(
                Calificacion.estudiante_id == estudiante_id
            )
        
        promedio = query.scalar()
        return float(promedio) if promedio is not None else 0.0

    def update(self, nota=None, comentarios=None):
        if nota is not None:
            self.nota = nota
        if comentarios is not None:
            self.comentarios = comentarios
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()