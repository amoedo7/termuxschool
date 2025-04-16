import requests
from termcolor import cprint

host = input("URL objetivo (ej: http://192.168.1.1): ")
paths = ['admin', 'login', 'panel', 'control', 'manager']

for path in paths:
    url = f"{host}/{path}"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            cprint(f"[+] Panel encontrado: {url}", "green")
        else:
            cprint(f"[-] {url} ({r.status_code})", "yellow")
    except:
        cprint(f"[!] Error con {url}", "red")
