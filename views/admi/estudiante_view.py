from flask import render_template

def list(estudiantes,usuarios):
    return render_template('admi/estudiantes/index.html',estudiantes=estudiantes,usuarios=usuarios)

def create(usuarios):
    return render_template('admi/estudiantes/create.html',usuarios=usuarios)

def edit(estudiante):
    return render_template('admi/estudiantes/edit.html',estudiante= estudiante)

def vista(estudiante):
    return render_template('admi/estudiantes/vista.html',estudiante=estudiante)