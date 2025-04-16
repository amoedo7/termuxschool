# WifiNow.ps1 - Versión PRO real
# Ejecutar como administrador para control total de WiFi

# == Inicialización segura del log ==
$basePath = "$env:USERPROFILE\WifiNow"
if (-not (Test-Path $basePath)) { New-Item -Path $basePath -ItemType Directory -Force | Out-Null }
$logPath = "$basePath\WifiNow.log"

function Log-Action($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $msg" | Out-File -Append -FilePath $logPath -Encoding UTF8
}

function Show-Banner {
    try {
        $test = [char]9556 # ╔
        Write-Host "`n╔═════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║        W I F I   N O W   (PRO)      ║" -ForegroundColor Cyan
        Write-Host "║ Usuario: $env:USERNAME    Hora: $(Get-Date -Format "HH:mm:ss")     ║" -ForegroundColor DarkCyan
        Write-Host "╚═════════════════════════════════════╝`n" -ForegroundColor Cyan
    } catch {
        Write-Host "`n=== WIFI NOW PRO ==="
        Write-Host "Usuario: $env:USERNAME"
        Write-Host "Hora: $(Get-Date -Format "HH:mm:ss")`n"
    }
}

function Check-Adapter {
    $adapter = netsh interface show interface | Where-Object { $_ -match "Wi-Fi" }
    if ($adapter -match "Deshabilitado" -or $adapter -match "Disabled") {
        Write-Host "[!] WiFi está apagado. Activando..." -ForegroundColor Yellow
        netsh interface set interface "Wi-Fi" enabled
        Start-Sleep 2
    }
}

function Show-CurrentConnection {
    $info = netsh wlan show interfaces
    if ($info -match "SSID\s+:\s+(\S.+)") {
        $ssid = $matches[1]
        if ($info -match "Signal\s+:\s+(\d+)%") {
            $signal = [int]$matches[1]
            $color = if ($signal -ge 80) { "Green" } elseif ($signal -ge 50) { "Yellow" } else { "Red" }
            Write-Host "[+] Conectado a: $ssid ($signal`%)" -ForegroundColor $color
        }
    } else {
        Write-Host "[-] No estás conectado a ninguna red." -ForegroundColor Red
    }
}

function List-Networks {
    Write-Host "[*] Buscando redes cercanas..." -ForegroundColor Cyan
    $output = netsh wlan show networks mode=bssid 2>&1

    if ($output -match "permiso de ubicación") {
        Write-Host "[!] Windows requiere permisos de ubicación para ver redes cercanas." -ForegroundColor Yellow
        Write-Host "    Abrí esta dirección: ms-settings:privacy-location" -ForegroundColor Gray
        Start-Sleep 2
        return
    }

    $networks = ($output | Select-String "SSID\s+\d+\s+:\s+(.*)").Matches | ForEach-Object { $_.Groups[1].Value }
    if ($networks.Count -eq 0) {
        Write-Host "[-] No se detectaron redes WiFi." -ForegroundColor Red
    } else {
        $i = 1
        foreach ($n in $networks | Sort-Object -Unique) {
            Write-Host "  $i. Nombre de la red (SSID): $n" -ForegroundColor Green
            $i++
        }
    }
}

function Export-Profiles {
    $path = "$basePath\Profiles"
    mkdir $path -Force | Out-Null
    $result = netsh wlan export profile folder="$path" key=clear 2>&1
    $count = ($result | Select-String "guardado en el archivo").Count
    Write-Host "[+] $count perfiles exportados a:" -ForegroundColor Green
    Write-Host "    $path" -ForegroundColor Gray
    Invoke-Item $path
    Log-Action "Perfiles exportados ($count)"
}

function Secure-Input($prompt) {
    Write-Host $prompt -NoNewline
    $securePass = Read-Host -AsSecureString
    return [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePass))
}

function Connect-Network {
    param ($SSID, $Password)
    $ProfileXml = @"
<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>$SSID</name>
    <SSIDConfig><SSID><name>$SSID</name></SSID></SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM><security>
        <authEncryption>
            <authentication>WPA2PSK</authentication>
            <encryption>AES</encryption>
            <useOneX>false</useOneX>
        </authEncryption>
        <sharedKey>
            <keyType>passPhrase</keyType>
            <protected>false</protected>
            <keyMaterial>$Password</keyMaterial>
        </sharedKey>
    </security></MSM>
</WLANProfile>
"@
    $file = "$env:TEMP\$SSID.xml"
    $ProfileXml | Out-File -Encoding UTF8 -FilePath $file
    netsh wlan add profile filename="$file" > $null
    netsh wlan connect name="$SSID"
    Write-Host "[*] Conectando a $SSID..." -ForegroundColor Yellow
    Start-Sleep 5
    Show-CurrentConnection
    Log-Action "Conexión intentada a '$SSID'"
}

function Disconnect-Wifi {
    Write-Host "[*] Desconectando Wi-Fi..." -ForegroundColor Gray
    netsh wlan disconnect
    Log-Action "Desconectado"
}

# ========== MAIN LOOP ==========

while ($true) {
    Show-Banner
    Check-Adapter
    Show-CurrentConnection

    Write-Host "`nMenú:"
    Write-Host "1. Ver redes disponibles"
    Write-Host "2. Conectarse a una red"
    Write-Host "3. Desconectarse"
    Write-Host "4. Exportar perfiles Wi-Fi"
    Write-Host "5. Salir"

    $choice = Read-Host "`n>>"

    switch ($choice) {
        "1" { List-Networks; Pause }
        "2" {
            $ssid = Read-Host "Nombre de la red (SSID)"
            $pass = Secure-Input "Contraseña: "
            Connect-Network -SSID $ssid -Password $pass
            Pause
        }
        "3" { Disconnect-Wifi; Pause }
        "4" { Export-Profiles; Pause }
        "5" { break }
        default { Write-Host "[!] Opción inválida" -ForegroundColor Red; Pause }
    }
}
