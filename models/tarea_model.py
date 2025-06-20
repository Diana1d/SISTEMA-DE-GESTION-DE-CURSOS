from database import db

class Tarea(db.Model):
    __tablename__ = 'tareas'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    archivo_adjunto = db.Column(db.String(255))

    curso = db.relationship('Curso', backref='tareas')
    docente = db.relationship('Docente', backref='tareas')

    def __init__(self, titulo, descripcion, fecha_entrega, curso_id, docente_id, archivo_adjunto=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_entrega = fecha_entrega
        self.curso_id = curso_id
        self.docente_id = docente_id
        self.archivo_adjunto = archivo_adjunto
