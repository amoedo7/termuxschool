#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Keylogger Detector ░▒▓█
echo -e "\e[1;36m[+]\e[0m Escaneando por actividad de keyloggers..."
ps aux | grep -iE "logkeys|input|keylog|intercept|record" | grep -v grep
ls -alh /dev/input/
