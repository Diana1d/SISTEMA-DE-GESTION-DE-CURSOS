from flask import request, redirect, url_for, Blueprint, flash
from models.asistencia_model import Asistencia
from models.estudiante_model import Estudiante
from models.inscripcion_model import Inscripcion
from models.curso_model import Curso
from views.docente.asistencias_view import listar_asistencias, registrar_asistencia

asistencia_bp = Blueprint('docente_asistencia', __name__, url_prefix="/docente/asistencias")

@asistencia_bp.route("/")
def index():
    curso_id = request.args.get('curso_id')
    fecha = request.args.get('fecha')
    
    curso = Curso.get_by_id(curso_id) if curso_id else None
    asistencias = Asistencia.get_by_curso_and_date(curso_id, fecha) if curso_id and fecha else Asistencia.get_all()
    
    # Obtener estudiantes y sus asistencias
    estudiantes = []
    if curso_id:
        estudiantes = Estudiante.query.join(Inscripcion).filter(Inscripcion.curso_id == curso_id).all()
    
    # Calcular estadísticas
    total_clases = len({a.fecha for a in asistencias}) if asistencias else 0
    # ... otros cálculos
    
    return listar_asistencias(
        curso=curso,
        asistencias=asistencias,
        estudiantes=estudiantes,
        fechas=sorted({a.fecha for a in asistencias}, reverse=True) if asistencias else [],
        total_clases=total_clases,
        promedio_asistencia=75,  # Ejemplo, calcular esto
        estudiantes_riesgo=0      # Ejemplo, calcular esto
    )

@asistencia_bp.route("/registrar", methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        curso_id = request.form['curso_id']
        fecha = request.form['fecha']
        presente = 'presente' in request.form
        
        Asistencia.register(estudiante_id, curso_id, fecha, presente)
        flash('Asistencia registrada correctamente', 'success')
        return redirect(url_for('docente_asistencia.index'))
    
    estudiantes = Estudiante.get_all()
    cursos = Curso.get_all()
    return registrar_asistencia(estudiantes, cursos)