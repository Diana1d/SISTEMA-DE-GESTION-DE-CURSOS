from flask import request, redirect, url_for, Blueprint, flash
from models.calificacion_model import Calificacion
from models.estudiante_model import Estudiante
from models.evaluacion_model import Evaluacion
from models.inscripcion_model import Inscripcion
from views.docente.calificaciones_view import listar_calificaciones, editar_calificacion

calificacion_bp = Blueprint('docente_calificacion', __name__, url_prefix="/docente/calificaciones")

@calificacion_bp.route("/")
def index():
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    curso_id = request.args.get('curso_id')
    
    if curso_id:
        calificaciones = Calificacion.get_by_estudiante_and_curso(estudiante_id, curso_id)
    else:
        calificaciones = Calificacion.get_by_estudiante(estudiante_id)
    
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
        promedios=promedios
    )
    
@calificacion_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    calificacion = Calificacion.get_by_id(id)
    if request.method == 'POST':
        nota = request.form['nota']
        calificacion.update(nota=nota)
        flash('Calificación actualizada correctamente', 'success')
        return redirect(url_for('docente_calificacion.index'))
    
    estudiantes = Estudiante.get_all()
    evaluaciones = Evaluacion.get_all()
    return editar_calificacion(calificacion, estudiantes, evaluaciones)