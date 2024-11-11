import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import subprocess
import os
from utils.convertir_datos import convertir_mpl_a_dzn

# Ruta de las carpetas de datos y salidas
RUTA_SALIDAS = "Salidas/"
ARCHIVO_DZN = os.path.join(os.getcwd(), "Datos/DatosProyecto.dzn")
ARCHIVO_MODELO = os.path.join(os.getcwd(), "Proyecto.mzn")
print (ARCHIVO_DZN)

# Función para cargar el archivo .mpl y convertirlo a .dzn
def cargar_archivo():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("MPL files", "*.mpl")])
    if file_path:
        with open(file_path, 'r') as file:
            datos = file.readlines()
            if convertir_mpl_a_dzn(datos, ARCHIVO_DZN):
                messagebox.showinfo("Éxito", "Archivo .mpl convertido a .dzn correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo convertir el archivo .mpl.")

# Función para ejecutar el modelo en MiniZinc con el archivo .dzn generado usando la ruta completa al ejecutable
def ejecutar_modelo():
    if not os.path.exists(ARCHIVO_MODELO):
        messagebox.showerror("Error", f"No se encontró el modelo: {ARCHIVO_MODELO}")
        return
    if not os.path.exists(ARCHIVO_DZN):
        messagebox.showerror("Error", f"No se encontró el archivo de datos: {ARCHIVO_DZN}")
        return
    try:
        # Ruta completa al ejecutable de MiniZinc
        resultado = subprocess.run(
            ["C:/Program Files/MiniZinc/minizinc.exe", ARCHIVO_MODELO, ARCHIVO_DZN],
            capture_output=True, text=True, check=True
        )
        mostrar_resultado(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error en la ejecución del modelo: {e}") 
        messagebox.showerror("Error", f"Error en la ejecución del modelo: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el ejecutable de MiniZinc en la ruta especificada.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el modelo: {e}")

# Función para mostrar el resultado en la interfaz
def mostrar_resultado(resultado):
    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert(tk.END, resultado)

# Configuración de la interfaz
root = tk.Tk()
root.title("Interfaz MinPol - Optimización")

# Definir el tamaño de la ventana (ancho x alto)
window_width = 700
window_height = 520

# Obtener el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
position_x = int((screen_width - window_width) / 2)
position_y = int((screen_height - window_height) / 2)

# Establecer la geometría de la ventana y su posición
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
root.configure(bg="#fefae0")

# Etiqueta para el título en la parte superior
label_titulo = tk.Label(root, text="OPTIMIZACIÓN DE POLARIZACIÓN", font=("Georgia", 20), bg="#fefae0", fg="#003049")
label_titulo.pack(pady=10)

# Cargar y redimensionar la imagen
ruta_imagen = "Imagenes/polarizacion.png"  
imagen = PhotoImage(file=ruta_imagen)

# Redimensionar la imagen (en este caso, la escalamos a la mitad de su tamaño original)
imagen = imagen.subsample(3, 3)  # Ajusta el valor para cambiar el tamaño, cuanto más alto el número, más pequeña la imagen

# Mostrar la imagen debajo del título
label_imagen = tk.Label(root, image=imagen, bg="#fefae0")
label_imagen.pack(pady=5)

# Etiquetas y botones con estilo moderno


# Crear un Frame para organizar los botones y la flecha
frame_botones = tk.Frame(root, bg="#fefae0")
frame_botones.pack(pady=5)

# Botones con estilo moderno
btn_cargar = tk.Button(frame_botones, text="Cargar archivo .mpl", command=cargar_archivo, bg="#003049", fg="white", font=("Georgia", 12))
btn_cargar.pack(side="left", padx=10)

# Crear la flecha en el centro
flecha = tk.Label(frame_botones, text="→", font=("Georgia", 18), bg="#fefae0", fg="#c1121f")
flecha.pack(side="left", padx=10)

btn_ejecutar = tk.Button(frame_botones, text="Ejecutar Modelo", command=ejecutar_modelo, bg="#003049", fg="white", font=("Georgia", 12))
btn_ejecutar.pack(side="left", padx=10)

resultado_texto = tk.Text(root, height=10, width=60, font=("Georgia", 10), bg="#f1f8e9", fg="#004d40")
resultado_texto.pack(pady=10)

root.mainloop()