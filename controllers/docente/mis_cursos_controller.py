from flask import request, redirect, url_for, Blueprint, flash, render_template
from models.curso_model import Curso
from models.usuario_model import Usuario
from models.docente_model import Docente
from models.inscripcion_model import Inscripcion
from views.docente.cursos_view import listar_cursos, ver_curso

curso_docente_bp = Blueprint('curso_docente', __name__, url_prefix="/docente/cursos")

@curso_docente_bp.route("/")
def index():
    # Versión temporal sin login - usar ID fijo
    docente_id = 1  # ID de prueba - cambiar luego por current_user.id
    cursos = Curso.query.filter_by(docente_id=docente_id).all()
    
    return render_template('docente/cursos/index.html', cursos=cursos)

@curso_docente_bp.route("/vista/<int:id>")
def vista(id):
    curso = Curso.get_by_id(id)
    estudiantes = Inscripcion.get_estudiantes_by_curso(id)
    return ver_curso(curso=curso, estudiantes_inscritos=estudiantes)