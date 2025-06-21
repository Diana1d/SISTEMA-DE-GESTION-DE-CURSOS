from database import db

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    leido = db.Column(db.Boolean, default=False)

    usuario = db.relationship('Usuario', backref='notificaciones')

    def __init__(self, titulo, mensaje, fecha_envio, usuario_id):
        self.titulo = titulo
        self.mensaje = mensaje
        self.fecha_envio = fecha_envio
        self.usuario_id = usuario_id
