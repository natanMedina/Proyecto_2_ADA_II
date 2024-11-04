import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from utils.convertir_datos import convertir_mpl_a_dzn

# Ruta de las carpetas de datos y salidas
RUTA_DATOS = "Datos/"
RUTA_SALIDAS = "Salidas/"
ARCHIVO_DZN = os.path.join(RUTA_DATOS, "DatosProyecto.dzn")
ARCHIVO_MODELO = "Proyecto.mzn"

# Función para cargar el archivo .mpl y convertirlo a .dzn
def cargar_archivo():
    file_path = filedialog.askopenfilename(initialdir=RUTA_DATOS, filetypes=[("MPL files", "*.mpl")])
    if file_path:
        with open(file_path, 'r') as file:
            datos = file.readlines()
            if convertir_mpl_a_dzn(datos, ARCHIVO_DZN):
                messagebox.showinfo("Éxito", "Archivo .mpl convertido a .dzn correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo convertir el archivo .mpl.")

# Función para ejecutar el modelo en MiniZinc con el archivo .dzn generado
def ejecutar_modelo():
    try:
        resultado = subprocess.run(
            ["minizinc", ARCHIVO_MODELO, ARCHIVO_DZN],
            capture_output=True, text=True
        )
        mostrar_resultado(resultado.stdout)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el modelo: {e}")

# Función para mostrar el resultado en la interfaz
def mostrar_resultado(resultado):
    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert(tk.END, resultado)

# Configuración de la interfaz
root = tk.Tk()
root.title("Interfaz MiniZinc")

btn_cargar = tk.Button(root, text="Cargar archivo .mpl", command=cargar_archivo)
btn_cargar.pack()

btn_ejecutar = tk.Button(root, text="Ejecutar Modelo", command=ejecutar_modelo)
btn_ejecutar.pack()

resultado_texto = tk.Text(root, height=10, width=50)
resultado_texto.pack()

root.mainloop()