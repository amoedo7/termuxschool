# DashScan.py

import requests
from bs4 import BeautifulSoup

def obtener_info_dash(direccion):
    url = f"https://explorer.dash.org/insight/address/{direccion}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        print(f"\n📊 Información para: {direccion}")

        tabla = soup.find("table", class_="table")
        filas = tabla.find_all("tr")

        total_recibido = filas[0].find_all("td")[1].text.strip()
        total_enviado  = filas[1].find_all("td")[1].text.strip()
        balance_final  = filas[2].find_all("td")[1].text.strip()
        transacciones  = filas[3].find_all("td")[1].text.strip()

        print(f"📥 Total Recibido: {total_recibido}")
        print(f"📤 Total Enviado:  {total_enviado}")
        print(f"💰 Balance Final:  {balance_final}")
        print(f"📨 Transacciones:  {transacciones}")

    except Exception as e:
        print(f"❌ Error al obtener datos de Dash Explorer: {e}")


if __name__ == "__main__":
    direccion = "XwSweAMiFYpUjdo1ERygedreiMFHjMxDSY"
    obtener_info_dash(direccion)
