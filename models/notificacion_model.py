from database import db
from datetime import datetime

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    leido = db.Column(db.Boolean, default=False)
    tipo = db.Column(db.String(20))  # Nuevo campo: 'sistema', 'curso', 'tarea', etc.

    usuario = db.relationship('Usuario', backref='notificaciones_recibidas')  # Cambiado backref

    def __init__(self, titulo, mensaje, usuario_id, tipo='sistema'):
        self.titulo = titulo
        self.mensaje = mensaje
        self.usuario_id = usuario_id
        self.tipo = tipo

    def save(self):
        db.session.add(self)
        db.session.commit()

    def marcar_como_leido(self):
        self.leido = True
        db.session.commit()

    def marcar_como_no_leido(self):
        self.leido = False
        db.session.commit()

    @staticmethod
    def get_by_usuario(usuario_id, leido=None):
        query = Notificacion.query.filter_by(usuario_id=usuario_id)
        if leido is not None:
            query = query.filter_by(leido=leido)
        return query.order_by(Notificacion.fecha_envio.desc()).all()

    @staticmethod
    def get_no_leidas(usuario_id):
        return Notificacion.get_by_usuario(usuario_id, leido=False)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
