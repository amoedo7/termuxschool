import os
import subprocess
import time

def run_command(command):
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )
        output, error = process.communicate()
        
        if process.returncode == 0:
            if output:
                print(f"✅ {output}")
            return True
        else:
            print(f"❌ Error: {error}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def actualizar_git():
    print("\n🚀 Iniciando actualización de Git...\n")
    
    # Añadir todos los cambios
    print("📦 Añadiendo archivos modificados...")
    if not run_command("git add ."):
        return False
    
    # Obtener mensaje del commit
    mensaje = input("\n✏️ Ingresa el mensaje para el commit: ")
    if not mensaje:
        mensaje = "Update: " + time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Crear commit
    print("\n📝 Creando commit...")
    if not run_command(f'git commit -m "{mensaje}"'):
        return False
    
    # Subir cambios
    print("\n☁️ Subiendo cambios a GitHub...")
    if not run_command("git push origin main"):
        return False
    
    return True

def main():
    print("""
    ╔════════════════════════════╗
    ║     Actualizar ApostAmo    ║
    ╚════════════════════════════╝
    """)
    
    if actualizar_git():
        print("""
        ✨ ¡Actualización completada con éxito! ✨
        
        📱 Los cambios se desplegarán automáticamente en:
        🌐 https://apostamo.onrender.com/
        
        ⏳ El despliegue puede tardar unos minutos...
        """)
    else:
        print("""
        ❌ Hubo un error durante la actualización.
        👉 Por favor, revisa los mensajes de error anteriores.
        """)

if __name__ == "__main__":
    main() 