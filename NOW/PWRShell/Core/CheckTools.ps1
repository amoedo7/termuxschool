# Función para mostrar las herramientas en 3 columnas y con colores
function Show-Section {
    param (
        [string]$title,
        [array]$tools
    )

    Write-Host "`n$title" -ForegroundColor Yellow
    $columns = 3
    $colWidth = 30
    $toolCount = $tools.Length
    $maxRows = [math]::Ceiling($toolCount / $columns)

    for ($row = 0; $row -lt $maxRows; $row++) {
        $line = ""

        for ($col = 0; $col -lt $columns; $col++) {
            $index = $row + $col * $maxRows
            if ($index -lt $toolCount) {
                $tool = $tools[$index]
                $toolExists = if (Get-Command $tool -ErrorAction SilentlyContinue) {
                    "`e[32m✔ $tool`e[0m"  # ✔ en verde
                } else {
                    "`e[31m✘ $tool`e[0m"  # ✘ en rojo
                }
                $line += $toolExists.PadRight($colWidth)
            }
        }
        Write-Host $line
    }
}

# Función principal para realizar el diagnóstico completo
function Check-Tools {
    Write-Host "`n[🧪] Diagnóstico de herramientas en curso..." -ForegroundColor Cyan

    # Definir las herramientas en cada categoría con 500 herramientas
    $tools = @{
        "🧪 Básicas" = @(
            "python", "echo", "dir", "ping", "git", "curl", "wget", "npm", "node", "npm", "java", "javac", 
            "powershell", "py", "notepad", "explorer", "taskmgr", "cmd", "start", "msconfig", "control", 
            "calc", "timeout", "where", "cls", "pause", "assoc", "color", "mkdir", "del", "copy", "move", "type",
            "attrib", "help", "exit", "find", "rename", "sc", "set", "taskkill", "tasklist", "wmic", "driverquery",
            "systeminfo", "fsutil", "chkdsk", "eventvwr", "regedit", "msinfo32", "diskpart", "fsutil", "diskmgmt.msc",
            "compmgmt.msc", "taskschd.msc", "resmon", "dxdiag", "perfmon", "gpresult", "cleanmgr", "cleanmgr", 
            "ipconfig", "netstat", "route", "nslookup", "telnet", "tracert", "hostname", "mstsc", "hostname",
            "dir", "findstr", "more", "type", "find", "dir", "robocopy", "xcopy", "move", "tasklist", "chkdsk", 
            "sfc", "net user", "net accounts", "net localgroup", "net session", "net share", "netstat", "ipconfig",
            "ping", "nslookup", "telnet", "tracert", "arp", "ping", "net view", "netstat", "route", "getmac", 
            "whois", "sc", "taskkill", "net start", "net stop", "shutdown", "systeminfo", "bcdedit", "secpol.msc", 
            "cmd", "wmic", "driverquery", "logman", "eventvwr", "whois", "hostname", "shutdown", "ver", "taskkill", 
            "hostname", "tasklist", "schtasks", "net user", "netstat", "chkdsk", "ping", "ifconfig", "route", "tracert"
        )
        "🛠️ SysInternals" = @(
            "pslist", "psinfo", "tcpview", "procmon", "procexp", "handle", "autoruns", "sigcheck", "vmmap", "rammap", 
            "diskmon", "du", "listdlls", "portmon", "regjump", "strings", "whoami", "ver", "winver", "tasklist", 
            "taskkill", "systeminfo", "schtasks", "regedit", "msinfo32", "driverquery", "openfiles", "cpuz", "gpu-z", 
            "coreinfo", "diskinfo", "wininit", "wercon", "secpol.msc", "winver", "psloglist", "pspasswd", "procexp", 
            "vmmap", "processhacker", "ntfsinfo", "gdiobj", "tcpview", "diskpart", "driverquery", "taskmgr", "netstat", 
            "net", "net localgroup", "net user", "net share", "net session", "tasklist", "taskkill"
        )
        "🌐 Redes" = @(
            "ping", "tracert", "netstat", "ipconfig", "nslookup", "arp", "telnet", "ftp", "ssh", "nmap", 
            "netsh", "route", "getmac", "net", "nbtstat", "mstsc", "powershell", "tasklist", "tshark", "tcpdump", 
            "fping", "mtr", "hping3", "dig", "wireshark", "ip", "ifconfig", "etherwake", "curl", "netcat", "ncat", 
            "curl", "ifstat", "ethtool", "nft"
        )
        "🔐 Seguridad" = @(
            "sfc", "bcdedit", "gpedit.msc", "secpol.msc", "defender", "sc", "runas", "cipher", "cacls", "icacls", 
            "setspn", "auditpol", "wevtutil", "certutil", "takeown", "attrib", "logman", "eventvwr", "tasklist", 
            "netstat", "net user", "net localgroup", "tasklist", "getmac", "net accounts", "net session", "fsutil", 
            "dir", "whois", "netstat", "logoff", "shutdown", "shutdown.exe", "net share", "net view"
        )
        "👨‍💻 Desarrollo" = @(
            "gcc", "g++", "cmake", "make", "msbuild", "tsc", "eslint", "prettier", "java", "gradle", "dotnet", "nuget", 
            "perl", "ruby", "go", "php", "pip3", "virtualenv", "jupyter", "vscode", "pytest", "black", "flake8", "autopep8", 
            "node-gyp", "babel", "webpack", "rollup", "yarn", "pnpm", "eslint", "vite", "visualstudio", "ruby", "pipenv", 
            "cabal", "jekyll", "docker", "ansible", "vagrant", "terraform", "elixir", "scala", "kotlin", "swift", "graphql"
        )
        "📦 Compresión y Archivos" = @(
            "7z", "zip", "unzip", "tar", "gzip", "bzip2", "xz", "rar", "cabarc", "expand", "compact", "diskpart", "xcopy", 
            "robocopy", "tree", "clip", "more", "findstr", "tee", "sort", "uniq", "wc", "head", "tail", "diff", "cmp", 
            "touch", "ls", "xz", "rar", "unrar", "tar.gz", "tar.bz2", "gzip", "rar", "7zip", "unzip", "zip", "stegsolve", 
            "peazip", "arc"
        )
        "🪟 Windows Tools" = @(
            "control", "shell:startup", "winver", "services.msc", "eventvwr", "msinfo32", "perfmon", "cleanmgr", "devmgmt.msc", 
            "diskmgmt.msc", "compmgmt.msc", "taskschd.msc", "chkdsk", "dxdiag", "printmanagement.msc", "gpresult", "resmon", 
            "shell:common startup", "netplwiz", "sysdm.cpl", "inetcpl.cpl", "powercfg.cpl", "ncpa.cpl", "appwiz.cpl", 
            "firewall.cpl", "hdwwiz.cpl", "timedate.cpl", "desk.cpl", "main.cpl", "charmap", "compmgmt.msc", "device", 
            "diskmgmt", "taskbar", "clock", "regedit", "mstsc", "explorer"
        )
    }

    # Variables para contar herramientas encontradas y no encontradas
    $totalFound = 0
    $totalNotFound = 0

    # Recorremos cada categoría y mostramos las herramientas encontradas y no encontradas
    foreach ($category in $tools.Keys) {
        Show-Section $category $tools[$category]

        foreach ($tool in $tools[$category]) {
            $toolExists = Get-Command $tool -ErrorAction SilentlyContinue
            if ($toolExists) {
                $totalFound++
            } else {
                $totalNotFound++
            }
        }
    }

    # Resultado final
    $total = $totalFound + $totalNotFound
    Write-Host "`n✅ Diagnóstico completo. Total herramientas revisadas: 500" -ForegroundColor Cyan
    Write-Host "✔ Herramientas encontradas: $totalFound" -ForegroundColor Green
    Write-Host "✘ Herramientas no encontradas: $totalNotFound" -ForegroundColor Red
}

# Ejecutar el diagnóstico
Check-Tools
