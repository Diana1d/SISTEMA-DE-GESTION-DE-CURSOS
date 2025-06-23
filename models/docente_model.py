from database import db
from models.usuario_model import Usuario

class Docente(db.Model):
    __tablename__='docentes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    fecha_nac = db.Column(db.DateTime,nullable=False)
    genero = db.Column(db.String(10),nullable=False)
    telefono = db.Column(db.String(20),nullable=False)
    ci = db.Column(db.String(20),nullable=False)
    especialidad = db.Column(db.String(100),nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)
    
    #relacion con la tabla usuario,cursos
    usuario = db.relationship('Usuario', back_populates='docentes')
    cursos = db.relationship('Curso', back_populates='docente')
    
    #Pasar los parametros 
    def __init__(self,fecha_nac, genero, telefono,ci,especialidad,usuario_id):
        self.fecha_nac = fecha_nac
        self.genero = genero
        self.telefono = telefono
        self.ci = ci
        self.especialidad = especialidad
        self.usuario_id = usuario_id
        
       
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Docente.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Docente.query.get(id)
    
    def update(self,fecha_nac=None, genero=None, telefono=None,ci=None,especialidad=None,usuario_id=None):
        if  fecha_nac and genero and telefono and  ci and especialidad and usuario_id :
            self.fecha_nac = fecha_nac    
            self.genero = genero       
            self.telefono = telefono 
            self.ci = ci          
            self.especialidad = especialidad
            self.usuario_id = usuario_id         
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def contar_activos():
        from models.usuario_model import Usuario
        return Docente.query.join(Docente.usuario).filter(Usuario.activo == True).count()
    
    @staticmethod
    def contar_faltantes():
        # Obtener todos los usuario_id que ya están registrados como docentes
        registrados = db.session.query(Docente.usuario_id).all()
        ids_registrados = [r[0] for r in registrados]

        # Contar los usuarios con rol 'Docente' que no estén en la tabla Docente
        return Usuario.query.filter(
            Usuario.rol.has(nombre='Docente'),
            Usuario.id.notin_(ids_registrados),
            Usuario.activo == True
        ).count()



    
     

    

