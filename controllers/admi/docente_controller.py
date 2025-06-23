from flask import request, redirect,url_for,Blueprint,flash
from datetime import datetime
from models.docente_model import Docente
from models.usuario_model import Usuario
from models.rol_model import Rol
from views.admi import docente_view

docente_bp=Blueprint('docente',__name__ ,url_prefix="/admi/docentes")

@docente_bp.route("/")
def index():
    docentes = Docente.get_all()
    rol_docente = Rol.query.filter_by(nombre='Docente').first()
    usuarios = Usuario.query.filter_by(rol_id=rol_docente.id).all() if rol_docente else []
    return docente_view.list(docentes, usuarios)

@docente_bp.route("/vista/<int:id>")
def vista(id):
    docente = Docente.get_by_id(id)
    return docente_view.vista(docente)

@docente_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        
        fecha_str = request.form['fecha_nac']
        
        fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()
        genero = request.form['genero']
        telefono = request.form['telefono']
        ci = request.form['ci']
        especialidad = request.form['especialidad']
        usuario_id = request.form['usuario_id']

        existe = Docente.query.filter_by(usuario_id=usuario_id).first()
        if existe:
            flash("El docente ya está en la lista.", "warning")
            return redirect(url_for('docente.index', show_modal='true'))
                            
        docente = Docente(fecha_nac=fecha, genero=genero, telefono=telefono, ci=ci, especialidad=especialidad, usuario_id=usuario_id)
        docente.save()
        return redirect(url_for('docente.index'))
    
    # Este bloque debe estar fuera del if (para cuando es GET)
    rol_docente = Rol.query.filter_by(nombre='Docente').first()
    usuarios = Usuario.query.filter_by(rol_id=rol_docente.id).all() if rol_docente else []
    return docente_view.create(usuarios)

@docente_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    docente = Docente.get_by_id(id)
    if request.method == 'POST':
        fecha_str = request.form['fecha_nac']
        
        fecha = datetime.strptime(fecha_str,'%Y-%m-%d').date()
        genero = request.form['genero']
        telefono = request.form['telefono']
        ci = request.form['ci']
        especialidad = request.form['especialidad']
        usuario_id = request.form['usuario_id']
        
        # Actualiza el estado del usuario relacionado
        docente.usuario.activo = 'activo' in request.form
        #actualizar
        docente.update(fecha_nac=fecha,genero=genero,telefono=telefono,ci=ci,especialidad=especialidad,usuario_id=usuario_id)
        return redirect(url_for('docente.index'))
    
     # Este bloque debe estar fuera del if (para cuando es GET)
    rol_docente = Rol.query.filter_by(nombre='Docente').first()
    usuarios = Usuario.query.filter_by(rol_id=rol_docente.id).all() if rol_docente else []
    return docente_view.edit(docente,usuarios)

    
@docente_bp.route("/delete/<int:id>")
def delete(id):
    docente = Docente.get_by_id(id)
    if not docente:
        flash("Docente no encontrado", "warning")
        return redirect(url_for('docente.index'))
    
    # Actualizar estado en Usuario asociado
    usuario = docente.usuario  # Asumiendo relación docente.usuario
    if usuario:
        usuario.activo = False  # Marcar usuario como inactivo
     # Opcional, si quieres quitar el rol
    
    # Actualizar estado en Docente
    docente.activo = False  # Marcar docente como inactivo
    
    # Guardar cambios (depende de cómo guardas en tu ORM)
    from database import db  # o tu objeto de sesión
    db.session.commit()
    return redirect(url_for('docente.index'))







