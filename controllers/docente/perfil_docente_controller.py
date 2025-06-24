from flask import Blueprint, render_template, request ,redirect, url_for, flash
from flask_login import login_required, current_user
from models.docente_model import Docente
from werkzeug.security import generate_password_hash

perfil_bp = Blueprint('docente_perfil', __name__, url_prefix="/docente/perfil")

@perfil_bp.route("/")
@login_required
def ver_perfil():
    # Verificar si el usuario tiene rol de docente
    if not current_user.rol.nombre == 'Docente':
        flash('No tienes permiso para acceder a esta sección', 'danger')
        return redirect(url_for('usuario.login'))
    
    # Obtener el perfil del docente
    docente = current_user.obtener_perfil_docente()
    # Verificar si se encontró/creó el perfil
    if docente is None:
        flash('No se pudo cargar tu perfil de docente', 'error')
        return redirect(url_for('docente.inicio'))
    
    return render_template('docente/perfil/ver.html', docente=docente)

@perfil_bp.route("/editar", methods=['GET', 'POST'])
@login_required
def editar_perfil():
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    usuario = current_user
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        usuario.nombre = request.form.get('nombre')
        usuario.apellido = request.form.get('apellido')
        usuario.email = request.form.get('email')
        
        # Actualizar datos del docente
        docente.telefono = request.form.get('telefono')
        docente.especialidad = request.form.get('especialidad')
        
        try:
            usuario.save()
            docente.save()
            flash('Perfil actualizado correctamente', 'success')
            return redirect(url_for('docente_perfil.ver_perfil'))
        except Exception as e:
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')
    
    return render_template('docente/perfil/editar.html', docente=docente, usuario=usuario)

@perfil_bp.route("/cambiar-password", methods=['GET', 'POST'])
@login_required
def cambiar_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('La contraseña actual es incorrecta', 'danger')
        elif new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden', 'danger')
        else:
            current_user.set_password(new_password)
            current_user.save()
            flash('Contraseña cambiada exitosamente', 'success')
            return redirect(url_for('docente_perfil.ver_perfil'))
    
    return render_template('docente/perfil/cambiar_password.html')