#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Hidden Process Detector ░▒▓█
echo -e "\e[1;33m[*]\e[0m Buscando procesos sospechosos..."
ps -A -o user,pid,cmd | grep -vE "root|system" | grep -iE "su|nc|ssh|keylog|recon|inject|dump|scan"
