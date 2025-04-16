#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Deep Malware Analysis ░▒▓█
target="$1"

if [[ -z "$target" ]]; then
    echo -e "\e[1;31m[✘]\e[0m Uso: $0 <archivo o directorio>"
    exit 1
fi

echo -e "\e[1;35m[⚡] Análisis de bajo nivel:\e[0m $target"
find "$target" -type f | while read -r file; do
    echo -e "\n\033[1;34m[»]\033[0m $file"
    strings "$file" | grep -Ei 'bash|/bin/sh|nc|wget|curl|chmod|/dev/tcp|keylog|fork|while|eval|exec|base64' --color=always
    readelf -h "$file" 2>/dev/null | grep "Type:\|Machine:" || echo "No ELF headers"
done
