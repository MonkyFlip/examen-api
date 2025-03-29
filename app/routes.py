from app.models import User, db
from flask import Blueprint, jsonify, request, redirect, url_for

routes = Blueprint('routes', __name__)

# Ruta de inicio (GET /)
@routes.route('/', methods=['GET'])
def home():
    # Página HTML sencilla con un mensaje y enlace
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Página de Inicio</title>
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
        <h1>¡Bienvenido a la API de Usuarios!</h1>
        <p>Haz clic en el siguiente enlace para ver los usuarios registrados:</p>
        <a href="/users" style="color: blue; text-decoration: none; font-size: 18px;">Ver Usuarios</a>
    </body>
    </html>
    '''

# Ruta de login (POST /login)
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(correo=data['correo'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login exitoso', 'user': user.nombre})
    return jsonify({'message': 'Credenciales inválidas'}), 401

# Ruta para obtener listado de usuarios (GET /users)
@routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_json = [
        {'id': user.id, 'nombre': user.nombre, 'correo': user.correo, 'password': user.password}
        for user in users
    ]
    return jsonify(users_json)

# Ruta para crear usuario (POST /users)
@routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(nombre=data['nombre'], correo=data['correo'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado con éxito'})
