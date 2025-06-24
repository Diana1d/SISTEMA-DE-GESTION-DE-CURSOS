from flask import Blueprint, abort, render_template
from flask_login import login_required, current_user
from models.inscripcion_model import Inscripcion
from models.calificacion_model import Calificacion
from models.asistencia_model import Asistencia
from models.material_model import Material
from models.curso_model import Curso
from models.tarea_model import Tarea
from views.estudiante.cursos_view import listar_cursos, ver_curso
from flask_login import login_required, current_user

curso_bp = Blueprint('estudiante_curso', __name__, url_prefix="/estudiante/cursos")

@curso_bp.route("/")
def index():
    estudiante_id=current_user.id   # Reemplazar con el ID del estudiante autenticado
    cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
    return listar_cursos(cursos)

@curso_bp.route("/<int:id>")
def view(id):
    curso = Curso.get_by_id(id)
    if not curso:
        abort(404)
     # Obtener materiales del curso
    materiales = Material.query.filter_by(curso_id=curso.id).order_by(Material.fecha_subida.desc()).all()
    # Calcular estadísticas
    promedio_curso = Calificacion.calcular_promedio_curso(curso.id)
    porcentaje_asistencia = Asistencia.calcular_porcentaje_asistencia(curso.id, current_user.id)
    tareas_pendientes = Tarea.get_pendientes(curso.id, current_user.id)
    
    return render_template('estudiante/cursos/vista.html',
                         curso=curso,
                         materiales=materiales,
                         promedio_curso=promedio_curso,
                         porcentaje_asistencia=porcentaje_asistencia,
                         tareas_pendientes=tareas_pendientes)
