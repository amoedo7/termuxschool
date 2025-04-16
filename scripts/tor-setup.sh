#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Tor Setup ░▒▓█
echo -e "\e[1;35m[*]\e[0m Iniciando Tor + ProxyChains..."

pkg install -y tor proxychains-ng
tor &

echo -e "\e[1;32m[+]\e[0m Probando conexión con proxychains..."
proxychains curl https://check.torproject.org/
