#!/data/data/com.termux/files/usr/bin/bash
# █▓▒░ Hash Checker ░▒▓█
echo -e "\e[1;34m[+]\e[0m Verificación de hashes"
read -p "Archivo: " file
echo -e "\e[1;32mMD5:\e[0m    $(md5sum "$file" | cut -d ' ' -f1)"
echo -e "\e[1;32mSHA1:\e[0m   $(sha1sum "$file" | cut -d ' ' -f1)"
echo -e "\e[1;32mSHA256:\e[0m $(sha256sum "$file" | cut -d ' ' -f1)"
