from flask import render_template
from models.curso_model import Curso
from models.tarea_model import Tarea
from models.calificacion_model import Calificacion
from models.asistencia_model import Asistencia
from models.inscripcion_model import Inscripcion
from datetime import datetime

def mostrar_dashboard(estudiante_id):
    # Obtener cursos del estudiante
    cursos = Curso.query.join(Inscripcion).filter(Inscripcion.estudiante_id == estudiante_id).all()
    
    # Tareas pendientes
    tareas_pendientes = (
        Tarea.query
        .join(Curso)
        .join(Inscripcion)
        .filter(Inscripcion.estudiante_id == estudiante_id)
        .filter(Tarea.fecha_entrega >= datetime.now())
        .order_by(Tarea.fecha_entrega.asc())
        .limit(5)
        .all()
    )
    
    # Últimas calificaciones
    ultimas_calificaciones = (
        Calificacion.query
        .filter_by(estudiante_id=estudiante_id)
        .order_by(Calificacion.fecha_registro.desc())
        .limit(5)
        .all()
    )
    
    # Últimas asistencias
    ultimas_asistencias = (
        Asistencia.query
        .filter_by(estudiante_id=estudiante_id)
        .order_by(Asistencia.fecha.desc())
        .limit(5)
        .all()
    )
    
    return render_template(
        'estudiante/inicio/dashboard.html',
        cursos=cursos,
        tareas_pendientes=tareas_pendientes,
        calificaciones=ultimas_calificaciones,
        asistencias=ultimas_asistencias
    )