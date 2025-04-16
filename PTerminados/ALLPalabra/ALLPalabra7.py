import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import hashlib
import ecdsa
import base58
import requests
import datetime
import threading
from Crypto.Hash import keccak

# --- FUNCIONES CRIPTOGRÁFICAS ---

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

# --- FUNCIONES DE CONSULTA DE SALDOS ---

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

def consultar_saldo_etherscan(direccion, api_key="YourEtherscanAPIKey"):
    try:
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={direccion}&tag=latest&apikey={api_key}"
        r = requests.get(url, timeout=10).json()
        saldo = int(r['result']) / 10**18
        return saldo
    except Exception:
        return None

def consultar_saldo_bscscan(direccion, api_key="YourBscscanAPIKey"):
    try:
        url = f"https://api.bscscan.com/api?module=account&action=balance&address={direccion}&tag=latest&apikey={api_key}"
        r = requests.get(url, timeout=10).json()
        saldo = int(r['result']) / 10**18
        return saldo
    except Exception:
        return None

# --- FUNCIONES DE INTERFAZ GRÁFICA ---

def mostrar_resultados(frase):
    priv, direcciones = generate_addresses(frase)
    salida_direcciones.delete("1.0", tk.END)
    salida_direcciones.insert(tk.END, f"🔐 Frase:\n{frase}\n\n🔑 Clave Privada:\n{priv}\n\n🏦 Direcciones:\n")
    for coin, addr in direcciones.items():
        salida_direcciones.insert(tk.END, f" - {coin}: {addr}\n")

    salida_saldo.delete("1.0", tk.END)
    salida_saldo.insert(tk.END, "\n⏳ Consultando saldos...\n")

    # Consultar saldos
    saldos = {}
    saldos["Bitcoin"], _ = consultar_saldo_btc(direcciones["Bitcoin"])
    saldos["Litecoin"] = consultar_saldo_sochain("LTC", direcciones["Litecoin"])
    saldos["Dogecoin"] = consultar_saldo_sochain("DOGE", direcciones["Dogecoin"])
    saldos["Dash"] = consultar_saldo_sochain("DASH", direcciones["Dash"])
    saldos["Zcash"] = consultar_saldo_sochain("ZEC", direcciones["Zcash"])
    saldos["Ethereum"] = consultar_saldo_etherscan(direcciones["Ethereum"])
    saldos["BNB"] = consultar_saldo_bscscan(direcciones["BNB"])

    for coin, saldo in saldos.items():
        if saldo is not None:
            salida_saldo.insert(tk.END, f" - {coin}: {saldo:.8f}\n")
            if saldo > 0 and auto_save_saldo.get():
                guardar_frase(frase)
        else:
            salida_saldo.insert(tk.END, f" - {coin}: ❌ Error al consultar\n")

def generar():
    frase = entrada.get()
    if not frase.strip():
        messagebox.showwarning("Advertencia", "La frase no puede estar vacía.")
        return
    mostrar_resultados(frase)

def guardar_frase(frase=None):
    if not frase:
        frase = entrada.get()
    with open("FrasesGuardadas.txt", "a", encoding="utf-8") as f:
        f.write(frase + "\n")
    messagebox.showinfo("Guardado", "Frase guardada correctamente.")

def guardar_como():
    texto = salida_direcciones.get("1.0", tk.END)
    archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(texto)
        messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")

def ejecutar_en_hilo():
    threading.Thread(target=generar, daemon=True).start()

# --- INTERFAZ GRÁFICA TKINTER ---

app = tk.Tk()
app.title("Generador de CriptoDirecciones & Buscador de Saldo")
app.geometry("900x650")
app.config(bg="#111")

tk.Label(app, text="🔐 Frase semilla:", fg="white", bg="#111", font=("Arial", 12)).pack(pady=5)
entrada = tk.Entry(app, width=80, font=("Arial", 12))
entrada.pack(pady=5)

frame_botones = tk.Frame(app, bg="#111")
frame_botones.pack()

tk.Button(frame_botones, text="🚀 Generar", command=ejecutar_en_hilo, bg="green", fg="white",
          font=("Arial", 12), width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="💾 Guardar", command=guardar_frase, bg="#007ACC", fg="white",
          font=("Arial", 12), width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="📝 Exportar", command=guardar_como, bg="#444", fg="white",
          font=("Arial", 12), width=12).pack(side=tk.LEFT, padx=5)

auto_save_saldo = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Guardar frase si tiene saldo", variable=auto_save_saldo,
               bg="#111", fg="white", selectcolor="#222", font=("Arial", 10)).pack()

tk.Label(app, text="📄 Claves y Direcciones:", fg="white", bg="#111", font=("Arial", 12)).pack(pady=5)
salida_direcciones = scrolledtext.ScrolledText(app, width=100, height=12, font=("Courier", 10))
salida_direcciones.pack()

tk.Label(app, text="💰 Saldos detectados:", fg="white", bg="#111", font=("Arial", 12)).pack(pady=5)
salida_saldo = scrolledtext.ScrolledText(app, width=100, height=10, font=("Courier", 10))
salida_saldo.pack()

app.mainloop()
