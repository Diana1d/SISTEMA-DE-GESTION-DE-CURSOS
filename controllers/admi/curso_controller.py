from flask import request, redirect,url_for,Blueprint,flash
from models.curso_model import Curso
from models.usuario_model import Usuario
from models.rol_model import Rol
from views.admi import curso_view


curso_bp=Blueprint('curso',__name__ ,url_prefix="/admi/cursos")

@curso_bp.route("/")
def index():
    cursos = Curso.get_all()
    docentes = Usuario.query.join(Rol).filter(Rol.nombre == "Docente", Usuario.activo == True).all()
    return curso_view.list(cursos, docentes)

@curso_bp.route("/vista/<int:id>")
def vista(id):
    curso = Curso.get_by_id(id)
    return curso_view.vista(curso)

@curso_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
     
        nombre =request.form['nombre']
        descripcion =request.form['descripcion']
        activo =request.form['activo']
        profesor_id =  request.form['profesor_id']
        
        curso = Curso(nombre=nombre,descripcion=descripcion,activo=activo,profesor_id=profesor_id)
        curso.save()
        return redirect(url_for('curso.index'))
    
    docentes = Usuario.query.join(Rol).filter(Rol.nombre == "Docente", Usuario.activo == True).all()
    return curso_view.create(docentes)

@curso_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    curso = Curso.get_by_id(id)
    if request.method == 'POST':
        nombre =request.form['nombre']
        descripcion =request.form['descripcion']
        activo =request.form['activo']
        profesor_id =  request.form['profesor_id']
        #actualizar
        curso.update(nombre=nombre,descripcion=descripcion,activo=activo,profesor_id=profesor_id)
        return redirect(url_for('curso.index'))
    
    docentes = Usuario.query.join(Rol).filter(Rol.nombre == "Docente", Usuario.activo == True).all()
    return curso_view.edit(curso,docentes)

    
@curso_bp.route("/delete/<int:id>")
def delete(id):
    curso = Curso.get_by_id(id)
    curso.delete()
    return redirect(url_for('curso.index'))







