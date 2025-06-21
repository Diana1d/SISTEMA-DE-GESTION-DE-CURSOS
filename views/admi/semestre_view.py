from flask import render_template

def list(semestres):
    return render_template('admi/semestres/index.html',semestres=semestres)

def create():
    return render_template('admi/semestres/create.html')

def edit(semestre):
    return render_template('admi/semestres/edit.html',semestre=semestre)


