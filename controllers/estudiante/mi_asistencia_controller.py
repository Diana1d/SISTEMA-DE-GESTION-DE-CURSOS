from flask import request, redirect, url_for, Blueprint, flash
from models.asistencia_model import Asistencia
from models.inscripcion_model import Inscripcion
from views.estudiante.asistencias_view import listar_asistencias, ver_asistencia

asistencia_bp = Blueprint('estudiante_asistencia', __name__, url_prefix="/estudiante/asistencias")

@asistencia_bp.route("/")
def index():
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    curso_id = request.args.get('curso_id')
    
    if curso_id:
        asistencias = Asistencia.get_by_estudiante_and_curso(estudiante_id, curso_id)
    else:
        asistencias = Asistencia.get_by_estudiante(estudiante_id)
    
    cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
    
    return listar_asistencias(asistencias=asistencias, cursos=cursos, curso_seleccionado=curso_id)

@asistencia_bp.route("/<int:id>")
def view(id):
    asistencia = Asistencia.get_by_id(id)
    return ver_asistencia(asistencia)