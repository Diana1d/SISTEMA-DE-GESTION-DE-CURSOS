from flask import render_template

def listar_asistencias(asistencias, cursos, curso_seleccionado=None):
    """Lista todas las asistencias del estudiante"""
    return render_template(
        'estudiante/asistencias/index.html',
        asistencias=asistencias,
        cursos=cursos,
        curso_seleccionado=curso_seleccionado
    )

def ver_asistencia(asistencia):
    """Muestra el detalle de una asistencia"""
    return render_template(
        'estudiante/asistencias/detalle.html',
        asistencia=asistencia
    )