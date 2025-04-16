#!/usr/bin/env python3
import os
import subprocess
import argparse
import time

RED = '\033[1;31m'
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
MAGENTA = '\033[1;35m'
RESET = '\033[0m'

def banner():
    print(f"{MAGENTA}🌍 WHOIS Lookup Tool — TermuxSchool Edition{RESET}")
    print(f"{CYAN}By: El3imm    |    DeepNet Reconnaissance Mode{RESET}")
    print("-" * 50)

def loading_animation(text="🔍 Consultando WHOIS"):
    print(f"{GREEN}{text}", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print(RESET)

def whois_lookup(target):
    try:
        loading_animation(f"📡 Consultando {target}")
        result = subprocess.check_output(["whois", target], stderr=subprocess.DEVNULL).decode()
        print(f"\n{CYAN}📃 Resultado para {target}:{RESET}\n")
        print(result)
        print(f"\n{GREEN}✅ Consulta completada.{RESET}\n")
    except subprocess.CalledProcessError:
        print(f"{RED}❌ Error al consultar {target}. Puede que no exista o no tengas conexión.{RESET}")

def get_wifi_ips():
    try:
        output = subprocess.check_output(["termux-wifi-scaninfo"]).decode()
        ips = set()
        for line in output.splitlines():
            if "bssid" in line.lower():
                ip = line.split(":")[-1].strip().replace('"','').replace(',', '')
                if ip.count(":") == 5 or ip.count(":") == 0:
                    continue
                ips.add(ip)
        return list(ips)
    except Exception:
        return []

def main():
    banner()
    parser = argparse.ArgumentParser(description="🌍 WHOIS Lookup Tool")
    parser.add_argument("target", nargs="?", help="Dominio o IP a consultar")
    parser.add_argument("--wifi", action="store_true", help="Usar IPs detectadas por wifi-scan")
    args = parser.parse_args()

    if args.wifi:
        ips = get_wifi_ips()
        if not ips:
            print(f"{RED}❌ No se detectaron IPs desde wifi-scan.sh{RESET}")
            return
        for ip in ips:
            whois_lookup(ip)
    elif args.target:
        whois_lookup(args.target)
    else:
        print(f"{RED}❗ Debes indicar un dominio/IP o usar --wifi para detectar desde redes.\nEjemplo: python whois-lookup.py google.com{RESET}")

if __name__ == "__main__":
    main()
