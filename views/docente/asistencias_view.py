from flask import render_template

def listar_asistencias(curso, asistencias, estudiantes, fechas, total_clases, promedio_asistencia, estudiantes_riesgo):
    """Muestra el registro de asistencias de un curso"""
    return render_template('docente/asistencias/index.html',
                         curso=curso,
                         asistencias=asistencias,
                         estudiantes=estudiantes,
                         fechas=fechas,
                         total_clases=total_clases,
                         promedio_asistencia=promedio_asistencia,
                         estudiantes_riesgo=estudiantes_riesgo)


def registrar_asistencia(curso, estudiantes):
    """Formulario para registrar asistencias"""
    return render_template('docente/asistencias/registrar.html',
                         curso=curso,
                         estudiantes=estudiantes)

# Nueva función para reportes
def generar_reporte_asistencias(curso, reporte_data, nombres_estudiantes, porcentajes):
    """Genera reporte PDF/HTML de asistencias"""
    return render_template(
        'docente/asistencias/reporte.html',
        curso=curso,
        reporte=reporte_data,
        nombres_estudiantes=nombres_estudiantes,
        porcentajes=porcentajes
    )