#!/data/data/com.termux/files/usr/bin/bash

clear

# 🎭 Estilo infernal
RED='\033[1;31m'
GRN='\033[1;32m'
YLW='\033[1;33m'
RST='\033[0m'

# 🎤 Voz de bienvenida
termux-tts-speak "Bienvenido al ritual de preparación para TermuxHell... Iniciando secuencia infernal"

# 🔥 Banner demoníaco
echo -e "${RED}
echo -e "\e[91m
████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗███████╗██╗     ██╗     
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║██║  ██║██╔════╝██║     ██║     
   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║███████║█████╗  ██║     ██║     
   ██║   ██╔══╝  ██╔═══╝ ██║╚██╔╝██║██║   ██║██╔══██║██╔══╝  ██║     ██║     
   ██║   ███████╗██║     ██║ ╚═╝ ██║╚██████╔╝██║  ██║███████╗███████╗███████╗
   ╚═╝   ╚══════╝╚═╝     ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
\e[0m"
${RST}"
sleep 1

echo -e "${YLW}🔧 Iniciando preparación del entorno Termux...${RST}"
sleep 1

# 🧪 Falsa barra de carga
function fake_loading() {
    for i in {1..20}; do
        echo -ne "${RED}["
        for j in $(seq 1 $i); do echo -ne "█"; done
        for k in $(seq $((20-i)) -1 1); do echo -ne " "; done
        echo -ne "] $((i*5))%\r"
        sleep 0.07
    done
    echo ""
}

fake_loading

echo -e "${GRN}✔ Sistema listo para actualizar e instalar paquetes...${RST}"
sleep 1

# 💥 Actualización del sistema
echo -e "${YLW}🔁 Actualizando paquetes del sistema...${RST}"
pkg update -y && pkg upgrade -y

# 🧰 Instalación infernal
echo -e "${YLW}📦 Instalando herramientas esenciales para el infierno...${RST}"
pkg install -y \
  curl \
  wget \
  git \
  jq \
  neofetch \
  termux-api \
  traceroute \
  python \
  tsu \
  nmap \
  net-tools \
  dnsutils \
  openssh \
  proot \
  man \
  figlet \
  toilet \
  ruby \
  perl \
  nano \
  vim \
  unzip \
  zip \
  coreutils \
  util-linux \
  cmatrix

# 🐍 PIP y librerías Python clave
echo -e "${YLW}🐍 Actualizando pip y librerías Python útiles...${RST}"
pip install --upgrade pip
pip install requests rich colorama psutil

# ✅ Confirmación
echo -e "${GRN}✔ Paquetes y librerías instalados correctamente.${RST}"

# 🎉 Final demoníaco
echo -e "${RED}
🔥 RITUAL COMPLETADO 🔥
El infierno está listo para ser invocado desde: ${GRN}./TermuxHell.sh${RED}

Prepárate para el caos...
${RST}"

# 🎤 Voz de cierre
termux-tts-speak "El infierno está listo. Ya puedes lanzar TermuxHell punto S H. Que empiece el caos"
