# CloseUsrsFinal.ps1
# Script interactivo para listar y cerrar sesiones activas
# ¡ADVERTENCIA: Usar con precaución y preferiblemente en un entorno de pruebas!

# Función para listar las sesiones activas
function List-Sessions {
    Write-Host "`n[💻] Sesiones activas actuales:" -ForegroundColor Cyan
    Write-Host "--------------------------------------" -ForegroundColor DarkGray

    # Usamos Get-CimInstance en lugar de Get-WmiObject (más moderno)
    $sessions = Get-CimInstance -ClassName Win32_LogonSession
    foreach ($session in $sessions) {
        $logonId = $session.LogonId
        $logonType = $session.LogonType

        switch ($logonType) {
            0 {
                Write-Host "[✔️] LogonType '0' detectado - Sesión de usuario interactiva normal (ID: $logonId)" -ForegroundColor Green
            }
            5 {
                Write-Host "[⚠️] LogonType '5' detectado - Podría ser una sesión de consola no interactiva (ID: $logonId)" -ForegroundColor Yellow
            }
            2 {
                Write-Host "[🔍] LogonType '2' - Tipo no clasificado (ID: $logonId)" -ForegroundColor Yellow
            }
            default {
                Write-Host "[⚠️] LogonType '$logonType' no clasificado - Atención (ID: $logonId)" -ForegroundColor Red
            }
        }

        if ($logonId -gt 10000000) {
            Write-Host "[⚠️] LogonId '$logonId' parece extremadamente alto." -ForegroundColor Red
        } elseif ($logonId -lt 1000) {
            Write-Host "[⚠️] LogonId '$logonId' parece inusualmente bajo." -ForegroundColor Red
        }
    }
    Write-Host "--------------------------------------" -ForegroundColor DarkGray
    return $sessions
}

# Función para cerrar una sesión usando logoff (llamado a cmd.exe con la ruta completa)
function Close-Session {
    param(
        [Parameter(Mandatory=$true)]
        [int]$LogonId
    )
    try {
        Write-Host "Intentando cerrar sesión con LogonId $LogonId..." -ForegroundColor Yellow
        # Invocar logoff usando la ruta completa para asegurar que se reconozca
        cmd.exe /c "C:\Windows\System32\logoff.exe $LogonId"
        Write-Host "Sesión con LogonId $LogonId cerrada exitosamente." -ForegroundColor Green
    } catch {
        Write-Host "Error al cerrar la sesión con LogonId ${LogonId}: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# --- Bloque Principal del Script ---
# Asegúrate de ejecutar PowerShell "Como Administrador" para tener permisos suficientes.
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Este script debe ejecutarse como Administrador." -ForegroundColor Red
    exit
}

# Listar las sesiones activas
$sessions = List-Sessions

# Pedir al usuario los LogonIds de las sesiones que desea cerrar
$idsInput = Read-Host "`nIngrese los LogonIds de las sesiones que desea cerrar, separados por comas (o presione Enter para omitir)"
if ($idsInput -and $idsInput.Trim() -ne "") {
    $idArray = $idsInput -split ',' | ForEach-Object { $_.Trim() }
    foreach ($id in $idArray) {
        if ($id -as [int]) {
            Close-Session -LogonId ([int]$id)
        } else {
            Write-Host "El valor '$id' no es un LogonId válido." -ForegroundColor Red
        }
    }
} else {
    Write-Host "No se cerraron sesiones." -ForegroundColor Cyan
}

Write-Host "`n[⚙️] Fin de la verificación y cierre de sesiones" -ForegroundColor Cyan
