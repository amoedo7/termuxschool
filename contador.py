import time

# Nombre del archivo donde guardaremos el contador
contador_file = 'contador.txt'

# Intentamos leer el contador desde el archivo si existe
try:
    with open(contador_file, 'r') as f:
        contador = int(f.read())  # Leemos el contador como un entero
except FileNotFoundError:
    contador = 0  # Si no existe el archivo, iniciamos el contador en 0

# Incrementamos el contador
contador += 1

# Guardamos el nuevo valor del contador en el archivo
with open(contador_file, 'w') as f:
    f.write(str(contador))  # Guardamos el contador como texto

print(f"Contador actualizado: {contador}")
