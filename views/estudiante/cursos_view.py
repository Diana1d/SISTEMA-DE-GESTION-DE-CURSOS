from flask import render_template

def listar_cursos(cursos):
    """Lista todos los cursos del estudiante"""
    return render_template(
        'estudiante/cursos/index.html',
        cursos=cursos
    )

def ver_curso(curso):
    """Muestra el detalle de un curso"""
    return render_template(
        'estudiante/cursos/vista.html',
        curso=curso
    )