import tkinter as tk
from tkinter import ttk, Label
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from datetime import datetime, timedelta
import numpy as np

import numpy as np

def mostrar_video():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (400, 300))  # Ajuste de la imagen al frame de 400x300
    im = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=im)
    label_camara.imgtk = img
    label_camara.configure(image=img)
    label_camara.after(10, mostrar_video)

# Configuración inicial de la ventana y del dispositivo de captura de video
root = tk.Tk()
root.title("CALIBRACIÓN - ASIGNACIÓN DE DOSIS. IR-14D")
root.configure(bg='white')

# 
style = ttk.Style()
style.theme_use('clam')

cap = cv2.VideoCapture(0)  # Inicialización de la captura de video. '0' es la cámara predeterminada


# Marco para el título
titulo_frame = tk.Frame(root, height=30, width=1300)
titulo_frame.pack_propagate(False)
titulo_frame.pack(fill=tk.X)
titulo = tk.Label(titulo_frame, text="CALIBRACIÓN - ASIGNACIÓN DE DOSIS. IR-14D", font=("Arial", 24, "bold"))
titulo_frame.configure(bg='white')
titulo.configure(bg='white')
titulo.pack()


# Primera fila de frames
primera_fila_frame = tk.Frame(root)
primera_fila_frame.pack(fill=tk.X)
primera_fila_frame.configure(bg='white')


# Frame de entrada de datos
entrada_datos_frame = tk.Frame(primera_fila_frame, width=400, height=300, bd=2, relief="groove")
entrada_datos_frame.pack_propagate(False)
entrada_datos_frame.pack(side=tk.LEFT, padx=10, pady=5)
entrada_datos_frame.configure(bg='white')


# Título para el Frame de entrada de datos
titulo_entrada_datos = tk.Label(entrada_datos_frame, text="DATOS DE ENTRADA", font=("Arial", 14, "bold"))
titulo_entrada_datos.pack(pady=5)
titulo_entrada_datos.configure(bg='white')


# Función para agregar una etiqueta y campo de entrada en una fila
def agregar_fila_entrada(frame, texto_etiqueta, valores_combobox=None):
    fila_frame = tk.Frame(frame)
    fila_frame.pack(fill=tk.X, pady=5)
    
    etiqueta = tk.Label(fila_frame, text=texto_etiqueta)
    etiqueta.pack(side=tk.LEFT)
    
    if valores_combobox:  # Si se proporcionan valores, usar un Combobox
        entrada = ttk.Combobox(fila_frame, values=valores_combobox, state="readonly")  # Corrección aquí
    else:  # De lo contrario, usar un Entry
        entrada = tk.Entry(fila_frame)
    entrada.pack(side=tk.LEFT)

    return entrada

# Usando la función `agregar_fila_entrada` para crear las entradas
nombre_entry = agregar_fila_entrada(entrada_datos_frame, "Nombre del Servicio Técnico:", None)
supervisor_combobox = agregar_fila_entrada(entrada_datos_frame, "Supervisor:", ["Marta Borrego", "Xandra Campo", "Miguel Embid"])
tipo_servicio_combobox = agregar_fila_entrada(entrada_datos_frame, "Tipo de Servicio:", ["Kerma en aire", "asignación de dosis", "otra cosa"])
camara_patron_combobox = agregar_fila_entrada(entrada_datos_frame, "Cámara Patrón:", ["506", "557"])
tipo_medida_combobox = agregar_fila_entrada(entrada_datos_frame, "Tipo de medida:", ["Fondo", "Equipo", "Dosímetro"])
numero_medidas_entry = agregar_fila_entrada(entrada_datos_frame, "Número de medidas a realizar:", None)
config_electrometro_combobox = agregar_fila_entrada(entrada_datos_frame, "Configuración del electrómetro:", ["Alta", "Media", "Baja"])
# Obtiene la fecha y hora actuales
fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
# Crear un Label para mostrar la fecha y hora
fecha_hora_label = tk.Label(entrada_datos_frame, text="Fecha y hora de realización: " + fecha_hora_actual)
fecha_hora_label.configure(bg='white')
fecha_hora_label.pack()

# Frame para visualizar la imagen en directo de una cámara web
camara_frame = tk.Frame(primera_fila_frame, width=400, height=300, bd=2, relief="groove")
camara_frame.pack_propagate(False)  # Evita que el frame cambie de tamaño automáticamente
camara_frame.configure(bg='white')

camara_frame.pack(side=tk.LEFT, padx=10, pady=5)

# Label para mostrar la imagen de la cámara web
label_camara = tk.Label(camara_frame)
label_camara.pack(fill=tk.BOTH, expand=True)  # Ocupa todo el espacio disponible en el frame

# Colocando el título superpuesto en la parte superior del frame de la cámara
titulo_camara = tk.Label(camara_frame, text="CÁMARA WEB", font=("Arial", 14, "bold"), bg='white', fg='black')
titulo_camara.place(relx=0.5, rely=0.01, anchor="n")  # Centrado en la parte superior dentro del frame
titulo_camara.configure(bg='white')


# Frame para la gráfica del barómetro y termómetro
grafica_frame = tk.Frame(primera_fila_frame, width=500, height=280, bd=2, relief="groove")
grafica_frame.pack_propagate(False)
grafica_frame.pack(side=tk.LEFT, padx=10, pady=5)
grafica_frame.configure(bg='white')

# Título superpuesto para el frame de la gráfica
titulo_grafica = tk.Label(grafica_frame, text="PRESIÓN Y TEMPERATURA", font=("Arial", 14, "bold"), bg='lightgrey', fg='black')
titulo_grafica.place(relx=0.5, rely=0.01, anchor="n")  # Centrado en la parte superior dentro del frame
titulo_grafica.configure(bg='white')

