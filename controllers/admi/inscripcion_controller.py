from flask import request, redirect,url_for,Blueprint,flash
from models.inscripcion_model import Inscripcion

from models.estudiante_model import Estudiante
from models.paralelo_modal import Paralelo
from views.admi import inscripcion_view

inscripcion_bp=Blueprint('inscripcion',__name__ ,url_prefix="/admi/inscripciones")

@inscripcion_bp.route("/")
def index():
    #Recupera tosos los registros de usuarios
    inscripciones = Inscripcion.get_all()
    return inscripcion_view.list(inscripciones)

@inscripcion_bp.route("/vista/<int:id>")
def vista(id):
    inscripcion = Inscripcion.get_by_id(id)
    return inscripcion_view.vista(inscripcion)

@inscripcion_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        
        paralelo_id = request.form['paralelo_id']
        estudiante_id = request.form['estudiante_id']
        
        
        inscripcion = Inscripcion(paralelo_id,estudiante_id)
        inscripcion.save()
        return redirect(url_for('inscripcion.index'))
    return inscripcion_view.create()


@inscripcion_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    inscripcion = Inscripcion.get_by_id(id)
    if request.method == 'POST':
        paralelo_id = request.form['paralelo_id']
        estudiante_id = request.form['estudiante_id']
        
        #actualizar
        inscripcion.update(paralelo_id=paralelo_id,estudiante_id=estudiante_id)
        return redirect(url_for('inscripcion.index'))
    return inscripcion_view.edit(inscripcion)

    
@inscripcion_bp.route("/delete/<int:id>")
def delete(id):
    inscripcion = Inscripcion.get_by_id(id)
    inscripcion.delete()
    return redirect(url_for('inscripcion.index'))