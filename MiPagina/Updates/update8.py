import os

# Ruta del archivo server.py que será modificado
server_file = "Server.py"

# Contenido que debe ser añadido o modificado en Server.py
new_code = """
from flask import jsonify

# Ruta para obtener los pedidos de cocina
@app.route("/pedidos_cocina", methods=["GET"])
def pedidos_cocina():
    pedidos = []
    # Leer los archivos de comida en la carpeta de cocina
    ruta_cocina = "Pedidos/cocina"
    for filename in os.listdir(ruta_cocina):
        if filename.endswith("_comida.txt"):
            with open(os.path.join(ruta_cocina, filename), "r", encoding="utf-8") as f:
                contenido = f.readlines()
            pedidos.append({
                "mesa": filename.split("_")[1],
                "pedido": contenido,
                "estado": "Pendiente"
            })
    return jsonify(pedidos)

# Ruta para obtener los pedidos de bar
@app.route("/pedidos_bar", methods=["GET"])
def pedidos_bar():
    pedidos = []
    # Leer los archivos de bebida en la carpeta de bar
    ruta_bar = "Pedidos/bar"
    for filename in os.listdir(ruta_bar):
        if filename.endswith("_bebida.txt"):
            with open(os.path.join(ruta_bar, filename), "r", encoding="utf-8") as f:
                contenido = f.readlines()
            pedidos.append({
                "mesa": filename.split("_")[1],
                "pedido": contenido,
                "estado": "Pendiente"
            })
    return jsonify(pedidos)

# Ruta para marcar los pedidos como "listos"
@app.route("/marcar_listo", methods=["POST"])
def marcar_listo():
    data = request.get_json()
    mesa = data.get("mesa")
    tipo = data.get("tipo")  # "comida" o "bebida"
    
    if not mesa or not tipo:
        return "Datos incompletos", 400

    # Actualizar el estado del pedido
    if tipo == "comida":
        ruta = f"Pedidos/cocina/mesa_{mesa}_comida.txt"
    elif tipo == "bebida":
        ruta = f"Pedidos/bar/mesa_{mesa}_bebida.txt"
    else:
        return "Tipo de pedido no válido", 400

    if not os.path.exists(ruta):
        return "Pedido no encontrado", 404
    
    # Actualizar el estado en el archivo (marcarlo como listo)
    with open(ruta, "a", encoding="utf-8") as f:
        f.write("\nEstado: Listo para llevar")
    
    return "✅ Pedido marcado como listo", 200
"""

# Ruta de los archivos HTML (cocina.html y bar.html)
cocina_html = "templates/cocina.html"
bar_html = "templates/bar.html"

# Código para ser insertado en las vistas de cocina y bar
cocina_table_code = """
<h2>Pedidos de Cocina</h2>
<table border="1">
    <thead>
        <tr>
            <th>Mesa</th>
            <th>Pedido</th>
            <th>Estado</th>
            <th>Acción</th>
        </tr>
    </thead>
    <tbody id="cocina-pedidos">
        <!-- Los pedidos de comida se cargarán aquí dinámicamente -->
    </tbody>
</table>
"""

bar_table_code = """
<h2>Pedidos de Bar</h2>
<table border="1">
    <thead>
        <tr>
            <th>Mesa</th>
            <th>Pedido</th>
            <th>Estado</th>
            <th>Acción</th>
        </tr>
    </thead>
    <tbody id="bar-pedidos">
        <!-- Los pedidos de bebida se cargarán aquí dinámicamente -->
    </tbody>
</table>
"""

# Código JavaScript para actualizar la interfaz con los pedidos
js_code = """
<script>
function cargarPedidos(tipo) {
    fetch('/pedidos_' + tipo)
        .then(response => response.json())
        .then(pedidos => {
            let tabla = tipo === 'cocina' ? document.getElementById('cocina-pedidos') : document.getElementById('bar-pedidos');
            tabla.innerHTML = '';
            pedidos.forEach(pedido => {
                let fila = document.createElement('tr');
                fila.innerHTML = `
                    <td>${pedido.mesa}</td>
                    <td>${pedido.pedido.join('<br>')}</td>
                    <td>${pedido.estado}</td>
                    <td><button onclick="marcarListo('${pedido.mesa}', '${tipo}')">Listo</button></td>
                `;
                tabla.appendChild(fila);
            });
        });
}

function marcarListo(mesa, tipo) {
    fetch('/marcar_listo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mesa: mesa, tipo: tipo })
    })
    .then(response => response.json())
    .then(data => {
        alert(data);
        cargarPedidos(tipo);  // Recargar los pedidos para actualizar el estado
    });
}

window.onload = function() {
    cargarPedidos('cocina');
    cargarPedidos('bar');
};
</script>
"""

# Modificar cocina.html
with open(cocina_html, "a", encoding="utf-8") as f:
    f.write(cocina_table_code + js_code)

# Modificar bar.html
with open(bar_html, "a", encoding="utf-8") as f:
    f.write(bar_table_code + js_code)

# Leer el archivo server.py
with open(server_file, "r", encoding="utf-8") as file:
    server_content = file.read()

# Verificar si el bloque de código ya existe en server.py
if "pedidos_cocina" not in server_content and "pedidos_bar" not in server_content:
    # Agregar el nuevo código para las rutas de cocina y bar
    server_content = server_content.replace(
        "if __name__ == '__main__':",
        new_code + "\n\nif __name__ == '__main__':"
    )

    # Escribir los cambios de vuelta a server.py
    with open(server_file, "w", encoding="utf-8") as file:
        file.write(server_content)

    print("✔️ El código de las rutas para cocina y bar ha sido agregado correctamente a server.py.")
else:
    print("🚫 Las rutas de cocina y bar ya existen en server.py.")
