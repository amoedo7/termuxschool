import os
import sys
import sqlite3
import subprocess

# Establecer la raíz del proyecto (C:\Users\El3imm\MiPagina) como el directorio principal
project_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))  # La raíz del proyecto es un nivel arriba de 'Updates'
sys.path.insert(0, project_dir)  # Aseguramos que la raíz del proyecto esté en el path para las importaciones

# Definir los archivos esenciales y plantillas en relación con la raíz del proyecto
essential_files = ['models.py', 'routes.py', 'socket_handlers.py', 'Server.py']
templates_files = ['index.html', 'menu.html', 'cocina.html', 'bar.html']
errors = False

# Verificar existencia de archivos esenciales
print("Verificando archivos esenciales...")
for filename in essential_files:
    file_path = os.path.join(project_dir, filename)  # Ruta absoluta de los archivos esenciales
    if not os.path.exists(file_path):
        print(f"❌ El archivo {filename} NO existe.")
        errors = True
    else:
        print(f"✅ {filename} encontrado.")

        # Verificar el código con pylint si el archivo existe
        try:
            print(f"Ejecutando pylint en {filename}...")
            result = subprocess.run(['pylint', os.path.join(project_dir, filename)], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {filename} pasó la verificación de pylint.")
            else:
                print(f"❌ Errores en {filename} con pylint:\n{result.stdout}")
        except Exception as e:
            print(f"❌ Error al ejecutar pylint en {filename}: {e}")
            errors = True

# Verificar directorio 'templates' y sus archivos
templates_dir = os.path.join(project_dir, 'templates')
if not os.path.isdir(templates_dir):
    print("❌ El directorio 'templates' NO existe.")
    errors = True
else:
    print("✅ Directorio 'templates' encontrado.")
    for filename in templates_files:
        template_path = os.path.join(templates_dir, filename)
        if not os.path.exists(template_path):
            print(f"❌ La plantilla {filename} NO existe en el directorio 'templates'.")
            errors = True
        else:
            print(f"✅ Plantilla {filename} encontrada.")

# Verificar la base de datos y la tabla 'pedidos'
print("\nVerificando la base de datos 'pidamo.db' y la tabla 'pedidos'...")
db_path = os.path.join(project_dir, 'pidamo.db')  # Ruta absoluta para la base de datos
if not os.path.exists(db_path):
    print("❌ La base de datos 'pidamo.db' NO existe.")
    errors = True
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pedidos'")
        table = cursor.fetchone()
        if table:
            print("✅ Tabla 'pedidos' encontrada en la base de datos.")
        else:
            print("❌ La tabla 'pedidos' NO existe en la base de datos.")
            errors = True
        conn.close()
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")
        errors = True

# Utilizar el cliente de pruebas de Flask para verificar algunos endpoints
print("\nVerificando endpoints con el cliente de pruebas de Flask...")
try:
    # Importar la aplicación (según la estructura en Server.py)
    from Server import app
    app.testing = True
    client = app.test_client()

    # Verificar /menu?mesa=21
    response = client.get('/menu?mesa=21')
    if response.status_code == 200:
        print("✅ Endpoint /menu?mesa=21 responde correctamente (200).")
    else:
        print(f"❌ Endpoint /menu?mesa=21 responde con código {response.status_code}.")

    # Verificar /cocina
    response = client.get('/cocina')
    if response.status_code == 200:
        print("✅ Endpoint /cocina responde correctamente (200).")
    else:
        print(f"❌ Endpoint /cocina responde con código {response.status_code}.")

    # Verificar /bar
    response = client.get('/bar')
    if response.status_code == 200:
        print("✅ Endpoint /bar responde correctamente (200).")
    else:
        print(f"❌ Endpoint /bar responde con código {response.status_code}.")
except Exception as e:
    print(f"❌ Error al probar los endpoints: {e}")
    errors = True

# Mostrar resumen final
if errors:
    print("\nVerificación completada CON errores. Revisa los mensajes anteriores.")
else:
    print("\nVerificación completada exitosamente. Todo está en orden.")
