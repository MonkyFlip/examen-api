### **1. Descripción de la API**
Esta API fue diseñada con **Flask** como parte de un proyecto académico para manejar usuarios registrados. Cuenta con funcionalidades básicas como inicio de sesión, creación de usuarios, y obtención de la lista de usuarios.

El desarrollo incluye el uso de **Flask SQLAlchemy** para la gestión de la base de datos, **Flask CORS** para habilitar solicitudes de origen cruzado, y **itsdangerous** para manejar tokens de autenticación.

### **2. Instalación de Dependencias**
Se instalaron las siguientes librerías para la creación de la API:

1. **Flask**: Framework principal.
   pip install flask

2. **Flask SQLAlchemy**: Gestión de la base de datos.
   pip install flask-sqlalchemy

3. **Flask CORS**: Permitir solicitudes de origen cruzado.
   pip install flask-cors


4. **itsdangerous**: Manejo de generación y validación de tokens.
   pip install itsdangerous

### **3. Estructura del Proyecto**
El proyecto está organizado de la siguiente manera:
examen-api/
├── app/
│   ├── __init__.py       # Inicializa el módulo Flask
│   ├── models.py         # Definición de la base de datos
│   ├── routes.py         # Define las rutas de la API
├── config.py             # Configuración del proyecto
├── run.py                # Archivo principal para ejecutar el servidor



### **4. Configuración de la Base de Datos**
En **models.py**, se configuró el modelo de usuario usando SQLAlchemy:
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

### **5. Rutas de la API**
La API incluye los siguientes endpoints:

#### **Ruta: Inicio**
Muestra un mensaje de bienvenida al abrir la API en el navegador.
@routes.route('/', methods=['GET'])
def home():
    return '''
    <html>
        <h1>¡Bienvenido a la API de Usuarios!</h1>
        <p>Haz clic <a href="/users">aquí</a> para ver los usuarios registrados.</p>
    </html>
    '''

#### **Ruta: Login**
Valida las credenciales enviadas y retorna un mensaje.
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(correo=data['correo'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login exitoso'}), 200
    return jsonify({'message': 'Credenciales inválidas'}), 401


#### **Ruta: Obtención de Usuarios**
Devuelve la lista de usuarios registrados en formato JSON. Está protegida con un token de autorización.

@routes.route('/users', methods=['GET'])
@token_required
def get_users():
    users = User.query.all()
    users_json = [{'id': user.id, 'nombre': user.nombre, 'correo': user.correo} for user in users]
    return jsonify(users_json)

#### **Ruta: Creación de Usuario**
Permite registrar nuevos usuarios en la base de datos.
@routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(nombre=data['nombre'], correo=data['correo'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado con éxito'}), 201

#### **Ruta: Actualización de Usuario**
Actualiza los datos de un usuario específico.
@routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if user:
        user.nombre = data['nombre']
        user.correo = data['correo']
        user.password = data['password']
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado con éxito'}), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404

#### **Ruta: Eliminación de Usuario**
Elimina un usuario específico de la base de datos.
@routes.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado con éxito'}), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404

### **6. Manejo de Tokens**
Se implementó un decorador para manejar la autenticación mediante tokens. Este decorador verifica si el token es válido antes de ejecutar las rutas protegidas.
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization').split()[1] if request.headers.get('Authorization') else None
        if not token:
            return jsonify({'message': 'Token faltante'}), 403
        try:
            s = Serializer(SECRET_KEY)
            data = s.loads(token)
            return f(*args, **kwargs)
        except:
            return jsonify({'message': 'Token inválido o expirado'}), 403
    return decorator



### **7. Configuración y Ejecución**
El archivo **run.py** inicializa el servidor y corre la aplicación:
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

Para ejecutar el servidor:
python run.py

### **8. Pruebas**
Puedes usar herramientas como **Postman** o **curl** para probar los endpoints de la API.

#### **Prueba del Endpoint Login:**
curl -X POST -H "Content-Type: application/json" -d '{"correo": "user@example.com", "password": "123456"}' https://3.12.241.112/login

#### **Prueba de Obtención de Usuarios:**
curl -X GET -H "Authorization: Bearer <token>" https://3.12.241.112/users

#### **Prueba de Creación de Usuario:**
curl -X POST -H "Content-Type: application/json" -d '{"nombre": "Nuevo Usuario", "correo": "nuevo@example.com", "password": "password"}' https://3.12.241.112/users
### **9. Créditos**
La API fue diseñada y desarrollada como parte del proyecto académico para la materia **Desarrollo Móvil Multiplataforma**. Utiliza **Flask**, **SQLAlchemy**, y otras librerías esenciales.
