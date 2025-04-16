# PwrShell.ps1
Clear-Host
Import-Module "$PSScriptRoot\Core\CheckTools.ps1"
Import-Module "$PSScriptRoot\Core\CheckPerms.ps1"

function Mostrar-Menu {
    Clear-Host
    Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║        [💻] PwrShell System Panel         ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════╝`n" -ForegroundColor Cyan

    Write-Host "[1] Verificar herramientas esenciales" -ForegroundColor Green
    Write-Host "[2] Verificar permisos y rol actual" -ForegroundColor Yellow
    Write-Host "[3] Diagnóstico del sistema" -ForegroundColor Cyan
    Write-Host "[4] Análisis de red" -ForegroundColor Cyan
    Write-Host "[5] Usuarios y sesiones" -ForegroundColor Cyan
    Write-Host "[6] Alertas de seguridad" -ForegroundColor Red
    Write-Host "[0] Salir`n"

    $opcion = Read-Host "Selecciona una opción"
    Ejecutar-Opcion $opcion
}

function Ejecutar-Opcion($opcion) {
    switch ($opcion) {
        "1" { . "$PSScriptRoot\Core\CheckTools.ps1"; Pause }
        "2" { . "$PSScriptRoot\Core\CheckPerms.ps1"; Pause }
        "3" { . "$PSScriptRoot\Core\SysDiag.ps1"; Pause }
        "4" { . "$PSScriptRoot\Core\NetScan.ps1"; Pause }
        "5" { . "$PSScriptRoot\Core\UserControl.ps1"; Pause }
        "6" { . "$PSScriptRoot\Core\SecAlerts.ps1"; Pause }
        "0" { Exit }
        default {
            Write-Host "`n[!] Opción inválida. Intenta de nuevo." -ForegroundColor Red
            Start-Sleep -Seconds 1.5
        }
    }
    Mostrar-Menu
}

Mostrar-Menu
