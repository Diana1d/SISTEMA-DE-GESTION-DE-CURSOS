from database import db

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    
    #relacion con la tabla usuario
    usuarios = db.relationship('Usuario', back_populates='rol')
    
    @staticmethod        
    def get_all():
        return Rol.query.all()
    
    
