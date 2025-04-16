import os

def create_directories():
    # Lista de carpetas a crear
    directories = ['templates', 'static', 'logs', 'src', 'config', 'data']
    for d in directories:
        os.makedirs(d, exist_ok=True)
    print("Directorios creados.")

def create_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Archivo creado: {file_path}")

def generate_templates_py():
    # Este script generará las plantillas HTML necesarias en la carpeta templates/
    content = r'''"""
Este archivo genera las plantillas HTML de la aplicación PidAmo.
Se crearán los siguientes archivos en la carpeta "templates/":
  - index.html
  - menu.html
  - mozos.html
  - bar.html
"""

import os

templates = {
    'index.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PidAmo - Inicio</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>
<body>
    <h1>Bienvenido a PidAmo</h1>
    <p>Escanee el código QR para acceder al menú.</p>
    <a href="/menu">Ir al Menú</a>
</body>
</html>
""",
    'menu.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Menú Digital</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
    <script src="/static/script.js"></script>
</head>
<body>
    <h1>Menú Digital</h1>
    <form action="/order" method="post">
        <label for="table_number">Número de Mesa:</label>
        <input type="text" name="table_number" id="table_number" required>
        <h2>Productos</h2>
        <div>
            <label>Hamburguesa - $9,000</label>
            <input type="number" name="quantity_hamburguesa" min="0" value="0">
        </div>
        <div>
            <label>Cerveza - $6,000</label>
            <input type="number" name="quantity_cerveza" min="0" value="0">
        </div>
        <div>
            <label>Pizza - $20,000</label>
            <input type="number" name="quantity_pizza" min="0" value="0">
        </div>
        <div>
            <label>Refresco - $5,000</label>
            <input type="number" name="quantity_refresco" min="0" value="0">
        </div>
        <div>
            <label>Ensalada - $7,000</label>
            <input type="number" name="quantity_ensalada" min="0" value="0">
        </div>
        <div>
            <label>Pollo Frito - $12,000</label>
            <input type="number" name="quantity_pollo_frito" min="0" value="0">
        </div>
        <div>
            <label>Fries - $4,000</label>
            <input type="number" name="quantity_fries" min="0" value="0">
        </div>
        <div>
            <label>Nachos - $8,000</label>
            <input type="number" name="quantity_nachos" min="0" value="0">
        </div>
        <div>
            <label>Hot Dog - $6,500</label>
            <input type="number" name="quantity_hot_dog" min="0" value="0">
        </div>
        <div>
            <label>Soda - $3,500</label>
            <input type="number" name="quantity_soda" min="0" value="0">
        </div>
        <div>
            <label>Cócteles - $15,000</label>
            <input type="number" name="quantity_cocteles" min="0" value="0">
        </div>
        <div>
            <label>Vino - $18,000</label>
            <input type="number" name="quantity_vino" min="0" value="0">
        </div>
        <div>
            <label>Tequila - $14,000</label>
            <input type="number" name="quantity_tequila" min="0" value="0">
        </div>
        <div>
            <label>Whisky - $20,000</label>
            <input type="number" name="quantity_whisky" min="0" value="0">
        </div>
        <div>
            <label>Cerveza Artesanal - $10,000</label>
            <input type="number" name="quantity_cerveza_artesanal" min="0" value="0">
        </div>
        <div>
            <label>Gaseosa Dietética - $5,500</label>
            <input type="number" name="quantity_gaseosa_dietetica" min="0" value="0">
        </div>
        <div>
            <label>Cheeseburger - $10,000</label>
            <input type="number" name="quantity_cheeseburger" min="0" value="0">
        </div>
        <div>
            <label>Pizza Caliente - $22,000</label>
            <input type="number" name="quantity_pizza_caliente" min="0" value="0">
        </div>
        <div>
            <label>Wraps - $9,500</label>
            <input type="number" name="quantity_wraps" min="0" value="0">
        </div>
        <button type="submit">Realizar Pedido</button>
    </form>
</body>
        <button type="submit">Realizar Pedido</button>
    </form>
</body>
</html>
""",
    'mozos.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Interfaz de Mozos</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>
<body>
    <h1>Pedidos en Curso</h1>
    <table>
        <tr>
            <th>Mesa</th>
            <th>Productos</th>
            <th>Estado</th>
        </tr>
        {% for order in orders %}
        <tr>
            <td>{{ order['table'] }}</td>
            <td>
                {% for item, qty in order['items'].items() %}
                    {{ item }}: {{ qty }}<br>
                {% endfor %}
            </td>
            <td>{{ order['status'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
""",
    'bar.html': """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Interfaz del Bar</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>
<body>
    <h1>Pedidos para el Bar</h1>
    <table>
        <tr>
            <th>Mesa</th>
            <th>Bebidas</th>
            <th>Estado</th>
        </tr>
        {% for order in orders %}
        <tr>
            <td>{{ order['table'] }}</td>
            <td>
                {{ order['items']['Cerveza'] }}
            </td>
            <td>{{ order['status'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""
}

# Asegurarse de que exista la carpeta "templates"
os.makedirs('templates', exist_ok=True)

# Escribir cada plantilla en su respectivo archivo
for filename, html in templates.items():
    with open(os.path.join('templates', filename), 'w', encoding='utf-8') as f:
        f.write(html)
print("Plantillas HTML generadas en la carpeta 'templates'.")
'''
    return content

