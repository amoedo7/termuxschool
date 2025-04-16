function Run-SecAlerts {
    Write-Host "`n[🛡️] Alertas de seguridad:" -ForegroundColor Cyan

    # Comprobación de servicios importantes
    $service = Get-Service -Name "SearchIndexer" -ErrorAction SilentlyContinue
    if ($service) {
        if ($service.Status -eq "Running") {
            Write-Host "[✔] El servicio SearchIndexer está en ejecución." -ForegroundColor Green
        } else {
            Write-Warning "[⚠] El servicio SearchIndexer no está en ejecución."
        }
    } else {
        Write-Warning "[⚠] No se encontró el servicio SearchIndexer."
    }

    # Comprobar sesiones remotas
    $rdpSessions = query session 2>$null | Where-Object { $_.UserName -like "*El3imm*" }
    if ($rdpSessions) {
        Write-Host "`n[🖥️] Sesiones remotas detectadas:" -ForegroundColor Red
        $rdpSessions | Format-Table -Property SessionId, UserName
    } else {
        Write-Host "[✔] No se detectaron sesiones remotas" -ForegroundColor Green
    }
}
Run-SecAlerts
