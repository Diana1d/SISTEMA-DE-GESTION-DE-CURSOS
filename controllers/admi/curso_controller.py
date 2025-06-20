from flask import request, redirect,url_for,Blueprint,flash
from models.curso_model import Curso
from models.usuario_model import Usuario
from models.docente_model import Docente
from views.admi import curso_view


curso_bp=Blueprint('curso',__name__ ,url_prefix="/admi/cursos")

@curso_bp.route("/")
def index():
    cursos = Curso.get_all()
    docentes = get_docentes()
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
        activo ='activo' in request.form
        docente_id =  request.form['docente_id']
        
        curso = Curso(nombre=nombre,descripcion=descripcion,activo=activo,docente_id=docente_id)
        curso.save()
        return redirect(url_for('curso.index'))
    
    docentes = get_docentes()
    return curso_view.create(docentes)

@curso_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    curso = Curso.get_by_id(id)
    if request.method == 'POST':
        nombre =request.form['nombre']
        descripcion =request.form['descripcion']
        activo ='activo' in request.form
        docente_id =  request.form['docente_id']
        #actualizar
        curso.update(nombre=nombre,descripcion=descripcion,activo=activo,docente_id=docente_id)
        return redirect(url_for('curso.index'))
    
    docentes = get_docentes()
    return curso_view.edit(curso,docentes)

    
@curso_bp.route("/delete/<int:id>")
def delete(id):
    curso = Curso.get_by_id(id)
    curso.delete()
    return redirect(url_for('curso.index'))

# Este método obtiene todos los usuarios activos con rol de Docente.
def get_docentes():
    return Docente.query.join(Docente.usuario).filter(Usuario.activo == True).all()






