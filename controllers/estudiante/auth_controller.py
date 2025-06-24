from flask import Blueprint, redirect, url_for
from flask_login import logout_user

auth_bp = Blueprint('estudiante_auth', __name__, url_prefix="/estudiante")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('autentica.login'))