from flask import render_template

def listar_tareas(tareas, cursos, curso_seleccionado=None, estado='pendientes'):
    """Lista todas las tareas del estudiante"""
    return render_template(
        'estudiante/tareas/index.html',
        tareas=tareas,
        cursos=cursos,
        curso_seleccionado=curso_seleccionado,
        estado=estado
    )

def ver_tarea(tarea, entrega=None):
    """Muestra el detalle de una tarea"""
    return render_template(
        'estudiante/tareas/detalle.html',
        tarea=tarea,
        entrega=entrega
    )

def entregar_tarea_form(tarea):
    """Muestra el formulario para entregar una tarea"""
    return render_template(
        'estudiante/tareas/entregar.html',
        tarea=tarea
    )