from flask import render_template
from models.curso_model import Curso
from models.material_model import Material
from models.tarea_model import Tarea
from datetime import datetime

def mostrar_dashboard(docente_id):
    # Obtener cursos del docente (sin verificar autenticación)
    cursos = Curso.query.filter_by(docente_id=docente_id).all()
    
    materiales_recientes = (
        Material.query
        .filter_by(docente_id=docente_id)
        .order_by(Material.fecha_subida.desc())
        .limit(5)
        .all()
    )
    
    tareas_pendientes = (
        Tarea.query
        .filter_by(docente_id=docente_id)
        .filter(Tarea.fecha_entrega >= datetime.now())
        .order_by(Tarea.fecha_entrega.asc())
        .all()
    )
    
    return render_template(
        'docente/inicio/dashboard.html',
        cursos=cursos,
        materiales_recientes=materiales_recientes,
        tareas_pendientes=tareas_pendientes
    )