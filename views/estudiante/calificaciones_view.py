from flask import render_template

def listar_calificaciones(calificaciones, cursos, curso_seleccionado=None):
    """Lista todas las calificaciones del estudiante"""
    return render_template(
        'estudiante/calificaciones/index.html',
        calificaciones=calificaciones,
        cursos=cursos,
        curso_seleccionado=curso_seleccionado
    )

def ver_calificacion(calificacion):
    """Muestra el detalle de una calificación"""
    return render_template(
        'estudiante/calificaciones/detalle.html',
        calificacion=calificacion
    )