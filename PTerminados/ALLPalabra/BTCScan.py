import requests

def get_btc_balance(address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        balance = data['final_balance'] / 1e8
        print(f"💰 Dirección: {address}\n🔎 Balance: {balance:.8f} BTC")
    else:
        print("⚠️ Error al consultar la dirección.")

if __name__ == "__main__":
    addr = input("🔗 Dirección BTC: ").strip()
    get_btc_balance(addr)
