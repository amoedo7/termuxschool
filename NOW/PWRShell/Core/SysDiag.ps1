function Run-SysDiag {
    Write-Host "`n[🩺] Diagnóstico del sistema:" -ForegroundColor Cyan

    # CPU y RAM
    $cpu = Get-CimInstance Win32_Processor | Select-Object -ExpandProperty LoadPercentage
    $ram = Get-CimInstance Win32_OperatingSystem
    $totalMem = [math]::Round($ram.TotalVisibleMemorySize / 1MB, 2)
    $freeMem = [math]::Round($ram.FreePhysicalMemory / 1MB, 2)
    $usedMem = [math]::Round($totalMem - $freeMem, 2)

    Write-Host "CPU en uso: $cpu%" -ForegroundColor Yellow
    Write-Host "RAM usada: $usedMem GB / $totalMem GB" -ForegroundColor Yellow

    # Disco
    $drives = Get-PSDrive -PSProvider FileSystem
    foreach ($drive in $drives) {
        $free = [math]::Round($drive.Free / 1GB, 2)
        $used = [math]::Round($drive.Used / 1GB, 2)
        $total = [math]::Round(($drive.Used + $drive.Free) / 1GB, 2)

        # Validación para mostrar el tamaño del disco correctamente
        $maxSize = if ($drive.MaximumSize -eq 0) { "Desconocido" } else { [math]::Round($drive.MaximumSize / 1GB, 2) }
        
        Write-Host "Disco [$($drive.Name)]: $free GB libres de $maxSize GB (Usado: $used GB)" -ForegroundColor Cyan
    }

    # Batería (si aplica)
    $batt = Get-WmiObject Win32_Battery
    if ($batt) {
        $charge = $batt.EstimatedChargeRemaining
        Write-Host "Batería: $charge%" -ForegroundColor Green
    } else {
        Write-Host "Batería: No detectada (equipo de escritorio o sin soporte)" -ForegroundColor DarkGray
    }
}
Run-SysDiag
