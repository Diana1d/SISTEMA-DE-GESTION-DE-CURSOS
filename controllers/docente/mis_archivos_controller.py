from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user
from views.docente.mis_archivos_view import listar_archivos, formulario_subir_archivo, ver_detalles_archivo
import os

mis_archivos_bp = Blueprint('docente_mis_archivos', __name__, url_prefix="/docente/mis_archivos")

@mis_archivos_bp.route("/")
def index():
    # Usar ID fijo para pruebas (o current_user.id cuando actives el login)
    return listar_archivos(docente_id=1)

@mis_archivos_bp.route("/subir", methods=['GET', 'POST'])
def subir():
    if request.method == 'POST':
        # Lógica para manejar la subida de archivos (similar a material_controller.py)
        flash('Archivo subido correctamente', 'success')
        return redirect(url_for('docente_mis_archivos.index'))
    return formulario_subir_archivo()

@mis_archivos_bp.route("/detalles/<int:archivo_id>/<tipo>")
def detalles(archivo_id, tipo):
    return ver_detalles_archivo(archivo_id, tipo)