param (
    [string]$Modo = "seguro",   # Modo seguro o peligroso
    [string]$LogPath = "C:\logs\netkiller_log.txt"  # Ruta para el archivo de log
)

# Variables para almacenar los resúmenes
$bloqueados = @()
$eliminados = @()
$no_tocados = @()

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

# Función para evaluar conexiones
function Evaluar-Conexión {
    param ($con)

    $processId = $con.OwningProcess
    $proc = Get-Process | Where-Object { $_.Id -eq $processId }
    $nombreProc = $proc.ProcessName

    $ip = $con.RemoteAddress
    $puerto = $con.RemotePort

    $peligro = $Modo -eq "peligro"

    if ($ip -like "127.*" -or $ip -like "192.168.*" -or $ip -eq "::1") {
        Show-Status "$($nombreProc) → $($ip):$($puerto)" "seguro"
        $no_tocados += "$($nombreProc) → $($ip):$($puerto) - Razón: Conexión local"
    }
    elseif ($ip -eq "0.0.0.0" -or $ip -eq "::") {
        Show-Status "$($nombreProc) → $($ip):$($puerto) (escuchando)" "seguro"
        $no_tocados += "$($nombreProc) → $($ip):$($puerto) - Razón: Escuchando en puerto"
    }
    elseif ($nombreProc -in @("powershell", "cmd", "netcat", "python", "telnet", "ssh", "ftp")) {
        Show-Status "$($nombreProc) → $($ip):$($puerto)" "peligro"
        if ($peligro) {
            Write-Host "   🔒 ¿Deseas bloquear esta conexión? (S/N):" -ForegroundColor Red
            $decision = Read-Host
            if ($decision -eq "S") {
                # Acción para bloquear la conexión
                New-NetFirewallRule -DisplayName "Bloqueo_$($nombreProc)_$($ip)" -Direction Inbound -RemoteAddress $ip -Action Block -Protocol TCP -RemotePort $puerto
                $bloqueados += "$($nombreProc) → $($ip):$($puerto) - Razón: Conexión peligrosa detectada"
                Add-Content -Path $LogPath -Value "$(Get-Date) - Bloqueada: $($nombreProc) → $($ip):$($puerto)"
                Write-Host "   ✔ Conexión bloqueada: $($nombreProc) → $($ip):$($puerto)" -ForegroundColor Green
            }
            else {
                Write-Host "   ❌ Conexión no bloqueada." -ForegroundColor Yellow
                $no_tocados += "$($nombreProc) → $($ip):$($puerto) - Razón: Decisión del usuario"
            }
        }
    }
    else {
        Show-Status "$($nombreProc) → $($ip):$($puerto)" "seguro"
        $no_tocados += "$($nombreProc) → $($ip):$($puerto) - Razón: Conexión segura"
    }
}

# Función para eliminar conexiones
function Eliminar-Conexión {
    param ($con)

    $processId = $con.OwningProcess
    try {
        # Verificamos si el proceso puede ser detenido
        $proc = Get-Process -Id $processId -ErrorAction Stop
        Stop-Process -Id $processId -Force
        $eliminados += "$($con.LocalAddress):$($con.LocalPort) → $($con.RemoteAddress):$($con.RemotePort) - Razón: Proceso detenido"
        Add-Content -Path $LogPath -Value "$(Get-Date) - Eliminado: $($con.LocalAddress):$($con.LocalPort) → $($con.RemoteAddress):$($con.RemotePort)"
        Write-Host "   ✔ Conexión eliminada: $($con.LocalAddress):$($con.LocalPort) → $($con.RemoteAddress):$($con.RemotePort)" -ForegroundColor Green
    }
    catch {
        Write-Host "   ❌ No se pudo eliminar la conexión: $($con.LocalAddress):$($con.LocalPort) → $($con.RemoteAddress):$($con.RemotePort)" -ForegroundColor Red
        $no_tocados += "$($con.LocalAddress):$($con.LocalPort) → $($con.RemoteAddress):$($con.RemotePort) - Razón: No se pudo detener el proceso"
    }
}

# Función para iniciar el escaneo
function Start-NetKiller {
    Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host "[🌐] INICIANDO ESCANEO DE CONEXIONES ACTIVAS" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════`n" -ForegroundColor DarkCyan

    $conexiones = Get-NetTCPConnection | Where-Object { $_.State -eq 'Established' }
    foreach ($con in $conexiones) {
        Evaluar-Conexión -con $con
        Eliminar-Conexión -con $con  # Llamamos a la eliminación del proceso
    }

    Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor DarkYellow
    Write-Host "[📊] RESUMEN DE ACCIONES REALIZADAS" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════════════════════`n" -ForegroundColor DarkYellow

    # Resumen de las acciones realizadas
    if ($bloqueados.Count -gt 0) {
        Write-Host "[🔴] Conexiones bloqueadas:" -ForegroundColor Red
        $bloqueados | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-Host "[🟢] No se bloquearon conexiones." -ForegroundColor Green
    }

    if ($eliminados.Count -gt 0) {
        Write-Host "[🟢] Conexiones eliminadas:" -ForegroundColor Green
        $eliminados | ForEach-Object { Write-Host "   - $_" -ForegroundColor Green }
    } else {
        Write-Host "[🟡] No se eliminaron conexiones." -ForegroundColor Yellow
    }

    if ($no_tocados.Count -gt 0) {
        Write-Host "[🟡] Conexiones no tocadas:" -ForegroundColor Yellow
        $no_tocados | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
    }

    Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor DarkGreen
    Write-Host "[✅] ESCANEO COMPLETADO" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor DarkGreen
}

Start-NetKiller
