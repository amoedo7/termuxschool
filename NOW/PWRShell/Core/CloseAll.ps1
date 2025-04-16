function Close-RemoteSessions {
    # Obtener sesiones activas (excluyendo la consola)
    $sessions = Get-WmiObject -Class Win32_LogonSession | Where-Object { $_.LogonType -eq 10 }

    foreach ($session in $sessions) {
        $sessionId = $session.LogonId
        Write-Host "Cerrando sesión remota con LogonId: $sessionId" -ForegroundColor Red
        logoff $sessionId
    }
}

Close-RemoteSessions
