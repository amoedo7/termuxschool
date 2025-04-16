#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Sensor Viewer ░▒▓█
echo -e "\e[1;36m[+]\e[0m Mostrando sensores activos..."
termux-sensor -s accelerometer,gyroscope,magnetic_field,proximity -n 5
