import os
import shutil

# Archivos y carpetas que no deben eliminarse
excluir = {"ELAMO.py", "ReNew.py", "Updates"}

# Obtener el path actual
directorio_actual = os.getcwd()

for item in os.listdir(directorio_actual):
    if item in excluir:
        print(f"🛡️ Protegido: {item}")
        continue

    ruta_completa = os.path.join(directorio_actual, item)

    try:
        if os.path.isdir(ruta_completa):
            shutil.rmtree(ruta_completa)
            print(f"🧹 Carpeta eliminada: {item}")
        else:
            os.remove(ruta_completa)
            print(f"🧹 Archivo eliminado: {item}")
    except Exception as e:
        print(f"❌ Error eliminando {item}: {e}")

print("\n🧼 Limpieza completada. Solo quedan los archivos esenciales.")
