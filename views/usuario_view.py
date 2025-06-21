from flask import render_template

def list(usuarios,roles):
    
    return render_template('admi/usuarios/index.html',usuarios= usuarios,roles=roles)

def create(roles):
    return render_template('admi/usuarios/create.html',roles=roles)

def edit(usuario):
    return render_template('admi/usuarios/edit.html',usuario= usuario)

def vista(usuario):
    return render_template('admi/usuarios/vista.html',usuario=usuario)

def login():
    return render_template('autentica/login.html')

def index():
    return render_template('autentica/index.html')

def dashboard(usuario):
    return render_template('admi/dashboard.html',usuario=usuario)




 