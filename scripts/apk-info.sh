#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ APK Analyzer ░▒▓█
echo -e "\e[1;36m[+]\e[0m Análisis de APK"
read -p "Ruta del APK: " apk

if command -v aapt &> /dev/null; then
    aapt dump badging "$apk"
else
    echo -e "\e[1;31m[-]\e[0m 'aapt' no está instalado. Ejecuta: pkg install aapt"
fi
