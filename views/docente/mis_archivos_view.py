from flask import render_template
from models.material_model import Material
from models.tarea_model import Tarea

def listar_archivos(docente_id):
    """Lista todos los archivos del docente (materiales y tareas)"""
    materiales = Material.query.filter_by(docente_id=docente_id).all()
    tareas = Tarea.query.filter_by(docente_id=docente_id).all()
    return render_template(
        'docente/mis_archivos/index.html',
        materiales=materiales,
        tareas=tareas
    )

def formulario_subir_archivo():
    """Muestra el formulario para subir un nuevo archivo"""
    return render_template('docente/mis_archivos/subir_archivo.html')

def ver_detalles_archivo(archivo_id, tipo):
    """Muestra detalles de un archivo específico"""
    if tipo == 'material':
        archivo = Material.query.get_or_404(archivo_id)
    elif tipo == 'tarea':
        archivo = Tarea.query.get_or_404(archivo_id)
    return render_template('docente/mis_archivos/detalles.html', archivo=archivo, tipo=tipo)