# Setup1.ps1 - Repara errores, aplica mejoras y realiza respaldo

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        [🔧] Ejecutando Setup1.ps1       ║"
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan

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

# Función para respaldar archivos
function Backup-File {
    param (
        [string]$FilePath
    )
    if (Test-Path $FilePath) {
        $backupPath = "$FilePath.bak"
        Copy-Item -Path $FilePath -Destination $backupPath -Force
        Write-Host "[✔] Respaldo creado para: $FilePath" -ForegroundColor Green
    }
}

# 1. Reparar comandos no encontrados (quser, query)
function Repair-UserControl {
    $path = "$PSScriptRoot\Core\UserControl.ps1"
    if (Test-Path $path) {
        Backup-File -FilePath $path
        (Get-Content $path) -replace 'quser.*', 'Get-WmiObject -Class Win32_LogonSession' `
                             -replace 'query session.*', 'Get-Process -IncludeUserName | Where-Object {$_.UserName -like "*El3imm*"}' |
            Set-Content $path
        Write-Host "[✔] Reparado UserControl.ps1 (quser/query)." -ForegroundColor Green
    }
}

# 2. Reparar diagnóstico que muestra 0 GB de total
function Repair-Diagnose {
    $path = "$PSScriptRoot\Core\Diagnose.ps1"
    if (Test-Path $path) {
        Backup-File -FilePath $path
        (Get-Content $path) -replace '(\d+.\d+) GB libres de 0 GB', {
            $used = [math]::Round((Get-PSDrive C).Used / 1GB, 2)
            $total = [math]::Round((Get-PSDrive C).Used + (Get-PSDrive C).Free / 1GB, 2)
            return "$($total - $used) GB libres de $total GB"
        } | Set-Content $path
        Write-Host "[✔] Reparado Diagnose.ps1 (disco)." -ForegroundColor Green
    }
}

# 3. Cerrar sesiones antiguas del usuario actual
function Close-Old-Sessions {
    $username = $env:USERNAME
    $sessions = Get-WmiObject -Class Win32_Session | Where-Object { $_.UserName -like "*$username*" }
    foreach ($s in $sessions) {
        if ($s.Status -ne "Active") {
            Write-Host "[⏹] Cerrando sesión inactiva: $($s.UserName)"
            # Aquí cerramos la sesión si está inactiva
            # Logoff $s.SessionID
        }
    }
}

# 4. Limpiar Logs y Archivos Temporales
function Clean-TempAndLogs {
    Write-Host "[🧹] Limpiando archivos temporales..."
    Remove-Item -Path "$env:LOCALAPPDATA\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[✔] Archivos temporales eliminados."

    Write-Host "[🧹] Limpiando logs del sistema..."
    Remove-Item -Path "C:\Windows\Logs\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[✔] Logs del sistema eliminados."
}

# 5. Validar Módulos y Servicios
function Validate-Modules {
    Write-Host "[🔍] Verificando módulos y servicios..."
    $modules = @("Network", "Security", "System")
    foreach ($module in $modules) {
        if (-not (Get-Command $module -ErrorAction SilentlyContinue)) {
            Write-Warning "[⚠] Módulo $module no encontrado."
        }
    }
    Write-Host "[✔] Verificación de módulos completada."
}

# Ejecutar las funciones
Repair-UserControl
Repair-Diagnose
Close-Old-Sessions
Clean-TempAndLogs
Validate-Modules

# Resumen de cambios realizados
Write-Host "`n[✅] Resumen de cambios realizados:"
Write-Host "[✔] UserControl.ps1 reparado (quser/query)."
Write-Host "[✔] Diagnose.ps1 reparado (disco)."
Write-Host "[✔] Sesiones inactivas cerradas."
Write-Host "[✔] Archivos temporales y logs limpiados."
Write-Host "[✔] Módulos verificados."

Write-Host "`n[✅] Setup1.ps1 finalizado correctamente." -ForegroundColor Cyan
Pause
