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
                $exists = Get-Command $tool -ErrorAction SilentlyContinue
                if ($exists) {
                    $status = "`e[32m✔ $tool`e[0m"
                } else {
                    $status = "`e[31m✘ $tool`e[0m"
                }
                $line += $status.PadRight($colWidth)
            }
        }
        Write-Host $line
    }
}

# Función principal para realizar el diagnóstico completo
function Check-Tools {
    $totalFound = 0
    $totalNotFound = 0
    $categoryStats = @{ }

    foreach ($category in $tools.Keys) {
        $found = 0
        $notFound = 0

        foreach ($tool in $tools[$category]) {
            if (Get-Command $tool -ErrorAction SilentlyContinue) {
                $found++
                $totalFound++
            } else {
                $notFound++
                $totalNotFound++
            }
        }

        # Guardar las estadísticas por categoría
        $categoryStats[$category] = @{
            Found = $found
            NotFound = $notFound
            Total = $found + $notFound
        }
    }

    # Mostrar estadísticas por categoría
    Write-Host "`n📊 Resumen por categoría:`n" -ForegroundColor Yellow
    "{0,-20} {1,10} {2,12} {3,10}" -f "Categoría", "Encontradas", "No Encontradas", "Total"
    Write-Host ("-"*56)

    foreach ($category in $categoryStats.Keys) {
        $data = $categoryStats[$category]
        "{0,-20} {1,10} {2,12} {3,10}" -f $category, $data.Found, $data.NotFound, $data.Total
    }

    # Mostrar resumen total
    $total = $totalFound + $totalNotFound
    Write-Host "`n✅ Diagnóstico completo. Total herramientas revisadas: $total" -ForegroundColor Cyan
    Write-Host "✔ Herramientas encontradas: $totalFound" -ForegroundColor Green
    Write-Host "✘ Herramientas no encontradas: $totalNotFound" -ForegroundColor Red
}

