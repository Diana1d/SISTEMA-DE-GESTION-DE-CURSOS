from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.estudiante_model import Estudiante
from werkzeug.security import generate_password_hash

perfil_bp = Blueprint('estudiante_perfil', __name__, url_prefix="/estudiante/perfil")

@perfil_bp.route("/")
@login_required
def ver_perfil():
    # Verificar si el usuario tiene rol de estudiante
    if not current_user.rol.nombre == 'Estudiante':
        flash('No tienes permiso para acceder a esta sección', 'danger')
        return redirect(url_for('usuario.login'))
    
    # Obtener el perfil del estudiante
    estudiante = Estudiante.get_by_usuario_id(current_user.id)
    if not estudiante:
        flash('No se encontró tu perfil de estudiante', 'error')
        return redirect(url_for('estudiante.inicio'))
    
    return render_template('estudiante/perfil/ver.html', estudiante=estudiante)

@perfil_bp.route("/editar", methods=['GET', 'POST'])
@login_required
def editar_perfil():
    estudiante = Estudiante.get_by_usuario_id(current_user.id)
    usuario = current_user
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        usuario.nombre = request.form.get('nombre')
        usuario.apellido = request.form.get('apellido')
        usuario.email = request.form.get('email')
        
        # Actualizar datos del estudiante
        estudiante.telefono = request.form.get('telefono')
        estudiante.matricula = request.form.get('matricula')
        estudiante.ci = request.form.get('ci')
        
        try:
            usuario.save()
            estudiante.save()
            flash('Perfil actualizado correctamente', 'success')
            return redirect(url_for('estudiante_perfil.ver_perfil'))
        except Exception as e:
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')
    
    return render_template('estudiante/perfil/editar.html', estudiante=estudiante, usuario=usuario)

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
            return redirect(url_for('estudiante_perfil.ver_perfil'))
    
    return render_template('estudiante/perfil/cambiar_password.html')