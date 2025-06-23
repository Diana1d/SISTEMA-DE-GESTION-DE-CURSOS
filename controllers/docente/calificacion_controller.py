from flask import request, redirect, url_for, Blueprint, flash
from models.calificacion_model import Calificacion
from models.estudiante_model import Estudiante
from models.evaluacion_model import Evaluacion
from views.docente.calificaciones_view import listar_calificaciones, editar_calificacion

calificacion_bp = Blueprint('docente_calificacion', __name__, url_prefix="/docente/calificaciones")

@calificacion_bp.route("/")
def index():
    evaluacion_id = request.args.get('evaluacion_id')
    evaluacion = Evaluacion.get_by_id(evaluacion_id) if evaluacion_id else None
    curso = evaluacion.curso if evaluacion else None
    
    calificaciones = Calificacion.get_by_evaluacion(evaluacion_id) if evaluacion_id else Calificacion.get_all()
    
    # Organizar calificaciones por estudiante
    estudiantes_calif = {}
    for cal in calificaciones:
        if cal.estudiante_id not in estudiantes_calif:
            estudiantes_calif[cal.estudiante_id] = Estudiante.get_by_id(cal.estudiante_id)
            estudiantes_calif[cal.estudiante_id].calificaciones = []
        estudiantes_calif[cal.estudiante_id].calificaciones.append(cal)
    
    return listar_calificaciones(
        curso=curso,
        estudiantes_con_calificaciones=list(estudiantes_calif.values())
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