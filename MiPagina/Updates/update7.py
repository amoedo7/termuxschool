import os

# Ruta del archivo server.py que será modificado
server_file = "Server.py"

# Contenido que debe ser añadido o modificado en Server.py
new_code = """
@app.route("/enviar_pedido", methods=["POST"])
def enviar_pedido():
    data = request.get_json()
    mesa = data.get("mesa")
    pedido = data.get("pedido")

    if not mesa or not pedido:
        return "Datos incompletos", 400

    comida = [item for item in pedido if item.get("tipo") == "comida"]
    bebida = [item for item in pedido if item.get("tipo") == "bebida"]

    # Crear directorios para cocina y bar si no existen
    ruta_base_cocina = "Pedidos/cocina"
    ruta_base_bar = "Pedidos/bar"
    os.makedirs(ruta_base_cocina, exist_ok=True)
    os.makedirs(ruta_base_bar, exist_ok=True)

    # Guardar comida en el directorio cocina
    with open(f"{ruta_base_cocina}/mesa_{mesa}_comida.txt", "w", encoding="utf-8") as f:
        for item in comida:
            f.write(f"{item['nombre']} - ${item['precio']}\n")

    # Guardar bebidas en el directorio bar
    with open(f"{ruta_base_bar}/mesa_{mesa}_bebida.txt", "w", encoding="utf-8") as f:
        for item in bebida:
            f.write(f"{item['nombre']} - ${item['precio']}\n")

    print(f"🧾 Pedido registrado para la mesa {mesa}")
    return "✅ Pedido enviado!", 200
"""

# Leer el archivo server.py
with open(server_file, "r", encoding="utf-8") as file:
    server_content = file.read()

# Verificar si el bloque de código ya existe en server.py
if "enviar_pedido" not in server_content:
    # Agregar el nuevo código antes del "if __name__ == '__main__':"
    server_content = server_content.replace(
        "if __name__ == '__main__':",
        new_code + "\n\nif __name__ == '__main__':"
    )

    # Escribir los cambios de vuelta a server.py
    with open(server_file, "w", encoding="utf-8") as file:
        file.write(server_content)

    print("✔️ El código de la ruta '/enviar_pedido' ha sido agregado correctamente a server.py.")
else:
    print("🚫 La ruta '/enviar_pedido' ya existe en server.py.")
