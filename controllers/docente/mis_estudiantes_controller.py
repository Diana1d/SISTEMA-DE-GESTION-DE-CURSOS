from flask import request, redirect, url_for, Blueprint, flash
from models.estudiante_model import Estudiante
from models.inscripcion_model import Inscripcion
from models.curso_model import Curso
from views.docente.estudiantes_view import listar_estudiantes, ver_estudiante

estudiante_bp = Blueprint('docente_estudiante', __name__, url_prefix="/docente/estudiantes")

@estudiante_bp.route("/")
def index():
    curso_id = request.args.get('curso_id')
    if curso_id:
        estudiantes = Inscripcion.get_estudiantes_by_curso(curso_id)
        curso = Curso.get_by_id(curso_id)  # Obtener el curso por su ID
    else:
        estudiantes = Estudiante.get_all()
        curso = None  # Si no hay curso_id, establecer como None
    
    return listar_estudiantes(estudiantes, curso)  # Pasar el curso a la vista

@estudiante_bp.route("/vista/<int:id>")
def vista(id):
    estudiante = Estudiante.get_by_id(id)
    cursos_inscritos = Inscripcion.get_cursos_by_estudiante(id)  # Necesitarás implementar este método
    return ver_estudiante(estudiante, cursos_inscritos)