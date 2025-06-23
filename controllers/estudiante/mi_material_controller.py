from flask import request, Blueprint, send_from_directory
from models.material_model import Material
from models.inscripcion_model import Inscripcion
from views.estudiante.materiales_view import listar_materiales, ver_material
import os

material_bp = Blueprint('estudiante_material', __name__, url_prefix="/estudiante/materiales")

@material_bp.route("/")
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

@material_bp.route("/<int:id>")
def view(id):
    material = Material.get_by_id(id)
    return ver_material(material)

@material_bp.route("/descargar/<nombre_archivo>")
def descargar(nombre_archivo):
    return send_from_directory(nombre_archivo, as_attachment=True)