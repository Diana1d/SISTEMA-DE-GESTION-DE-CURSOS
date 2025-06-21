from flask import Flask,request,render_template,redirect,url_for
from flask_login import LoginManager
from models.rol_model import Rol
from models.turno_modal import Turno
from models.paralelo_modal import Paralelo
from models.usuario_model import Usuario

from controllers import usuario_controller
from controllers.admi import docente_controller
from controllers.admi import estudiante_controller
from controllers.admi import curso_controller
from controllers.admi import inscripcion_controller
from controllers.admi import semestre_controller
from database import db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'claveSecreta'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#CONFIGURAR FLASK-LOGIN
login_manager = LoginManager()
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.login_message_category = "warning"
login_manager.login_view = 'usuario.login'
login_manager.init_app(app)

def init_db():
    with app.app_context():
        db.create_all()  # Crea la base de datos y las tablas

        # Insertar roles si no existen
        if not Rol.query.filter_by(nombre="Administrador").first():
            rol1 = Rol(nombre="Administrador")
            rol2 = Rol(nombre="Docente")
            rol3 = Rol(nombre="Estudiante")
            db.session.add_all([rol1, rol2, rol3])
            db.session.commit()
            print("Roles insertados.")
        else:
            print("Roles ya existen.")

        # Insertar turnos si no existen
        if not Turno.query.first():
            turno1 = Turno(tipo_turno="Mañana")
            turno2 = Turno(tipo_turno="Tarde")
            turno3 = Turno(tipo_turno="Noche")
            db.session.add_all([turno1, turno2, turno3])
            db.session.commit()
            print("Turnos insertados.")
        else:
            print("Turnos ya existen.")
        
         # Insertar turnos si no existen
        if not Paralelo.query.first():
            paralelo1 = Paralelo(paralelo="A")
            paralelo2 = Paralelo(paralelo="B")
            paralelo3= Paralelo(paralelo="C")
            db.session.add_all([paralelo1,paralelo2, paralelo3])
            db.session.commit()
            print("Paralelos  insertados.")
        else:
            print("Paralelos  ya existen.")

# BLUEPRINTS
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(docente_controller.docente_bp)
app.register_blueprint(estudiante_controller.estudiante_bp)
app.register_blueprint(curso_controller.curso_bp)
app.register_blueprint(inscripcion_controller.inscripcion_bp)
app.register_blueprint(semestre_controller.semestre_bp)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id)

@app.route('/')
def home():
    return render_template('autentica/index.html')


# PUNTO DE ENTRADA
if __name__ == "__main__":
    init_db()

    app.run(debug=True)