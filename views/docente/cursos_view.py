from flask import render_template

def listar_cursos(cursos):
    """Lista todos los cursos asignados al docente"""
    return render_template('docente/cursos/index.html', cursos=cursos)

def ver_curso(curso, estudiantes_inscritos):
    """Muestra los detalles de un curso específico"""
    return render_template('docente/cursos/vista.html', curso=curso, estudiantes=estudiantes_inscritos)