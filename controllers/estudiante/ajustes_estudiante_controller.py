from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.notificacion_model import Notificacion

ajustes_bp = Blueprint('estudiante_ajustes', __name__, url_prefix="/estudiante/ajustes")

@ajustes_bp.route("/")
@login_required
def configuracion():
    # Verificar rol de estudiante
    if not current_user.rol.nombre == 'Estudiante':
        flash('No tienes permiso para acceder a esta sección', 'danger')
        return redirect(url_for('usuario.login'))
    
    notificaciones = Notificacion.get_by_usuario(current_user.id)
    return render_template('estudiante/ajustes/index.html', notificaciones=notificaciones)

@ajustes_bp.route("/notificaciones", methods=['POST'])
@login_required
def gestionar_notificaciones():
    # Verificar rol de estudiante
    if not current_user.rol.nombre == 'Estudiante':
        flash('No tienes permiso para esta acción', 'danger')
        return redirect(url_for('usuario.login'))
    
    accion = request.form.get('accion')
    notificacion_id = request.form.get('notificacion_id')
    
    if notificacion_id:
        notificacion = Notificacion.query.get(notificacion_id)
        if notificacion and notificacion.usuario_id == current_user.id:
            if accion == 'marcar_leido':
                notificacion.marcar_como_leido()
                flash('Notificación marcada como leída', 'success')
            elif accion == 'eliminar':
                notificacion.delete()
                flash('Notificación eliminada', 'success')
    
    return redirect(url_for('estudiante_ajustes.configuracion'))