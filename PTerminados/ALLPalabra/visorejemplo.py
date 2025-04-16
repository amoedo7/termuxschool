import tkinter as tk
from tkinter import ttk
import webview

# Datos de ejemplo
frase = "love"
clave_privada = "686f746a95b6f836d7d70567c302c3f9ebb5ee0def3d1220ee9d4e9f34f5e131"
direcciones = {
    "Bitcoin": "1Mm6ouhpHqbtahCRNYfTo7Art1fbmk7PcR",
    "Litecoin": "Lfz4581eNVqwqVtaYgem58Ed6E2sqaeoAi",
    "Dogecoin": "DRuCMAeTbFWB7hP278f2LsLTm9Pu6AWYYr",
    "BitcoinCash": "1Mm6ouhpHqbtahCRNYfTo7Art1fbmk7PcR",
    "Clams": "xV4jhnYHZZ5vd5JHj2J8EHTe77xq9WjK3r",
    "Zcash": "t1edhpF7xGAPVBLFKJyUavvGn8frgYijQFp",
    "Dash": "XwSweAMiFYpUjdo1ERygedreiMFHjMxDSY",
    "Ethereum": "0x2a0db1c3c1049f38c4e03d9c8bdfbf05930578c5",
    "BNB": "0x2a0db1c3c1049f38c4e03d9c8bdfbf05930578c5"
}
exploradores = {
    "Bitcoin": f"https://www.blockchain.com/explorer/search?search={direcciones['Bitcoin']}",
    "Litecoin": f"https://litecoinspace.org/es/address/{direcciones['Litecoin']}",
    "Dogecoin": f"https://www.oklink.com/es-la/doge/address/{direcciones['Dogecoin']}",
    "BitcoinCash": f"https://www.blockchain.com/explorer/addresses/bch/{direcciones['BitcoinCash']}",
    "Dash": f"https://www.oklink.com/es-la/dash/address/{direcciones['Dash']}",
    "Ethereum": f"https://etherscan.io/address/{direcciones['Ethereum']}",
    "BNB": f"https://bscscan.com/address/{direcciones['BNB']}"
    # Clams y Zcash los dejamos para después
}

# -------- Interfaz Principal (Tkinter) ----------
root = tk.Tk()
root.title("CriptoScan Underground")
root.geometry("900x600")
root.configure(bg="#111")

# -------- Frame Superior Izquierda (Frase + Claves + Direcciones) ----------
left_frame = tk.Frame(root, bg="#111", width=450)
left_frame.pack(side="left", fill="both", expand=True)

tk.Label(left_frame, text="🔐 Frase:", fg="#0f0", bg="#111", font=("Courier", 12)).pack(anchor="w", padx=10)
tk.Label(left_frame, text=frase, fg="white", bg="#111", font=("Courier", 10)).pack(anchor="w", padx=20)

tk.Label(left_frame, text="\n🔑 Clave Privada:", fg="#0f0", bg="#111", font=("Courier", 12)).pack(anchor="w", padx=10)
tk.Label(left_frame, text=clave_privada, fg="white", bg="#111", font=("Courier", 9)).pack(anchor="w", padx=20)

tk.Label(left_frame, text="\n🏦 Direcciones:", fg="#0f0", bg="#111", font=("Courier", 12)).pack(anchor="w", padx=10)
for cripto, address in direcciones.items():
    tk.Label(left_frame, text=f" - {cripto}: {address}", fg="white", bg="#111", font=("Courier", 9)).pack(anchor="w", padx=20)

# -------- Frame Superior Derecha (Saldo BTC) ----------
right_frame = tk.Frame(root, bg="#111", width=450)
right_frame.pack(side="right", fill="both", expand=True)

tk.Label(right_frame, text="⏳ Consultando saldo BTC...", fg="#0ff", bg="#111", font=("Courier", 12)).pack(anchor="w", padx=10, pady=10)
tk.Label(right_frame, text="💰 Saldo BTC: 0.00000000 BTC", fg="white", bg="#111", font=("Courier", 12)).pack(anchor="w", padx=10)
tk.Label(right_frame, text="📌 Última transacción:", fg="#0ff", bg="#111", font=("Courier", 11)).pack(anchor="w", padx=10, pady=5)
tk.Label(right_frame, text=" 🔗 Hash: 56025d6d46cd4dd6b91be02498546e...", fg="white", bg="#111", font=("Courier", 9)).pack(anchor="w", padx=20)
tk.Label(right_frame, text=" 💸 Valor: 0.0095 BTC", fg="white", bg="#111", font=("Courier", 9)).pack(anchor="w", padx=20)
tk.Label(right_frame, text=" 🕒 Fecha: 2012-08-30 09:26:46 UTC", fg="white", bg="#111", font=("Courier", 9)).pack(anchor="w", padx=20)

# -------- WebView inferior en ventana separada (por ahora) ----------
def abrir_navegador(cripto):
    url = exploradores.get(cripto)
    if url:
        webview.create_window(f'{cripto} Explorer', url, width=1000, height=600)
        webview.start()

# -------- Tabs con botones ----------
tab_frame = tk.Frame(root, bg="#111")
tab_frame.pack(side="bottom", fill="x")

tk.Label(tab_frame, text="🔍 Navegadores Cripto:", bg="#111", fg="#0f0", font=("Courier", 12)).pack(anchor="w", padx=10)

for cripto in exploradores:
    btn = tk.Button(tab_frame, text=cripto, command=lambda c=cripto: abrir_navegador(c), bg="#222", fg="#0f0", font=("Courier", 10))
    btn.pack(side="left", padx=5, pady=5)

root.mainloop()
