import os
import re

# Función para buscar variables en archivos de Python
def buscar_variables_python(archivo):
    # Expresión regular para encontrar variables en Python (basado en asignaciones simples)
    patron = r'\b\w+\s*=\s*'
    with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
        contenido = f.read()
    return re.findall(patron, contenido)

# Función para buscar variables en archivos JavaScript
def buscar_variables_js(archivo):
    # Expresión regular para encontrar variables en JavaScript (let, const, var)
    patron = r'\b(?:let|const|var)\s+(\w+)'
    with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
        contenido = f.read()
    return re.findall(patron, contenido)

# Función para buscar variables en archivos HTML (suponiendo que las variables estén dentro de <script>)
def buscar_variables_html(archivo):
    # Expresión regular para encontrar variables en el contenido de etiquetas <script>
    patron = r'\b(?:let|const|var)\s+(\w+)'
    with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
        contenido = f.read()
    return re.findall(patron, contenido)

# Función para recorrer todos los archivos en la carpeta y subcarpetas
def buscar_variables_en_directorio(directorio):
    variables_encontradas = {}
    
    for root, dirs, files in os.walk(directorio):
        for archivo in files:
            # Obtener la ruta completa del archivo
            archivo_completo = os.path.join(root, archivo)
            
            # Filtrar los archivos que no te interesan
            if archivo.startswith('.') or archivo == 'VariablesP.txt':
                continue
            
            # Identificar el tipo de archivo y buscar variables
            if archivo.endswith('.py'):
                variables = buscar_variables_python(archivo_completo)
                if variables:
                    # Almacenamos solo el nombre del archivo, no la ruta completa
                    variables_encontradas[archivo] = variables
            elif archivo.endswith('.js') or archivo.endswith('.html'):
                variables = buscar_variables_js(archivo_completo) + buscar_variables_html(archivo_completo)
                if variables:
                    # Almacenamos solo el nombre del archivo, no la ruta completa
                    variables_encontradas[archivo] = variables

    return variables_encontradas

# Función principal para generar el archivo VariablesP.txt
def generar_variables(directorio):
    variables = buscar_variables_en_directorio(directorio)

    # Crear el archivo de salida
    with open("VariablesP.txt", "w", encoding="utf-8") as f:
        f.write("# Lista de variables encontradas en el proyecto\n\n")
        for archivo, vars in variables.items():
            f.write(f"{archivo}:\n")
            for var in vars:
                f.write(f"  - {var}\n")
            f.write("\n")

# Ejecutar el proceso en el directorio actual
directorio_actual = os.getcwd()
generar_variables(directorio_actual)

print("Archivo 'VariablesP.txt' generado con éxito.")
