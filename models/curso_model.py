from database import db

class Curso(db.Model):
    __tablename__ = "cursos"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey("docentes.id"),nullable=False)


    docente = db.relationship("Docente", back_populates="cursos")
    
    #Pasar los parametros 
    def __init__(self,nombre,descripcion,activo,profesor_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = activo
        self.profesor_id = profesor_id
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Curso.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Curso.query.get(id)
    
    def update(self, nombre=nombre,descripcion=descripcion,activo=activo,profesor_id=profesor_id):
        if  nombre and descripcion and profesor_id:
            self.nombre = nombre
            self.descripcion = descripcion
            self.activo=activo
            self.profesor_id = profesor_id      
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    
    