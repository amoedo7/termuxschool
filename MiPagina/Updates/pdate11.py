import os
import sqlite3

# ---------------------
# Utilidad para crear/actualizar archivos
# ---------------------
def create_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Archivo creado/actualizado: {file_path}")

# ---------------------
# Rutas de archivo de la nueva estructura
# ---------------------
project_dir = os.getcwd()  # Directorio raíz del proyecto
models_file = os.path.join(project_dir, 'models.py')
routes_file = os.path.join(project_dir, 'routes.py')
socket_handlers_file = os.path.join(project_dir, 'socket_handlers.py')
server_file = os.path.join(project_dir, 'server.py')
templates_dir = os.path.join(project_dir, 'templates')

# Asegurarse de que el directorio "templates" exista
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
    print(f"Directorio creado: {templates_dir}")

# ---------------------
# Contenido para cada archivo
# ---------------------

# 1. models.py (Base de datos y lógica de pedidos)
models_content = '''import sqlite3

# Ruta de la base de datos
DB_PATH = 'pidamo.db'

# Crear la base de datos y las tablas si no existen
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mesa INTEGER,
                tipo TEXT,
                estado TEXT,
                descripcion TEXT
            );
        """)
        conn.commit()

# Función para insertar un pedido en la base de datos
def crear_pedido(mesa, tipo, descripcion):
    estado = 'Pendiente'  # Estado inicial
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pedidos (mesa, tipo, estado, descripcion)
            VALUES (?, ?, ?, ?)
        """, (mesa, tipo, estado, descripcion))
        conn.commit()

# Función para obtener los pedidos por estado
def obtener_pedidos(estado=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if estado:
            cursor.execute("SELECT * FROM pedidos WHERE estado = ?", (estado,))
        else:
            cursor.execute("SELECT * FROM pedidos")
        pedidos = cursor.fetchall()
    return pedidos

# Función para cambiar el estado de un pedido
def cambiar_estado_pedido(id_pedido, nuevo_estado):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pedidos SET estado = ? WHERE id = ?
        """, (nuevo_estado, id_pedido))
        conn.commit()
'''

# 2. routes.py (Rutas de la aplicación, incluyendo las nuevas)
routes_content = '''from flask import Flask, render_template, request, redirect, url_for
from models import crear_pedido, obtener_pedidos, cambiar_estado_pedido
from flask_socketio import SocketIO, emit

# Iniciar la aplicación Flask y SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    pedidos = obtener_pedidos()
    return render_template('index.html', pedidos=pedidos)

@app.route('/menu')
def menu():
    mesa = request.args.get('mesa')
    if not mesa:
        return "Número de mesa no proporcionado", 400
    return render_template('menu.html', mesa=mesa)

@app.route('/cocina')
def cocina():
    # Aquí se podrían listar los pedidos de cocina
    return render_template('cocina.html')

@app.route('/bar')
def bar():
    # Aquí se podrían listar los pedidos de bar
    return render_template('bar.html')

@app.route('/pedidos/<estado>')
def ver_pedidos_estado(estado):
    pedidos = obtener_pedidos(estado)
    return render_template('index.html', pedidos=pedidos)

@app.route('/crear_pedido', methods=['POST'])
def crear_pedido_route():
    mesa = request.form['mesa']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']
    crear_pedido(mesa, tipo, descripcion)
    return redirect(url_for('index'))

@app.route('/marcar_listo/<int:id_pedido>')
def marcar_listo(id_pedido):
    cambiar_estado_pedido(id_pedido, 'Listo')
    socketio.emit('actualizar_estado', {'id': id_pedido, 'estado': 'Listo'})
    return redirect(url_for('index'))

@app.route('/marcar_entregado/<int:id_pedido>')
def marcar_entregado(id_pedido):
    cambiar_estado_pedido(id_pedido, 'Entregado')
    socketio.emit('actualizar_estado', {'id': id_pedido, 'estado': 'Entregado'})
    return redirect(url_for('index'))
'''

