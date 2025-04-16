#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Advanced Net Recon ░▒▓█
echo -e "\e[1;36m[+]\e[0m Escaneo avanzado de red..."
read -p "Subred objetivo (ej: 192.168.1.0/24): " subnet
pkg install nmap -y

echo -e "\e[1;32m[*]\e[0m Dispositivos detectados:"
nmap -sP "$subnet" -oG - | awk '/Up$/{print $2}' | tee /tmp/ips.txt

echo -e "\e[1;34m[*]\e[0m Fingerprinting:"
while read -r ip; do
    echo -e "\n\e[1;33m>> $ip\e[0m"
    nmap -O "$ip" | grep -E "OS details|Running|MAC"
done < /tmp/ips.txt
