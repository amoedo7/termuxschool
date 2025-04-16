import os

ruta = "Server.py"
log_path = "executed_updates.txt"
update_log_path = "update_log.txt"

# Leer el contenido de Server.py
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

# Asegurarse de que las importaciones necesarias están presentes
if "request" not in contenido:
    contenido = contenido.replace(
        "from flask import Flask, render_template",
        "from flask import Flask, render_template, request"
    )
if "import os" not in contenido:
    contenido = "import os\n" + contenido

# Insertar las nuevas rutas (antes del if __name__)
nuevas_rutas = """
@app.route("/menu")
def menu():
    mesa = request.args.get("mesa")
    if not mesa:
        return "Número de mesa no proporcionado", 400
    return render_template("menu.html", mesa=mesa)


@app.route("/enviar_pedido", methods=["POST"])
def enviar_pedido():
    data = request.get_json()
    mesa = data.get("mesa")
    pedido = data.get("pedido")

    if not mesa or not pedido:
        return "Datos incompletos", 400

    comida = [item for item in pedido if item.get("tipo") == "comida"]
    bebida = [item for item in pedido if item.get("tipo") == "bebida"]

    ruta_base = "Pedidos"
    os.makedirs(ruta_base, exist_ok=True)

    with open(f"{ruta_base}/mesa_{mesa}_comida.txt", "w", encoding="utf-8") as f:
        for item in comida:
            f.write(f"{item['nombre']} - ${item['precio']}\\n")

    with open(f"{ruta_base}/mesa_{mesa}_bebida.txt", "w", encoding="utf-8") as f:
        for item in bebida:
            f.write(f"{item['nombre']} - ${item['precio']}\\n")

    print(f"🧾 Pedido registrado para la mesa {mesa}")
    return "OK", 200
"""

# Insertar las nuevas rutas justo antes de `if __name__ == "__main__":`
if "__name__" in contenido:
    contenido = contenido.replace(
        'if __name__ == "__main__":',
        nuevas_rutas + '\n\nif __name__ == "__main__":'
    )

# Escribir el contenido modificado de nuevo en Server.py
with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

# Registrar la actualización en los logs
update_message = f"update6.py ejecutado correctamente en Server.py\n"

# Añadir a executed_updates.txt
with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write(update_message)

# Añadir a update_log.txt
with open(update_log_path, "a", encoding="utf-8") as update_log_file:
    update_log_file.write(update_message)

print("✅ update6.py aplicado con éxito y registros guardados.")
