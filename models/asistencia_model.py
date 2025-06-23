from database import db
from datetime import datetime

class Asistencia(db.Model):
    __tablename__ = 'asistencias'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, default=False, nullable=False)
    hora_registro = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante = db.relationship('Estudiante', backref='asistencias')
    curso = db.relationship('Curso', backref='asistencias')

    def __init__(self, estudiante_id, curso_id, fecha, presente):
        self.estudiante_id = estudiante_id
        self.curso_id = curso_id
        self.fecha = fecha
        self.presente = presente

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Asistencia.query.all()

    @staticmethod
    def get_by_id(id):
        return Asistencia.query.get(id)

    @staticmethod
    def get_by_estudiante(estudiante_id):
        return Asistencia.query.filter_by(estudiante_id=estudiante_id).all()

    @staticmethod
    def get_by_curso(curso_id):
        return Asistencia.query.filter_by(curso_id=curso_id).all()

    @staticmethod
    def get_by_curso_and_date(curso_id, fecha):
        return Asistencia.query.filter_by(curso_id=curso_id, fecha=fecha).all()

    @staticmethod
    def register(estudiante_id, curso_id, fecha, presente):
        asistencia = Asistencia(estudiante_id=estudiante_id, curso_id=curso_id, 
                              fecha=fecha, presente=presente)
        asistencia.save()
        return asistencia

    def update(self, presente=None):
        if presente is not None:
            self.presente = presente
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()