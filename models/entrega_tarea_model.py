from database import db

class EntregaTarea(db.Model):
    __tablename__ = 'entrega_tarea'

    id = db.Column(db.Integer, primary_key=True)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    archivo_entregado = db.Column(db.String(255))
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    calificacion = db.Column(db.Float)
    comentarios_docente = db.Column(db.Text)

    tarea = db.relationship('Tarea', backref='entregas')
    estudiante = db.relationship('Estudiante', backref='entregas')

    def __init__(self, tarea_id, estudiante_id, archivo_entregado, fecha_entrega, calificacion=None, comentarios_docente=None):
        self.tarea_id = tarea_id
        self.estudiante_id = estudiante_id
        self.archivo_entregado = archivo_entregado
        self.fecha_entrega = fecha_entrega
        self.calificacion = calificacion
        self.comentarios_docente = comentarios_docente
