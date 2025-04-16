#!/data/data/com.termux/files/usr/bin/bash
# Instalador automático para Termux Hacker Toolkit 🐍

# Lista de paquetes necesarios
PAQUETES=(
  python
  termux-api
  nmap
  jq
  whois
  tsu
  net-tools
  inetutils
  dnsutils
  coreutils
  grep
  curl
  git
)

echo -e "\n🛠️  [Instalador] Iniciando instalación de dependencias para Termux Hacker Toolkit...\n"
sleep 1

# Actualización inicial
echo "🔄 Actualizando repositorios..."
pkg update -y && pkg upgrade -y
echo -e "✅ Repositorios actualizados\n"

# Instalación de paquetes
echo "📦 Comprobando e instalando paquetes del sistema..."

for paquete in "${PAQUETES[@]}"; do
    if command -v "$paquete" >/dev/null 2>&1; then
        echo -e "✅ $paquete ya está instalado"
    else
        echo -ne "🧩 Instalando $paquete... "
        pkg install -y "$paquete" >/dev/null 2>&1 && echo -e "✅ Hecho" || echo -e "❌ Error"
    fi
    sleep 0.2
done

# Requisitos de Python
echo -e "\n🐍 Instalando librerías Python requeridas..."
pip install --upgrade pip
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
    echo "✅ Librerías Python instaladas desde requirements.txt"
else
    echo "⚠️  No se encontró el archivo requirements.txt"
fi

# Mensaje final
echo -e "\n🎉 ¡Todo listo!"
echo "🚀 Ya podés correr tus herramientas. Ejemplo:"
echo "   ./whois-lookup.py google.com"
echo -e "\n📱 Recordá que algunas herramientas necesitan acceso a Termux API."
echo "   Activalo con: termux-change-repo y asegurate de tener Termux:API instalado desde F-Droid."
