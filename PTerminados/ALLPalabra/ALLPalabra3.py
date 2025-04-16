import tkinter as tk
from tkinter import ttk, scrolledtext
import hashlib, ecdsa, base58, requests, datetime, os
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

def guardar_frase():
    frase = entrada.get()
    if not frase.strip():
        return
    with open("FrasesSaves.txt", "a", encoding="utf-8") as f:
        f.write(frase.strip() + "\n")
    salida_general.insert(tk.END, f"\n💾 Frase guardada en FrasesSaves.txt\n")

def generar():
    frase = entrada.get().strip()
    if not frase:
        salida_general.insert(tk.END, "\n⚠️ Ingrese una frase.\n")
        return
    salida_general.delete("1.0", tk.END)
    salida_direcciones.delete("1.0", tk.END)
    salida_saldos.delete("1.0", tk.END)

    salida_general.insert(tk.END, f"\n🔐 Frase: {frase}\n")
    priv, direcciones = generate_addresses(frase)
    salida_general.insert(tk.END, f"🔑 Clave Privada:\n{priv}\n")

    salida_direcciones.insert(tk.END, "\n🏦 Direcciones:\n")
    for coin, addr in direcciones.items():
        salida_direcciones.insert(tk.END, f" - {coin}: {addr}\n")

    salida_saldos.insert(tk.END, "\n⏳ Consultando saldo BTC...\n")
    saldo, tx = consultar_saldo_btc(direcciones["Bitcoin"])
    if saldo is not None:
        salida_saldos.insert(tk.END, f"💰 Saldo BTC: {saldo:.8f} BTC\n")
        if tx:
            salida_saldos.insert(tk.END, f"📌 Última transacción:\n")
            salida_saldos.insert(tk.END, f"   🔗 Hash: {tx['hash'][:30]}...\n")
            salida_saldos.insert(tk.END, f"   💸 Valor: {tx['valor']} BTC\n")
            salida_saldos.insert(tk.END, f"   🕒 Fecha: {tx['fecha']}\n")
        else:
            salida_saldos.insert(tk.END, "📭 Sin transacciones registradas.\n")
    else:
        salida_saldos.insert(tk.END, f"⚠️ Error al consultar saldo BTC: {tx}\n")

# --- INTERFAZ ---
app = tk.Tk()
app.title("🧠 BrainCrack v1.1")
app.geometry("800x650")
app.config(bg="black")

fuente = ("Consolas", 11)
verde = "#00FF00"

# Entrada
tk.Label(app, text="Ingrese frase:", bg="black", fg=verde, font=fuente).pack(pady=5)
entrada = tk.Entry(app, font=fuente, width=60, bg="#111", fg=verde, insertbackground=verde)
entrada.pack(pady=5)

# Botones
frame_botones = tk.Frame(app, bg="black")
frame_botones.pack(pady=5)
tk.Button(frame_botones, text="🧠 Generar Dirección", command=generar, font=fuente, bg="#003300", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="💾 Guardar Frase", command=guardar_frase, font=fuente, bg="#222", fg="white").pack(side=tk.LEFT, padx=5)

# Resultado general (Frase + Clave Privada)
salida_general = scrolledtext.ScrolledText(app, font=fuente, height=6, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD)
salida_general.pack(fill="x", padx=10, pady=10)

# Solapas
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

style = ttk.Style()
style.theme_use('default')
style.configure("TNotebook", background="black", borderwidth=0)
style.configure("TNotebook.Tab", background="#222", foreground=verde, padding=10)
style.map("TNotebook.Tab", background=[("selected", "#005500")], foreground=[("selected", "white")])

# Tab 1 - Direcciones
tab_direcciones = tk.Frame(notebook, bg="black")
salida_direcciones = scrolledtext.ScrolledText(tab_direcciones, font=fuente, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD)
salida_direcciones.pack(expand=True, fill="both", padx=10, pady=10)
notebook.add(tab_direcciones, text="📬 Direcciones")

# Tab 2 - Saldos
tab_saldos = tk.Frame(notebook, bg="black")
salida_saldos = scrolledtext.ScrolledText(tab_saldos, font=fuente, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD)
salida_saldos.pack(expand=True, fill="both", padx=10, pady=10)
notebook.add(tab_saldos, text="💰 Saldos")

app.mainloop()
