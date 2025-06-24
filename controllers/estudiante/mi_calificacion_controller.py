from flask import request, Blueprint
from models.calificacion_model import Calificacion
from models.inscripcion_model import Inscripcion
from views.estudiante.calificaciones_view import listar_calificaciones, ver_calificacion

calificacion_bp = Blueprint('estudiante_calificacion', __name__, url_prefix="/estudiante/calificaciones")

@calificacion_bp.route("/")
def index():
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    curso_id = request.args.get('curso_id')
    
    # Obtener calificaciones según filtro
    if curso_id:
        calificaciones = Calificacion.get_by_estudiante_and_curso(estudiante_id, curso_id)
    else:
        calificaciones = Calificacion.get_by_estudiante(estudiante_id)
    
    # Obtener cursos del estudiante
    cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
    
    # Calcular promedios por curso
    promedios = {}
    for curso in cursos:
        promedio = Calificacion.calcular_promedio_curso(curso.id, estudiante_id)
        promedios[curso] = promedio
    
    return listar_calificaciones(
        calificaciones=calificaciones,
        cursos=cursos,
        curso_seleccionado=curso_id,
        promedios=promedios  # Añadir los promedios al contexto
    )

@calificacion_bp.route("/<int:id>")
def view(id):
    calificacion = Calificacion.get_by_id(id)
    if not calificacion:
        abort(404)  # Importar abort desde flask si no está importado
    return ver_calificacion(calificacion)