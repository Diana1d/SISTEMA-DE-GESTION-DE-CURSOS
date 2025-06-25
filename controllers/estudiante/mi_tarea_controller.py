from flask import request, redirect, url_for, Blueprint, flash, current_app
from werkzeug.utils import secure_filename
import os
from models.tarea_model import Tarea
from models.entrega_tarea_model import EntregaTarea
from models.inscripcion_model import Inscripcion
from views.estudiante.tareas_view import listar_tareas, ver_tarea, entregar_tarea_form
from datetime import datetime

tarea_bp = Blueprint('estudiante_tarea', __name__, url_prefix="/estudiante/tareas")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'zip', 'pptx', 'jpg', 'png'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # Verificar si se envió el archivo
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        archivo = request.files['archivo']
        
        # Si el usuario no selecciona un archivo
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        # Verificar que el archivo sea permitido
        if archivo and allowed_file(archivo.filename):
            # Asegurar el nombre del archivo
            filename = secure_filename(archivo.filename)
            
            # Crear la carpeta uploads si no existe
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Guardar el archivo
            filepath = os.path.join(upload_folder, filename)
            archivo.save(filepath)
            
            # Crear la entrega en la base de datos
            entrega = EntregaTarea(
                tarea_id=id,
                estudiante_id=1,  # ID de estudiante
                archivo_entregado=filename
            )
            entrega.save()
            
            flash('Tarea entregada correctamente', 'success')
            return redirect(url_for('estudiante_tarea.view', id=id))
        else:
            flash('Tipo de archivo no permitido', 'error')
    
    return entregar_tarea_form(tarea)