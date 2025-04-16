import os
from datetime import datetime

BASE_PATH = os.getcwd()
TEMPLATES = os.path.join(BASE_PATH, "templates")
STATIC = os.path.join(BASE_PATH, "static")

def crear_index():
    contenido = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PidAmo 🍽️</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="container">
        <h1>🍕 Bienvenido a <span class="marca">PidAmo</span></h1>
        <p>Ingrese su número de mesa para comenzar con el pedido:</p>
        <form action="/menu" method="get">
            <input type="number" name="mesa" placeholder="N° de mesa" required>
            <button type="submit">Entrar</button>
        </form>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
'''
    with open(os.path.join(TEMPLATES, "index.html"), "w", encoding="utf-8") as f:
        f.write(contenido)

def crear_plantilla(nombre, titulo):
    contenido = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{titulo} | PidAmo</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="container">
        <h1>{titulo}</h1>
        <p>Contenido de {nombre}. Personalizar aquí.</p>
        <a href="/">🔙 Volver al inicio</a>
    </div>
</body>
</html>
'''
    with open(os.path.join(TEMPLATES, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)

def crear_styles():
    contenido = '''body {
    font-family: "Segoe UI", sans-serif;
    background: #f8f8f8;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 500px;
    margin: 80px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: center;
}

h1 {
    color: #222;
    margin-bottom: 10px;
}

.marca {
    color: #e63946;
}

input[type="number"] {
    padding: 10px;
    font-size: 1rem;
    border: 2px solid #ddd;
    border-radius: 8px;
    width: 80%;
    margin-bottom: 15px;
}

button {
    padding: 10px 20px;
    font-size: 1rem;
    background: #457b9d;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease;
}

button:hover {
    background: #1d3557;
}

a {
    color: #457b9d;
    text-decoration: none;
}
'''
    with open(os.path.join(STATIC, "styles.css"), "w", encoding="utf-8") as f:
        f.write(contenido)

def crear_script():
    contenido = '''// script.js
console.log("🎉 PidAmo cargado correctamente.");
'''
    with open(os.path.join(STATIC, "script.js"), "w", encoding="utf-8") as f:
        f.write(contenido)

def asegurar_directorios():
    os.makedirs(TEMPLATES, exist_ok=True)
    os.makedirs(STATIC, exist_ok=True)

def main():
    log = ["===== update4.py ====="]
    log.append(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        asegurar_directorios()

        log.append("🎨 Creando archivos de interfaz...")
        crear_index()
        crear_plantilla("menu.html", "Menú del Restaurante")
        crear_plantilla("mozos.html", "Vista de Mozos")
        crear_plantilla("cocina.html", "Vista de Cocina")
        crear_plantilla("bebida.html", "Vista de Bebidas")
        crear_plantilla("Boss.html", "Panel del Dueño")
        crear_styles()
        crear_script()

        log.append("✅ Interfaz inicial creada con éxito.")
    except Exception as e:
        log.append("❌ ERROR:")
        log.append(str(e))

    log.append(f"⏱️ Duración: {round(0.1, 2)} segundos")
    log.append("\n")
    return "\n".join(log)

if __name__ == "__main__":
    print(main())
