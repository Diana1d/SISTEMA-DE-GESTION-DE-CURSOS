from database import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True)
    fecha_nac = db.Column(db.DateTime,nullable=False)
    genero = db.Column(db.String(10),nullable=False)
    telefono = db.Column(db.String(20),nullable=False)
    ci = db.Column(db.String(20),nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)

    usuario = db.relationship('Usuario', back_populates='estudiantes')
    inscripciones = db.relationship('Inscripcion',back_populates='estudiante')
    
    
    #Pasar los parametros 
    def __init__(self,matricula,fecha_nac, genero, telefono,ci,usuario_id):
        self.matricula = matricula
        self.fecha_nac = fecha_nac
        self.genero = genero
        self.telefono = telefono
        self.ci = ci
        self.usuario_id = usuario_id
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Estudiante.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Estudiante.query.get(id)
    
    def update(self,matricula=None,fecha_nac=None, genero=None, telefono=None,ci=None,usuario_id=None):
       if  matricula  and fecha_nac and genero and telefono and  ci and usuario_id :
            self.matricula = matricula
            self.fecha_nac = fecha_nac    
            self.genero = genero       
            self.telefono = telefono 
            self.ci = ci          
            self.usuario_id = usuario_id        
       db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def desactivar_inscripciones(self):
        for inscripcion in self.inscripciones:
            inscripcion.activo = False
        db.session.commit()

# Modificado
    