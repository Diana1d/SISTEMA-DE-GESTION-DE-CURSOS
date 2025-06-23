from flask import render_template, request
from flask_login import login_required, current_user
from models import Asistencia, Inscripcion, db
from datetime import datetime

@login_required
def ver_asistencias():
    try:
        # Obtener parámetros de filtrado
        curso_id = request.args.get('curso_id', type=int)
        mes = request.args.get('mes', type=int)
        año = request.args.get('año', type=int, default=datetime.now().year)
        
        # Obtener el estudiante actual
        estudiante = current_user.estudiante
        
        # Consulta base
        query = db.session.query(Asistencia)\
            .join(Inscripcion, Asistencia.inscripcion_id == Inscripcion.id)\
            .filter(Inscripcion.estudiante_id == estudiante.id)
        
        # Aplicar filtros
        if curso_id:
            query = query.filter(Inscripcion.curso_id == curso_id)
        
        query = query.filter(db.extract('year', Asistencia.fecha) == año)
        
        if mes:
            query = query.filter(db.extract('month', Asistencia.fecha) == mes)
        
        # Obtener resultados
        asistencias = query.order_by(Asistencia.fecha.desc()).all()
        cursos = list({inscripcion.curso for inscripcion in estudiante.inscripciones})
        
        # Calcular estadísticas
        total_clases = len({(a.fecha, a.inscripcion.curso_id) for a in asistencias})
        total_presentes = sum(1 for a in asistencias if a.presente)
        porcentaje = (total_presentes / total_clases * 100) if total_clases > 0 else 0
        
        return render_template('estudiantes/estu_asistencia.html',
            total_presentes=total_presentes,
            
            total_ausentes=total_clases - total_presentes,
            total_clases=total_clases,
            asistencias=asistencias,
            cursos_inscritos=cursos,
            curso_id=curso_id,
            mes=mes,
            año=año,
            porcentaje_asistencia=round(porcentaje, 2),
            estudiante=estudiante
        )
    
    except Exception as e:
        # Manejo de errores mejorado
        print(f"Error al obtener asistencias: {str(e)}")
        return render_template('estudiantes/estu_asistencia.html',
            error="Ocurrió un error al cargar las asistencias",
            total_presentes=0,
            total_ausentes=0,
            total_clases=0,
            asistencias=[],
            cursos_inscritos=[],
            porcentaje_asistencia=0
        )