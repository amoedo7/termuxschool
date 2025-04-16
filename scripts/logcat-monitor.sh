#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Logcat Live ░▒▓█
echo -e "\e[1;36m[+]\e[0m Monitoreando logs del sistema..."
logcat | grep -i --color "error\|denied\|permission\|keylog\|root"
