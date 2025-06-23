from flask import render_template

def listar_materiales(materiales, cursos, curso_seleccionado=None):
    """Lista todos los materiales disponibles para el estudiante"""
    return render_template(
        'estudiante/materiales/index.html',
        materiales=materiales,
        cursos=cursos,
        curso_seleccionado=curso_seleccionado
    )

def ver_material(material):
    """Muestra el detalle de un material"""
    return render_template(
        'estudiante/materiales/descargar.html',
        material=material
    )