from flask import render_template

def list(cursos,docentes):
    return render_template('admi/cursos/index.html',cursos=cursos,docentes= docentes)

def create(docentes):
    return render_template('admi/cursos/create.html',docentes= docentes)

def edit(curso,docentes):
    return render_template('admi/cursos/edit.html',curso=curso,docentes= docentes)

def vista(curso):
    return render_template('admi/cursos/vista.html',curso=curso)



