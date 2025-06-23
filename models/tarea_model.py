from database import db
from datetime import datetime

class Tarea(db.Model):
    __tablename__ = 'tareas'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)  # Nuevo campo
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    archivo_adjunto = db.Column(db.String(255))
    estado = db.Column(db.String(20), default='activa')  # 'activa', 'completada', 'cancelada'

    curso = db.relationship('Curso', backref='tareas_asignadas')  # Cambiado backref
    docente = db.relationship('Docente', backref='tareas_creadas')  # Cambiado backref

    def __init__(self, titulo, descripcion, fecha_entrega, curso_id, docente_id, archivo_adjunto=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_entrega = fecha_entrega
        self.curso_id = curso_id
        self.docente_id = docente_id
        self.archivo_adjunto = archivo_adjunto

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Tarea.query.get(id)

    @staticmethod
    def get_by_curso(curso_id):
        return Tarea.query.filter_by(curso_id=curso_id).order_by(Tarea.fecha_entrega.asc()).all()

    @staticmethod
    def get_by_docente(docente_id):
        return Tarea.query.filter_by(docente_id=docente_id).order_by(Tarea.fecha_entrega.asc()).all()

    def update(self, titulo=None, descripcion=None, fecha_entrega=None, estado=None):
        if titulo:
            self.titulo = titulo
        if descripcion:
            self.descripcion = descripcion
        if fecha_entrega:
            self.fecha_entrega = fecha_entrega
        if estado:
            self.estado = estado
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
