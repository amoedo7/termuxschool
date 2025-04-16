"""
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
