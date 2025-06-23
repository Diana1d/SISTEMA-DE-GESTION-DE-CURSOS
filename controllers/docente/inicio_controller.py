from flask import Blueprint
from views.docente.inicio_view import mostrar_dashboard

inicio_bp = Blueprint('docente_inicio', __name__, url_prefix="/docente/inicio")

@inicio_bp.route("/")
def dashboard():
    # Usa un ID de docente fijo (ej: 1) para pruebas
    return mostrar_dashboard(docente_id=1)  # Cambia el 1 por el ID que exista en tu DB