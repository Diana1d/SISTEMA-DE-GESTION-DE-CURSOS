from flask import render_template

def mostrar_perfil(estudiante):
    return render_template('estudiante/perfil/ver.html', estudiante=estudiante)

def editar_perfil_form(estudiante, usuario):
    return render_template('estudiante/perfil/editar.html', estudiante=estudiante, usuario=usuario)

def cambiar_password_form():
    return render_template('estudiante/perfil/cambiar_password.html')