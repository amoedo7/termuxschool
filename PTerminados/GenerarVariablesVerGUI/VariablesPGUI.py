import tkinter as tk
from tkinter import ttk
import os

class VariablesPGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Variables del Proyecto PidAmo")
        self.geometry("800x600")

        # Crear un campo de búsqueda
        self.search_label = tk.Label(self, text="Buscar Variable:")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filtrar_resultados)  # Filtrar al escribir

        # Crear el Treeview para las tres columnas
        self.tree = ttk.Treeview(self, columns=("Archivo", "Variable", "También en"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar las columnas
        self.tree.heading("Archivo", text="Archivo")
        self.tree.heading("Variable", text="Variable")
        self.tree.heading("También en", text="También en")

        self.tree.column("Archivo", width=200, anchor="w")
        self.tree.column("Variable", width=200, anchor="w")
        self.tree.column("También en", width=200, anchor="w")

        # Cargar datos desde el archivo
        self.variables_por_archivo = self.cargar_datos("VariablesP.txt")
        self.colores = self.generar_colores()

        # Mostrar los datos
        self.mostrar_datos()

    def cargar_datos(self, archivo):
        """Carga las variables desde el archivo de texto"""
        datos = {}
        if not os.path.exists(archivo):
            return datos

        with open(archivo, "r", encoding="utf-8") as f:
            actual = None
            for linea in f:
                linea = linea.strip()
                if linea.endswith(":"):
                    actual = linea[:-1]
                    datos[actual] = []
                elif linea.startswith("-") and actual:
                    variable = linea[2:].strip()
                    datos[actual].append(variable)

        return datos

    def generar_colores(self):
        """Genera una lista de colores para cada archivo"""
        colores = {}
        paleta = ["red", "blue", "green", "purple", "orange", "cyan", "magenta"]
        for idx, archivo in enumerate(self.variables_por_archivo.keys()):
            colores[archivo] = paleta[idx % len(paleta)]
        return colores

    def mostrar_datos(self):
        """Muestra los archivos y variables en el Treeview"""
        self.items = []  # Guardamos los items aquí para referencia
        for archivo, color in self.colores.items():
            for variable in self.variables_por_archivo.get(archivo, []):
                # Encontrar otros archivos que contienen la misma variable
                archivos_relacionados = [arch for arch, vars in self.variables_por_archivo.items() if variable in vars and arch != archivo]
                archivos_relacionados_str = ", ".join(archivos_relacionados) if archivos_relacionados else "Ninguno"

                # Insertar datos en el Treeview con la información sobre otros archivos        
                item = self.tree.insert("", tk.END, values=(archivo, variable, archivos_relacionados_str))  # Tercera columna con "También en"
                self.items.append(item)  # Guardar item para referencia futura

    def filtrar_resultados(self, event=None):
        """Filtra los resultados en el Treeview según el texto ingresado en la barra de búsqueda"""
        query = self.search_entry.get().lower()

        # Limpiar el Treeview antes de mostrar los resultados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Si la barra de búsqueda está vacía, mostrar todos los elementos
        if not query:
            self.mostrar_datos()
            return

        # Si hay texto en la búsqueda, solo mostrar los elementos que coinciden
        for archivo, color in self.colores.items():
            for variable in self.variables_por_archivo.get(archivo, []):
                # Encontrar otros archivos que contienen la misma variable
                archivos_relacionados = [arch for arch, vars in self.variables_por_archivo.items() if variable in vars and arch != archivo]
                archivos_relacionados_str = ", ".join(archivos_relacionados) if archivos_relacionados else "Ninguno"

                # Verificar si el nombre del archivo o la variable contiene el texto de la búsqueda
                if query in archivo.lower() or query in variable.lower():
                    # Insertar los elementos que coinciden en el Treeview
                    self.tree.insert("", tk.END, values=(archivo, variable, archivos_relacionados_str))  # Tercera columna con "También en"

if __name__ == "__main__":
    app = VariablesPGUI()
    app.mainloop()
