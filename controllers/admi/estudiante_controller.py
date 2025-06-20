from flask import request, redirect,url_for,Blueprint,flash
from datetime import datetime
from models.estudiante_model import Estudiante
from models.usuario_model import Usuario
from models.rol_model import Rol
from views.admi import estudiante_view

estudiante_bp=Blueprint('estudiante',__name__ ,url_prefix="/admi/estudiantes")

@estudiante_bp.route("/")
def index():
    #Recupera tosos los registros de usuarios
    estudiantes = Estudiante.get_all()
    rol_estudiante = Rol.query.filter_by(nombre='Estudiante').first()
    usuarios = Usuario.query.filter_by(rol_id=rol_estudiante.id).all() if rol_estudiante else []
    return estudiante_view.list(estudiantes, usuarios)

@estudiante_bp.route("/vista/<int:id>")
def vista(id):
    estudiante = Estudiante.get_by_id(id)
    return estudiante_view.vista(estudiante)

@estudiante_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        
        matricula = request.form['matricula']
        fecha_str = request.form['fecha_nac']
        
        fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()
        genero = request.form['genero']
        telefono = request.form['telefono']
        ci = request.form['ci']
        usuario_id = request.form['usuario_id']
        
        
        estudiante = Estudiante(matricula=matricula,fecha_nac=fecha,genero=genero,telefono=telefono,ci=ci,usuario_id=usuario_id)
        estudiante.save()
        return redirect(url_for('estudiante.index'))
    # Este bloque debe estar fuera del if (para cuando es GET)
    rol_estudiante = Rol.query.filter_by(nombre='Estudiante').first()
    usuarios = Usuario.query.filter_by(rol_id=rol_estudiante.id).all() if rol_estudiante else []
    return estudiante_view.create(usuarios)


@estudiante_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    estudiante = Estudiante.get_by_id(id)
    if request.method == 'POST':
        
        matricula = request.form['matricula']
        fecha_str = request.form['fecha_nac']
        
        fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()
        genero = request.form['genero']
        telefono = request.form['telefono']
        ci = request.form['ci']
        usuario_id = request.form['usuario_id']
        #actualizar
        estudiante.update(matricula=matricula,fecha_nac=fecha,genero=genero,telefono=telefono,ci=ci,usuario_id=usuario_id)
        return redirect(url_for('estudiante.index'))
    
    rol_estudiante = Rol.query.filter_by(nombre='Estudiante').first()
    usuarios = Usuario.query.filter_by(rol_id=rol_estudiante.id).all() if rol_estudiante else []
    return estudiante_view.edit(estudiante,usuarios)

    
@estudiante_bp.route("/delete/<int:id>")
def delete(id):
    estudiante = Estudiante.get_by_id(id)
    estudiante.delete()
    return redirect(url_for('estudiante.index'))