def generate_static_py():
    # Este script generará los archivos estáticos en la carpeta static/
    content = r'''"""
Este archivo genera los archivos estáticos para la aplicación PidAmo:
  - styles.css
  - script.js
"""

import os

# Contenido del archivo CSS
styles = """
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}
h1 {
    color: #333;
    text-align: center;
}
table {
    width: 80%;
    margin: 20px auto;
    border-collapse: collapse;
}
table, th, td {
    border: 1px solid #ccc;
}
th, td {
    padding: 10px;
    text-align: center;
}
"""

# Contenido del archivo JavaScript
script = """
document.addEventListener('DOMContentLoaded', function() {
    console.log('PidAmo app loaded.');
});
"""

# Crear la carpeta "static" si no existe
os.makedirs('static', exist_ok=True)

# Escribir el archivo CSS
with open(os.path.join('static', 'styles.css'), 'w', encoding='utf-8') as f:
    f.write(styles)

# Escribir el archivo JavaScript
with open(os.path.join('static', 'script.js'), 'w', encoding='utf-8') as f:
    f.write(script)

print("Archivos estáticos generados en la carpeta 'static'.")
'''
    return content

def generate_server_py():
    # Código del servidor Flask
    content = r'''from flask import Flask, render_template, request, redirect, url_for
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de logs
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Lista en memoria para almacenar los pedidos
orders = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order', methods=['POST'])
def order():
    table_number = request.form.get('table_number')
    quantity_hamburguesa = int(request.form.get('quantity_hamburguesa', 0))
    quantity_cerveza = int(request.form.get('quantity_cerveza', 0))
    order_details = {
        'table': table_number,
        'items': {
            'Hamburguesa': quantity_hamburguesa,
            'Cerveza': quantity_cerveza
        },
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'Pendiente'
    }
    orders.append(order_details)
    logging.info(f"Nuevo pedido: {order_details}")
    # Se simula el procesamiento del pago y la actualización del pedido
    return redirect(url_for('order_confirmation', table=table_number))

@app.route('/order_confirmation')
def order_confirmation():
    table = request.args.get('table')
    return f"Pedido recibido para la mesa {table}. Gracias por su compra."

@app.route('/mozos')
def mozos():
    return render_template('mozos.html', orders=orders)

@app.route('/bar')
def bar():
    return render_template('bar.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
'''
    return content

def generate_database_py():
    # Archivo opcional para manejar la base de datos con SQLite
    content = r'''import sqlite3
import os

DB_PATH = os.path.join('data', 'pidamo.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number TEXT,
            items TEXT,
            time TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada.")
'''
    return content

def main():
    create_directories()
    # Generar y guardar los archivos necesarios
    create_file('templates.py', generate_templates_py())
    create_file('static.py', generate_static_py())
    create_file('server.py', generate_server_py())
    create_file('database.py', generate_database_py())
    print("Todos los archivos se han generado correctamente. ¡Listo para desplegar!")

if __name__ == '__main__':
    main()
