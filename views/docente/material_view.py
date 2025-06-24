from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app
import os

def listar_materiales(curso, materiales):
    """Muestra todos los materiales de un curso"""
    return render_template('docente/materiales/index.html', 
                         curso=curso, 
                         materiales=materiales)  # Variable correcta 'materiales'

def subir_material_form(curso):
    """Muestra el formulario para subir material"""
    return render_template('docente/materiales/subir.html', 
                         curso=curso)

def handle_upload(file):
    """Maneja la subida de archivos"""
    if file:
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Asegurar que el directorio existe
        os.makedirs(upload_folder, exist_ok=True)
        
        # Guardar el archivo
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Obtener información del archivo
        file_size = os.path.getsize(filepath)
        file_type = filename.split('.')[-1].lower() if '.' in filename else 'desconocido'
        
        return {
            'nombre_archivo': filename,
            'tipo_archivo': file_type,
            'tamanio': file_size
        }
    return None