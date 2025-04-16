import hashlib
import ecdsa
import base58
import requests
import datetime
from Crypto.Hash import keccak

def sha256(data):
    return hashlib.sha256(data).digest()

def ripemd160(data):
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.digest()

def base58check_encode(prefix, payload):
    data = prefix + payload
    checksum = sha256(sha256(data))[:4]
    return base58.b58encode(data + checksum).decode()

def keccak256(data):
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

def generate_all_addresses(phrase):
    private_key = sha256(phrase.encode())
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    public_key_compressed = (
        b'\x02' + vk.to_string()[:32] if vk.to_string()[-1] % 2 == 0
        else b'\x03' + vk.to_string()[:32]
    )

    results = {}

    # Bitcoin (0x00)
    btc_hash160 = ripemd160(sha256(public_key))
    results["Bitcoin"] = base58check_encode(b'\x00', btc_hash160)

    # Litecoin (0x30)
    results["Litecoin"] = base58check_encode(b'\x30', btc_hash160)

    # Dogecoin (0x1e)
    results["Dogecoin"] = base58check_encode(b'\x1e', btc_hash160)

    # Bitcoin Cash (Legacy, igual que BTC)
    results["BitcoinCash"] = base58check_encode(b'\x00', btc_hash160)

    # Clams (0x1c)
    results["Clams"] = base58check_encode(b'\x1c', btc_hash160)

    # Zcash (0x1cb8 = t-addr)
    results["Zcash"] = base58check_encode(b'\x1c\xb8', btc_hash160)

    # Dash (0x4c)
    results["Dash"] = base58check_encode(b'\x4c', btc_hash160)

    # Ethereum (keccak)
    eth_address = '0x' + keccak256(public_key[1:])[12:].hex()
    results["Ethereum"] = eth_address

    # Binance Smart Chain (igual que Ethereum)
    results["BNB"] = eth_address

    return private_key.hex(), results

def consultar_saldo_btc(direccion):
    try:
        api_url = f"https://blockchain.info/rawaddr/{direccion}"
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            saldo_satoshis = int(data.get("final_balance", 0))
            saldo_btc = saldo_satoshis / 100_000_000

            if "txs" in data and len(data["txs"]) > 0:
                ultima_tx = data["txs"][0]
                tx_hash = ultima_tx.get("hash", "Desconocido")
                tx_valor = sum(out["value"] for out in ultima_tx.get("out", [])) / 100_000_000
                tx_time = ultima_tx.get("time", None)
                fecha_legible = datetime.datetime.utcfromtimestamp(tx_time).strftime('%Y-%m-%d %H:%M:%S UTC') if tx_time else "Desconocido"
                return saldo_btc, {"hash": tx_hash, "valor": tx_valor, "fecha": fecha_legible}

            return saldo_btc, None
    except Exception as e:
        print(f"⚠️ Error consultando BTC: {e}")
    return None, None

if __name__ == "__main__":
    while True:
        frase = input("\n🧠 Introduce una frase para la Brainwallet (o 'exit'): ")
        if frase.lower() == "exit":
            print("Saliendo...")
            break

        private_key, addresses = generate_all_addresses(frase)
        print(f"\n🔑 Clave Privada: {private_key}\n")

        for nombre, direccion in addresses.items():
            print(f"🏦 {nombre}: {direccion}")

        print("\n⏳ Consultando saldo de BTC...")
        saldo, transaccion = consultar_saldo_btc(addresses["Bitcoin"])
        if saldo is not None:
            print(f"💰 Saldo BTC: {saldo} BTC")
            if transaccion:
                print("📌 Última transacción:")
                print(f"   🔗 Hash: {transaccion['hash']}")
                print(f"   💸 Valor: {transaccion['valor']} BTC")
                print(f"   🕒 Fecha: {transaccion['fecha']}")
            else:
                print("📭 Sin transacciones en esta dirección.")
        else:
            print("⚠️ No se pudo consultar el saldo BTC.")
