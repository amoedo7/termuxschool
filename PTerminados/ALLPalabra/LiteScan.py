from ALLPalabra import obtener_direccion_litecoin
import requests
from bs4 import BeautifulSoup

def obtener_saldo_litecoin(direccion):
    url = f"https://blockchair.com/litecoin/address/{direccion}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        filas = soup.find_all('tr')
        for fila in filas:
            columnas = fila.find_all('td')
            if len(columnas) == 2 and "Saldo" in columnas[0].text:
                saldo = columnas[1].text.strip().replace("\xa0", " ")
                return saldo

        return "❌ No se encontró el saldo"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Uso
if __name__ == "__main__":
    direccion = obtener_direccion_litecoin()
    resultado = obtener_saldo_litecoin(direccion)
    print(f"📦 Dirección: {direccion}")
    print(f"💰 Saldo LTC: {resultado}")
