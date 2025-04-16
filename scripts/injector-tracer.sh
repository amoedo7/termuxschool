#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Inyecciones sospechosas ░▒▓█
echo -e "\e[1;31m[💉] Buscando inyecciones en scripts y cron...\e[0m"

grep -rEi 'eval|bash -c|`.+`|\$\(.*\)|base64 -d|nc -e|rm -rf /' "$HOME" /data/data/com.termux/files/usr/etc/cron* 2>/dev/null
