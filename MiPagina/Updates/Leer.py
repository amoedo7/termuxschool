import os

# Ruta base del proyecto
BASE_DIR = "C:\\Users\\El3imm\\MiPagina"

# Mapeo de archivos que el usuario puede buscar
FILES_DIR = {
    "script.js": "static/js/script.js",
    "Server.py": "Server.py",
    "routes": "app/routes/routes.py",
    "models.py": "models.py",
    "socket_handlers.py": "app/socket_handlers/socket_handlers.py",
    "mesa_21_comida.txt": "Pedidos/mesa_21_comida.txt",
}

def leer_archivo(file_name):
    """Muestra el contenido de un archivo específico o un mensaje de error si no se encuentra."""
    # Obtener la ruta completa del archivo a buscar
    file_path = os.path.join(BASE_DIR, FILES_DIR.get(file_name, ""))
    
    if os.path.exists(file_path):
        # Si el archivo existe, leer y mostrar el contenido
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            print(f"\n🔍 Contenido de {file_name}:")
            print("="*40)
            print(file.read())
            print("="*40)
    else:
        print(f"❌ {file_name} archivo no fue encontrado en {file_path}.")

def main():
    # Pedir al usuario los nombres de los archivos que quiere leer
    archivos = input("Escribe los nombres de los archivos que quieres leer (separados por coma): ").split(",")
    
    # Limpiar entradas de espacios extra
    archivos = [a.strip() for a in archivos]
    
    # Leer cada archivo
    for archivo in archivos:
        leer_archivo(archivo)

if __name__ == "__main__":
    main()
