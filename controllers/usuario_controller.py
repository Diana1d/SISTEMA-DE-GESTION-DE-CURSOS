from flask import request, redirect,url_for,Blueprint,flash
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario_model import Usuario
from models.rol_model import Rol
from models.curso_model import Curso
from models.docente_model import Docente
from models.estudiante_model import Estudiante
from views import usuario_view
from database import db
from werkzeug.security import check_password_hash


usuario_bp=Blueprint('usuario',__name__ ,url_prefix="/usuarios")

@usuario_bp.route("/")

def index():
    #Recupera tosos los registros de usuarios
    usuarios = Usuario.get_all()
    roles = Rol.get_all() 
    return usuario_view.list(usuarios,roles)

@usuario_bp.route("/vista/<int:id>")

def vista(id):
    usuario = Usuario.get_by_id(id)
    return usuario_view.vista(usuario)

@usuario_bp.route("/create", methods=['GET','POST'])

def create():
    roles = Rol.get_all() 

    if not roles:
        flash("Primero debes crear al menos un rol en el sistema.", "danger")
        return redirect(url_for("rol.index"))  # Redirige a la gestión de roles
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password'] 
        activo = 'activo' in request.form
        rol_id = request.form['rol_id']
        
        existe = Usuario.query.filter_by(nombre=nombre, apellido=apellido).first()
        if existe:
            flash('Ya existe un usuario con ese nombre y apellido.', 'danger')
            return redirect(url_for('usuario.index',show_modal='true'))
        
        # 1) Validación previa
        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            flash('Ya existe un usuario con ese correo.', 'danger')
            return redirect(url_for('usuario.index',show_modal='true'))
        
        usuario = Usuario(nombre,apellido,email,username,password,activo,rol_id)
        usuario.save()
        return redirect(url_for('usuario.index'))
    return usuario_view.create(roles)

@usuario_bp.route("/edit/<int:id>",methods=['GET','POST'])

def edit(id):
    usuario = Usuario.get_by_id(id)
    roles = Rol.get_all()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        activo = 'activo' in request.form
        rol_id = request.form['rol_id']
        
        if usuario.rol and usuario.rol.nombre == 'Estudiante':
            estudiante = Estudiante.query.filter_by(usuario_id=usuario.id).first()
            if estudiante:
                tiene_inscripciones = any(ins.activo for ins in estudiante.inscripciones)
                
                if not activo and tiene_inscripciones:
                    for ins in estudiante.inscripciones:
                        ins.activo = False
                    db.session.commit()
                    flash("Usuario desactivado. Las inscripciones del estudiante también han sido desactivadas.", "warning")
                elif activo and tiene_inscripciones:
                    flash("Usuario activado. Por favor, revisa las inscripciones del estudiante.", "info")

            
        # Si el campo password está vacío, pasamos None para no cambiar
        password_cambio = password if password else None
        #actualizar
        usuario.update(nombre=nombre,apellido=apellido,email=email,username=username,password=password_cambio,activo=activo,rol_id=rol_id)
        return redirect(url_for('usuario.index'))
    return usuario_view.edit(usuario, roles)

    
@usuario_bp.route("/delete/<int:id>")

def delete(id):
    usuario = Usuario.get_by_id(id)
    usuario.delete()
    return redirect(url_for('usuario.index'))

@usuario_bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.get_by_username(username)    
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sección exitosa','success')
    
            # Redirige según el rol
            if user.rol.nombre == "Administrador":
                return redirect(url_for("usuario.dashboard"))
            elif user.rol.nombre == "Docente":
                return redirect(url_for("docente_inicio.dashboard"))
            elif user.rol.nombre == "Estudiante":
                return redirect(url_for("usuario.dashboard_estudiante"))
            else:
                logout_user()
                flash("Rol desconocido.", "danger")             
                return redirect(url_for("usuario.login"))

        else:
            flash('Credenciales inválidas', 'danger')
    return usuario_view.login()

@usuario_bp.route("/logout")

def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("usuario.login"))

@usuario_bp.route("/dashboard")

def dashboard():
    datos = obtener_datos_dashboard()
    return usuario_view.dashboard(current_user,**datos)


def obtener_datos_dashboard():
    cursos = Curso.query.filter_by(activo=True).all()
    labels = [curso.nombre for curso in cursos]
    valores = [sum(1 for ins in curso.inscripciones if ins.activo) for curso in cursos]

    datos = {
        'labels': labels,
        'valores': valores,
        'total_cursos': Curso.contar_activos(),
        'total_docentes': Docente.contar_activos(),
        'total_estudiantes': Estudiante.contar_activos(),
        'docentes_faltantes':Docente.contar_faltantes(),
        'estudiantes_faltantes':Estudiante.contar_faltantes_est()
    }
    return datos