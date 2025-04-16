function Check-Perms {
    # Obtener identidad del usuario
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    # Mostrar el título
    Write-Host "`n[🔐] Verificación de Permisos" -ForegroundColor Yellow

    # Verificar si el usuario es administrador
    if ($isAdmin) {
        # Si el usuario es admin, mostrar mensaje en verde
        Write-Host "`n[✔️] Estás ejecutando con permisos de administrador." -ForegroundColor Green
        Write-Host "   Todas las funciones están disponibles para ti." -ForegroundColor Green
    } else {
        # Si el usuario no es admin, mostrar mensaje en rojo
        Write-Host "`n[✘] No estás ejecutando como administrador." -ForegroundColor Red
        Write-Host "   Algunas funciones pueden no estar disponibles." -ForegroundColor Red
        Write-Host "   Por favor, considera reiniciar este script con permisos elevados." -ForegroundColor DarkRed
        Write-Host "`n💡 Para ejecutar como administrador, haz clic derecho en PowerShell y selecciona 'Ejecutar como administrador'." -ForegroundColor DarkYellow
    }

    # Separación visual
    Write-Host "`n[⚙️] Fin de la verificación de permisos" -ForegroundColor Yellow
}

# Ejecutar la función
Check-Perms
