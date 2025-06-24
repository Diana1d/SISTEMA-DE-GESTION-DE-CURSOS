from flask import request, Blueprint, send_from_directory, current_app, abort
from models.material_model import Material
from models.inscripcion_model import Inscripcion
from views.estudiante.materiales_view import listar_materiales, ver_material
import os

mi_material_bp = Blueprint('estudiante_material', __name__, url_prefix="/estudiante/materiales")

# Configuración de la ruta de uploads (ajusta según tu estructura)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')

@mi_material_bp.route("/")
def index():
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    curso_id = request.args.get('curso_id')
    
    if curso_id:
        materiales = Material.get_by_curso(curso_id)
    else:
        cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
        materiales = []
        for curso in cursos:
            materiales.extend(Material.get_by_curso(curso.id))
    
    cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
    
    return listar_materiales(materiales=materiales, cursos=cursos, curso_seleccionado=curso_id)

@mi_material_bp.route("/<int:id>")
def view(id):
    material = Material.get_by_id(id)
    return ver_material(material)

@mi_material_bp.route("/descargar/<nombre_archivo>")
def descargar(nombre_archivo):
    try:
        # Verificación de seguridad básica
        if '..' in nombre_archivo or nombre_archivo.startswith('/'):
            abort(400, description="Nombre de archivo inválido")
        
        # Construye la ruta completa al archivo
        file_path = os.path.join(UPLOAD_FOLDER, nombre_archivo)
        
        # Verifica si el archivo existe
        if not os.path.exists(file_path):
            abort(404, description="Archivo no encontrado")
        
        # Descarga el archivo
        return send_from_directory(
            directory=UPLOAD_FOLDER,
            path=nombre_archivo,
            as_attachment=True
        )
    except Exception as e:
        current_app.logger.error(f"Error al descargar archivo: {str(e)}")
        abort(500, description="Error al procesar la descarga")