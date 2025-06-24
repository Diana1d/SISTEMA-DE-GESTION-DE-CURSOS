from flask import Flask,request,render_template,redirect,url_for
from flask_login import current_user, login_required  # Importar current_user y login_required
from datetime import datetime
import os
from flask_login import LoginManager

from models.rol_model import Rol
from models.turno_modal import Turno
from models.paralelo_modal import Paralelo
from models.usuario_model import Usuario

# ADMIN

from controllers import usuario_controller
from controllers.admi import docente_controller
from controllers.admi import estudiante_controller
from controllers.admi import curso_controller
from controllers.admi import inscripcion_controller
from controllers.admi import semestre_controller
from controllers import reset_password_controller
from database import db,mail

# DOCENTE

from controllers.docente import inicio_controller
from controllers.docente import asistencia_controller
from controllers.docente import calificacion_controller
from controllers.docente import mis_cursos_controller
from controllers.docente import mis_estudiantes_controller
from controllers.docente import material_controller
from controllers.docente import mis_archivos_controller
from controllers.docente import perfil_docente_controller
from controllers.docente import ajustes_docente_controller
from controllers.docente import auth_controller
from database import db

# ESTUDIANTE

from controllers.estudiante import mi_asistencia_controller
from controllers.estudiante import mi_calificacion_controller
from controllers.estudiante import mi_curso_controller
from controllers.estudiante import mi_inicio_controller
from controllers.estudiante import mi_material_controller
from controllers.estudiante import mi_tarea_controller
from controllers.estudiante import perfil_estudiante_controller
from controllers.estudiante import ajustes_estudiante_controller
from controllers.estudiante import auth_controller

app = Flask(__name__)



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'admi.prueba432@gmail.com'
app.config['MAIL_PASSWORD'] = 'tcyiblqjkiayzzgs'
app.config['MAIL_DEFAULT_SENDER'] = 'admi.prueba432@gmail.com'

app.config['SECRET_KEY'] = 'clave_super_segura_generada'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
mail.init_app(app)

# Registrar filtro de fecha
@app.template_filter('date')
def format_date(value, format='%d/%m/%Y'):
    if value is None:
        return ""
    if isinstance(value, str):
        # Si es string, convertir a datetime primero
        value = datetime.strptime(value, '%Y-%m-%d')
    return value.strftime(format)

# Configuración para subida de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB límite

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

# BLUEPRINTS ADMI
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(docente_controller.docente_bp)
app.register_blueprint(estudiante_controller.estudiante_bp)
app.register_blueprint(curso_controller.curso_bp)
app.register_blueprint(inscripcion_controller.inscripcion_bp)
app.register_blueprint(semestre_controller.semestre_bp)
app.register_blueprint(reset_password_controller.recuperar_bp)

# BLUEPRINTS DOCENTE
app.register_blueprint(asistencia_controller.asistencia_bp)
app.register_blueprint(calificacion_controller.calificacion_bp)
app.register_blueprint(mis_cursos_controller.curso_docente_bp)
app.register_blueprint(mis_estudiantes_controller.estudiante_bp)
app.register_blueprint(material_controller.material_bp) 
app.register_blueprint(inicio_controller.inicio_bp)
app.register_blueprint(mis_archivos_controller.mis_archivos_bp)
app.register_blueprint(perfil_docente_controller.perfil_bp)
app.register_blueprint(ajustes_docente_controller.ajustes_bp)
app.register_blueprint(auth_controller.auth_bp)

# BLUEPRINTS ESTUDIANTE
app.register_blueprint(mi_asistencia_controller.asistencia_bp)
app.register_blueprint(mi_calificacion_controller.calificacion_bp)
app.register_blueprint(mi_curso_controller.curso_bp)
app.register_blueprint(mi_inicio_controller.inicio_bp)
app.register_blueprint(mi_material_controller.mi_material_bp)
app.register_blueprint(mi_tarea_controller.tarea_bp)
app.register_blueprint(perfil_estudiante_controller.perfil_bp)
app.register_blueprint(ajustes_estudiante_controller.ajustes_bp)
#app.register_blueprint(auth_controller.auth_bp)


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