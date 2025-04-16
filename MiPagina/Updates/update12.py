import os

def create_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Archivo creado/actualizado: {file_path}")

# ---------------------
# Rutas de archivo de la nueva estructura
# ---------------------
project_dir = os.getcwd()  # Directorio raíz del proyecto
routes_file = os.path.join(project_dir, 'routes.py')
templates_dir = os.path.join(project_dir, 'templates')

# Asegurarse de que el directorio "templates" exista
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
    print(f"Directorio creado: {templates_dir}")

# ---------------------
# Nuevo contenido actualizado para routes.py
# ---------------------
routes_content = '''from flask import Flask, render_template, request, redirect, url_for
from models import crear_pedido, obtener_pedidos, cambiar_estado_pedido
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    pedidos = obtener_pedidos()
    return render_template('index.html', pedidos=pedidos)

# Ruta de menú: presenta el menú para la mesa indicada.
@app.route('/menu')
def menu():
    mesa = request.args.get('mesa')
    if not mesa:
        return "Número de mesa no proporcionado", 400
    return render_template('menu.html', mesa=mesa)

# Nueva ruta para recibir el pedido enviado desde el menú.
@app.route('/enviar_pedido', methods=['POST'])
def enviar_pedido():
    mesa = request.form.get('mesa')
    tipo = request.form.get('tipo')
    descripcion = request.form.get('descripcion')
    if not mesa or not tipo or not descripcion:
        return "Datos incompletos", 400
    crear_pedido(mesa, tipo, descripcion)
    return "Pedido enviado", 200

# Vista para la cocina: muestra solo pedidos de "comida" que no estén finalizados.
@app.route('/cocina')
def cocina():
    pedidos = obtener_pedidos()
    pedidos_cocina = [p for p in pedidos if p[2].lower() == 'comida' and p[3] != 'Finalizado']
    return render_template('cocina.html', pedidos=pedidos_cocina)

# Vista para el bar: muestra solo pedidos de "bebida" que no estén finalizados.
@app.route('/bar')
def bar():
    pedidos = obtener_pedidos()
    pedidos_bar = [p for p in pedidos if p[2].lower() == 'bebida' and p[3] != 'Finalizado']
    return render_template('bar.html', pedidos=pedidos_bar)

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

# Nueva ruta para finalizar un pedido, ocultándolo de las vistas activas.
@app.route('/finalizar/<int:id_pedido>')
def finalizar(id_pedido):
    cambiar_estado_pedido(id_pedido, 'Finalizado')
    socketio.emit('actualizar_estado', {'id': id_pedido, 'estado': 'Finalizado'})
    return redirect(url_for('index'))
'''

# Actualizar routes.py
create_file(routes_file, routes_content)

# ---------------------
# Nuevo contenido para las plantillas de cocina y bar
# ---------------------
cocina_html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Pedidos de Cocina</title>
</head>
<body>
    <h1>Pedidos para Cocina</h1>
    {% if pedidos %}
    <ul>
        {% for pedido in pedidos %}
        <li>
            Mesa {{ pedido[1] }} - {{ pedido[4] }} - Estado: {{ pedido[3] }}
            [<a href="/finalizar/{{ pedido[0] }}">Finalizar</a>]
        </li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No hay pedidos pendientes.</p>
    {% endif %}
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
    {% if pedidos %}
    <ul>
        {% for pedido in pedidos %}
        <li>
            Mesa {{ pedido[1] }} - {{ pedido[4] }} - Estado: {{ pedido[3] }}
            [<a href="/finalizar/{{ pedido[0] }}">Finalizar</a>]
        </li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No hay pedidos pendientes.</p>
    {% endif %}
    <a href="/">Volver</a>
</body>
</html>
'''

# Actualizar las plantillas en el directorio templates
cocina_template = os.path.join(templates_dir, 'cocina.html')
bar_template = os.path.join(templates_dir, 'bar.html')

create_file(cocina_template, cocina_html_content)
create_file(bar_template, bar_html_content)

print("\nUpdate12 completado: Las rutas y vistas han sido actualizadas para gestionar la finalización de pedidos.")
