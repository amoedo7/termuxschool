function Run-UserControl {
    # Título de la verificación
    Write-Host "`n[👥] Control de Usuarios y Sesiones Activas" -ForegroundColor Yellow

    # Usuarios locales
    Write-Host "`n[🧑‍💻] Usuarios locales del sistema:" -ForegroundColor Cyan
    Write-Host "--------------------------------------" -ForegroundColor DarkGray
    Get-LocalUser | Format-Table Name, Enabled, LastLogon | Out-String | Write-Host -ForegroundColor White
    Write-Host "--------------------------------------" -ForegroundColor DarkGray

    # Sesiones activas
    Write-Host "`n[💻] Sesiones activas actuales:" -ForegroundColor Cyan
    Write-Host "--------------------------------------" -ForegroundColor DarkGray
    $logonSessions = Get-WmiObject -Class Win32_LogonSession

    foreach ($session in $logonSessions) {
        $logonType = $session.LogonType
        $logonId = $session.LogonId

        # Resaltar LogonType peligrosos
        if ($logonType -eq 5) {
            Write-Host "[⚠️] LogonType '5' detectado - Podría ser una sesión de consola no interactiva" -ForegroundColor Red
        } elseif ($logonType -eq 0) {
            Write-Host "[✔️] LogonType '0' detectado - Sesión de usuario interactiva normal" -ForegroundColor Green
        } else {
            Write-Host "[🔍] LogonType '$logonType' - Tipo no clasificado" -ForegroundColor Yellow
        }

        # Resaltar LogonId sospechosos
        if ($logonId -gt 10000000) {
            Write-Host "[⚠️] LogonId '$logonId' parece sospechoso (ID alto)" -ForegroundColor Red
        } elseif ($logonId -lt 1000) {
            Write-Host "[⚠️] LogonId '$logonId' parece sospechoso (ID bajo)" -ForegroundColor Red
        } else {
            Write-Host "[✔️] LogonId '$logonId' parece normal" -ForegroundColor Green
        }

        # Check for specific user login
        $userName = $session.PSComputerName
        if ($userName -eq "El3imm" -and $logonId -gt 10000000) {
            Write-Host "[⚠️] Sesión de usuario 'El3imm' con LogonId sospechoso" -ForegroundColor Red
        }
    }
    Write-Host "--------------------------------------" -ForegroundColor DarkGray

    # Sesiones remotas (usando Get-WmiObject o Get-CimInstance)
    $rdpSessions = Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty UserName
    if ($rdpSessions) {
        Write-Host "`n[🖥️] Sesiones remotas detectadas:" -ForegroundColor Red
        $rdpSessions | Format-Table | Out-String | Write-Host -ForegroundColor White
        Write-Host "[⚠️] Verificar las sesiones remotas activas para detectar posibles accesos no autorizados." -ForegroundColor Red
    } else {
        Write-Host "`n[✔️] No se detectaron sesiones remotas" -ForegroundColor Green
    }

    # Separador visual
    Write-Host "`n[⚙️] Fin de la verificación de usuarios y sesiones" -ForegroundColor Yellow
}

# Ejecutar la función
Run-UserControl
