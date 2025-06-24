from flask import Blueprint, request, flash, redirect, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from models.usuario_model import Usuario
from views import reset_password_view
from database import db, mail
from flask import current_app



recuperar_bp = Blueprint('recuperar', __name__,url_prefix='/recuperar')

# Generador de token
def generar_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='recuperar-clave')

# Verificador de token
def verificar_token(token, expiracion=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        return s.loads(token, salt='recuperar-clave', max_age=expiracion)
    except:
        return None

@recuperar_bp.route('/', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form['email']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            token = generar_token(email)
            enlace = url_for('recuperar.nueva_contrasena', token=token, _external=True)
            msg = Message('Recuperar tu contraseña', recipients=[email])
            msg.body = f'Hola, haz clic aquí para cambiar tu contraseña:\n{enlace}'
            mail.send(msg)
            flash('Te enviamos un correo con instrucciones', 'info')
        else:
            flash('Correo no encontrado', 'danger')
    return  reset_password_view.recuperar()

@recuperar_bp.route('/nueva-contrasena/<token>', methods=['GET', 'POST'])
def nueva_contrasena(token):
    email = verificar_token(token)
    if not email:
        flash('El enlace es inválido o ha expirado', 'danger')
        return redirect(url_for('recuperar.recuperar'))

    if request.method == 'POST':
        nueva = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            usuario.set_password(nueva)  # asegura que este método use hash
            db.session.commit()
            flash('Contraseña actualizada, ahora inicia sesión.', 'success')
            return redirect(url_for('usuario.login'))
        else:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('recuperar.recuperar'))

    return reset_password_view.nueva_contrasena()
