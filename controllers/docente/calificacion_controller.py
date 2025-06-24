from flask import request, redirect, url_for, Blueprint, flash
from models.calificacion_model import Calificacion
from models.estudiante_model import Estudiante
from models.evaluacion_model import Evaluacion
from models.inscripcion_model import Inscripcion
from datetime import datetime
from database import db
from views.docente.calificaciones_view import listar_calificaciones, editar_calificacion

calificacion_bp = Blueprint('docente_calificacion', __name__, url_prefix="/docente/calificaciones")

@calificacion_bp.route("/")
def index():
    estudiante_id = 1  # Reemplazar con el ID del estudiante autenticado
    curso_id = request.args.get('curso_id')
    
    # Obtener todos los cursos del estudiante
    cursos = Inscripcion.get_cursos_by_estudiante(estudiante_id)
    
    # Determinar el curso seleccionado
    curso_seleccionado = None
    if curso_id:
        curso_seleccionado = next((c for c in cursos if str(c.id) == curso_id), None)
    elif cursos:
        curso_seleccionado = cursos[0]
        curso_id = str(curso_seleccionado.id)
    
    # Obtener calificaciones según el filtro
    if curso_id:
        calificaciones = Calificacion.get_by_estudiante_and_curso(estudiante_id, curso_id)
    else:
        calificaciones = Calificacion.get_by_estudiante(estudiante_id)
    
    # Calcular promedios por curso
    promedios = {}
    for curso in cursos:
        promedio = Calificacion.calcular_promedio_curso(curso.id, estudiante_id)
        promedios[curso.id] = promedio
    
    return listar_calificaciones(
        calificaciones=calificaciones,
        cursos=cursos,
        curso_seleccionado=curso_seleccionado,
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

@calificacion_bp.route('/crear_evaluacion/<int:curso_id>', methods=['POST'])
def crear_evaluacion(curso_id):
    if request.method == 'POST':
        try:
            # Convertir porcentaje a float
            porcentaje = float(request.form['porcentaje'])
            
            # Convertir fecha de string a objeto date
            fecha_str = request.form['fecha']
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            nueva_evaluacion = Evaluacion(
                nombre=request.form['nombre'],
                porcentaje=porcentaje,
                fecha=fecha,
                descripcion=request.form.get('descripcion', ''),
                curso_id=curso_id
            )
            
            db.session.add(nueva_evaluacion)
            db.session.commit()
            
            flash('Evaluación creada exitosamente', 'success')
            return redirect(url_for('calificacion.index', curso_id=curso_id))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Error en los datos: {str(e)}', 'danger')
            return redirect(url_for('calificacion.index', curso_id=curso_id))