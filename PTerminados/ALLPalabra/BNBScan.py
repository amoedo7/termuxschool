# BNBScan.py

import requests
from bs4 import BeautifulSoup

def obtener_info_bnb(direccion):
    url = f"https://bscscan.com/address/{direccion}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # Extraer balance
        balance_div = soup.find('div', string='BNB Balance')
        if balance_div:
            balance_value = balance_div.find_next('div').text.strip()
        else:
            balance_value = "No encontrado"

        # Extraer valor en USD
        value_div = soup.find('div', string='BNB Value')
        if value_div:
            usd_value = value_div.find_next('div').text.strip()
        else:
            usd_value = "No encontrado"

        # Extraer transacciones
        tx_div = soup.find('div', string='Transactions Sent')
        if tx_div:
            tx_info = tx_div.find_next('div').text.strip().replace('\n', ' ')
        else:
            tx_info = "No encontrado"

        print(f"\n📊 Información para: {direccion}")
        print(f"🔹 Balance: {balance_value}")
        print(f"💵 Valor USD: {usd_value}")
        print(f"📨 Transacciones: {tx_info}")

    except Exception as e:
        print(f"❌ Error al obtener datos de BscScan: {e}")


if __name__ == "__main__":
    direccion = "0x2a0db1c3c1049f38c4e03d9c8bdfbf05930578c5"
    obtener_info_bnb(direccion)
