# Configuración
$Username = "amoedo7"
$Repo = "termuxschool"
$Branch = "main"
$Token = $env:GH_TOKEN

if (-not $Token) {
    Write-Host "[❌] GH_TOKEN no está definido en el entorno." -ForegroundColor Red
    Write-Host "Usá: `$env:GH_TOKEN = 'tu_token'" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🔄 Preparando para hacer PUSH forzado al repositorio..." -ForegroundColor Cyan

# Reconstruir Git desde cero
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
git init
git remote add origin "https://${Username}:${Token}@github.com/${Username}/${Repo}.git"
git branch -M $Branch

# Agregar y commitear todo
git add .
$Fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "🧹 Limpieza total y reinicio del repositorio - $Fecha"

# Hacer PUSH forzado
git push -u origin $Branch --force

Write-Host "`n✅ ¡Push forzado completado! El repositorio remoto ahora está limpio." -ForegroundColor Green
