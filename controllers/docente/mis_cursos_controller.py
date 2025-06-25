from flask import request, redirect, url_for, Blueprint, flash, render_template, abort, current_app, send_from_directory
from models.curso_model import Curso
from models.usuario_model import Usuario
from models.docente_model import Docente
from models.inscripcion_model import Inscripcion
from models.tarea_model import Tarea
from models.entrega_tarea_model import EntregaTarea
from datetime import datetime
import os
from views.docente.cursos_view import listar_cursos, ver_curso, crear_tarea_form, ver_tareas_curso

curso_docente_bp = Blueprint('curso_docente', __name__, url_prefix="/docente/cursos")

@curso_docente_bp.route("/")
def index():
    docente_id = 1  # Cambiar por current_user.id cuando tengas login
    cursos = Curso.query.filter_by(docente_id=docente_id).all()
    
    # Agregar conteo de estudiantes a cada curso
    for curso in cursos:
        curso.num_estudiantes = Inscripcion.query.filter_by(
            curso_id=curso.id, 
            activo=True
        ).count()
    
    return listar_cursos(cursos=cursos)

@curso_docente_bp.route("/vista/<int:id>")
def vista(id):
    curso = Curso.get_by_id(id)
    estudiantes = Inscripcion.get_estudiantes_by_curso(id)
    return ver_curso(curso=curso, estudiantes_inscritos=estudiantes)

@curso_docente_bp.route("/<int:curso_id>")
def ver_curso(curso_id):
    curso = Curso.get_by_id(curso_id)
    if not curso:
        abort(404)
    estudiantes = Inscripcion.get_estudiantes_by_curso(curso_id)
    tareas = Tarea.get_by_curso(curso_id)
    return render_template('docente/cursos/vista.html', 
                         curso=curso, 
                         estudiantes=estudiantes,
                         tareas=tareas)

@curso_docente_bp.route("/<int:curso_id>/tareas/nueva", methods=['GET', 'POST'])
def crear_tarea(curso_id):
    curso = Curso.get_by_id(curso_id)
    if not curso:
        abort(404)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            fecha_entrega = datetime.strptime(request.form['fecha_entrega'], '%Y-%m-%dT%H:%M')
            archivo_adjunto = request.files.get('archivo_adjunto')
            
            # Guardar archivo si existe
            archivo_path = None
            if archivo_adjunto and archivo_adjunto.filename != '':
                # Aquí deberías implementar la lógica para guardar el archivo
                # Por ejemplo: archivo_path = guardar_archivo(archivo_adjunto)
                pass
            
            # Crear nueva tarea
            nueva_tarea = Tarea(
                titulo=titulo,
                descripcion=descripcion,
                fecha_entrega=fecha_entrega,
                curso_id=curso_id,
                docente_id=1,  # Cambiar por current_user.id cuando tengas login
                archivo_adjunto=archivo_path
            )
            nueva_tarea.save()
            
            flash('Tarea creada exitosamente', 'success')
            return redirect(url_for('curso_docente.ver_tareas', curso_id=curso_id))
        
        except Exception as e:
            flash(f'Error al crear la tarea: {str(e)}', 'danger')
    
    return crear_tarea_form(curso=curso)

@curso_docente_bp.route("/<int:curso_id>/tareas")
def ver_tareas(curso_id):
    curso = Curso.get_by_id(curso_id)
    if not curso:
        abort(404)
    
    tareas = Tarea.get_by_curso(curso_id)
    return ver_tareas_curso(curso=curso, tareas=tareas)

# Añade estas nuevas rutas al controlador existente

