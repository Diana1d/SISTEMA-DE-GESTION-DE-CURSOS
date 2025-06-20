from database import db

class MaterialDidactico(db.Model):
    __tablename__ = 'material'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    archivo = db.Column(db.String(255))  # nombre o ruta del archivo
    fecha_subida = db.Column(db.DateTime, nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)

    curso = db.relationship('Curso', backref='materiales')
    docente = db.relationship('Docente', backref='materiales')

    def __init__(self, titulo, descripcion, archivo, fecha_subida, curso_id, docente_id):
        self.titulo = titulo
        self.descripcion = descripcion
        self.archivo = archivo
        self.fecha_subida = fecha_subida
        self.curso_id = curso_id
        self.docente_id = docente_id

    def save(self):
        db.session.add(self)
        db.session.commit()