# Configuración inicial de la gráfica
figura = Figure(figsize=(5, 4), dpi=100)
ax1 = figura.add_subplot(111)
ax2 = ax1.twinx() 

# Ajustar el tamaño de los textos y los títulos de los ejes
tamanio_fuente = 8  # Tamaño de fuente ajustado
ax1.set_xlabel('Tiempo (s)', fontsize=tamanio_fuente)
ax1.set_ylabel('Presión (kPa)', color='g', fontsize=tamanio_fuente)
ax2.set_ylabel('Temperatura (ºC)', color='b', fontsize=tamanio_fuente-2, labelpad=15, rotation=-90)
ax1.tick_params(labelsize=tamanio_fuente)
ax2.tick_params(labelsize=tamanio_fuente)

# Variables para almacenar los datos
contador = 0
datos_kPa = []
datos_temp = []
inicio_tiempo = datetime.now()
timestamps = []


# Función actualizada para actualizar la gráfica
def actualizar_grafica():
    global contador, datos_kPa, datos_temp, inicio_tiempo, timestamps
    
    contador += 1
    # Generar datos de ejemplo para presión y temperatura
    datos_kPa.append(np.random.uniform(93.5, 94.5))
    datos_temp.append(np.random.uniform(19, 21))
    # Añadir un nuevo timestamp para cada punto de dato
    timestamps.append(inicio_tiempo + timedelta(seconds=5*contador))  # Asume una medida cada 5 segundos
    # Asume una medida cada 5 segundos
    
    # Limpieza de los ejes y re-plot
    ax1.clear()
    ax2.clear()
    
    # Configurar formato del eje X para mostrar hh:mm:ss
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    # Rotar las etiquetas para que estén verticales y ajustar su tamaño
    plt.setp(ax1.get_xticklabels(), rotation=25, fontsize=5)
    
    # Actualizar los datos en la gráfica
    ax1.plot(timestamps, datos_kPa, 'g-')
    ax2.plot(timestamps, datos_temp, 'b-')
    
    # Reestablecer configuraciones de los ejes tras limpiar
    ax1.set_xlabel('Tiempo (hh:mm:ss)', fontsize=5)
    ax1.set_ylabel('Presión (kPa)', color='g', fontsize=tamanio_fuente-2)
    ax2.set_ylabel('Temperatura (ºC)', color='b', fontsize=tamanio_fuente-2, labelpad=15)
    
    ax1.tick_params(labelsize=5)
    ax2.tick_params(labelsize=5, labelright=True)
    
    figura.tight_layout()  # Ajuste de la disposición para asegurar la visibilidad de todos los componentes
    
    canvas.draw()
    grafica_frame.after(5000, actualizar_grafica)

# Integración con Tkinter
canvas = FigureCanvasTkAgg(figura, master=grafica_frame)
canvas.draw()
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

actualizar_grafica()

# Segunda fila de frames
segunda_fila_frame = tk.Frame(root)
segunda_fila_frame.pack(fill=tk.X)
segunda_fila_frame.configure(bg='white')

# Frame de resultados escritos
resultados_frame = tk.Frame(segunda_fila_frame, width=900, height=300, bd=2, relief="groove")
resultados_frame.pack_propagate(False)
resultados_frame.pack(side=tk.LEFT, padx=10, pady=5)
resultados_frame.configure(bg='white')
# label_resultados = tk.Label(resultados_frame, text="TABLA DE RESULTADOS")
# label_resultados.pack()
# Colocando el título superpuesto en la parte superior del frame 
titulo_label_resultados = tk.Label(resultados_frame, text="TABLA DE RESULTADOS", font=("Arial", 14, "bold"), bg='white', fg='black')
titulo_label_resultados.place(relx=0.5, rely=0.01, anchor="n")  # Centrado en la parte superior dentro del frame
titulo_label_resultados.configure(bg='white')

# Frame de botones de acción
acciones_frame = tk.Frame(segunda_fila_frame, width=400, height=300, bd=2, relief="groove")
acciones_frame.pack_propagate(False)
acciones_frame.pack(side=tk.LEFT, padx=10, pady=5)
acciones_frame.configure(bg='white')

# Colocando el título superpuesto en la parte superior del frame
titulo_acciones = tk.Label(acciones_frame, text="BOTONES DE ACCIÓN", font=("Arial", 14, "bold"), bg='white', fg='black')
# Cambio clave: usar `pack()` con `side=tk.TOP` para asegurar que el título esté arriba
titulo_acciones.pack(side=tk.TOP, fill=tk.X)

# Frame intermedio para los botones
botones_frame = tk.Frame(acciones_frame)
botones_frame.pack(expand=True)
botones_frame.configure(bg='white')

# Botones de ejemplo, centrados en el frame intermedio
btn_inicio = tk.Button(botones_frame, text="Inicio de toma de datos")
btn_inicio.pack(pady=5)
btn_parada = tk.Button(botones_frame, text="Parada")
btn_parada.pack(pady=5)
btn_guardar = tk.Button(botones_frame, text="Guardar en ficheros")
btn_guardar.pack(pady=5)
btn_inicio.configure(bg='white')
btn_parada.configure(bg='white')
btn_guardar.configure(bg='white')

# Frame para la gráfica del electrómetro
# electrometro_frame = tk.Frame(segunda_fila_frame, width=400, height=300, bd=2, relief="groove")
# electrometro_frame.pack_propagate(False)
# electrometro_frame.pack(side=tk.LEFT, padx=10, pady=5)

mostrar_video()  # Inicia la visualización del video

root.mainloop()

# Asegúrate de liberar la captura de video cuando la aplicación se cierre
cap.release()
cv2.destroyAllWindows()
