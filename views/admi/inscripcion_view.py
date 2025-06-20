from flask import render_template

def list(inscripciones):
    return render_template('admi/inscripciones/index.html',inscripciones=inscripciones)

def create(usuarios):
    return render_template('admi/docentes/create.html',usuarios=usuarios)

def edit(docente,usuarios):
    return render_template('admi/docentes/edit.html',docente= docente,usuarios=usuarios)

def vista(docente):
    return render_template('admi/docentes/vista.html',docente=docente)