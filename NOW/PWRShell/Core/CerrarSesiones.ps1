# Obtener las sesiones activas
$sessions = Get-WmiObject -Class Win32_Session

# Mostrar las sesiones activas (esto es solo para referencia, puedes quitarlo después)
$sessions | Select-Object LogonId, UserName

# Solicitar al usuario los LogonIds a cerrar (se pueden separar por coma o usar 'ALL' para cerrar todas)
$logonIds = Read-Host "Ingrese los LogonIds de las sesiones que desea cerrar, separados por comas (o 'ALL' para cerrar todas)"

# Función para cerrar la sesión usando tscon
function Close-Session($logonId) {
    try {
        # Buscar la sesión por LogonId
        $session = $sessions | Where-Object { $_.LogonId -eq $logonId }
        if ($session) {
            # Aquí utilizamos 'tscon' para desconectar la sesión de forma segura
            Write-Host "Cerrando sesión con LogonId $logonId..."
            tscon $logonId /dest:console
            Write-Host "Sesión con LogonId $logonId cerrada exitosamente."
        } else {
            Write-Host "Sesión con LogonId $logonId no encontrada."
        }
    } catch {
        Write-Host "Error al intentar cerrar la sesión con LogonId ${logonId}: $_"
    }
}

# Si el usuario ingresa 'ALL', cerramos todas las sesiones
if ($logonIds -eq "ALL") {
    $sessions | ForEach-Object { Close-Session $_.LogonId }
} else {
    # Cerrar las sesiones especificadas
    $logonIds.Split(',') | ForEach-Object {
        Close-Session $_.Trim()
    }
}
