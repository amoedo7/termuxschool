import tkinter as tk
from tkinter import scrolledtext
import hashlib, ecdsa, base58, requests, datetime
from Crypto.Hash import keccak

def sha256(data): return hashlib.sha256(data).digest()
def ripemd160(data): h = hashlib.new('ripemd160'); h.update(data); return h.digest()
def base58check_encode(prefix, payload):
    data = prefix + payload
    checksum = sha256(sha256(data))[:4]
    return base58.b58encode(data + checksum).decode()
def keccak256(data):
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

def generate_addresses(phrase):
    private_key = sha256(phrase.encode())
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    public_key_compressed = (
        b'\x02' + vk.to_string()[:32] if vk.to_string()[-1] % 2 == 0
        else b'\x03' + vk.to_string()[:32]
    )

    results = {}
    hash160 = ripemd160(sha256(public_key))

    results["Bitcoin"]      = base58check_encode(b'\x00', hash160)
    results["Litecoin"]     = base58check_encode(b'\x30', hash160)
    results["Dogecoin"]     = base58check_encode(b'\x1e', hash160)
    results["BitcoinCash"]  = base58check_encode(b'\x00', hash160)
    results["Clams"]        = base58check_encode(b'\x89', hash160)
    results["Zcash"]        = base58check_encode(b'\x1c\xb8', hash160)
    results["Dash"]         = base58check_encode(b'\x4c', hash160)
    
    eth_address = '0x' + keccak256(public_key[1:])[12:].hex()
    results["Ethereum"]     = eth_address
    results["BNB"]          = eth_address

    return private_key.hex(), results

def consultar_saldo_btc(direccion):
    try:
        api_url = f"https://blockchain.info/rawaddr/{direccion}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            saldo = int(data.get("final_balance", 0)) / 100_000_000
            tx = data.get("txs", [])[0] if data.get("txs") else None
            if tx:
                valor = sum(o["value"] for o in tx["out"]) / 100_000_000
                fecha = datetime.datetime.utcfromtimestamp(tx["time"]).strftime('%Y-%m-%d %H:%M:%S UTC')
                return saldo, {"hash": tx["hash"], "valor": valor, "fecha": fecha}
            return saldo, None
    except Exception as e:
        return None, str(e)
    return None, None

def generar():
    frase = entrada.get()
    if not frase:
        salida.insert(tk.END, "\n⚠️ Ingrese una frase.\n")
        return
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, f"\n🔐 Frase: {frase}\n")
    priv, direcciones = generate_addresses(frase)
    salida.insert(tk.END, f"🔑 Clave Privada:\n{priv}\n\n🏦 Direcciones:\n")
    for coin, addr in direcciones.items():
        salida.insert(tk.END, f" - {coin}: {addr}\n")

    salida.insert(tk.END, "\n⏳ Consultando saldo BTC...\n")
    saldo, tx = consultar_saldo_btc(direcciones["Bitcoin"])
    if saldo is not None:
        salida.insert(tk.END, f"💰 Saldo BTC: {saldo:.8f} BTC\n")
        if tx:
            salida.insert(tk.END, f"📌 Última transacción:\n")
            salida.insert(tk.END, f"   🔗 Hash: {tx['hash'][:30]}...\n")
            salida.insert(tk.END, f"   💸 Valor: {tx['valor']} BTC\n")
            salida.insert(tk.END, f"   🕒 Fecha: {tx['fecha']}\n")
        else:
            salida.insert(tk.END, "📭 Sin transacciones registradas.\n")
    else:
        salida.insert(tk.END, f"⚠️ Error al consultar saldo BTC: {tx}\n")

# Interfaz estilo hacker
app = tk.Tk()
app.title("🧠 BrainCrack v1.0")
app.geometry("780x600")
app.config(bg="black")

fuente = ("Consolas", 11)
verde = "#00FF00"

tk.Label(app, text="Ingrese frase:", bg="black", fg=verde, font=fuente).pack(pady=5)
entrada = tk.Entry(app, font=fuente, width=60, bg="#111", fg=verde, insertbackground=verde)
entrada.pack(pady=5)

tk.Button(app, text="🧠 Generar Dirección", command=generar, font=fuente, bg="#003300", fg="white").pack(pady=5)

salida = scrolledtext.ScrolledText(app, font=fuente, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD)
salida.pack(expand=True, fill="both", padx=10, pady=10)

app.mainloop()
