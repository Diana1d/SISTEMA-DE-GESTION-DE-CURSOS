from database import db

class Asignacion(db.Model):
    __tablename__ = 'asignaciones'

    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semestres.id'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, nullable=False)

    docente = db.relationship('Docente', backref='asignaciones')
    curso = db.relationship('Curso', backref='asignaciones')
    semestre = db.relationship('Semestre', backref='asignaciones')

    def __init__(self, docente_id, curso_id, semestre_id, fecha_asignacion):
        self.docente_id = docente_id
        self.curso_id = curso_id
        self.semestre_id = semestre_id
        self.fecha_asignacion = fecha_asignacion

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Asignacion.query.all()

    @staticmethod
    def get_by_id(id):
        return Asignacion.query.get(id)

    @staticmethod
    def get_by_docente(docente_id):
        return Asignacion.query.filter_by(docente_id=docente_id).all()

    @staticmethod
    def get_by_curso(curso_id):
        return Asignacion.query.filter_by(curso_id=curso_id).all()

    def update(self, docente_id=None, curso_id=None, semestre_id=None, fecha_asignacion=None):
        if docente_id:
            self.docente_id = docente_id
        if curso_id:
            self.curso_id = curso_id
        if semestre_id:
            self.semestre_id = semestre_id
        if fecha_asignacion:
            self.fecha_asignacion = fecha_asignacion
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()