function Remove-NonEl3immUsers {
    Write-Host "`n[⚠️] AVISO: Este script eliminará permanentemente las cuentas de usuario locales que no sean las protegidas." -ForegroundColor Red
    Write-Host "[👤] Cuentas protegidas: El3imm, Administrator, DefaultAccount, WDAGUtilityAccount" -ForegroundColor Yellow
    Write-Host "`n¿Estás seguro que deseas proceder? (S/N):" -NoNewline -ForegroundColor Cyan
    $confirm = Read-Host
    if ($confirm -notin @("S","s")) {
        Write-Host "`nOperación cancelada." -ForegroundColor Yellow
        return
    }
    
    # Obtener la lista de usuarios locales
    $users = Get-LocalUser

    # Lista de cuentas que NO se eliminarán
    $protectedAccounts = @("El3imm", "Administrator", "DefaultAccount", "WDAGUtilityAccount")

    Write-Host "`n[🗑️] Iniciando la eliminación de cuentas no protegidas..." -ForegroundColor Magenta

    foreach ($user in $users) {
        if ($protectedAccounts -notcontains $user.Name) {
            Write-Host "[❌] Eliminando cuenta '$($user.Name)'..." -ForegroundColor Magenta
            try {
                Remove-LocalUser -Name $user.Name -ErrorAction Stop
                Write-Host "[✔️] Cuenta '$($user.Name)' eliminada exitosamente." -ForegroundColor Green
            } catch {
                Write-Host "[⚠️] Error al eliminar '$($user.Name)': $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "[✔️] Cuenta protegida '$($user.Name)' - No se eliminará." -ForegroundColor Cyan
        }
    }
    
    Write-Host "`n[⚙️] Operación completada." -ForegroundColor Yellow
}

# Ejecutar la función
Remove-NonEl3immUsers
