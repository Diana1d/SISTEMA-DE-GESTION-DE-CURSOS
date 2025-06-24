from flask import Blueprint, redirect, url_for
from flask_login import logout_user

auth_bp = Blueprint('docente_auth', __name__, url_prefix="/docente")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('autentica.login'))