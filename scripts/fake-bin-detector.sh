#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Bin Imposter Scanner ░▒▓█
echo -e "\e[1;33m[🕵️‍♂️] Buscando binarios modificados...\e[0m"

for bin in ls cat ps ping top netstat; do
    path=$(which $bin)
    hash=$(sha256sum "$path" | cut -d ' ' -f1)
    echo "$bin: $path → $hash"
done
