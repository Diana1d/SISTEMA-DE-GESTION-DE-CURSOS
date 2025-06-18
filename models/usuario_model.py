from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__="usuarios"
    
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(80),nullable=False)
    apellido = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String,nullable=False)
    activo = db.Column(db.Boolean, default=True)
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"), nullable=False)
    
    #relacion con la tabla rol
    rol = db.relationship("Rol", back_populates="usuarios")
    docentes = db.relationship("Docente", back_populates="usuario")
    estudiantes = db.relationship("Estudiante", back_populates="usuario")
    
    #Pasar los parametros 
    def __init__(self, nombre, apellido, email, username, password, activo,rol_id):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.username = username
        self.password = self.hash_password(password)
        self.activo = activo
        self.rol_id = rol_id
       
    #devuelve el password encriptado 
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod        
    def get_all():
        return Usuario.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)
    
    def update(self,nombre=None,apellido=None,email=None,username=None,password=None,activo=None,rol_id=None):
        if nombre:
            self.nombre = nombre    
        if apellido:
            self.apellido = apellido 
        if email and email != self.email:
        # Verifica si el email ya está en uso por otro usuario
            existente = Usuario.query.filter_by(email=email).first()
            if existente and existente.id != self.id:
                raise ValueError("El email ya está en uso por otro usuario.")
            self.email = email       
        if username:
            self.username = username           
        if password:
            self.password = self.hash_password(password)
        if activo is not None:
            self.activo = activo            
        if rol_id:
            self.rol_id = rol_id
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
     
    @staticmethod
    def get_by_id(user_id):
        return Usuario.query.get(user_id)
    
    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(username=username).first()   

