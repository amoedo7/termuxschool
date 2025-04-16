#!/data/data/com.termux/files/usr/bin/bash

clear
termux-tts-speak "Cargando TermuxHell, la prueba definitiva del Infierno Portátil"

echo -e "\e[91m🔥 Bienvenidos al Infierno Portátil de El3imm 🔥\e[0m"
echo -e "\e[93m\"Dicen que Termux es absurdo... veamos qué tan equivocados están.\"\e[0m"
sleep 3

echo -e "\n🎤 VOZ EN OFF:"
termux-tts-speak "Tus compañeros se rieron, dijeron que esto era una tontería. Hoy, demostrarás lo contrario."

# 🧠 Diagnóstico del sistema
echo -e "\n🧠 Análisis del sistema operativo y hardware...\n"
termux-tts-speak "Escaneando sistema... procesador, RAM, distribución"

if ! command -v neofetch &>/dev/null; then
    echo "📦 Instalando neofetch..."
    pkg install neofetch -y
fi

neofetch --stdout | tee /tmp/neoinfo.txt
sleep 1

# 🎙️ Interpretar parte del neofetch
MODEL=$(grep 'Model:' /tmp/neoinfo.txt | cut -d: -f2)
termux-tts-speak "Modelo detectado: $MODEL"
sleep 1

# 🧪 Diagnóstico de red
echo -e "\n🌐 Analizando red...\n"
termux-tts-speak "Escaneando la conexión a internet..."

IP_LOCAL=$(ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
IP_PUBLICA=$(curl -s https://ipinfo.io/ip)

echo "📍 IP Local: $IP_LOCAL"
echo "🌍 IP Pública: $IP_PUBLICA"
termux-tts-speak "Tu IP local es $IP_LOCAL. Tu IP pública es $IP_PUBLICA."

# 🧑‍🏫 Perfil del estudiante
echo -e "\n📚 Perfil del Estudiante"
termux-tts-speak "Veamos qué tiene instalado este aprendiz de TermSchool"

tools=(nmap curl python php nodejs git jq termux-api net-tools)
for tool in "${tools[@]}"; do
    if command -v $tool &>/dev/null; then
        echo -e "✅ $tool: Instalado"
    else
        echo -e "❌ $tool: No encontrado"
        termux-tts-speak "$tool no encontrado. No pasarás al siguiente nivel sin él."
    fi
done

# 📡 Escaneo de red básico
echo -e "\n📡 Escaneo básico de red (nmap -F)"
termux-tts-speak "Ejecutando escaneo rápido de puertos..."
nmap -F "$IP_LOCAL"/24 || echo "⚠️ Nmap falló o no tiene permisos"

# 🛣️ Traceroute básico
echo -e "\n🛣️ Trazando ruta hasta Google"
termux-tts-speak "Trazando ruta hasta los servidores de Google..."
traceroute google.com || echo "⚠️ traceroute no disponible"

# 🚨 Activando MODO INFIERNO
echo -e "\n🔥 Activando Modo Infierno Digital..."
termux-tts-speak "Ahora comienza el infierno digital. Te advierto, esto no es un juego."

sleep 2
echo -e "💀 Ejecutando simulación de sigilo..."
termux-tts-speak "Modo sigilo activo. No dejarás huellas. Esto... si sabes lo que estás haciendo."

# 🐍 Simulación de sniffer
for i in {1..5}; do
    echo "[+] Paquete interceptado desde 192.168.0.$((RANDOM%255))"
    sleep 0.4
done
termux-tts-speak "Captura de paquetes simulada completada. No todo es lo que parece."

# ⚔️ Consejo Final
echo -e "\n🎓 Consejo final:"
echo "1. Nunca subestimes una terminal, ni siquiera en Android."
echo "2. Termux puede no tener root, pero sí cerebro."
echo "3. Aprende a moverte sin ser visto, sin pedir permiso."

termux-tts-speak "Consejo final. No subestimes la terminal. Termux es para quienes piensan."

# 👋 Despedida épica
echo -e "\n👋 Finalizando TermuxHell..."
termux-tts-speak "Misión cumplida. El infierno fue superado. Ahora ve y haz que se traguen sus palabras."

echo -e "\n🧠 TermuxHell cerrado. Tu reputación fue restaurada. Ahora... ¡que hablen ellos!"

