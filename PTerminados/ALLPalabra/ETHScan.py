# ETHScan.py

import requests
from bs4 import BeautifulSoup

def obtener_info_eth(direccion):
    url = f"https://etherscan.io/address/{direccion}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        print(f"\n📊 Información para: {direccion}")

        # Buscar balance y USD (usando atributos más confiables)
        balance_tag = soup.find("span", {"id": "ContentPlaceHolder1_divSummary"}).find("div", class_="card-body").find("div", class_="row align-items-center").find_all("div")[1]
        eth_balance = balance_tag.text.strip().split("Ether")[0].strip()

        usd_tag = soup.find("span", {"id": "ContentPlaceHolder1_divSummary"}).find("div", class_="card-body").find("div", class_="row align-items-center").find_all("div")[2]
        usd_value = usd_tag.text.strip().split("@")[0].strip()

        # Transacciones (puede que no esté siempre)
        tx_div = soup.find("div", class_="col-md-6").find("div", class_="card-body")
        tx_count = "No encontrado"
        if tx_div:
            for d in tx_div.find_all("div", class_="row"):
                if "Transactions" in d.text:
                    tx_count = d.find_all("div")[-1].text.strip()
                    break

        print(f"🔹 Balance ETH: {eth_balance}")
        print(f"💵 Valor USD: {usd_value}")
        print(f"📨 Transacciones: {tx_count}")

    except Exception as e:
        print(f"❌ Error al obtener datos de Etherscan: {e}")


if __name__ == "__main__":
    direccion = "0x2a0db1c3c1049f38c4e03d9c8bdfbf05930578c5"
    obtener_info_eth(direccion)
