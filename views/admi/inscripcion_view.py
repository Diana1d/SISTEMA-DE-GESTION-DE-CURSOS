from flask import render_template

def list(inscripciones,**kwargs):
    return render_template('admi/inscripciones/index.html',inscripciones=inscripciones,**kwargs)

def create(**kwargs):
    return render_template('admi/docentes/create.html',**kwargs)

def edit(inscripciones,**kwargs):
    return render_template('admi/docentes/edit.html',inscripciones=inscripciones,**kwargs)

def vista(inscripcion):
    return render_template('admi/docentes/vista.html',inscripcion=inscripcion)