# 3. socket_handlers.py (Manejo de eventos SocketIO)
socket_handlers_content = '''from flask_socketio import SocketIO, emit

def handle_connect():
    print('Cliente conectado')

def handle_disconnect():
    print('Cliente desconectado')

def configurar_notificaciones(socketio):
    socketio.on_event('connect', handle_connect)
    socketio.on_event('disconnect', handle_disconnect)
'''

# 4. server.py (Archivo principal para ejecutar la aplicación)
server_content = '''import os
from flask_socketio import SocketIO
from models import init_db
from routes import app as flask_app
from socket_handlers import configurar_notificaciones

# Configuración de la aplicación
app = flask_app
socketio = SocketIO(app)

if __name__ == '__main__':
    init_db()  # Inicializa la base de datos y las tablas
    configurar_notificaciones(socketio)
    socketio.run(app, debug=True)
'''

# ---------------------
# Contenido para plantillas HTML (si no existen)
# ---------------------
index_html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PidAmo - Pedidos</title>
</head>
<body>
    <h1>Lista de Pedidos</h1>
    {% if pedidos %}
        <ul>
        {% for pedido in pedidos %}
            <li>Mesa {{ pedido[1] }} - {{ pedido[2] }} - Estado: {{ pedido[3] }} - {{ pedido[4] }}
                [<a href="/marcar_listo/{{ pedido[0] }}">Listo</a>] 
                [<a href="/marcar_entregado/{{ pedido[0] }}">Entregado</a>]
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No hay pedidos.</p>
    {% endif %}
    <h2>Crear Pedido</h2>
    <form action="/crear_pedido" method="post">
        <label>Mesa: <input type="number" name="mesa" required></label><br>
        <label>Tipo:
            <select name="tipo">
                <option value="comida">Comida</option>
                <option value="bebida">Bebida</option>
            </select>
        </label><br>
        <label>Descripción: <input type="text" name="descripcion" required></label><br>
        <button type="submit">Crear Pedido</button>
    </form>
    <br>
    <a href="/menu?mesa=21">Ver Menú (Mesa 21)</a> |
    <a href="/cocina">Ver Cocina</a> |
    <a href="/bar">Ver Bar</a>
</body>
</html>
'''

menu_html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Menú de PidAmo</title>
</head>
<body>
    <h1>Menú - Mesa {{ mesa }}</h1>
    <p>Aquí se mostrará el menú para la mesa {{ mesa }}.</p>
    <a href="/">Volver</a>
</body>
</html>
'''

cocina_html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Pedidos de Cocina</title>
</head>
<body>
    <h1>Pedidos para Cocina</h1>
    <p>Aquí se mostrarán los pedidos de comida.</p>
    <a href="/">Volver</a>
</body>
</html>
'''

bar_html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Pedidos de Bar</title>
</head>
<body>
    <h1>Pedidos para Bar</h1>
    <p>Aquí se mostrarán los pedidos de bebida.</p>
    <a href="/">Volver</a>
</body>
</html>
'''

# ---------------------
# Crear o actualizar los archivos en el sistema
# ---------------------
create_file(models_file, models_content)
create_file(routes_file, routes_content)
create_file(socket_handlers_file, socket_handlers_content)
create_file(server_file, server_content)

# Crear plantillas si no existen (no se sobrescriben si ya están)
templates = {
    "index.html": index_html_content,
    "menu.html": menu_html_content,
    "cocina.html": cocina_html_content,
    "bar.html": bar_html_content
}

for filename, content in templates.items():
    template_path = os.path.join(templates_dir, filename)
    if not os.path.exists(template_path):
        create_file(template_path, content)
    else:
        print(f"Archivo de plantilla ya existe: {template_path}")

# ---------------------
# Inicializar la base de datos (sin ejecutar el servidor)
# ---------------------
def init_db_func():
    with sqlite3.connect('pidamo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mesa INTEGER,
                tipo TEXT,
                estado TEXT,
                descripcion TEXT
            );
        """)
        conn.commit()

init_db_func()
print("Base de datos y tablas creadas exitosamente.")

print("\nEstructura de archivos y plantillas actualizada exitosamente.")
