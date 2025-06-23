from flask import render_template, make_response
#import pdfkit

def generar_reporte_curso(curso, datos_estadisticos):
    """Genera reporte completo del curso"""
    html = render_template(
        'docente/reportes/reporte_curso.html',
        curso=curso,
        datos=datos_estadisticos
    )
    # Opción para PDF
    #pdf = pdfkit.from_string(html, False)
    #response = make_response(pdf)
    #response.headers['Content-Type'] = 'application/pdf'
    #return response