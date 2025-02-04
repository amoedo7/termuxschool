import time
import os

# Verificar si el archivo existe para leer el contador guardado
if os.path.exists("contador.txt"):
    with open("contador.txt", "r") as f:
        counter = int(f.read())
else:
    counter = 0

while True:
    print("Contador:", counter)
    counter += 1
    
    # Guardar el contador actualizado en el archivo
    with open("contador.txt", "w") as f:
        f.write(str(counter))
    
    time.sleep(60)  # Suma 1 cada minuto
