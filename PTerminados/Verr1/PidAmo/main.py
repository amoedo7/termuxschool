import subprocess

def run_script(script_name):
    print(f"Ejecutando {script_name}...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def main():
    # Generar plantillas y archivos estáticos
    run_script("templates.py")
    run_script("static.py")
    
    # Inicializar la base de datos (opcional)
    run_script("database.py")
    
    # Iniciar el servidor (este proceso quedará en ejecución)
    print("Iniciando el servidor Flask...")
    subprocess.run(["python", "server.py"])

if __name__ == '__main__':
    main()
