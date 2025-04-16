# 🛡️ Termux Hacker Toolkit

Conjunto de herramientas de seguridad, análisis forense y monitoreo de red para Android (Termux). Pensado para usuarios con o sin root.

## 📦 Instalación

```bash
curl -O https://tu-url.com/Termux-Hacker-Pack.zip
unzip Termux-Hacker-Pack.zip
cd Termux-Hacker-Pack
pip install -r requirements.txt
chmod +x scripts/*.sh scripts/*.py
⚙️ Post-Instalación Recomendada
bash
Copiar
Editar
chmod +x scripts/whois-lookup.py
chmod +x keylogger-detector.sh
chmod +x find-hidden-files.sh
chmod +x backdoor-scanner.sh
chmod +x net-connections.sh
🔎 Comandos útiles
bash
Copiar
Editar
# Whois
python scripts/whois-lookup.py google.com
python scripts/whois-lookup.py --wifi  # analiza IPs de redes detectadas antes

# Escaneo de archivos ocultos
./find-hidden-files.sh --fast   # rápido
./find-hidden-files.sh --deep   # completo

# Conexiones de red
./net-connections.sh            # modo vivo
./net-connections.sh --bg       # segundo plano
🧰 Herramientas Incluidas
Herramienta	Función principal
✅ net-info.sh	Info básica de red (IP local, Gateway, MAC...)
✅ port-scan.sh	Escaneo de puertos abiertos
✅ wifi-scan.sh	Escaneo de redes WiFi cercanas
✅ whois-lookup.py	Dueño de IPs o dominios
✅ proc-monitor.sh	Monitoreo de procesos sospechosos (tcpdump, logkeys, etc.)
✅ keylogger-detector.sh	Detección de keyloggers y módulos raros
✅ find-hidden-files.sh	Archivos sospechosos: .bak, .log, .old, ocultos
✅ backdoor-scanner.sh	Detección de posibles backdoors activos
✅ net-connections.sh	Conexiones salientes/entrantes con análisis
✅ sys-info.sh	Información del sistema
✅ all-root-termux.sh	Gestión de privilegios: Root, FakeRoot, Mortal
✅ report-gen.sh	Generador de informes forenses en HTML con módulos combinados
📄 Generación de Reportes
bash
Copiar
Editar
./report-gen.sh
Genera automáticamente un archivo .html con:

Usuarios sospechosos activos

Procesos inusuales

Conexiones abiertas

IPs externas con whois

Archivos ocultos

...y más

Se abre automáticamente al finalizar (si termux tiene permisos).

📂 Estructura del Proyecto
pgsql
Copiar
Editar
Termux-Hacker-Pack/
│
├── scripts/
│   ├── net-info.sh
│   ├── port-scan.sh
│   ├── wifi-scan.sh
│   ├── whois-lookup.py
│   ├── proc-monitor.sh
│   ├── keylogger-detector.sh
│   ├── find-hidden-files.sh
│   ├── backdoor-scanner.sh
│   ├── net-connections.sh
│   ├── sys-info.sh
│   ├── all-root-termux.sh
│   └── report-gen.sh
│
├── estructura.txt
├── requirements.txt
└── README.md
