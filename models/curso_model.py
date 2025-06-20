from database import db

class Curso(db.Model):
    __tablename__ = 'cursos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'),nullable=False)

    #relacion
    docente = db.relationship('Docente', back_populates='cursos')
    paralelos = db.relationship('Paralelo',back_populates='curso') 
    
    #Pasar los parametros 
    def __init__(self,nombre,descripcion,activo,docente_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = activo
        self.docente_id = docente_id
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Curso.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Curso.query.get(id)
    
    def update(self, nombre=None,descripcion=None,activo=None,docente_id=None):
        if  nombre and descripcion and docente_id:
            self.nombre = nombre
            self.descripcion = descripcion
            self.activo=activo
            self.docente_id = docente_id      
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    

    
    
    