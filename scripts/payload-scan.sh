#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Payload Hunter ░▒▓█
echo -e "\e[1;35m[*]\e[0m Buscando payloads conocidos..."
read -p "Ruta del script o carpeta: " path
grep -REi "nc -e|bash -i|python -c|/dev/tcp|exec \| sh" "$path"
