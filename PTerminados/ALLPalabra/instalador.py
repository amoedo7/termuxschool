import os
import subprocess
import sys
import shutil

# Paquetes necesarios
REQUIREMENTS = [
    "requests",
    "pycryptodome",
    "ecdsa",
    "base58"
]

# Carpetas y archivos base
SCRIPTS_DIR = "Scanners"
SCRIPTS = {
    "BTCScan.py": "print('BTCScan listo!')",
    "ETHScan.py": "print('ETHScan listo!')",
    "BNBScan.py": "print('BNBScan listo!')",
    "DashScan.py": "print('DashScan listo!')",
    "DogeScan.py": "print('DogeScan listo!')",
    "BCHScan.py": "print('BCHScan listo!')"
}

def instalar_paquetes():
    print("📦 Instalando paquetes necesarios...")
    for pkg in REQUIREMENTS:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print(f"✅ {pkg} instalado correctamente.")
        except subprocess.CalledProcessError:
            print(f"❌ Error al instalar {pkg}")

def crear_directorio():
    print(f"📁 Verificando carpeta '{SCRIPTS_DIR}'...")
    if not os.path.exists(SCRIPTS_DIR):
        os.makedirs(SCRIPTS_DIR)
        print(f"✅ Carpeta creada: {SCRIPTS_DIR}")
    else:
        print(f"📂 Carpeta ya existe.")

def generar_scripts():
    print("🧾 Generando scripts...")
    for nombre, contenido in SCRIPTS.items():
        path = os.path.join(SCRIPTS_DIR, nombre)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(contenido)
            print(f"✅ {nombre} generado.")
        else:
            print(f"📌 {nombre} ya existe.")

def main():
    print("🚀 Iniciando instalación completa...\n")
    instalar_paquetes()
    crear_directorio()
    generar_scripts()
    print("\n🎉 Instalación completa. Todo está listo para usar.")

if __name__ == "__main__":
    main()
