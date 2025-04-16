import os
import subprocess
import time
import sys
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init()

# Forzar UTF-8 para salida estándar (consola)
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UPDATES_DIR = "Updates"
LOG_FILE = "update_log.txt"
EXECUTED_TRACKER = "executed_updates.txt"

def get_last_log_entry(script_name):
    """Devuelve la última sección del log relacionada a un script específico."""
    if not os.path.exists(LOG_FILE):
        return ""

    with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as log:
        lines = log.readlines()

    start_marker = f"===== {script_name} ====="
    start_idx = None
    for i in range(len(lines)-1, -1, -1):
        if start_marker in lines[i]:
            start_idx = i
            break

    if start_idx is None:
        return "⚠️ No se encontró entrada en el log para este script."

    return "".join(lines[start_idx:]).strip()

def ensure_directories():
    if not os.path.exists(UPDATES_DIR):
        os.makedirs(UPDATES_DIR)
        print(f"📁 Carpeta '{UPDATES_DIR}' creada.")
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w", encoding="utf-8").close()

def log_message(message):
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as log:
        log.write((message or "") + "\n")

def already_executed(script):
    if not os.path.exists(EXECUTED_TRACKER):
        return False
    with open(EXECUTED_TRACKER, "r", encoding="utf-8") as file:
        return script in file.read().splitlines()

def mark_as_executed(script):
    with open(EXECUTED_TRACKER, "a", encoding="utf-8") as file:
        file.write(script + "\n")

def run_update(script):
    print(f"\n🛠️ Ejecutando {script}...")
    start_time = time.time()
    log_message(f"\n===== {script} =====")
    log_message(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        result = subprocess.run(
            ["python", f"{UPDATES_DIR}/{script}"],
            check=True,
            capture_output=True,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"}
        )
        stdout = result.stdout.decode("utf-8", errors="replace") if result.stdout else "Sin salida."
        log_message(stdout)
        print("✅ Finalizado correctamente")
        mark_as_executed(script)
    except subprocess.CalledProcessError as e:
        error_output = (
            (e.stderr.decode("utf-8", errors="replace") if e.stderr else "") +
            (e.stdout.decode("utf-8", errors="replace") if e.stdout else "")
        )
        log_message("❌ ERROR:\n" + error_output)
        print(f"{Fore.LIGHTRED_EX}❌ Falló la ejecución. Revisa el log.{Style.RESET_ALL}")
        print(f"\n{Fore.LIGHTBLUE_EX}{get_last_log_entry(script)}{Style.RESET_ALL}")
    finally:
        duration = round(time.time() - start_time, 2)
        log_message(f"⏱️ Duración: {duration} segundos\n")
        time.sleep(0.2)  # Pausa de 0.2 segundos entre actualizaciones

def get_update_number(script_name):
    """Devuelve el número de la actualización (por ejemplo, de 'update1.py' devuelve 1)."""
    try:
        return int(script_name[6:script_name.index('.py')])
    except ValueError:
        return float('inf')  # Para manejar casos donde el nombre no sea válido

def main():
    ensure_directories()

    updates = sorted(
        (f for f in os.listdir(UPDATES_DIR) if f.startswith("update") and f.endswith(".py")),
        key=get_update_number  # Ordenar por número extraído del nombre del archivo
    )

    if not updates:
        print("⚠️ No se encontraron scripts de actualización.")
        return

    print("\n🔧 Ejecutando updates de PidAmo...\n")

    for script in updates:
        if already_executed(script):
            print(f"🔁 {script} ya fue ejecutado. (omitido)")
            continue
        run_update(script)

    print("\n🧩 Todos los updates fueron procesados.\n📜 Log guardado en:", LOG_FILE)

if __name__ == "__main__":
    main()
