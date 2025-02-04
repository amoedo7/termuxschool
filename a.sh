#!/bin/bash

# Cargar el token de GitHub desde claves.txt
export GITHUB_TOKEN=$(grep 'TokenGitHub' claves.txt | cut -d ' ' -f2)

# Asegurarse de estar en la rama correcta
echo "Verificando rama actual..."
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$current_branch" != "main" ]]; then
    echo "Estás en la rama '$current_branch'. Cambiando a 'main'."
    git checkout main
fi

# Verificar si hay cambios antes de proceder
echo "Verificando cambios..."
git status -s
if [[ $(git status -s) == "" ]]; then
    echo "No hay cambios para subir. Saliendo del script."
    exit 0
fi

# Agregar todos los archivos al staging area
echo "Agregando archivos..."
git add .

# Crear el commit con un mensaje automático o personalizado
commit_message="${1:-Actualización de archivos de la página rápido}"
echo "Haciendo commit con el mensaje: $commit_message"
git commit -m "$commit_message"

# Empujar los cambios a GitHub con el token
echo "Empujando cambios a GitHub..."
git push https://amoedo7:$GITHUB_TOKEN@github.com/amoedo7/termtroops.git main || { echo 'Error al empujar cambios'; exit 1; }

# Confirmación de éxito
echo "¡Cambios empujados exitosamente!"
