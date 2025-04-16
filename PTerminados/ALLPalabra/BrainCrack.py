import tkinter as tk
from tkinter import filedialog, scrolledtext
import hashlib, ecdsa, base58, requests, datetime, threading, time, json
from Crypto.Hash import keccak

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
    hash160 = ripemd160(sha256(public_key))
    eth_addr = '0x' + keccak256(public_key[1:])[12:].hex()
    results = {
        "Bitcoin": base58check_encode(b'\x00', hash160),
        "Ethereum": eth_addr,
        "BNB": eth_addr,
        "Litecoin": base58check_encode(b'\x30', hash160),
        "Dogecoin": base58check_encode(b'\x1e', hash160),
    }
    return private_key.hex(), results

# --- CONSULTAS DE SALDO ---
def consultar_saldo_btc(direccion):
    try:
        url = f"https://blockchain.info/rawaddr/{direccion}"
        r = requests.get(url, timeout=10)
        if r.ok:
            data = r.json()
            saldo = int(data["final_balance"]) / 100_000_000
            tx = data["txs"][0] if data.get("txs") else None
            if tx:
                valor = sum(o["value"] for o in tx["out"]) / 100_000_000
                fecha = datetime.datetime.utcfromtimestamp(tx["time"]).strftime('%Y-%m-%d %H:%M:%S')
                return saldo, {"hash": tx["hash"], "valor": valor, "fecha": fecha}
            return saldo, None
    except Exception as e:
        return None, str(e)

def consultar_saldo_blockchair(coin, address):
    try:
        url = f"https://api.blockchair.com/{coin}/dashboards/address/{address}"
        r = requests.get(url, timeout=10)
        if r.ok:
            data = r.json()["data"][address]["address"]
            saldo = float(data.get("balance", 0)) / 10**18
            return saldo
    except Exception as e:
        return None

# --- GUARDADO ---
def guardar_frase(frase):
    if not frase.strip(): return
    with open("FrasesSaves.txt", "a") as f:
        f.write(frase + "\n")

def log_found(data):
    with open("LogFound.json", "a") as f:
        f.write(json.dumps(data) + "\n")

# --- INTERFAZ ---
def mostrar_resultados(frase):
    priv, direcciones = generate_addresses(frase)
    salida_direcciones.delete("1.0", tk.END)
    salida_direcciones.insert(tk.END, f"🔐 Frase:\n{frase}\n\n🔑 Clave Privada:\n{priv}\n\n🏦 Direcciones:\n")
    for coin, addr in direcciones.items():
        salida_direcciones.insert(tk.END, f" - {coin}: {addr}\n")

    salida_saldo.delete("1.0", tk.END)
    salida_saldo.insert(tk.END, "⏳ Consultando saldos...\n")

    data_log = {"frase": frase, "priv": priv, "direcciones": direcciones, "saldos": {}}
    guardado = False

    # --- Bitcoin ---
    saldo_btc, tx = consultar_saldo_btc(direcciones["Bitcoin"])
    if saldo_btc is not None:
        salida_saldo.insert(tk.END, f"\n₿ BTC: {saldo_btc:.8f} BTC\n")
        data_log["saldos"]["BTC"] = saldo_btc
        if saldo_btc > 0 and auto_save_saldo.get():
            guardar_frase(frase)
            guardado = True
        if tx:
            salida_saldo.insert(tk.END, f"   📌 Última Tx: {tx['hash'][:28]}...\n   💸 {tx['valor']} BTC el {tx['fecha']}\n")
            if auto_save_tx.get() and tx['valor'] > 0:
                guardar_frase(frase)
                guardado = True
    else:
        salida_saldo.insert(tk.END, "⚠️ Error al consultar BTC\n")

    # --- Ethereum ---
    saldo_eth = consultar_saldo_blockchair("ethereum", direcciones["Ethereum"])
    if saldo_eth is not None:
        salida_saldo.insert(tk.END, f"\n🦊 ETH: {saldo_eth:.8f} ETH\n")
        data_log["saldos"]["ETH"] = saldo_eth
        if saldo_eth > 0 and auto_save_saldo.get():
            guardar_frase(frase)
            guardado = True
    else:
        salida_saldo.insert(tk.END, "⚠️ Error al consultar ETH\n")

    # --- Binance ---
    saldo_bnb = consultar_saldo_blockchair("binance-smart-chain", direcciones["BNB"])
    if saldo_bnb is not None:
        salida_saldo.insert(tk.END, f"\n🔶 BNB: {saldo_bnb:.8f} BNB\n")
        data_log["saldos"]["BNB"] = saldo_bnb
        if saldo_bnb > 0 and auto_save_saldo.get():
            guardar_frase(frase)
            guardado = True
    else:
        salida_saldo.insert(tk.END, "⚠️ Error al consultar BNB\n")

    if guardado:
        log_found(data_log)

def generar():
    frase = entrada.get()
    if not frase.strip(): return
    mostrar_resultados(frase)

def leer_archivo():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not path: return
    def procesar():
        with open(path) as f:
            for linea in f:
                frase = linea.strip()
                if frase:
                    entrada.delete(0, tk.END)
                    entrada.insert(0, frase)
                    mostrar_resultados(frase)
                    time.sleep(10)
    threading.Thread(target=procesar, daemon=True).start()

# --- UI ---
app = tk.Tk()
app.title("🧠 BrainCrack v2.5 - MultiChain Balance Checker")
app.geometry("1000x620")
app.config(bg="black")

fuente = ("Consolas", 11)
verde = "#00FF00"

frame_top = tk.Frame(app, bg="black")
frame_top.pack(pady=5)
entrada = tk.Entry(frame_top, font=fuente, width=60, bg="#111", fg=verde, insertbackground=verde)
entrada.grid(row=0, column=0, padx=5)
tk.Button(frame_top, text="🧠 Generar", command=generar, font=fuente, bg="#003300", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_top, text="💾 Guardar", command=guardar_frase, font=fuente, bg="#333300", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame_top, text="📂 Leer Archivo", command=leer_archivo, font=fuente, bg="#003366", fg="white").grid(row=0, column=3, padx=5)

frame_auto = tk.Frame(app, bg="black")
frame_auto.pack()
auto_save_saldo = tk.BooleanVar(value=False)
auto_save_tx = tk.BooleanVar(value=False)
tk.Checkbutton(frame_auto, text="Guardar si Saldo > 0", variable=auto_save_saldo, font=fuente, bg="black", fg=verde, selectcolor="black").pack(side="left", padx=10)
tk.Checkbutton(frame_auto, text="Guardar si Tx > 0", variable=auto_save_tx, font=fuente, bg="black", fg=verde, selectcolor="black").pack(side="left", padx=10)

frame_main = tk.Frame(app, bg="black")
frame_main.pack(expand=True, fill="both", padx=10, pady=10)

salida_direcciones = scrolledtext.ScrolledText(frame_main, font=fuente, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD, width=60)
salida_direcciones.pack(side="left", expand=True, fill="both", padx=5)
salida_saldo = scrolledtext.ScrolledText(frame_main, font=fuente, bg="black", fg=verde, insertbackground=verde, wrap=tk.WORD, width=60)
salida_saldo.pack(side="right", expand=True, fill="both", padx=5)

app.mainloop()
