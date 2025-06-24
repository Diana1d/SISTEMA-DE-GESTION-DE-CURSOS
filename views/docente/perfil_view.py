from flask import render_template

def mostrar_perfil(docente):
    return render_template('docente/perfil/ver.html', docente=docente)

def editar_perfil_form(docente, usuario):
    return render_template('docente/perfil/editar.html', docente=docente, usuario=usuario)

def cambiar_password_form():
    return render_template('docente/perfil/cambiar_password.html')