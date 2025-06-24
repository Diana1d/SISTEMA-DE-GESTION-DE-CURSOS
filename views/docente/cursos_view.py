from flask import render_template

def listar_cursos(cursos):
    """Lista todos los cursos asignados al docente"""
    return render_template('docente/cursos/index.html', cursos=cursos)

def ver_curso(curso, estudiantes_inscritos):
    """Muestra los detalles de un curso específico"""
    return render_template('docente/cursos/vista.html', curso=curso, estudiantes=estudiantes_inscritos)

def crear_tarea_form(curso):
    """Muestra el formulario para crear una nueva tarea"""
    return render_template('docente/cursos/crear_tarea.html', curso=curso)

def ver_tareas_curso(curso, tareas):
    """Muestra todas las tareas de un curso"""
    return render_template('docente/cursos/tareas.html', 
                         curso=curso, 
                         tareas=tareas)