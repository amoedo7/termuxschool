import tkinter as tk
from tkinter import filedialog, scrolledtext
import hashlib, ecdsa, base58, requests, datetime, threading, time
from Crypto.Hash import keccak
import os

# --- FUNCIONES CRIPTO ---
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
    hash160 = ripemd160(sha256(public_key))
    results = {
        "Bitcoin": base58check_encode(b'\x00', hash160),
        "Litecoin": base58check_encode(b'\x30', hash160),
        "Dogecoin": base58check_encode(b'\x1e', hash160),
        "BitcoinCash": base58check_encode(b'\x00', hash160),
        "Clams": base58check_encode(b'\x89', hash160),
        "Zcash": base58check_encode(b'\x1c\xb8', hash160),
        "Dash": base58check_encode(b'\x4c', hash160),
        "Ethereum": '0x' + keccak256(public_key[1:])[12:].hex(),
        "BNB": '0x' + keccak256(public_key[1:])[12:].hex()
    }
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

def consultar_saldo_sochain(moneda, direccion):
    try:
        url = f"https://sochain.com/api/v2/get_address_balance/{moneda}/{direccion}"
        r = requests.get(url, timeout=10).json()
        saldo = float(r['data']['confirmed_balance'])
        return saldo
    except Exception:
        return None

def tiene_transacciones_btc(direccion):
    try:
        url = f"https://mempool.space/api/address/{direccion}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("chain_stats", {}).get("tx_count", 0) > 0
    except Exception:
        return False
    return False

# --- FUNCIONES INTERFAZ ---
def mostrar_resultados(frase):
    priv, direcciones = generate_addresses(frase)
    salida_direcciones.delete("1.0", tk.END)
    salida_direcciones.insert(tk.END, f"🔐 Frase:\n{frase}\n\n🔑 Clave Privada:\n{priv}\n\n🏦 Direcciones:\n")
    for coin, addr in direcciones.items():
        salida_direcciones.insert(tk.END, f" - {coin}: {addr}\n")

    salida_saldo.delete("1.0", tk.END)
    salida_saldo.insert(tk.END, "\n⏳ Consultando saldo BTC...\n")
    saldo, tx = consultar_saldo_btc(direcciones["Bitcoin"])
    if saldo is not None:
        salida_saldo.insert(tk.END, f"💰 Saldo BTC: {saldo:.8f} BTC\n")
        if tx:
            salida_saldo.insert(tk.END, f"📌 Última transacción:\n")
            salida_saldo.insert(tk.END, f"   🔗 Hash: {tx['hash'][:30]}...\n")
            salida_saldo.insert(tk.END, f"   💸 Valor: {tx['valor']} BTC\n")
            salida_saldo.insert(tk.END, f"   🕒 Fecha: {tx['fecha']}\n")
            if auto_save_tx.get() and tx['valor'] > 0:
                guardar_frase(frase)
        else:
            salida_saldo.insert(tk.END, "📭 Sin transacciones registradas.\n")
        if auto_save_saldo.get() and saldo > 0:
            guardar_frase(frase)
    else:
        salida_saldo.insert(tk.END, f"⚠️ Error al consultar saldo BTC: {tx}\n")

    salida_saldo.insert(tk.END, "\n🔎 Saldos en otras monedas:\n")
    for coin, code in [("Litecoin", "LTC"), ("Dogecoin", "DOGE"), ("Dash", "DASH"), ("Zcash", "ZEC")]:
        direccion = direcciones[coin]
        saldo = consultar_saldo_sochain(code, direccion)
        if saldo is not None:
            salida_saldo.insert(tk.END, f" - {coin}: {saldo:.8f}\n")
            if saldo > 0 and auto_save_saldo.get():
                guardar_frase(frase)
        else:
            salida_saldo.insert(tk.END, f" - {coin}: ❌ Error al consultar\n")

    # Verificación extra con mempool (opcional)
    if tiene_transacciones_btc(direcciones["Bitcoin"]):
        salida_saldo.insert(tk.END, "✅ Verificado: Tiene transacciones BTC registradas en mempool.space\n")

def generar():
    frase = entrada.get()
    if not frase.strip(): return
    mostrar_resultados(frase)

def guardar_frase(frase=None):
    frase = frase or entrada.get()
    if not frase.strip(): return
    with open("FrasesSaves.txt", "a") as f:
        f.write(frase + "\n")

def leer_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path: return
    def procesar():
        with open(file_path, "r") as f:
            for linea in f:
                frase = linea.strip()
                if frase:
                    entrada.delete(0, tk.END)
                    entrada.insert(0, frase)
                    mostrar_resultados(frase)
                    time.sleep(10)
    threading.Thread(target=procesar, daemon=True).start()

# --- INTERFAZ TK ---
app = tk.Tk()
app.title("🧠 BrainCrack v2.1")
app.geometry("980x600")
app.config(bg="black")

fuente = ("Consolas", 11)
verde = "#00FF00"

frame_top = tk.Frame(app, bg="black")
frame_top.pack(pady=5)

entrada = tk.Entry(frame_top, font=fuente, width=60, bg="#111", fg=verde, insertbackground=verde)
entrada.grid(row=0, column=0, padx=5)

tk.Button(frame_top, text="🧠 Generar Dirección", command=generar, font=fuente, bg="#003300", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_top, text="💾 Guardar Frase", command=guardar_frase, font=fuente, bg="#333300", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame_top, text="📂 Leer Archivo", command=leer_archivo, font=fuente, bg="#003366", fg="white").grid(row=0, column=3, padx=5)

frame_auto = tk.Frame(app, bg="black")
frame_auto.pack()

auto_save_saldo = tk.BooleanVar(value=False)
auto_save_tx = tk.BooleanVar(value=False)

tk.Checkbutton(frame_auto, text="Guardar si Saldo > 0", variable=auto_save_saldo, font=fuente, bg="black", fg=verde, selectcolor="black", activebackground="black", activeforeground="green").pack(side="left", padx=10)
tk.Checkbutton(frame_auto, text="Guardar si Tx > 0", variable=auto_save_tx, font=fuente, bg="black", fg=verde, selectcolor="black", activebackground="black", activeforeground="green").pack(side="left", padx=10)

frame_main = tk.Frame(app, bg="black")
frame_main.pack(expand=True, fill="both", padx=10, pady=10)

salida_direcciones = scrolledtext.ScrolledText(frame_main, font=fuente, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD, width=60)
salida_direcciones.pack(side="left", expand=True, fill="both", padx=5)

salida_saldo = scrolledtext.ScrolledText(frame_main, font=fuente, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD, width=60)
salida_saldo.pack(side="right", expand=True, fill="both", padx=5)

app.mainloop()
