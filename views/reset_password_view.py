from flask import render_template

def recuperar():
    return render_template('autentica/solicitar.html')

def nueva_contrasena():
    return render_template('autentica/nueva_contrasena.html')
