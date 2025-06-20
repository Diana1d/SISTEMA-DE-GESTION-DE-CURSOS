from flask import request, redirect,url_for,Blueprint,flash
from models.turno_modal import Turno
from models.inscripcion_model import Inscripcion
from views.admi import  turno_view

turno_bp=Blueprint('turno',__name__ ,url_prefix="/admi/turnos")

@turno_bp.route("/")
def index():
    #Recupera tosos los registros de usuarios
    turnos = Turno.get_all()
    return turno_view.list(turnos)

@turno_bp.route("/vista/<int:id>")
def vista(id):
    turno = Turno.get_by_id(id)
    return turno_view.vista(turno)

@turno_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        
        tipo_turno = request.form['tipo_turno']        
        
        turno = Turno(tipo_turno)
        turno.save()
        return redirect(url_for('turno.index'))
    return turno_view.create()


@turno_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    turno = Turno.get_by_id(id)
    if request.method == 'POST':
        
        tipo_turno = request.form['tipo_turno'] 
        
        #actualizar
        turno.update(tipo_turno=tipo_turno)
        return redirect(url_for('turno.index'))
    return turno_view.edit(turno)
    
@turno_bp.route("/delete/<int:id>")
def delete(id):
    turno = Turno.get_by_id(id)
    turno.delete()
    return redirect(url_for('turno.index'))