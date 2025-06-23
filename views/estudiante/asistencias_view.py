from flask import render_template, request, session
from datetime import datetime
from models import Asistencia, Inscripcion, Curso, db

def ver_mis_asistencias():
    """Muestra las asistencias del estudiante logueado con filtros"""
    estudiante_id = session.get('estudiante_id')
    
    # Obtener parámetros de filtrado
    curso_id = request.args.get('curso_id', type=int)
    mes = request.args.get('mes', type=int)
    
    # Consulta base de asistencias
    query = db.session.query(Asistencia).join(Inscripcion).filter(
        Inscripcion.estudiante_id == estudiante_id
    ).order_by(Asistencia.fecha.desc())
    
    # Aplicar filtros
    if curso_id:
        query = query.join(Inscripcion.curso).filter(Curso.id == curso_id)
    if mes:
        query = query.filter(db.extract('month', Asistencia.fecha) == mes)
    
    asistencias = query.all()
    
    # Cálculo de estadísticas
    total_clases = len(asistencias)
    total_presentes = sum(1 for a in asistencias if a.presente)
    porcentaje = (total_presentes / total_clases * 100) if total_clases > 0 else 0
    
    # Cursos inscritos para filtro
    cursos_inscritos = Inscripcion.query.filter_by(estudiante_id=estudiante_id).join(Curso).all()
    
    # Meses para filtro
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    return render_template('estudiante/asistencias/index.html',
                         asistencias=asistencias,
                         cursos_inscritos=cursos_inscritos,
                         meses=meses,
                         total_clases=total_clases,
                         total_presentes=total_presentes,
                         porcentaje_asistencia=round(porcentaje, 2),
                         curso_filtro=curso_id,
                         mes_filtro=mes)

def generar_reporte_personal():
    """Genera reporte PDF/HTML de asistencias personales"""
    estudiante_id = session.get('estudiante_id')
    
    # Obtener datos consolidados
    asistencias = db.session.query(Asistencia).join(Inscripcion).filter(
        Inscripcion.estudiante_id == estudiante_id
    ).all()
    
    # Cálculos para el reporte
    total_clases = len(asistencias)
    total_presentes = sum(1 for a in asistencias if a.presente)
    porcentaje = (total_presentes / total_clases * 100) if total_clases > 0 else 0
    
    # Agrupar por curso
    cursos = {}
    for asist in asistencias:
        curso_nombre = asist.inscripcion.curso.nombre
        if curso_nombre not in cursos:
            cursos[curso_nombre] = {'presentes': 0, 'totales': 0}
        cursos[curso_nombre]['totales'] += 1
        if asist.presente:
            cursos[curso_nombre]['presentes'] += 1
    
    return render_template('estudiante/asistencias/reporte.html',
                         asistencias=asistencias,
                         total_clases=total_clases,
                         total_presentes=total_presentes,
                         porcentaje_asistencia=round(porcentaje, 2),
                         cursos=cursos,
                         fecha_reporte=datetime.now().strftime('%d/%m/%Y'))