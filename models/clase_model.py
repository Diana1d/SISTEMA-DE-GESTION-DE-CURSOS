from database import db

class Clase(db.Model):
    __tablename__ = 'clases'
    
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    fecha = db.Column(db.DateTime, nullable=False)
    tema = db.Column(db.String(200))
    
    curso = db.relationship('Curso', back_populates='clases')
    
    def __repr__(self):
        return f'<Clase {self.id} - Curso {self.curso_id}>'