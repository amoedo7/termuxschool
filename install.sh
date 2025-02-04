#!/bin/bash

# Actualiza el sistema y las dependencias
echo "Actualizando el sistema..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Instala Git si no está instalado
echo "Instalando Git..."
sudo apt-get install git -y

# Instala Python si no está instalado
echo "Instalando Python..."
sudo apt-get install python3 python3-pip -y

# Instala dependencias necesarias
echo "Instalando dependencias de Python..."
pip3 install -r requirements.txt

# Configura el repositorio de Git
echo "Configurando Git..."
git config --global user.name "TuNombre"  # Cambia con tu nombre de usuario
git config --global user.email "tu_email@dominio.com"  # Cambia con tu correo

# Crea el repositorio local y lo conecta a GitHub
echo "Conectando a GitHub..."
git init
git remote add origin https://github.com/amoedo7/termuxschool.git  # Cambia la URL si es necesario

# Crea el archivo contador.py con el script del contador
echo "Creando el archivo contador.py..."
cat <<EOF > contador.py
import time

counter = 0
while True:
    print("Contador:", counter)
    counter += 1
    time.sleep(60)  # Suma 1 cada minuto
EOF

# Crea el flujo de trabajo para GitHub Actions (Auto-run)
echo "Creando archivo de workflow en .github/workflows/Auto-run.yml..."
mkdir -p .github/workflows
cat <<EOF > .github/workflows/Auto-run.yml
name: Auto-run

on:
  push:
    branches:
      - main
  schedule:
    - cron: '*/5 * * * *'  # Ejecutar cada 5 minutos

jobs:
  run-counter:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Run contador.py
      run: |
        python3 contador.py
EOF

# Realiza commit y push de los archivos al repositorio
echo "Haciendo commit y push a GitHub..."
git add .
git commit -m "Agregado script del contador y flujo de trabajo de auto-run"
git push origin main

echo "Instalación y configuración completadas. El contador debería ejecutarse en GitHub Actions."
