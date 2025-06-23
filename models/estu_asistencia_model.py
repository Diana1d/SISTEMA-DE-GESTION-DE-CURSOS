from datetime import datetime
from database import db
from models.inscripcion_model import Inscripcion

class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    
    id = db.Column(db.Integer, primary_key=True)
    inscripcion_id = db.Column(db.Integer, db.ForeignKey('inscripciones.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, default=True)
    observaciones = db.Column(db.String(200))
    
    # Relación con Inscripcion
    inscripcion = db.relationship('Inscripcion', back_populates='asistencias')
    
    def __repr__(self):
        return f'<Asistencia {self.id} - {self.fecha} - {"Presente" if self.presente else "Ausente"}>'
    
    @staticmethod
    def get_by_estudiante(estudiante_id):
        """Obtiene todas las asistencias de un estudiante ordenadas por fecha descendente"""
        return Asistencia.query\
            .join(Inscripcion)\
            .filter(Inscripcion.estudiante_id == estudiante_id)\
            .order_by(Asistencia.fecha.desc())\
            .all()
    
    @classmethod
    def crear_asistencia(cls, inscripcion_id, fecha, presente=True, observaciones=None):
        """Método para crear un nuevo registro de asistencia"""
        nueva_asistencia = cls(
            inscripcion_id=inscripcion_id,
            fecha=fecha,
            presente=presente,
            observaciones=observaciones
        )
        db.session.add(nueva_asistencia)
        db.session.commit()
        return nueva_asistencia