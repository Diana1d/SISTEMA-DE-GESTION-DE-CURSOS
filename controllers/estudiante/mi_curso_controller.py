from flask import Blueprint
from models.inscripcion_model import Inscripcion
from views.estudiante.cursos_view import listar_cursos, ver_curso

curso_bp = Blueprint('estudiante_curso', __name__, url_prefix="/estudiante/cursos")

@curso_bp.route("/")
def index():
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
    return listar_cursos(cursos)

@curso_bp.route("/<int:id>")
def view(id):
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    curso = Inscripcion.get_curso_by_estudiante(estudiante_id, id)
    return ver_curso(curso)