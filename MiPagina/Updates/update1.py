# update1.py
# -*- coding: utf-8 -*-
import os
import time
import sys
import io

# Forzar UTF-8 para salida en consola
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def crear_directorios():
    rutas = [
        "static", "templates", "Updates",
        "static/img", "static/css", "static/js",
        "templates/restaurantes", "templates/mesas", "templates/cocina"
    ]
    for ruta in rutas:
        os.makedirs(ruta, exist_ok=True)

def crear_index_html():
    contenido = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PidAmo</title>
</head>
<body>
    <h1>Bienvenido a PidAmo</h1>
    <p>Ingrese el número de mesa para continuar.</p>
</body>
</html>
"""
    with open("templates/index.html", "w", encoding="utf-8") as f:
        f.write(contenido)

def main():
    print("\n🧱 Generando estructura inicial de PidAmo...\n")
    crear_directorios()
    crear_index_html()
    print("✅ Directorios y archivo index.html generados correctamente.\n")

if __name__ == "__main__":
    inicio = time.time()
    try:
        main()
    except Exception as e:
        print("❌ Error:", e)
    duracion = round(time.time() - inicio, 2)
    print(f"⏱️ Duración: {duracion} segundos")
