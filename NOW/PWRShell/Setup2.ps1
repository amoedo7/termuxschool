# Setup2.ps1 - Mejora la funcionalidad del sistema

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        [🔧] Ejecutando Setup2.ps1       ║"
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan

# Función para verificar si el script se está ejecutando como administrador
function Check-Admin {
    if (-not ([Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()
        ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Warning "Este script debe ejecutarse como administrador."
        Start-Sleep -Seconds 3
        exit
    }
}
Check-Admin

# Función para hacer un backup de un archivo
function Backup-File {
    param (
        [string]$FilePath
    )

    $backupPath = "$FilePath.bak"
    if (Test-Path $FilePath) {
        Copy-Item $FilePath -Destination $backupPath -Force
        Write-Host "[✔] Respaldo creado para: $FilePath" -ForegroundColor Green
    } else {
        Write-Warning "[⚠] El archivo $FilePath no existe, no se puede crear respaldo."
    }
}

# 1. Reparar diagnóstico de disco (total disponible)
function Repair-DiskDiag {
    $path = "$PSScriptRoot\Core\SysDiag.ps1"
    if (Test-Path $path) {
        Backup-File -FilePath $path
        (Get-Content $path) -replace '(\d+.\d+) GB libres de 0 GB', {
            $used = [math]::Round((Get-PSDrive C).Used / 1GB, 2)
            $total = [math]::Round((Get-PSDrive C).Used + (Get-PSDrive C).Free / 1GB, 2)
            return "$($total - $used) GB libres de $total GB"
        } | Set-Content $path
        Write-Host "[✔] Reparado SysDiag.ps1 (disco total)." -ForegroundColor Green
    }
}

# 2. Mejorar la salida del análisis de red
function Improve-NetworkAnalysis {
    $path = "$PSScriptRoot\Core\NetScan.ps1"
    if (Test-Path $path) {
        Backup-File -FilePath $path
        (Get-Content $path) -replace 'echo "Network analysis complete."', {
            return @"
[🔍] Análisis de Red Completado:
---------------------------------
- Conexión activa a: $(Get-NetIPAddress | Select-Object -First 1).IPAddress
- Dispositivos conectados: $(Get-NetNeighbor | Select-Object -First 5 | Format-Table -AutoSize)
"@
        } | Set-Content $path
        Write-Host "[✔] Mejorada salida de NetScan.ps1." -ForegroundColor Green
    }
}

# 3. Reparar error en UserControl.ps1 (función Run-UserControl)
function Repair-UserControlFunction {
    $path = "$PSScriptRoot\Core\UserControl.ps1"
    if (Test-Path $path) {
        Backup-File -FilePath $path
        $content = Get-Content $path
        if ($content -notcontains "}") {
            $content += "`n}"
        }
        Set-Content $path -Value $content
        Write-Host "[✔] Reparada sintaxis en UserControl.ps1." -ForegroundColor Green
    }
}

# 4. Mejorar análisis de servicios de seguridad (WSearch y otros)
function Improve-SecurityAnalysis {
    $path = "$PSScriptRoot\Core\SecAlerts.ps1"
    if (Test-Path $path) {
        Backup-File -FilePath $path
        (Get-Content $path) -replace 'WSearch', 'SearchIndexer' | Set-Content $path
        Write-Host "[✔] Mejorado análisis de seguridad en SecAlerts.ps1." -ForegroundColor Green
    }
}

# Ejecutar las mejoras
Repair-DiskDiag
Improve-NetworkAnalysis
Repair-UserControlFunction
Improve-SecurityAnalysis

# Resumen de cambios realizados
Write-Host "`n[✅] Resumen de cambios realizados:"
Write-Host "[✔] SysDiag.ps1 reparado (cálculo de espacio total)."
Write-Host "[✔] Mejorada salida de NetScan.ps1 (análisis de red)."
Write-Host "[✔] Corregida sintaxis en UserControl.ps1."
Write-Host "[✔] Mejorado análisis de seguridad (WSearch)."

Write-Host "`n[✅] Setup2.ps1 finalizado correctamente." -ForegroundColor Cyan
Pause
