import os
import subprocess

def run_pylint(file_path):
    """Ejecuta pylint en un archivo dado y retorna los resultados."""
    result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
    return result.stdout

def check_files():
    """Verifica la existencia de archivos esenciales."""
    essential_files = ['models.py', 'routes.py', 'socket_handlers.py', 'Server.py']
    missing_files = []

    for file in essential_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def check_werkzeug_version():
    """Verifica la versión de werkzeug para posibles problemas de compatibilidad."""
    try:
        import werkzeug
        return subprocess.check_output(['pip', 'show', 'werkzeug']).decode().strip().split('\n')[1].split(":")[1].strip()
    except ImportError:
        return None

def update_werkzeug():
    """Intenta actualizar werkzeug si es necesario."""
    print("Actualizando werkzeug...")
    subprocess.run(["pip", "install", "--upgrade", "werkzeug"])

def main():
    print("Verificando archivos esenciales...")
    missing_files = check_files()

    if missing_files:
        print("❌ Archivos faltantes:", ", ".join(missing_files))
    else:
        print("✅ Todos los archivos esenciales están presentes.")

    # Ejecutar pylint en los archivos
    files_to_check = ['models.py', 'routes.py', 'socket_handlers.py', 'Server.py']
    
    for file in files_to_check:
        print(f"\nEjecutando pylint en {file}...")
        pylint_output = run_pylint(file)
        print(pylint_output)

    # Verificar la versión de werkzeug
    werkzeug_version = check_werkzeug_version()
    if werkzeug_version:
        print(f"\nVersión de werkzeug: {werkzeug_version}")
    else:
        print("❌ No se encontró werkzeug. Intentando actualizar...")
        update_werkzeug()
        werkzeug_version = check_werkzeug_version()
        if werkzeug_version:
            print(f"✅ werkzeug actualizado a la versión: {werkzeug_version}")
        else:
            print("❌ No se pudo instalar werkzeug.")

    print("\nVerificación completada CON errores. Revisa los mensajes anteriores.")

if __name__ == "__main__":
    main()
