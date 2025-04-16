import hashlib
import ecdsa
import base58
import requests
import datetime  # <-- Agregado para convertir timestamps

def brainwallet(phrase):
    """ Convierte una frase en clave privada y dirección Bitcoin """
    private_key = hashlib.sha256(phrase.encode()).digest()
    
    # Generar clave pública
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()

    # Hash de la clave pública (SHA-256 + RIPEMD-160)
    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

    # Agregar prefijo de red (0x00 para Bitcoin Mainnet)
    network_byte = b'\x00' + ripemd160_hash

    # Checksum (SHA-256 doble)
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]

    # Dirección en Base58Check
    address = base58.b58encode(network_byte + checksum).decode()

    return private_key.hex(), address

def consultar_saldo_y_transaccion(direccion):
    """ Consulta el saldo y la última transacción de una dirección Bitcoin """
    try:
        api_url = f"https://blockchain.info/rawaddr/{direccion}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            saldo_satoshis = int(data.get("final_balance", 0))
            saldo_btc = saldo_satoshis / 100_000_000  # Convertir satoshis a BTC
            
            # Obtener última transacción si existen transacciones
            ultima_tx = None
            if "txs" in data and len(data["txs"]) > 0:
                ultima_tx = data["txs"][0]  # Última transacción
                tx_hash = ultima_tx.get("hash", "Desconocido")
                tx_valor = sum(out["value"] for out in ultima_tx.get("out", [])) / 100_000_000  # Convertir a BTC
                tx_time = ultima_tx.get("time", None)  # Timestamp UNIX
                
                # 🔥 Convertimos el timestamp UNIX a una fecha legible
                if tx_time:
                    fecha_legible = datetime.datetime.utcfromtimestamp(tx_time).strftime('%Y-%m-%d %H:%M:%S UTC')
                else:
                    fecha_legible = "Desconocido"
                
                return saldo_btc, {"hash": tx_hash, "valor": tx_valor, "fecha": fecha_legible}
            
            return saldo_btc, None
        
    except Exception as e:
        print(f"⚠️ Error consultando datos: {e}")
    return None, None

if __name__ == "__main__":
    while True:
        frase = input("\nIntroduce una frase para la Brainwallet (o escribe 'exit' para salir): ")
        if frase.lower() == "exit":
            print("Saliendo...")
            break
        
        private_key, btc_address = brainwallet(frase)
        print(f"\n🔑 Clave Privada: {private_key}")
        print(f"🏦 Dirección Bitcoin: {btc_address}")

        saldo, transaccion = consultar_saldo_y_transaccion(btc_address)
        if saldo is not None:
            print(f"💰 Saldo de la dirección: {saldo} BTC")
            if transaccion:
                print(f"📌 Última transacción:")
                print(f"   🔗 Hash: {transaccion['hash']}")
                print(f"   💸 Valor: {transaccion['valor']} BTC")
                print(f"   🕒 Fecha: {transaccion['fecha']}")
            else:
                print("📭 No hay transacciones registradas en esta dirección.")
        else:
            print("⚠️ No se pudo consultar el saldo (puede que la API esté bloqueada o la dirección no exista).")
