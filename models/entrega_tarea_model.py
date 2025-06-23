from database import db
from datetime import datetime

class EntregaTarea(db.Model):
    __tablename__ = 'entrega_tarea'

    id = db.Column(db.Integer, primary_key=True)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    archivo_entregado = db.Column(db.String(255), nullable=False)  # Cambiado a nullable=False
    fecha_entrega = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    calificacion = db.Column(db.Float)
    comentarios_docente = db.Column(db.Text)
    fecha_calificacion = db.Column(db.DateTime)  # Nuevo campo útil

    tarea = db.relationship('Tarea', backref='entregas')
    estudiante = db.relationship('Estudiante', backref='entregas_tareas')  # Cambiado el backref para evitar conflicto

    def __init__(self, tarea_id, estudiante_id, archivo_entregado, calificacion=None, comentarios_docente=None):
        self.tarea_id = tarea_id
        self.estudiante_id = estudiante_id
        self.archivo_entregado = archivo_entregado
        self.calificacion = calificacion
        self.comentarios_docente = comentarios_docente

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return EntregaTarea.query.get(id)

    @staticmethod
    def get_by_tarea(tarea_id):
        return EntregaTarea.query.filter_by(tarea_id=tarea_id).all()

    @staticmethod
    def get_by_estudiante(estudiante_id):
        return EntregaTarea.query.filter_by(estudiante_id=estudiante_id).all()
    
    @staticmethod
    def get_by_estudiante_and_tarea(estudiante_id, tarea_id):
        return EntregaTarea.query.filter_by(
            estudiante_id=estudiante_id,
            tarea_id=tarea_id
        ).first()

    def update(self, calificacion=None, comentarios_docente=None):
        if calificacion is not None:
            self.calificacion = calificacion
            self.fecha_calificacion = datetime.utcnow()
        if comentarios_docente is not None:
            self.comentarios_docente = comentarios_docente
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()