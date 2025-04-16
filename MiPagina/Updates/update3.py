import os
from datetime import datetime

def generar_server_py():
    contenido = '''from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

# Aquí podés ir sumando más rutas como /menu, /mozos, etc.

if __name__ == "__main__":
    app.run(debug=True)
'''

    ruta = os.path.join(os.getcwd(), "Server.py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta

def main():
    log = ["===== update3.py ====="]
    log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

    try:
        log.append("Generando archivo Server.py para iniciar PidAmo...")
        ruta = generar_server_py()
        log.append(f"Server.py creado en: {ruta}")
    except Exception as e:
        log.append("ERROR:")
        log.append(str(e))

    log.append(f"Duración estimada: {round(0.1, 2)} segundos")
    log.append("\n")
    return "\n".join(log)

if __name__ == "__main__":
    print(main())
