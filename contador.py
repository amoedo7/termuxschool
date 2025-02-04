import time

counter = 0
while True:
    with open("contador.txt", "w") as f:
        f.write(f"Contador: {counter}\n")
    counter += 1
    time.sleep(60)  # Suma 1 cada minuto
