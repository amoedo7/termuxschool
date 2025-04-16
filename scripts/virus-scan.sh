#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Virus Scan - Termux Style ░▒▓█
echo -e "\e[1;32m[+]\e[0m Iniciando escaneo antivirus..."
read -p "Ruta del archivo o directorio: " target

if command -v clamscan &> /dev/null; then
    clamscan -r "$target"
else
    echo -e "\e[1;33m[!]\e[0m ClamAV no encontrado, usando escaneo básico por strings..."
    grep -iEr 'hack|trojan|keylog|malware|virus|shellshock|rootkit' "$target"
fi
