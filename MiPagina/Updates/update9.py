import os
import json

# Ruta base de los archivos de pedidos
BASE_PEDIDOS_DIR = 'Pedidos'

# Crear los directorios necesarios si no existen
os.makedirs(BASE_PEDIDOS_DIR, exist_ok=True)

# Crear un archivo de ejemplo para pedidos si no existen
def crear_archivo_pedido(mesa, tipo):
    archivo_nombre = f"mesa_{mesa}_{tipo}.txt"
    archivo_path = os.path.join(BASE_PEDIDOS_DIR, archivo_nombre)
    if not os.path.exists(archivo_path):
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(f"Pedido de mesa {mesa} para {tipo}. \n")
        print(f"Archivo {archivo_nombre} creado.")
    return archivo_nombre

# Leer los archivos de pedidos y devolverlos como una lista
def obtener_pedidos(tipo):
    pedidos = []
    for file_name in os.listdir(BASE_PEDIDOS_DIR):
        if tipo in file_name:  # Filtra los archivos de comida o bebida
            with open(os.path.join(BASE_PEDIDOS_DIR, file_name), 'r', encoding='utf-8') as f:
                pedidos.append({
                    "mesa": file_name.split('_')[1],  # Extrae el número de mesa
                    "pedido": f.read(),
                    "file_name": file_name
                })
    return pedidos

# Marcar un pedido como listo, renombrando el archivo
def marcar_pedido_listo(file_name):
    archivo_path = os.path.join(BASE_PEDIDOS_DIR, file_name)
    if os.path.exists(archivo_path):
        nuevo_nombre = f"listo_{file_name}"
        nuevo_path = os.path.join(BASE_PEDIDOS_DIR, nuevo_nombre)
        os.rename(archivo_path, nuevo_path)
        print(f"Pedido {file_name} marcado como listo.")
        return nuevo_nombre
    return None

# Ruta para la vista de cocina
def ver_pedidos_cocina():
    pedidos_cocina = obtener_pedidos('comida')
    return pedidos_cocina

# Ruta para la vista de bar
def ver_pedidos_bar():
    pedidos_bar = obtener_pedidos('bebida')
    return pedidos_bar

# Función principal que se ejecutará como parte de la actualización
def ejecutar_actualizacion():
    # Crear archivos de pedidos para las mesas de ejemplo (si no existen)
    for mesa in [21, 22]:
        crear_archivo_pedido(mesa, 'comida')
        crear_archivo_pedido(mesa, 'bebida')

    # Obtener los pedidos para cocina y bar
    pedidos_cocina = ver_pedidos_cocina()
    pedidos_bar = ver_pedidos_bar()

    # Mostrar los pedidos para asegurarnos que todo funciona
    print("Pedidos en Cocina:")
    for pedido in pedidos_cocina:
        print(f"Mesa {pedido['mesa']}: {pedido['pedido']}")

    print("\nPedidos en Bar:")
    for pedido in pedidos_bar:
        print(f"Mesa {pedido['mesa']}: {pedido['pedido']}")

    # Simulando la acción de marcar un pedido como listo
    if pedidos_cocina:
        marcar_pedido_listo(pedidos_cocina[0]["file_name"])

    if pedidos_bar:
        marcar_pedido_listo(pedidos_bar[0]["file_name"])

# Ejecutar la actualización
if __name__ == "__main__":
    ejecutar_actualizacion()
