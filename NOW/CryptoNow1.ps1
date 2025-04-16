# Instalar dependencias necesarias
Write-Host "Instalando dependencias..." -ForegroundColor Cyan
npm install -g truffle ganache-cli
pip install plotly matplotlib pandas seaborn numpy ta-lib requests cryptography

Write-Host "---- Fin de la instalación de herramientas ----" -ForegroundColor Green

# Obtener el Top 10 de criptomonedas desde CoinGecko
Write-Host "Obteniendo el Top 10 de criptomonedas..." -ForegroundColor Cyan
$cryptoData = Invoke-RestMethod -Uri "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"

# Verificar si la API respondió correctamente
if ($cryptoData) {
    # Mostrar el Top 10 en formato de tabla
    Write-Host "`nTop 10 Criptomonedas por Valor de Mercado:" -ForegroundColor Yellow
    $cryptoData | ForEach-Object {
        [PSCustomObject]@{
            "#": $_.market_cap_rank
            "Nombre": $_.name
            "Símbolo": $_.symbol.ToUpper()
            "Precio Actual (USD)": "$($($_.current_price).ToString('F2'))"
        }
    } | Format-Table -AutoSize
} else {
    Write-Host "No se pudo obtener la información de las criptomonedas." -ForegroundColor Red
}

Write-Host "`n---- Fin del listado de las 10 criptomonedas más valiosas ----" -ForegroundColor Green

# Comprobar herramientas necesarias
Write-Host "Comprobando herramientas necesarias..." -ForegroundColor Cyan
$tools = @("bitcoin-cli", "eth", "cardano-cli", "solana", "bsc-cli", "truffle", "ganache", "metamask")
$tools | ForEach-Object {
    if (Get-Command $_ -ErrorAction SilentlyContinue) {
        Write-Host "$_ está instalado" -ForegroundColor Green
    } else {
        Write-Host "$_ no está instalado" -ForegroundColor Red
    }
}

Write-Host "`n---- Fin de la comprobación de herramientas ----" -ForegroundColor Green