@curso_docente_bp.route("/<int:curso_id>/tareas/<int:tarea_id>/editar", methods=['GET', 'POST'])
def editar_tarea(curso_id, tarea_id):
    curso = Curso.get_by_id(curso_id)
    tarea = Tarea.get_by_id(tarea_id)
    
    if not curso or not tarea or tarea.curso_id != curso_id:
        abort(404)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            tarea.titulo = request.form['titulo']
            tarea.descripcion = request.form['descripcion']
            tarea.fecha_entrega = datetime.strptime(request.form['fecha_entrega'], '%Y-%m-%dT%H:%M')
            tarea.estado = request.form['estado']
            
            # Manejar archivo adjunto si se sube uno nuevo
            archivo_adjunto = request.files.get('archivo_adjunto')
            if archivo_adjunto and archivo_adjunto.filename != '':
                # Aquí deberías implementar la lógica para actualizar el archivo
                # Por ejemplo: tarea.archivo_adjunto = guardar_archivo(archivo_adjunto)
                pass
            
            tarea.update()
            
            flash('Tarea actualizada exitosamente', 'success')
            return redirect(url_for('curso_docente.ver_tareas', curso_id=curso_id))
        
        except Exception as e:
            flash(f'Error al actualizar la tarea: {str(e)}', 'danger')
    
    return render_template('docente/cursos/editar_tarea.html', 
                         curso=curso, 
                         tarea=tarea)

@curso_docente_bp.route("/<int:curso_id>/tareas/<int:tarea_id>/entregas")
def ver_entregas_tarea(curso_id, tarea_id):
    curso = Curso.get_by_id(curso_id)
    tarea = Tarea.get_by_id(tarea_id)
    
    if not curso or not tarea or tarea.curso_id != curso_id:
        abort(404)
    
    # Obtener todas las entregas para esta tarea
    entregas = tarea.entregas
    
    # Obtener estudiantes inscritos en el curso
    estudiantes_inscritos = Inscripcion.get_estudiantes_by_curso(curso_id)
    
    return render_template('docente/cursos/entregas_tarea.html', 
                         curso=curso, 
                         tarea=tarea,
                         entregas=entregas,
                         estudiantes_inscritos=estudiantes_inscritos)

@curso_docente_bp.route("/<int:curso_id>/tareas/<int:tarea_id>/entregas/<int:entrega_id>/calificar", methods=['POST'])
def calificar_entrega(curso_id, tarea_id, entrega_id):
    if request.method == 'POST':
        try:
            entrega = EntregaTarea.get_by_id(entrega_id)
            if not entrega or entrega.tarea_id != tarea_id:
                abort(404)
            
            calificacion = float(request.form['calificacion'])
            comentarios = request.form.get('comentarios', '')
            
            entrega.update(calificacion=calificacion, comentarios_docente=comentarios)
            
            flash('Calificación guardada exitosamente', 'success')
            return redirect(url_for('curso_docente.ver_entregas_tarea', 
                                 curso_id=curso_id, 
                                 tarea_id=tarea_id))
        
        except ValueError:
            flash('La calificación debe ser un número válido', 'danger')
        except Exception as e:
            flash(f'Error al calificar: {str(e)}', 'danger')
    
    return redirect(url_for('curso_docente.ver_entregas_tarea', 
                         curso_id=curso_id, 
                         tarea_id=tarea_id))
    
# Añade esta ruta al final del archivo
@curso_docente_bp.route("/descargar/<path:nombre_archivo>")
def descargar_archivo(nombre_archivo):
    # Asegúrate de que esta ruta coincida con donde guardas los archivos
    directorio_uploads = os.path.join(current_app.root_path, 'static/uploads')
    
    # Verifica que el archivo exista
    if not os.path.exists(os.path.join(directorio_uploads, nombre_archivo)):
        abort(404)
    
    return send_from_directory(directorio_uploads, nombre_archivo, as_attachment=True)

@curso_docente_bp.route("/<int:curso_id>/tareas/<int:tarea_id>/eliminar", methods=['POST'])
def eliminar_tarea(curso_id, tarea_id):
    try:
        tarea = Tarea.get_by_id(tarea_id)
        
        if not tarea or tarea.curso_id != curso_id:
            abort(404)
        
        # Eliminar archivos adjuntos si existen
        if tarea.archivo_adjunto:
            try:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], tarea.archivo_adjunto))
            except OSError:
                pass  # Si el archivo no existe, continuamos igual
        
        # Eliminar la tarea y sus entregas asociadas
        EntregaTarea.query.filter_by(tarea_id=tarea_id).delete()
        tarea.delete()
        
        flash('Tarea eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar la tarea: {str(e)}', 'danger')
    
    return redirect(url_for('curso_docente.ver_tareas', curso_id=curso_id))