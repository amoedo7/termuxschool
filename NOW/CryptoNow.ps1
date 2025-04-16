$CryptoTools = @{
    "🔐 Herramientas de Seguridad" = @(
        "openssl", "gnupg", "gpg", "cryptsetup", "yubico-piv-tool", "cryptography", "pycryptodome", "sodium"
    )
    "💻 Bibliotecas Python para Cripto" = @(
        "requests", "cryptography", "pycryptodome", "eth-utils", "web3", "bitcoinlib", "mnemonic", "blockchain", "pycoind"
    )
    "🧰 Herramientas de Blockchain" = @(
        "bitcoin-cli", "eth", "cardano-cli", "solana", "polkadot-cli", "bsc-cli", "truffle", "ganache", "metamask", "ethereumswagger"
    )
    "💼 API y Herramientas de Monitoreo" = @(
        "coinmarketcap", "coingecko", "cryptocompare", "nomics", "blockchair", "binance-cli", "ccxt"
    )
    "📈 Análisis y Gráficos" = @(
        "plotly", "matplotlib", "pandas", "seaborn", "numpy", "ta-lib", "pycryptodome", "cryptowatch", "tradingview", "dash"
    )
    "🌍 Exploradores y Dapps" = @(
        "etherscan", "bscscan", "cardanoscan", "polkaview", "solscan", "uniswap", "compound", "aave", "defi", "uniswap-cli"
    )
}

# Función para comprobar si las herramientas están instaladas
Function Check-CryptoTools {
    $missingTools = @()
    
    foreach ($category in $CryptoTools.Keys) {
        Write-Host "`nChecking category: $category"
        
        foreach ($tool in $CryptoTools[$category]) {
            $toolPath = Get-Command $tool -ErrorAction SilentlyContinue
            if ($null -eq $toolPath) {
                Write-Host "❌ $tool not found"
                $missingTools += $tool
            } else {
                Write-Host "✅ $tool is installed"
            }
        }
    }
    
    if ($missingTools.Count -eq 0) {
        Write-Host "`nAll Crypto tools are installed!"
    } else {
        Write-Host "`nMissing tools: $($missingTools -join ', ')"
    }
}

# Ejecutar el diagnóstico
Check-CryptoTools
