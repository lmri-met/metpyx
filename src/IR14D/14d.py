import tkinter as tk
from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import Label
from tkcalendar import DateEntry
import tkinter.font as tkFont

class ir14dGUI:
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("IR14D - PATRÓN DE RAYOS X")

        # Font for the title
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

        # Frame for the title using grid
        self.titulo_frame = tk.Frame(self.master, height=30)
        self.titulo_frame.grid(row=0, column=0, sticky="ew", columnspan=2)  # Make it span across all columns in the grid
        self.master.grid_columnconfigure(0, weight=1)  # Allows the title frame to expand across the full width of the window
        tk.Label(self.titulo_frame, text="IR14D - MEDIDAS", font=self.title_font).grid(row=0, column=0)

        # Create the frames of the first row
        self.frame_row1 = tk.Frame(self.master, borderwidth=2, relief="solid", bg='white')
        self.frame_row1.grid(row=1, column=0, sticky="ew")

        self.frame1 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame_row1.grid_columnconfigure(0, weight=1)  # Make frame1 expand to fill the space

        # Subframe for top options
        self.subframe1_top = tk.Frame(self.frame1, borderwidth=2, relief="solid", bg='white')
        self.subframe1_top.grid(row=0, column=0, sticky="ew")
        self.option_menu = ttk.Combobox(self.subframe1_top, values=["Seleccione una opción", "Calibración de equipos", "Asignación de dosis"])
        self.option_menu.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.option_menu.current(0)
        self.option_menu.bind("<<ComboboxSelected>>", self.update_subframe)

        # Subframe for additional controls, initially hidden
        self.subframe1_bottom = tk.Frame(self.frame1, borderwidth=2, relief="solid", bg='white')
        self.subframe1_bottom.grid(row=1, column=0, sticky="ew")
        self.subframe1_bottom.grid_remove()  # This subframe is initially hidden

        self.frame1.grid_rowconfigure(0, weight=1)  # Ensure the top subframe takes the necessary vertical space
        self.frame1.grid_rowconfigure(1, weight=1)  # Ensure the bottom subframe has space allocated when shown
        pass

    def update_subframe(self, event):
        selection = self.option_menu.get()
        for widget in self.subframe1_bottom.winfo_children():
            widget.destroy()

        if selection == "Calibración de equipos":
            self.subframe1_bottom.grid(row=0, column=0, sticky="nsew")

            style = ttk.Style()
            style.theme_use('default')
            style.configure("TFrame", background="white")
            style.configure("TLabel", background="white", foreground="black")
            style.configure("TEntry", fieldbackground="white", background="white")
            style.configure("TCombobox", fieldbackground="white", background="white")
            
            # Título para el subframe
            tk.Label(self.subframe1_bottom, text="Datos del Servicio Técnico", bg='white', fg='black', font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

            # Campo de Referencia del Servicio Técnico
            tk.Label(self.subframe1_bottom, text="Referencia del Servicio Técnico:", bg='white', fg='black').grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.entry_ref_servicio = tk.Entry(self.subframe1_bottom)
            self.entry_ref_servicio.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

            # Etiqueta para el campo de fecha
            tk.Label(self.subframe1_bottom, text="Fecha del Servicio:", bg='white', fg='black').grid(row=2, column=0, sticky="w", padx=5, pady=5)

            # Campo de entrada de fecha con calendario desplegable
            self.date_entry = DateEntry(self.subframe1_bottom, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
            self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

            # Campo de Supervisor
            tk.Label(self.subframe1_bottom, text="Supervisor/a:", bg='white', fg='black').grid(row=3, column=0, sticky="w", padx=5, pady=5)
            self.combo_supervisor = ttk.Combobox(self.subframe1_bottom, values=["Marta Borrego Ramos", "Xandra Campo Blanco", "Miguel Embid Segura"])
            self.combo_supervisor.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

            # Datos del Equipo a calibrar
            tk.Label(self.subframe1_bottom, text="Datos del Equipo a calibrar", bg='white', fg='black', font=('Helvetica', 14, 'bold')).grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)

            # Campo de Cliente
            tk.Label(self.subframe1_bottom, text="Cliente:", bg='white', fg='black').grid(row=6, column=0, sticky="w", padx=5, pady=5)
            self.entry_cliente = tk.Entry(self.subframe1_bottom)
            self.entry_cliente.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

            # Campo de Marca
            tk.Label(self.subframe1_bottom, text="Marca:", bg='white', fg='black').grid(row=7, column=0, sticky="w", padx=5, pady=5)
            self.entry_marca = tk.Entry(self.subframe1_bottom)
            self.entry_marca.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

            # Campo de Modelo
            tk.Label(self.subframe1_bottom, text="Modelo:", bg='white', fg='black').grid(row=8, column=0, sticky="w", padx=5, pady=5)
            self.entry_modelo = tk.Entry(self.subframe1_bottom)
            self.entry_modelo.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

            # Campo de NumSerie
            tk.Label(self.subframe1_bottom, text="Número de serie:", bg='white', fg='black').grid(row=9, column=0, sticky="w", padx=5, pady=5)
            self.entry_numserie = tk.Entry(self.subframe1_bottom)
            self.entry_numserie.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

            # Datos de la calibración
            tk.Label(self.subframe1_bottom, text="Datos del tipo de calibración", bg='white', fg='black', font=('Helvetica', 14, 'bold')).grid(row=11, column=0, columnspan=2, sticky="w", padx=5, pady=5)

            # Campo de Magnitud de medida
            tk.Label(self.subframe1_bottom, text="Magnitud de Medida:", bg='white', fg='black').grid(row=12, column=0, sticky="w", padx=5, pady=5)
            units_options = ["Equivalente de dosis direccional H'(0.07)", "Equivalente de dosis direccional H'(3)", "Equivalente de dosis ambiental H*(10)", "Exposición", "Kerma en aire", "Dosis aborbida en aire"]
            self.combo_units = ttk.Combobox(self.subframe1_bottom, values=units_options, width=35)
            self.combo_units.grid(row=12, column=1, sticky="ew", padx=5, pady=5)
            
            # Etiquetas para mostrar las unidades seleccionadas
            self.label_rate = tk.Label(self.subframe1_bottom, text="Unidades de tasa: ........", bg='white', fg='black')
            self.label_rate.grid(row=13, column=0, sticky="w", padx=5, pady=5)
            self.label_unit = tk.Label(self.subframe1_bottom, text="Unidades: ........", bg='white', fg='black')
            self.label_unit.grid(row=13, column=1, sticky="w", padx=5, pady=5)
            self.combo_units.bind("<<ComboboxSelected>>", self.update_labels)
            self.combo_units.current(0)
            self.update_labels(None)

            # Campo de Calidad de Radiación
            tk.Label(self.subframe1_bottom, text="Calidad de radiación:", bg='white', fg='black').grid(row=15, column=0, sticky="w", padx=5, pady=5)
            self.combo_quality = ttk.Combobox(self.subframe1_bottom, values=["L-10", "L-20", "L-30", "L-35", "L-55", "L-70", "L-100", "L-125", "L-170", "L-210", "L-240", "N-10", "N-15", "N-20", "N-25", "N-30", "N-40", "N-60", "N-80", "N-100", "N-120", "N-150", "N-200", "N-250", "N-300", "W-30", "W-40", "W-60", "W-80", "W-110", "W-150", "W-200", "W-250", "W-300"])
            self.combo_quality.grid(row=15, column=1, sticky="ew", padx=5, pady=5)

            # Campo de Cámara patrón
            tk.Label(self.subframe1_bottom, text="Cámara patrón:", bg='white', fg='black').grid(row=16, column=0, sticky="w", padx=5, pady=5)
            self.combo_chamber = ttk.Combobox(self.subframe1_bottom, values=["NE 2575-ns557-IR14D/014", "NE 2575-ns506-IR14D/006"])
            self.combo_chamber.grid(row=16, column=1, sticky="ew", padx=5, pady=5)
            self.combo_chamber.bind("<<ComboboxSelected>>", self.update_fields)

            # Asegurarse de que los widgets se expandan apropiadamente
            self.subframe1_bottom.columnconfigure(1, weight=1)

            # Frame 2
            self.frame2 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            self.frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)  # Asumimos que frame_row1 ya está usando grid

            # Título para el Frame 2
            self.title_label_frame2 = tk.Label(self.frame2, text="Instrumentación", bg='white', fg='black', font=('Arial', 14, 'bold'))
            self.title_label_frame2.grid(row=0, column=0, columnspan=2, sticky="ew")  # El título se extiende a lo largo de dos columnas

            # Campos Frame 2
            self.label_proc_ref = tk.Label(self.frame2, text="Procedimiento:", bg='white', fg='black')
            self.entry_proc_ref = tk.Entry(self.frame2)
            self.entry_proc_ref.insert(0, "P-LMRI-C_12")  
            self.label_proc_ref.grid(row=1, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_proc_ref.grid(row=1, column=1, sticky="ew")  # Campo de entrada en la segunda columna, alineado a la izquierda

            self.label_electrom_ref = tk.Label(self.frame2, text="Electrómetro:", bg='white', fg='black')
            self.entry_electrom_ref = tk.Entry(self.frame2)
            self.entry_electrom_ref.insert(0, "IR14D/018")  
            self.label_electrom_ref.grid(row=2, column=0, sticky="e")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_electrom_ref.grid(row=2, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda

            self.label_barom_ref = tk.Label(self.frame2, text="Barómetro:", bg='white', fg='black')
            self.entry_barom_ref = tk.Entry(self.frame2)
            self.entry_barom_ref.insert(0, "IR14D/009")  
            self.label_barom_ref.grid(row=3, column=0, sticky="e")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_barom_ref.grid(row=3, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda

            self.label_temp_ref = tk.Label(self.frame2, text="Termómetro:", bg='white', fg='black')
            self.entry_temp_ref = tk.Entry(self.frame2)
            self.entry_temp_ref.insert(0, "IR14D/010")  
            self.label_temp_ref.grid(row=4, column=0, sticky="e")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_temp_ref.grid(row=4, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda

            self.label_crono_ref = tk.Label(self.frame2, text="Cronómetro:", bg='white', fg='black')
            self.entry_crono_ref = tk.Entry(self.frame2)
            self.entry_crono_ref.insert(0, "IR14D/018")  
            self.label_crono_ref.grid(row=5, column=0, sticky="e")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_crono_ref.grid(row=5, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda

            # Datos de la calibración
            self.title2_label_frame2 = tk.Label(self.frame2, text="Datos de la medida", bg='white', fg='black', font=('Arial', 14, 'bold'))
            self.title2_label_frame2.grid(row=7, column=0, columnspan=2, sticky="ew")  # El título se extiende a lo largo de dos columnas

            # Campo de Magnitud de medida
            self.label_nummed_ref = tk.Label(self.frame2, text="Número de medidas:", bg='white', fg='black')
            nummed_options = ["1", "2", "3", "4"]
            self.combo_nummed_ref = ttk.Combobox(self.frame2, values=nummed_options, width=5)
            self.combo_nummed_ref.grid(row=8, column=0, sticky="e")
            self.combo_nummed_ref.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

            # Ajustar las configuraciones de la columna para que las etiquetas y entradas estén bien alineadas
            self.frame2.grid_columnconfigure(0, weight=1)  # Hace que la columna de las etiquetas tenga cierta expansión
            self.frame2.grid_columnconfigure(1, weight=2)  # Hace que la columna de las entradas se expanda más, para mayor espacio

            # Inicialmente ocultar todos los campos (si es necesario)
            self.title_label_frame2.grid_remove()
            self.label_proc_ref.grid_remove()
            self.entry_proc_ref.grid_remove()
            self.label_electrom_ref.grid_remove()
            self.entry_electrom_ref.grid_remove()
            self.label_barom_ref.grid_remove()
            self.entry_barom_ref.grid_remove()
            self.label_temp_ref.grid_remove()
            self.entry_temp_ref.grid_remove()
            self.label_crono_ref.grid_remove()
            self.entry_crono_ref.grid_remove()
            self.title2_label_frame2.grid_remove()
            self.label_nummed_ref.grid_remove()
            self.combo_nummed_ref.grid_remove()



        elif selection == "Asignación de dosis":
            self.subframe1_bottom.grid(row=1, column=0, sticky="ew", padx=5, pady=5)  # Use grid to place this frame
            tk.Label(self.subframe1_bottom, text="Tipo de Servicio:", bg='white', fg='black').grid(row=0, column=0, sticky="w")
            ttk.Combobox(self.subframe1_bottom, values=["Kerma en aire", "asignación de dosis", "otra cosa"]).grid(row=0, column=1, sticky="ew")
            tk.Label(self.subframe1_bottom, text="Cámara Patrón:", bg='white', fg='black').grid(row=1, column=0, sticky="w")
            ttk.Combobox(self.subframe1_bottom, values=["506", "557"]).grid(row=1, column=1, sticky="ew")
            tk.Label(self.subframe1_bottom, text="Tipo de medida:", bg='white', fg='black').grid(row=2, column=0, sticky="w")
            ttk.Combobox(self.subframe1_bottom, values=["Fondo", "Equipo", "Dosímetro"]).grid(row=2, column=1, sticky="ew")
        else:
            self.subframe1_bottom.grid_remove()  # Hide this frame using grid_remove()


            # Frame 3 setup
            self.frame3 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            self.frame3.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            tk.Label(self.frame3, text="Frame 3", bg='white', fg='black').grid(row=0, column=0)

            # Frame 4 setup
            self.frame4 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            self.frame4.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
            tk.Label(self.frame4, text="Frame 4", bg='white', fg='black').grid(row=0, column=0)

            # Setting up frame_row2
            self.frame_row2 = tk.Frame(self.master, borderwidth=2, relief="solid", bg='white')
            self.frame_row2.grid(row=2, column=0, sticky="ew")

            # Frame 5 setup
            self.frame5 = tk.Frame(self.frame_row2, borderwidth=2, relief="solid", bg='white')
            self.frame5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            tk.Label(self.frame5, text="Frame 5", bg='white', fg='black').grid(row=0, column=0)

            # Frame 6 setup
            self.frame6 = tk.Frame(self.frame_row2, borderwidth=2, relief="solid", bg='white')
            self.frame6.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            tk.Label(self.frame6, text="Frame 6", bg='white', fg='black').grid(row=0, column=0)



            # Evento de selección del combobox para actualizar las etiquetas directamente
    def update_labels(self, event):
        option = self.combo_units.get()
        unitsrate = ""  # Inicializar con un valor por defecto
        unitsunit = ""  # Inicializar con un valor por defecto
        if option in ["Equivalente de dosis direccional H'(0.07)", "Equivalente de dosis direccional H'(3)", "Equivalente de dosis ambiental H*(10)"]:
            unitsrate = "Sv/h"
            unitsunit = "Sv"
        elif option == "Exposición":
            unitsrate = "R/h"
            unitsunit = "R"
        elif option in ["Kerma en aire", "Dosis aborbida en aire"]:
            unitsrate = "Gy/h"
            unitsunit = "Gy"
        self.label_rate.config(text=f"Unidades de tasa:   {unitsrate}")
        self.label_unit.config(text=f"Unidades:    {unitsunit}")
        pass

    def update_fields(self, event=None):
        # Mostrar los campos y el título cuando se actualicen o se llame a este método
        self.title_label_frame2.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 0))  # Mostrar el título con expansión a lo largo del eje horizontal

        # Configuración de las etiquetas y entradas usando grid
        self.label_proc_ref.grid(row=1, column=0, sticky="e", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_proc_ref.grid(row=1, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_electrom_ref.grid(row=2, column=0, sticky="e", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_electrom_ref.grid(row=2, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_barom_ref.grid(row=3, column=0, sticky="e", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_barom_ref.grid(row=3, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_temp_ref.grid(row=4, column=0, sticky="e", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_temp_ref.grid(row=4, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_crono_ref.grid(row=5, column=0, sticky="e", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_crono_ref.grid(row=5, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.title2_label_frame2.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 0)) 
        self.label_nummed_ref.grid(row=8, column=0, sticky="e", padx=5, pady=2)
        self.combo_nummed_ref.grid(row=8, column=1, sticky="w", padx=5, pady=2)

def main():
    root = tk.Tk()
    app = ir14dGUI(master=root)
    root.configure(bg='white')
    frame = tk.Frame(root, bg='white')
    root.mainloop()

def update_progressbar():
    if progressbar.winfo_exists():
        progressbar.step(10)
        root.after(100, update_progressbar)

# Si este archivo se ejecuta como programa principal, se iniciará la GUI.
if __name__ == "__main__":
    # Crear una ventana de carga
    load_root = tk.Tk()
    load_root.title("Cargando...")
    load_root.geometry("300x100")  # Tamaño de la ventana de carga

    # Mensaje de carga
    ttk.Label(load_root, text="Cargando librerías, por favor espere...").pack(pady=20)

    # Barra de progreso
    progress = ttk.Progressbar(load_root, length=100, mode='indeterminate')
    progress.pack(pady=10)
    progress.start(10)  # Inicia la animación de la barra de progreso

    # Cargar bibliotecas pesadas aquí
    import time  # Simular la carga de bibliotecas con time.sleep
    load_root.after(100, lambda: time.sleep(2))  # Simula el tiempo de carga

    # Mostrar la ventana de carga y esperar un poco antes de lanzar la ventana principal
    load_root.after(2000, lambda: (load_root.destroy(), main()))  # Cierra la carga y abre la ventana principal

    load_root.mainloop()
