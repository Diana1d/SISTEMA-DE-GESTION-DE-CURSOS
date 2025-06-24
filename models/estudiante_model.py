from database import db
from models.usuario_model import Usuario

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

    
    @staticmethod
    def contar_activos():
        from models.usuario_model import Usuario
        return Estudiante.query.join(Estudiante.usuario).filter(Usuario.activo == True).count()
    
     
    @staticmethod
    def contar_faltantes_est():
        registrados = db.session.query(Estudiante.usuario_id).all()
        ids_registrados = [r[0] for r in registrados]

        query = Usuario.query.filter(
            Usuario.rol.has(nombre='Estudiante'),
            Usuario.activo == True
        )
        
        if ids_registrados:
            query = query.filter(~Usuario.id.in_(ids_registrados))

        return query.count()
    
    # Añade estos métodos si no los tienes
    def obtener_perfil_estudiante(self):
        """Obtiene o crea un perfil básico si no existe"""
        if not hasattr(self, 'usuario'):
            from models.usuario_model import Usuario
            self.usuario = Usuario.query.get(self.usuario_id)
        return self

    @staticmethod
    def get_by_usuario_id(usuario_id):
        return Estudiante.query.filter_by(usuario_id=usuario_id).first()

    