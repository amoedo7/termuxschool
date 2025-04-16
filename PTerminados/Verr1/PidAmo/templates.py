"""
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
            <label>Hamburguesa - $10</label>
            <input type="number" name="quantity_hamburguesa" min="0" value="0">
        </div>
        <div>
            <label>Cerveza - $5</label>
            <input type="number" name="quantity_cerveza" min="0" value="0">
        </div>
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
