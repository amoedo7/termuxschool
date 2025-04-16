# update2.py
# -*- coding: utf-8 -*-
import os
import sys
import io
import time

# Forzar UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def migrar_powershell_a_python():
    templates = [
        ("script.js", "console.log('JS listo para funcionar');"),
        ("styles.css", "body { font-family: sans-serif; background: #f0f0f0; }")
    ]
    for nombre, contenido in templates:
        ruta = os.path.join("static/js" if nombre.endswith(".js") else "static/css", nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)

def main():
    print("➡️ Update2: Migrando scripts PowerShell a Python y asegurando estructura\n")
    migrar_powershell_a_python()
    print("✅ Migración completada con éxito.\n")

if __name__ == "__main__":
    inicio = time.time()
    try:
        main()
    except Exception as e:
        print("❌ Error:", e)
    duracion = round(time.time() - inicio, 2)
    print(f"⏱️ Duración: {duracion} segundos")
