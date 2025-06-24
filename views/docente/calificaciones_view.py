from flask import render_template
from models.evaluacion_model import Evaluacion
from models.estudiante_model import Estudiante

def listar_calificaciones(calificaciones, cursos, curso_seleccionado, promedios):
    """Muestra las calificaciones de un curso"""
    # Obtener evaluaciones del curso seleccionado
    evaluaciones = []
    if curso_seleccionado:
        evaluaciones = Evaluacion.query.filter_by(curso_id=curso_seleccionado.id).all()
    
    # Organizar datos de estudiantes
    estudiantes_data = []
    if calificaciones:
        estudiantes_ids = {c.estudiante_id for c in calificaciones}
        estudiantes = Estudiante.query.filter(Estudiante.id.in_(estudiantes_ids)).all()
        
        for estudiante in estudiantes:
            estudiante_info = {
                'id': estudiante.id,
                'nombre_completo': estudiante.nombre_completo,
                'foto': estudiante.foto or 'default-user.png',
                'notas': {},
                'promedio': promedios.get(curso_seleccionado.id, 0.0) if curso_seleccionado else 0.0
            }
            
            for calificacion in calificaciones:
                if calificacion.estudiante_id == estudiante.id:
                    estudiante_info['notas'][calificacion.evaluacion_id] = calificacion.nota
            
            estudiantes_data.append(estudiante_info)
    
    return render_template(
        'docente/calificaciones/index.html',
        curso=curso_seleccionado,  # Pasamos como 'curso' para la plantilla
        cursos=cursos,
        evaluaciones=evaluaciones,
        estudiantes=estudiantes_data,
        promedios=promedios
    )

def editar_calificacion(calificacion, estudiantes, evaluaciones):
    """Formulario para editar calificaciones"""
    return render_template('docente/calificaciones/editar.html',
                         calificacion=calificacion,
                         estudiante=calificacion.estudiante,
                         evaluacion=calificacion.evaluacion,
                         nota=calificacion.nota,
                         observaciones=calificacion.comentarios)

def crear_evaluacion(curso):
    """Muestra formulario para nueva evaluación"""
    return render_template(
        'docente/calificaciones/crear_evaluacion.html',
        curso=curso
    )