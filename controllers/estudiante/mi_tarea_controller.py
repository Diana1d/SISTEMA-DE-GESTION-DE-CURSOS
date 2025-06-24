from flask import request, redirect, url_for, Blueprint, flash
from models.tarea_model import Tarea
from models.entrega_tarea_model import EntregaTarea
from models.inscripcion_model import Inscripcion
from views.estudiante.tareas_view import listar_tareas, ver_tarea, entregar_tarea_form
from datetime import datetime

tarea_bp = Blueprint('estudiante_tarea', __name__, url_prefix="/estudiante/tareas")

@tarea_bp.route("/")
def index():
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    curso_id = request.args.get('curso_id')
    estado = request.args.get('estado', 'pendientes')  # pendientes | completadas
    
    if curso_id:
        tareas = Tarea.get_by_curso(curso_id)
    else:
        cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
        tareas = []
        for curso in cursos:
            tareas.extend(Tarea.get_by_curso(curso.id))
    
    # Filtrar por estado
    if estado == 'pendientes':
        tareas = [t for t in tareas if not EntregaTarea.get_by_estudiante_and_tarea(estudiante_id, t.id)]
    elif estado == 'completadas':
        tareas = [t for t in tareas if EntregaTarea.get_by_estudiante_and_tarea(estudiante_id, t.id)]
    
    cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
    
    return listar_tareas(tareas=tareas, cursos=cursos, curso_seleccionado=curso_id, estado=estado)

@tarea_bp.route("/<int:id>")
def view(id):
    tarea = Tarea.get_by_id(id)
    entrega = EntregaTarea.get_by_estudiante_and_tarea(1, id)  # ID de estudiante
    return ver_tarea(tarea, entrega, datetime.utcnow())  # Pasar la fecha actual

@tarea_bp.route("/<int:id>/entregar", methods=['GET', 'POST'])
def entregar(id):
    tarea = Tarea.get_by_id(id)
    
    if request.method == 'POST':
        archivo = request.files['archivo']
        if archivo:
            filename = (archivo.filename)
            archivo.save(filename)
            
            entrega = EntregaTarea(
                tarea_id=id,
                estudiante_id=1,  # ID de estudiante
                archivo_entregado=filename
            )
            entrega.save()
            flash('Tarea entregada correctamente', 'success')
            return redirect(url_for('estudiante_tarea.view', id=id))
    
    return entregar_tarea_form(tarea)