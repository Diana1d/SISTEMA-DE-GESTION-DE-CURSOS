from database import db

class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Examen, Tarea, Proyecto, etc.
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    peso = db.Column(db.Float, nullable=False)  # Peso en la calificación final (ej. 0.3 para 30%)

    curso = db.relationship('Curso', backref='evaluaciones')

    def __init__(self, nombre, descripcion, fecha, tipo, curso_id, peso):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha
        self.tipo = tipo
        self.curso_id = curso_id
        self.peso = peso

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Evaluacion.query.all()

    @staticmethod
    def get_by_id(id):
        return Evaluacion.query.get(id)

    @staticmethod
    def get_by_curso(curso_id):
        return Evaluacion.query.filter_by(curso_id=curso_id).all()

    def update(self, nombre=None, descripcion=None, fecha=None, tipo=None, peso=None):
        if nombre:
            self.nombre = nombre
        if descripcion:
            self.descripcion = descripcion
        if fecha:
            self.fecha = fecha
        if tipo:
            self.tipo = tipo
        if peso:
            self.peso = peso
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()