# Diccionario de categorías y herramientas
$tools = @{
    "🧪 Básicas" = @(
        "python", "echo", "dir", "ping", "git", "curl", "wget", "npm", "node", "java", "javac", "powershell", "notepad",
        "explorer", "taskmgr", "cmd", "start", "msconfig", "control", "calc", "timeout", "where", "cls", "pause",
        "assoc", "color", "mkdir", "del", "copy", "move", "type", "attrib", "help", "exit", "find", "rename", "sc",
        "set", "taskkill", "tasklist", "wmic", "driverquery", "systeminfo", "fsutil", "chkdsk", "eventvwr", "regedit",
        "msinfo32", "diskpart", "diskmgmt.msc", "compmgmt.msc", "taskschd.msc", "resmon", "dxdiag", "perfmon",
        "gpresult", "cleanmgr", "ipconfig", "netstat", "route", "nslookup", "telnet", "tracert", "hostname", "findstr",
        "more", "robocopy", "xcopy", "sfc", "net user", "net accounts", "net localgroup", "net session", "net share",
        "arp", "getmac", "whois", "net start", "net stop", "shutdown", "bcdedit", "secpol.msc", "logman", "schtasks",
        "ifconfig", "more.com", "assoc.exe", "cacls.exe", "choice", "clip", "comp", "cmdkey", "convert", "debug",
        "diskcopy", "doskey", "fc", "find.exe", "finger", "format", "hostname.exe", "label", "mode", "replace",
        "sort.exe", "subst", "time", "tree", "tzutil", "verifier"
    )
    "🛠️ SysInternals" = @(
        "pslist", "psinfo", "tcpview", "procmon", "procexp", "handle", "autoruns", "sigcheck", "vmmap", "rammap",
        "diskmon", "du", "listdlls", "portmon", "regjump", "strings", "whoami", "ver", "openfiles", "cpuz", "gpu-z",
        "coreinfo", "diskinfo", "wininit", "wercon", "psloglist", "pspasswd", "processhacker", "ntfsinfo", "gdiobj",
        "bginfo", "accesschk", "accessenum", "adexplorer", "adinsight", "autologon", "clockres", "ctrl2cap",
        "desktops", "hex2dec", "junction", "ldmdump", "livekd", "notmyfault", "pendmoves"
    )
    "🌐 Redes" = @(
        "ping", "tracert", "netstat", "ipconfig", "nslookup", "arp", "telnet", "ftp", "ssh", "nmap", "netsh", "route",
        "getmac", "net", "nbtstat", "mstsc", "tshark", "tcpdump", "fping", "mtr", "hping3", "dig", "wireshark", "ip",
        "ifconfig", "etherwake", "netcat", "ncat", "ifstat", "ethtool", "nft", "curl.exe", "wget.exe", "httping",
        "iperf", "iperf3", "bmon", "vnstat", "arping", "wakeonlan", "mtr.exe", "ethtool.exe", "macchanger", "nbtscan",
        "reaver", "airmon-ng", "aircrack-ng", "hashcat", "wpscan", "dmitry", "sslscan"
    )
    "🔐 Seguridad" = @(
        "sfc", "bcdedit", "gpedit.msc", "secpol.msc", "defender", "sc", "runas", "cipher", "cacls", "icacls", "setspn",
        "auditpol", "wevtutil", "certutil", "takeown", "logman", "whois", "logoff", "shutdown.exe", "powershell -enc",
        "schtasks", "quser", "secedit", "auditpol.exe", "netsh advfirewall", "wevtutil.exe", "tasklist /v", "netstat -anbo",
        "whoami /groups", "whoami /priv", "sc qc", "netsh wlan show profiles", "cipher /w", "icacls /save", "get-acl",
        "set-acl", "wmic process", "runas /savecred", "mimikatz"
    )
    "👨‍💻 Desarrollo" = @(
        "gcc", "g++", "cmake", "make", "msbuild", "tsc", "eslint", "prettier", "gradle", "dotnet", "nuget", "perl",
        "ruby", "go", "php", "pip3", "virtualenv", "jupyter", "vscode", "pytest", "black", "flake8", "autopep8",
        "node-gyp", "babel", "webpack", "rollup", "yarn", "pnpm", "vite", "pipenv", "cabal", "jekyll", "docker",
        "ansible", "vagrant", "terraform", "elixir", "scala", "kotlin", "swift", "graphql", "py", "python3", "poetry",
        "pipx", "pyenv", "cmder", "shellcheck", "pre-commit", "tox", "bpython", "pylint", "mypy", "ipython",
        "jupyter-lab", "pydoc", "twine", "nuitka", "electron", "nx", "deno", "bun", "gfortran", "llvm", "gdb", "valgrind"
    )
    "📦 Compresión y Archivos" = @(
        "7z", "zip", "unzip", "tar", "gzip", "bzip2", "xz", "rar", "cabarc", "expand", "compact", "tree", "clip", "tee",
        "sort", "uniq", "wc", "head", "tail", "diff", "cmp", "touch", "ls", "stegsolve", "peazip", "arc", "unar", "lzma",
        "p7zip", "isoinfo", "cdrecord", "mkisofs", "split", "hxd", "binwalk", "foremost", "xxd", "dd", "hexdump",
        "cat", "file"
    )
    "🪟 Windows Tools" = @(
        "control", "shell:startup", "winver", "services.msc", "eventvwr", "msinfo32", "perfmon", "cleanmgr", "devmgmt.msc",
        "diskmgmt.msc", "compmgmt.msc", "taskschd.msc", "dxdiag", "printmanagement.msc", "gpresult", "resmon",
        "shell:common startup", "netplwiz", "sysdm.cpl", "inetcpl.cpl", "powercfg.cpl", "ncpa.cpl", "appwiz.cpl",
        "firewall.cpl", "hdwwiz.cpl", "timedate.cpl", "desk.cpl", "main.cpl", "charmap", "fsmgmt.msc", "lusrmgr.msc",
        "secpol.msc", "certmgr.msc", "dcomcnfg", "taskmgr.exe", "regedit.exe", "cmd.exe", "powershell_ise.exe",
        "printui.exe", "rstrui.exe", "comp", "syskey", "mstsc", "sigverif", "iscsicpl", "msdt", "msiexec", "cleanmgr.exe"
    )
}

  $totalFound = 0
    $totalNotFound = 0

    foreach ($category in $tools.Keys) {
        Show-Section $category $tools[$category]

        foreach ($tool in $tools[$category]) {
            if (Get-Command $tool -ErrorAction SilentlyContinue) {
                $totalFound++
            } else {
                $totalNotFound++
            }
        }
    

    $total = $totalFound + $totalNotFound
    Write-Host "`n✅ Diagnóstico completo. Total herramientas revisadas: $total" -ForegroundColor Cyan
    Write-Host "✔ Herramientas encontradas: $totalFound" -ForegroundColor Green
    Write-Host "✘ Herramientas no encontradas: $totalNotFound" -ForegroundColor Red
}

# Ejecutar el diagnóstico
Check-Tools
