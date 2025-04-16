from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Opciones para que no se abra ventana
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Reemplazá por la dirección que querés consultar
direccion = "qr3mn246hz4l9ppsmr6thym3rq2my0pp2ufx8es556"
url = f"https://www.blockchain.com/explorer/addresses/bch/{direccion}"

# Iniciamos Selenium
driver = webdriver.Chrome(options=options)
driver.get(url)

# Esperamos un poco que cargue JS
time.sleep(5)

# Buscamos el resumen
resumen_elementos = driver.find_elements(By.CLASS_NAME, "sc-92d5245a-2")
valores = [e.text for e in resumen_elementos]

print("💰 Total Recibido:", valores[0])
print("📤 Total Enviado:", valores[1])
print("🔁 Volumen Total:", valores[2])
print("📄 Transacciones:", valores[3])

# También podés buscar IDs de transacciones
transacciones = driver.find_elements(By.CLASS_NAME, "sc-c317e547-9")
ids = [e.text for e in transacciones if "-" in e.text]
print("\n🧾 Transacciones encontradas:")
for tx in ids:
    print("🆔", tx)

driver.quit()
