from database import db
from datetime import datetime
#from flask_login import current_app  # Importar current_user y login_required
import os

class Material(db.Model):
    __tablename__ = 'materiales'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    nombre_archivo = db.Column(db.String(100))
    tipo_archivo = db.Column(db.String(50))
    tamanio = db.Column(db.Integer)  # Tamaño en bytes
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)

    curso = db.relationship('Curso', backref='materiales')
    docente = db.relationship('Usuario', backref='materiales')

    def __init__(self, titulo, descripcion, nombre_archivo, tipo_archivo, tamanio, curso_id, docente_id):
        self.titulo = titulo
        self.descripcion = descripcion
        self.nombre_archivo = nombre_archivo
        self.tipo_archivo = tipo_archivo
        self.tamanio = tamanio
        self.curso_id = curso_id
        self.docente_id = docente_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Material.query.get(id)

    @staticmethod
    def get_by_curso(curso_id):
        return Material.query.filter_by(curso_id=curso_id).order_by(Material.fecha_subida.desc()).all()

    @staticmethod
    def get_by_docente(docente_id):
        return Material.query.filter_by(docente_id=docente_id).order_by(Material.fecha_subida.desc()).all()

    def delete(self):
        # Eliminar el archivo físico primero
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], self.nombre_archivo))
        except:
            pass
        # Eliminar el registro de la base de datos
        db.session.delete(self)
        db.session.commit()

    def get_file_path(self):
        return os.path.join(current_app.config['UPLOAD_FOLDER'], self.nombre_archivo)

    def get_file_size(self):
        sizes = ['B', 'KB', 'MB', 'GB']
        size = self.tamanio
        i = 0
        while size >= 1024 and i < len(sizes)-1:
            size /= 1024
            i += 1
        return f"{size:.2f} {sizes[i]}"