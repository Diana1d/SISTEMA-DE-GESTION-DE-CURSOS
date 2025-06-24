from flask import Blueprint
from views.estudiante.inicio_view import mostrar_dashboard


inicio_bp = Blueprint('estudiante_inicio', __name__, url_prefix="/estudiante/inicio")

@inicio_bp.route("/")
def dashboard():
    # Usar ID de estudiante autenticado
    return mostrar_dashboard(estudiante_id=1)