from ALLPalabra import obtener_direccion_dogecoin
import requests
from bs4 import BeautifulSoup

def obtener_saldo_dogecoin(direccion):
    url = f"https://www.oklink.com/es-la/doge/address/{direccion}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        bloques = soup.find_all("div", class_="index_item__8pabE")
        for bloque in bloques:
            titulo = bloque.find("div", class_="index_text__0nUfQ")
            if titulo and "Saldo en DOGE" in titulo.text:
                saldo_tag = bloque.find("div", class_="index_value__ErIti")
                if saldo_tag:
                    saldo = saldo_tag.get_text(strip=True).replace("DOGE", "").strip()
                    return saldo

        return "❌ No se encontró el saldo"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Uso
if __name__ == "__main__":
    direccion = obtener_direccion_dogecoin()
    resultado = obtener_saldo_dogecoin(direccion)
    print(f"🐶 Dirección DOGE: {direccion}")
    print(f"💰 Saldo DOGE: {resultado}")
