from flask import request, redirect,url_for,Blueprint,flash
from models.semestre_modal import Semestre 
from models.inscripcion_model import Inscripcion
from views.admi import  semestre_view

semestre_bp=Blueprint('semestre',__name__ ,url_prefix="/admi/semestres")

@semestre_bp.route("/")
def index():
    #Recupera tosos los registros de usuarios
    semestres = Semestre.get_all()
    return semestre_view.list(semestres)

@semestre_bp.route("/vista/<int:id>")
def vista(id):
    semestre = Semestre.get_by_id(id)
    return semestre_view.vista(semestre)

@semestre_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        
        gestion = request.form['gestion']
        semestre_num = request.form['semestre_num']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_inicio']
    
        
        
        semestre = Semestre(gestion,semestre_num,fecha_inicio,fecha_fin)
        semestre.save()
        return redirect(url_for('semestre.index'))
    return semestre_view.create()


@semestre_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    semestre = Semestre.get_by_id(id)
    if request.method == 'POST':
        
        gestion = request.form['gestion']
        semestre_num = request.form['semestre_num']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_inicio']
        
        #actualizar
        semestre.update(gestion=gestion,semestre_num=semestre_num,fecha_inicio=fecha_inicio,fecha_fin=fecha_fin)
        return redirect(url_for('semestre.index'))
    return semestre_view.edit(semestre)
    
@semestre_bp.route("/delete/<int:id>")
def delete(id):
    semestre = Semestre.get_by_id(id)
    semestre.delete()
    return redirect(url_for('semestre.index'))