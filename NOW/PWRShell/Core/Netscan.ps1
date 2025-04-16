param (
    [string]$Modo = "seguro"
)

# Función para mostrar el estado de las conexiones
function Show-Status {
    param ($msg, $nivel)
    switch ($nivel) {
        "peligro"  { Write-Host "☠️  $msg" -ForegroundColor Red }
        "dudoso"   { Write-Host "❓ $msg" -ForegroundColor Yellow }
        "seguro"   { Write-Host "✅ $msg" -ForegroundColor Green }
        default    { Write-Host "🔍 $msg" -ForegroundColor Gray }
    }
}

# Función para determinar el nivel de amenaza y si se debe cerrar una conexión
function Evaluar-Conexión {
    param ($con)

    $processId = $con.OwningProcess
    $proc = Get-Process | Where-Object { $_.Id -eq $processId }
    $nombreProc = $proc.ProcessName

    $ip = $con.RemoteAddress
    $puerto = $con.RemotePort

    $peligro = $Modo -eq "peligro"

    # Si es IP local, es seguro
    if ($ip -like "127.*" -or $ip -like "192.168.*" -or $ip -eq "::1") {
        Show-Status "$($nombreProc) ($($processId)) → $($ip):$($puerto)" "seguro"
    }
    elseif ($ip -eq "0.0.0.0" -or $ip -eq "::") {
        Show-Status "$($nombreProc) ($($processId)) → $($ip):$($puerto) (escuchando)" "seguro"
    }
    # Peligroso si el proceso es sospechoso
    elseif ($nombreProc -in @("powershell", "cmd", "netcat", "python", "telnet", "ssh", "ftp")) {
        Show-Status "$($nombreProc) ($($processId)) → $($ip):$($puerto)" "peligro"
        if ($peligro) {
            # Matar la conexión sospechosa
            Write-Host "   🔒 Cerrando conexión peligrosa: $($nombreProc) → $($ip):$($puerto)" -ForegroundColor Red
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            Write-Host "   ✔ Conexión cerrada: $($nombreProc) → $($ip):$($puerto)" -ForegroundColor Green
        }
    }
    # Dudar si es un puerto común pero no habitual
    elseif ($puerto -in @("80", "443", "8080", "445", "3389", "21", "23", "4444", "5555")) {
        Show-Status "$($nombreProc) ($($processId)) → $($ip):$($puerto)" "dudoso"
    }
    else {
        Show-Status "$($nombreProc) ($($processId)) → $($ip):$($puerto)" "seguro"
    }
}

# Escanear las conexiones activas
Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor DarkCyan
Write-Host "[🌐] INICIANDO ESCANEO DE CONEXIONES ACTIVAS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════`n" -ForegroundColor DarkCyan

$conexiones = Get-NetTCPConnection | Where-Object { $_.State -eq 'Established' }
$bloqueados = 0
$total = 0

foreach ($con in $conexiones) {
    $total++
    Evaluar-Conexión -con $con
}

# Mostrar puertos escuchando
Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor DarkYellow
Write-Host "[🔎] PUERTOS ESCUCHANDO:" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════`n" -ForegroundColor DarkYellow

Get-NetTCPConnection -State Listen |
Select-Object LocalAddress, LocalPort |
Format-Table -AutoSize

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor DarkGreen
Write-Host "[✅] ESCANEO COMPLETADO - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Green
Write-Host "→ Total de conexiones detectadas : $total" -ForegroundColor Green
Write-Host "→ Conexiones bloqueadas         : $bloqueados" -ForegroundColor Green
Write-Host "→ Modo                          : $Modo" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor DarkGreen
