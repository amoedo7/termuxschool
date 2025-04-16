import os

templates_dir = "templates"
static_dir = "static"

# 1. HTML con menú básico y lógica para carrito
menu_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Menú de PidAmo</title>
    <link rel="stylesheet" href="/static/styles.css">
    <script defer src="/static/script.js"></script>
</head>
<body>
    <h1>🍽️ Menú de PidAmo</h1>
    <p>Mesa: <span id="mesa-id"></span></p>

    <div id="menu">
        <div class="item" data-nombre="Pizza" data-precio="2000" data-tipo="comida">🍕 Pizza - $2000</div>
        <div class="item" data-nombre="Hamburguesa" data-precio="1500" data-tipo="comida">🍔 Hamburguesa - $1500</div>
        <div class="item" data-nombre="Fernet" data-precio="1200" data-tipo="bebida">🥃 Fernet - $1200</div>
        <div class="item" data-nombre="Gaseosa" data-precio="800" data-tipo="bebida">🥤 Gaseosa - $800</div>
        <div class="item" data-nombre="Cerveza" data-precio="1000" data-tipo="bebida">🍺 Cerveza - $1000</div>
    </div>

    <h2>🛒 Carrito</h2>
    <ul id="carrito"></ul>
    <p>Total: $<span id="total">0</span></p>
    <button onclick="finalizarPedido()">✅ Pagar</button>
</body>
</html>
"""

# 2. JS que maneja el carrito
script_js = """
const carrito = [];
const totalSpan = document.getElementById("total");
const carritoUl = document.getElementById("carrito");
const mesaIdSpan = document.getElementById("mesa-id");

// Mostrar número de mesa
const mesaId = new URLSearchParams(window.location.search).get("mesa");
mesaIdSpan.textContent = mesaId || "Desconocida";

document.querySelectorAll(".item").forEach(item => {
    item.addEventListener("click", () => {
        const nombre = item.dataset.nombre;
        const precio = parseInt(item.dataset.precio);
        const tipo = item.dataset.tipo;

        carrito.push({ nombre, precio, tipo });
        actualizarCarrito();
    });
});

function actualizarCarrito() {
    carritoUl.innerHTML = "";
    let total = 0;

    carrito.forEach((item, index) => {
        const li = document.createElement("li");
        li.textContent = `${item.nombre} - $${item.precio}`;
        carritoUl.appendChild(li);
        total += item.precio;
    });

    totalSpan.textContent = total;
}

function finalizarPedido() {
    if (carrito.length === 0) return alert("Carrito vacío.");

    fetch("/enviar_pedido", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mesa: mesaId, pedido: carrito })
    })
    .then(res => res.ok ? alert("✅ Pedido enviado!") : alert("❌ Error al enviar pedido"))
    .then(() => location.reload());
}
"""

# 3. CSS básico para estilo amigable
styles_css = """
body {
    font-family: sans-serif;
    padding: 20px;
    background-color: #f8f8f8;
}
h1, h2 {
    color: #444;
}
#menu {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
}
.item {
    background-color: #fff;
    border: 2px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    cursor: pointer;
    text-align: center;
    font-size: 1.1em;
}
.item:hover {
    background-color: #e0ffe0;
}
#carrito {
    margin-top: 10px;
    padding-left: 20px;
}
button {
    margin-top: 10px;
    padding: 10px 20px;
    font-size: 1em;
    border: none;
    border-radius: 8px;
    background-color: green;
    color: white;
    cursor: pointer;
}
button:hover {
    background-color: darkgreen;
}
"""

# 4. Crear archivos necesarios
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

with open(os.path.join(templates_dir, "menu.html"), "w", encoding="utf-8") as f:
    f.write(menu_html.strip())

with open(os.path.join(static_dir, "script.js"), "w", encoding="utf-8") as f:
    f.write(script_js.strip())

with open(os.path.join(static_dir, "styles.css"), "w", encoding="utf-8") as f:
    f.write(styles_css.strip())

print("✅ Menú creado correctamente.")
