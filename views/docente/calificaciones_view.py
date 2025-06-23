from flask import render_template

def listar_calificaciones(curso, estudiantes_con_calificaciones):
    """Muestra las calificaciones de un curso"""
    return render_template('docente/calificaciones/index.html',
                         curso=curso,
                         estudiantes=estudiantes_con_calificaciones)

def editar_calificacion(estudiante, curso, calificacion):
    """Formulario para editar calificaciones"""
    return render_template('docente/calificaciones/editar.html',
                         estudiante=estudiante,
                         curso=curso,
                         calificacion=calificacion)

# Nueva función para crear evaluaciones
def crear_evaluacion(curso):
    """Muestra formulario para nueva evaluación"""
    return render_template(
        'docente/calificaciones/crear_evaluacion.html',
        curso=curso
    )