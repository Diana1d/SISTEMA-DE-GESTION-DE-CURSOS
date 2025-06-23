from flask import render_template

def listar_estudiantes(estudiantes, curso=None):
    """Lista todos los estudiantes del docente"""
    return render_template(
        'docente/estudiantes/index.html', 
        estudiantes=estudiantes,
        curso=curso  # Pasar el curso a la plantilla
    )

def ver_estudiante(estudiante, cursos_inscritos):
    """Muestra el perfil de un estudiante con sus cursos"""
    return render_template(
        'docente/estudiantes/vista.html', 
        estudiante=estudiante, 
        cursos=cursos_inscritos
    )