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

# 🧹 1. Eliminar subrepositorios embebidos problemáticos
$posiblesSubrepos = @(
    "PTerminados/Verr1/PidAmo/.git",
    "PTerminados/Verr1/ApostAmo/.git"
)

foreach ($path in $posiblesSubrepos) {
    if (Test-Path $path) {
        Remove-Item -Recurse -Force $path -ErrorAction SilentlyContinue
        Write-Host "🗑️  Eliminado repositorio embebido: $path" -ForegroundColor Yellow
    }
}

# 🧹 2. Borrar el repo Git actual si existe
if (Test-Path ".git") {
    Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
    Write-Host "🧨 .git eliminado. Reiniciando el repositorio..." -ForegroundColor DarkCyan
}

# 🔧 3. Inicializar el nuevo repo y conectarlo a GitHub
git init
git remote add origin "https://${Username}:${Token}@github.com/${Username}/${Repo}.git"
git branch -M $Branch

# 🗃️ 4. Agregar y commitear todos los archivos
git add .
$Fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "🧹 Limpieza total y reinicio del repositorio - $Fecha"

# 🚀 5. Hacer PUSH forzado
git push -u origin $Branch --force

Write-Host "`n✅ ¡Push forzado completado! El repositorio remoto ahora está limpio." -ForegroundColor Green
