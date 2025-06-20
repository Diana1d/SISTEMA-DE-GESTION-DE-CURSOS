from flask import request, redirect,url_for,Blueprint,flash
from models.inscripcion_model import Inscripcion

from models.estudiante_model import Estudiante
from models.paralelo_modal import Paralelo
from views.admi import paralelo_view

paralelo_bp=Blueprint('paralelo',__name__ ,url_prefix="/admi/paralelos")

@paralelo_bp.route("/")
def index():
    #Recupera tosos los registros de usuarios
    paralelos = Paralelo.get_all()
    return paralelo_view.list(paralelos)

@paralelo_bp.route("/vista/<int:id>")
def vista(id):
    paralelo = Paralelo.get_by_id(id)
    return paralelo_view.vista(paralelo)

@paralelo_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        
        paralelo = request.form['paralelo']
        curso_id = request.form['curso_id']
        semestre_id = request.form['semestre_id']
        turno_id = request.form['turno_id']
        
        
        paralelo = Paralelo(paralelo,curso_id,semestre_id,turno_id)
        paralelo.save()
        return redirect(url_for('paralelo.index'))
    return paralelo_view.create()


@paralelo_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    paralelo = Paralelo.get_by_id(id)
    if request.method == 'POST':
        paralelo = request.form['paralelo']
        curso_id = request.form['curso_id']
        semestre_id = request.form['semestre_id']
        turno_id = request.form['turno_id']
        
        
        #actualizar
        paralelo.update(paralelo=paralelo,curso_id=curso_id,semestre_id=semestre_id,turno_id=turno_id)
        return redirect(url_for('paralelo.index'))
    return paralelo_view.edit(paralelo)
    
@paralelo_bp.route("/delete/<int:id>")
def delete(id):
    paralelo = Paralelo.get_by_id(id)
    paralelo.delete()
    return redirect(url_for('paralelo.index'))