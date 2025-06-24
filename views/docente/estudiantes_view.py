from flask import render_template

def listar_estudiantes(estudiantes, curso=None):
    """Lista todos los estudiantes del docente"""
    return render_template(
        'docente/estudiantes/index.html', 
        estudiantes=estudiantes,
        curso=curso
    )

def ver_estudiante(estudiante, cursos, notas, **kwargs):
    """Muestra el perfil de un estudiante con sus cursos y notas"""
    return render_template(
        'docente/estudiantes/vista.html', 
        estudiante=estudiante,
        cursos=cursos,
        notas=notas,
        **kwargs
    )