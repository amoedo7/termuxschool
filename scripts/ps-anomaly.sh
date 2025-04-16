#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Ghost Process Hunter ░▒▓█

echo -e "\e[1;36m[☠️ ] Escaneando procesos sospechosos...\e[0m"

for pid in $(ls /proc | grep -E '^[0-9]+$'); do
    cmd=$(cat /proc/$pid/cmdline 2>/dev/null)
    if [[ -n "$cmd" && "$cmd" != */* ]]; then
        echo -e "\e[1;31m[!] PID $pid: Proceso sin ruta clara\e[0m -> $cmd"
    fi
done
