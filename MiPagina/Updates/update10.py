import os

# Ruta base de los archivos de pedidos
BASE_PEDIDOS_DIR = 'Pedidos'

# Asegurarse de que la carpeta 'Pedidos' exista
os.makedirs(BASE_PEDIDOS_DIR, exist_ok=True)

# Crear archivos de ejemplo para pedidos si no existen
def crear_archivo_pedido(mesa, tipo):
    archivo_nombre = f"mesa_{mesa}_{tipo}.txt"
    archivo_path = os.path.join(BASE_PEDIDOS_DIR, archivo_nombre)
    # Si el archivo no existe, lo creamos con contenido base
    if not os.path.exists(archivo_path):
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(f"Pedido de mesa {mesa} para {tipo}. \n")
        print(f"Archivo {archivo_nombre} creado.")
    return archivo_nombre

# Crear pedidos de ejemplo (comida y bebida) para varias mesas
def crear_pedidos_ejemplo():
    # Mesas para las cuales se crearán los pedidos
    mesas = [21, 22, 23]
    tipos = ['comida', 'bebida']
    
    for mesa in mesas:
        for tipo in tipos:
            crear_archivo_pedido(mesa, tipo)

# Ejecutamos la creación de los archivos de pedidos
if __name__ == '__main__':
    crear_pedidos_ejemplo()
    print("Archivos de pedidos creados correctamente. Ahora puedes ejecutar 'server.py' para iniciar PidAmo.")
