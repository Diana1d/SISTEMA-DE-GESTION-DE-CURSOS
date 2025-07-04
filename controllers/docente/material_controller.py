from flask import Blueprint, request, redirect, url_for, flash, current_app, render_template
from flask_login import current_user, login_required
from models.material_model import Material
from models.curso_model import Curso
from views.docente.material_view import listar_materiales, subir_material_form, handle_upload
import os

# Asegúrate que el nombre del blueprint y el prefijo sean consistentes
material_bp = Blueprint('docente_material', __name__, url_prefix="/docente/materiales")

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'jpg', 'jpeg', 'png', 'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@material_bp.route("/<int:curso_id>")
def index(curso_id):
    curso = Curso.get_by_id(curso_id)
    if not curso:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('docente_curso.index'))
    
    materiales = Material.get_by_curso(curso_id)
    return listar_materiales(curso=curso, materiales=materiales)  # Asegúrate de pasar ambos parámetros

@material_bp.route("/subir/<int:curso_id>", methods=['GET', 'POST'])
def subir(curso_id):
    curso = Curso.get_by_id(curso_id)
    if not curso:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('docente_curso.index'))
    
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        file = request.files['archivo']
        
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            file_info = handle_upload(file)
            
            if file_info:
                material = Material(
                    titulo=request.form.get('titulo'),
                    descripcion=request.form.get('descripcion'),
                    nombre_archivo=file_info['nombre_archivo'],
                    tipo_archivo=file_info['tipo_archivo'],
                    tamanio=file_info['tamanio'],
                    curso_id=curso_id,
                    docente_id=current_user.id
                )
                material.save()
                
                flash('Material subido correctamente', 'success')
                return redirect(url_for('docente_material.index', curso_id=curso_id))
        
        flash('Tipo de archivo no permitido', 'error')
    
    return subir_material_form(curso)

@material_bp.route("/editar/<int:material_id>", methods=['GET', 'POST'])
def editar(material_id):
    material = Material.get_by_id(material_id)
    if not material:
        flash('Material no encontrado', 'error')
        return redirect(url_for('docente_curso.index'))
    
    if material.docente_id != current_user.id:
        flash('No tienes permiso para editar este material', 'error')
        return redirect(url_for('docente_material.index', curso_id=material.curso_id))
    
    curso = Curso.get_by_id(material.curso_id)
    
    if request.method == 'POST':
        # Procesar la edición
        material.titulo = request.form.get('titulo')
        material.descripcion = request.form.get('descripcion')
        
        # Manejar archivo si se subió uno nuevo
        if 'archivo' in request.files:
            file = request.files['archivo']
            if file.filename != '' and allowed_file(file.filename):
                # Eliminar el archivo antiguo
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], material.nombre_archivo))
                except:
                    pass
                
                # Guardar el nuevo archivo
                file_info = handle_upload(file)
                if file_info:
                    material.nombre_archivo = file_info['nombre_archivo']
                    material.tipo_archivo = file_info['tipo_archivo']
                    material.tamanio = file_info['tamanio']
        
        material.save()
        flash('Material actualizado correctamente', 'success')
        return redirect(url_for('docente_material.index', curso_id=material.curso_id))
    
    return render_template('docente/materiales/editar.html', curso=curso, material=material)

@material_bp.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    material = Material.get_by_id(id)
    if not material:
        flash('Material no encontrado', 'error')
        return redirect(url_for('docente_curso.index'))
    
    if material.docente_id != current_user.id:
        flash('No tienes permiso para eliminar este material', 'error')
        return redirect(url_for('docente_material.index', curso_id=material.curso_id))
    
    material.delete()
    flash('Material eliminado correctamente', 'success')
    return redirect(url_for('docente_material.index', curso_id=material.curso_id))