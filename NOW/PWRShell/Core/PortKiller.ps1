# Función para mostrar un mensaje de bienvenida
function Show-WelcomeMessage {
    Write-Host "Bienvenido al PortKiller Script. Este script cerrará procesos escuchando en puertos." -ForegroundColor Cyan
    Write-Host "--------------------------------------------------------------"
}

# Función para confirmar la acción
function Confirm-Action {
    param([string]$message)

    $response = Read-Host "$message (S/N)"
    if ($response -eq 'S' -or $response -eq 's') {
        return $true
    }
    return $false
}

# Función para obtener los puertos en escucha y sus procesos
function Get-ListeningPorts {
    Write-Host "Obteniendo puertos en escucha..." -ForegroundColor Yellow
    $ports = Get-NetTCPConnection | Where-Object { $_.State -eq 'Listen' }
    if ($ports.Count -eq 0) {
        Write-Host "[❌] No se encontraron puertos en escucha." -ForegroundColor Red
        return $null
    }
    return $ports
}

# Función para mostrar los puertos encontrados y sus procesos
function Show-PortsAndProcesses {
    param([array]$ports)
    Write-Host "Puertos en escucha encontrados:" -ForegroundColor Green
    $ports | ForEach-Object {
        Write-Host "Puerto: $($_.LocalPort) - Proceso: $(Get-Process -Id $_.OwningProcess).Name (PID: $($_.OwningProcess))" -ForegroundColor Yellow
    }
}

# Función para verificar si el proceso es esencial
function Is-EssentialProcess {
    param([int]$pid)
    
    # Lista de procesos esenciales que no deben ser cerrados
    $essentialProcesses = @(
        'System', 'svchost', 'explorer', 'cmd', 'lsass', 'winlogon', 'services', 'smss', 'csrss'
    )
    
    $processName = (Get-Process -Id $pid).Name
    return $essentialProcesses -contains $processName
}

# Función para cerrar procesos automáticamente
function Close-Ports {
    param([array]$ports)
    foreach ($port in $ports) {
        try {
            $targetPid = $port.OwningProcess
            if (Is-EssentialProcess -pid $targetPid) {
                Write-Host "[⚠️] El proceso $(Get-Process -Id $targetPid).Name (PID: $targetPid) es esencial y no se cerrará." -ForegroundColor Yellow
                continue
            }

            Stop-Process -Id $targetPid -Force
            Write-Host "[✅] Proceso $(Get-Process -Id $targetPid).Name (PID: $targetPid) cerrado exitosamente." -ForegroundColor Green
        }
        catch {
            Write-Host "[❌] No se pudo cerrar el proceso con PID: $targetPid. Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Función principal para ejecutar el script
function Run-PortKiller {
    Show-WelcomeMessage

    $ports = Get-ListeningPorts
    if ($ports -eq $null) { return }

    Show-PortsAndProcesses -ports $ports

    $actionConfirmed = Confirm-Action "¿Deseas cerrar todos los procesos en puertos escuchando?"
    if ($actionConfirmed) {
        Close-Ports -ports $ports
    }
    else {
        Write-Host "[⏳] Operación cancelada por el usuario." -ForegroundColor Yellow
    }
}

# Ejecutar el script
Run-PortKiller
