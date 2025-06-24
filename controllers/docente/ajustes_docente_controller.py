from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.notificacion_model import Notificacion

ajustes_bp = Blueprint('docente_ajustes', __name__, url_prefix="/docente/ajustes")

@ajustes_bp.route("/")
@login_required
def configuracion():
    notificaciones = Notificacion.get_by_usuario(current_user.id)
    return render_template('docente/ajustes/index.html', notificaciones=notificaciones)

@ajustes_bp.route("/notificaciones", methods=['POST'])
@login_required
def gestionar_notificaciones():
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
    
    return redirect(url_for('docente_ajustes.configuracion'))