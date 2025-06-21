from flask import request, redirect,url_for,Blueprint,flash
from models.inscripcion_model import Inscripcion
from models.estudiante_model import Estudiante
from models.curso_model import Curso
from models.paralelo_modal import Paralelo
from models.turno_modal import Turno
from models.semestre_modal import Semestre
from views.admi import inscripcion_view

inscripcion_bp=Blueprint('inscripcion',__name__ ,url_prefix="/admi/inscripciones")

@inscripcion_bp.route("/")
def index():
    #Recupera tosos los registros de usuarios
    inscripciones = Inscripcion.get_all()
    data = cargar_datos()
    return inscripcion_view.list(inscripciones,**data)

@inscripcion_bp.route("/vista/<int:id>")
def vista(id):
    inscripcion = Inscripcion.get_by_id(id)
    return inscripcion_view.vista(inscripcion)

@inscripcion_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        
        curso_id = request.form['curso_id']
        estudiante_id = request.form['estudiante_id']
        semestre_id = request.form['semestre_id']
        paralelo_id = request.form['paralelo_id']
        turno_id = request.form['turno_id']
        
        inscripcion = Inscripcion(curso_id,estudiante_id,semestre_id,paralelo_id,turno_id)
        inscripcion.save()
        return redirect(url_for('inscripcion.index'))
    data = cargar_datos()
    return inscripcion_view.create(**data)


@inscripcion_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    inscripcion = Inscripcion.get_by_id(id)
    if request.method == 'POST':
        curso_id = request.form['curso_id']
        estudiante_id = request.form['estudiante_id']
        semestre_id = request.form['semestre_id']
        paralelo_id = request.form['paralelo_id']
        turno_id = request.form['turno_id']
        
        #actualizar
        inscripcion.update(curso_id=curso_id,estudiante_id=estudiante_id,semestre_id=semestre_id,paralelo_id=paralelo_id,turno_id=turno_id)
        return redirect(url_for('inscripcion.index'))
    data = cargar_datos()
    return inscripcion_view.edit(inscripcion,**data)

    
@inscripcion_bp.route("/delete/<int:id>")
def delete(id):
    inscripcion = Inscripcion.get_by_id(id)
    inscripcion.delete()
    return redirect(url_for('inscripcion.index'))

def cargar_datos():
    return {
        "estudiantes": Estudiante.get_all(),
        "cursos": Curso.get_all(),
        "paralelos": Paralelo.get_all(),
        "turnos": Turno.get_all(),
        "semestres": Semestre.get_all()
    }