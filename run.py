from flask import Flask,request,render_template,redirect,url_for
from flask_login import LoginManager
from models.rol_model import Rol
from models.usuario_model import Usuario

from controllers.admi import usuario_controller
from controllers.admi import docente_controller
from controllers.admi import estudiante_controller
from controllers.admi import curso_controller
from database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#CONFIGURAR FLASK-LOGIN
app.secret_key = 'claveSecreta'
login_manager = LoginManager()
login_manager.login_view = 'usuario.login'
login_manager.init_app(app)

def init_db():
    with app.app_context():
        db.create_all()  #CREA LA BASE DE DATOS Y LAS TABLAS
        if not Rol.query.filter_by(nombre="Administrador").first():
            rol1 = Rol(nombre="Administrador")
            rol2 = Rol(nombre="Docente")
            rol3 = Rol(nombre="Estudiante")
            db.session.add_all([rol1, rol2, rol3])
            db.session.commit()
            print("Roles insertados.")
        else:
            print("Roles ya existen.")

# BLUEPRINTS
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(docente_controller.docente_bp)
app.register_blueprint(estudiante_controller.estudiante_bp)
app.register_blueprint(curso_controller.curso_bp)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id)

@app.route('/')
def home():
    return render_template('autentica/index.html')


# PUNTO DE ENTRADA
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)