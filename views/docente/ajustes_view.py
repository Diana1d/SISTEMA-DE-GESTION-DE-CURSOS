from flask import render_template

def mostrar_ajustes(notificaciones):
    return render_template('docente/ajustes/index.html', notificaciones=notificaciones)