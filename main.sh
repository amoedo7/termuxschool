#!/data/data/com.termux/files/usr/bin/bash
# Termux Hacker Toolkit - Menú Principal 🔥

SCRIPTS_DIR="./scripts"

function show_banner() {
    clear
    echo -e "\e[1;35m"
    echo "╔═══════════════════════════════╗"
    echo "║      🎓 TermSchool Menu       ║"
    echo "╚═══════════════════════════════╝"
    echo -e "\e[0m"
}

function list_scripts() {
    echo -e "\e[1;34m🧰 Herramientas disponibles:\e[0m"
    local i=1
    for script in "$SCRIPTS_DIR"/*.{sh,py}; do
        [[ -f "$script" ]] || continue
        script_name=$(basename "$script")
        ext="${script_name##*.}"
        case $ext in
            sh) icon="🖥️ " ;;
            py) icon="🐍" ;;
            *) icon="📄" ;;
        esac
        echo -e " [$i] $icon  $script_name"
        ((i++))
    done
    echo -e " [0] ❌ Salir"
}

function run_script_by_number() {
    mapfile -t scripts < <(find "$SCRIPTS_DIR" -type f \( -name "*.sh" -o -name "*.py" \) | sort)
    read -p $'\n🔢 Elige una herramienta: ' choice
    if [[ "$choice" == "0" ]]; then
        echo -e "\n👋 ¡Hasta luego, hacker!"
        exit 0
    fi
    if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#scripts[@]} )); then
        selected="${scripts[$((choice-1))]}"
        echo -e "\n🚀 Ejecutando: \e[1;33m$selected\e[0m"
        echo -e "\e[33m─────────────────────────────────────\e[0m"
        case "$selected" in
            *.sh) bash "$selected" ;;
            *.py) python "$selected" ;;
            *) echo "❌ Tipo de archivo desconocido." ;;
        esac
        echo -e "\e[33m─────────────────────────────────────\e[0m"
        read -p $'\n🔁 Presiona ENTER para volver al menú...' _
    else
        echo -e "\n❌ Opción inválida"
        sleep 1
    fi
}

# Bucle principal
while true; do
    show_banner
    list_scripts
    run_script_by_number
done
