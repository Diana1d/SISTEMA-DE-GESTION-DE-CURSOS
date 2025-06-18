from flask import request, redirect,url_for,Blueprint,flash
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario_model import Usuario
from views.admi import usuario_view
from werkzeug.security import check_password_hash


usuario_bp=Blueprint('usuario',__name__ ,url_prefix="/admi/usuarios")

@usuario_bp.route("/")
def index():
    #Recupera tosos los registros de usuarios
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/vista/<int:id>")
def vista(id):
    usuario = Usuario.get_by_id(id)
    return usuario_view.vista(usuario)

@usuario_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password'] 
        activo = 'activo' in request.form
        rol_id = request.form['rol_id']
        
        # 1) Validación previa
        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            flash('Ya existe un usuario con ese correo.', 'danger')
            return redirect(url_for('usuario.index'))
        
        usuario = Usuario(nombre,apellido,email,username,password,activo,rol_id)
        usuario.save()
        return redirect(url_for('usuario.index'))
    return usuario_view.create()

@usuario_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    usuario = Usuario.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        activo = 'activo' in request.form
        rol_id = request.form['rol_id']
        #actualizar
        usuario.update(nombre=nombre,apellido=apellido,email=email,username=username,password=password,activo=activo,rol_id=rol_id)
        return redirect(url_for('usuario.index'))
    return usuario_view.edit(usuario)

    
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
        print("Usuario encontrado:", user)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sección exitosa','success')
            # Redirige según el rol
            if user.rol.nombre == "Administrador":
                return redirect(url_for("usuario.dashboard"))
            elif user.rol.nombre == "Docente":
                return redirect(url_for("usuario.dashboard_docente"))
            elif user.rol.nombre == "Estudiante":
                return redirect(url_for("usuario.dashboard_estudiante"))
            else:
                flash("Rol no reconocido", "warning")
                return redirect(url_for("usuario.login"))

        else:
            flash('Credenciales inválidas', 'danger')

    return usuario_view.login()

@usuario_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("usuario.login"))

@usuario_bp.route("/dashboard")
@login_required
def dashboard():
    return usuario_view.dashboard(current_user)


