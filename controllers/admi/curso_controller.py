from flask import request, redirect,url_for,Blueprint,flash
from models.curso_model import Curso
from models.usuario_model import Usuario
from models.docente_model import Docente
from views.admi import curso_view


curso_bp=Blueprint('curso',__name__ ,url_prefix="/admi/cursos")

@curso_bp.route("/")
def index():
    cursos = Curso.get_all()
    docentes = Docente.query.join(Usuario).filter(Usuario.activo == True).filter(Docente.usuario != None).all()
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
        sigla = request.form['sigla']
        carga_horaria = request.form['carga_horaria']
        activo ='activo' in request.form
        docente_id =  request.form['docente_id']
        
        existe = Curso.query.filter(
            (Curso.nombre == nombre) | (Curso.sigla == sigla)
        ).first()
        
        if existe:
            flash("Ya existe un curso con ese nombre o sigla.", "warning")
            return redirect(url_for('curso.index', show_modal='true'))
        
        curso = Curso(nombre=nombre,descripcion=descripcion,sigla=sigla,carga_horaria=carga_horaria,activo=activo,docente_id=docente_id)
        curso.save()
        return redirect(url_for('curso.index'))
    
    docentes = Docente.query.join(Usuario).filter(Usuario.activo == True).filter(Docente.usuario != None).all()

    return curso_view.create(docentes)

@curso_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    curso = Curso.get_by_id(id)
    if request.method == 'POST':
        
        nombre =request.form['nombre']
        descripcion =request.form['descripcion']
        sigla = request.form['sigla']
        carga_horaria = request.form['carga_horaria']
        activo ='activo' in request.form
        docente_id =  request.form['docente_id']
        #actualizar
        curso.update(nombre=nombre,descripcion=descripcion,sigla=sigla,carga_horaria=carga_horaria,activo=activo,docente_id=docente_id)
        return redirect(url_for('curso.index'))
    
    docentes = Docente.query.join(Usuario).filter(Usuario.activo == True).filter(Docente.usuario != None).all()

    return curso_view.edit(curso,docentes)

    
@curso_bp.route("/delete/<int:id>")
def delete(id):
    curso = Curso.get_by_id(id)
    curso.delete()
    return redirect(url_for('curso.index'))

 






