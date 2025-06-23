from flask import Flask,request,render_template,redirect,url_for
from flask_login import current_user, login_required  # Importar current_user y login_required
from datetime import datetime
import os
from flask_login import LoginManager

# ADMIN
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

# DOCENTE
from models.asignacion_model import Asignacion
from models.asistencia_model import Asistencia
from models.calificacion_model import Calificacion
from models.curso_model import Curso
from models.docente_model import Docente
from models.entrega_tarea_model import EntregaTarea
from models.estudiante_model import Estudiante
from models.evaluacion_model import Evaluacion
from models.material_model import Material
from models.notificacion_model import Notificacion
from models.tarea_model import Tarea

from controllers.docente import inicio_controller
from controllers.docente import asistencia_controller
from controllers.docente import calificacion_controller
from controllers.docente import mis_cursos_controller
from controllers.docente import mis_estudiantes_controller
from controllers.docente import material_controller
from controllers.docente import mis_archivos_controller
from database import db

# ESTUDIANTE
from controllers.estudiante import mi_asistencia_controller
from controllers.estudiante import mi_calificacion_controller
from controllers.estudiante import mi_curso_controller
from controllers.estudiante import mi_inicio_controller
from controllers.estudiante import mi_material_controller
from controllers.estudiante import mi_tarea_controller

app = Flask(__name__)

app.config['SECRET_KEY'] = 'claveSecreta'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

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

# BLUEPRINTS DOCENTE
app.register_blueprint(asistencia_controller.asistencia_bp)
app.register_blueprint(calificacion_controller.calificacion_bp)
app.register_blueprint(mis_cursos_controller.curso_docente_bp)
app.register_blueprint(mis_estudiantes_controller.estudiante_bp)
app.register_blueprint(material_controller.material_bp) 
app.register_blueprint(inicio_controller.inicio_bp)
app.register_blueprint(mis_archivos_controller.mis_archivos_bp)

# BLUEPRINTS ESTUDIANTE
app.register_blueprint(mi_asistencia_controller.asistencia_bp)
app.register_blueprint(mi_calificacion_controller.calificacion_bp)
app.register_blueprint(mi_curso_controller.curso_bp)
app.register_blueprint(mi_inicio_controller.inicio_bp)
app.register_blueprint(mi_material_controller.material_bp)
app.register_blueprint(mi_tarea_controller.tarea_bp)


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