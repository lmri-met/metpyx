import tkinter as tk
from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import Label
from tkcalendar import DateEntry
import tkinter.font as tkFont
import pandas as pd
import openpyxl
import json
from tkinter import font  # Importar el módulo de fuente
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np
import serial
import time
import datetime
import random


class ir14dGUI(tk.Tk):
    # def __init__(self, master):
    def __init__(self):
        super().__init__()
        # self.master = master
        self.title("IR14D - PATRÓN DE RAYOS X")

        # self.correction_factor_str = "0.00"  # Valor inicial
        self.correction_factor_var = tk.StringVar(value="0.0")
        self.calibration_coefficient_var = tk.StringVar(value="0.0")
        
        # Font for the title
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

        # Frame for the title using grid
        # self.titulo_frame = tk.Frame(self.master, height=30)
        self.titulo_frame = tk.Frame(self, height=30)
        self.titulo_frame.grid(row=0, column=0, sticky="ew", columnspan=2)  # Make it span across all columns in the grid
        # self.master.grid_columnconfigure(0, weight=1)  # Allows the title frame to expand across the full width of the window
        self.grid_columnconfigure(0, weight=1)
        # tk.Label(self.titulo_frame, text="LABORATORIO DE RAYOS X - IR14D", anchor="center", font=self.title_font).grid(row=0, column=0)
        # Creando y posicionando el Label
        label = tk.Label(self.titulo_frame, text="LABORATORIO DE RAYOS X - IR14D", font=self.title_font)
        # label.grid(row=0, column=0, sticky="ew")
        label.grid(row=0, sticky="ew")

        # Create the frames of the first row
        self.frame_row1 = tk.Frame(self.master, borderwidth=2, relief="solid", bg='white')
        self.frame_row1.grid(row=1, column=0, sticky="ew")

        self.frame1 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame_row1.grid_columnconfigure(0, weight=1)  # Make frame1 expand to fill the space

        # Subframe for top options
        self.subframe1_top = tk.Frame(self.frame1, borderwidth=2, relief="solid", bg='white')
        self.subframe1_top.grid(row=0, column=0, sticky="ew")
        
        # Creando una fuente personalizada
        custom_font = font.Font(family="Helvetica", size=16, weight="bold")
        # Aplicar la fuente al Label
        label = tk.Label(self.subframe1_top, text="Medida a realizar:", bg='white', fg='black', font=custom_font)
        label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Aplicar la fuente al Combobox
        self.option_menu = ttk.Combobox(self.subframe1_top, values=["Calibración de equipos", "Asignación de dosis"], font=custom_font)
        self.option_menu.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.option_menu.current(0)
        self.option_menu.bind("<<ComboboxSelected>>", self.update_subframe)


        # tk.Label(self.subframe1_top, text="Seleccione una opción:", bg='white', fg='black').grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # self.option_menu = ttk.Combobox(self.subframe1_top, values=["Calibración de equipos", "Asignación de dosis"])
        # self.option_menu.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        # self.option_menu.current(0)
        # self.option_menu.bind("<<ComboboxSelected>>", self.update_subframe)

        # Creando y aplicando una fuente personalizada
        # custom_font = font.Font(family="Helvetica", size=16, weight="bold")

        # self.option_menu = ttk.Combobox(self.subframe1_top, values=["Seleccione una opción", "Calibración de equipos", "Asignación de dosis"], font=custom_font)
        # self.option_menu.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        # self.option_menu.current(0)
        # self.option_menu.bind("<<ComboboxSelected>>", self.update_subframe)

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
            self.subframe1_bottom.grid(row=1, column=0, sticky="nsew")

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

            # Campo de Dirección Cliente
            tk.Label(self.subframe1_bottom, text="Dirección Cliente:", bg='white', fg='black').grid(row=7, column=0, sticky="w", padx=5, pady=5)
            self.entry_cliente = tk.Entry(self.subframe1_bottom)
            self.entry_cliente.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

            # Campo de Marca
            tk.Label(self.subframe1_bottom, text="Marca:", bg='white', fg='black').grid(row=8, column=0, sticky="w", padx=5, pady=5)
            self.entry_marca = tk.Entry(self.subframe1_bottom)
            self.entry_marca.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

            # Campo de Modelo
            tk.Label(self.subframe1_bottom, text="Modelo:", bg='white', fg='black').grid(row=9, column=0, sticky="w", padx=5, pady=5)
            self.entry_modelo = tk.Entry(self.subframe1_bottom)
            self.entry_modelo.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

            # Campo de NumSerie
            tk.Label(self.subframe1_bottom, text="Número de serie:", bg='white', fg='black').grid(row=10, column=0, sticky="w", padx=5, pady=5)
            self.entry_numserie = tk.Entry(self.subframe1_bottom)
            self.entry_numserie.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

            # Datos de la calibración
            tk.Label(self.subframe1_bottom, text="Datos del tipo de calibración", bg='white', fg='black', font=('Helvetica', 14, 'bold')).grid(row=12, column=0, columnspan=2, sticky="w", padx=5, pady=5)

            # Campo de Magnitud de medida
            tk.Label(self.subframe1_bottom, text="Magnitud de Medida:", bg='white', fg='black').grid(row=13, column=0, sticky="w", padx=5, pady=5)
            units_options = ["Equivalente de dosis direccional H´(0,07)", "Equivalente de dosis direccional H´(3)", "Equivalente de dosis ambiental H*(10)", "Exposición", "Kerma en aire", "Dosis aborbida en aire"]
            self.combo_units = ttk.Combobox(self.subframe1_bottom, values=units_options, width=35)
            self.combo_units.grid(row=13, column=1, sticky="ew", padx=5, pady=5)
            self.combo_units.bind("<<ComboboxSelected>>", self.fetch_correction_factor)
            
            # Etiquetas para mostrar las unidades seleccionadas
            self.label_rate = tk.Label(self.subframe1_bottom, text="Unidades de tasa: ........", bg='white', fg='black')
            self.label_rate.grid(row=14, column=0, sticky="w", padx=5, pady=5)
            self.label_unit = tk.Label(self.subframe1_bottom, text="Unidades: ........", bg='white', fg='black')
            self.label_unit.grid(row=14, column=1, sticky="w", padx=5, pady=5)
            self.combo_units.bind("<<ComboboxSelected>>", self.update_labels)
            self.combo_units.current(0)
            self.update_labels(None)

            # Cargar datos de calibración desde JSON
            with open('calibration_data.json', 'r') as json_file:
                self.data = json.load(json_file)

            # Campo de Calidad de Radiación
            tk.Label(self.subframe1_bottom, text="Calidad de radiación:", bg='white', fg='black').grid(row=16, column=0, sticky="w", padx=5, pady=5)
            self.combo_quality = ttk.Combobox(self.subframe1_bottom, values=["L-10 1 m", "L-10 2,5 m", "L-20 1 m", "L-20 2,5 m", "L-30 1 m", "L-30 2,5 m", "L-35 1 m", "L-35 2,5 m", "L-55", "L-70", "L-100", "L-125", "L-170", "L-210", "L-240", "N-10 1 m", "N-10 2,5 m", "N-15 1 m", "N-15 2,5 m", "N-20 1 m", "N-20 2,5 m", "N-25 1 m", "N-25 2,5 m", "N-30 1 m", "N-30 2,5 m", "N-40 1 m", "N-40 2,5 m", "N-60", "N-80", "N-100", "N-120", "N-150", "N-200", "N-250", "N-300", "W-30 1 m", "W-30 2,5 m", "W-40 1 m", "W-40 2,5 m", "W-60", "W-80", "W-110", "W-150", "W-200", "W-250", "W-300"])
            self.combo_quality.grid(row=16, column=1, sticky="ew", padx=5, pady=5)
            self.combo_quality.bind("<<ComboboxSelected>>", self.handle_quality_selected)
                        
            self.entry = tk.Entry(self.subframe1_bottom)
            tk.Label(self.subframe1_bottom, text="Coef. Conversión de Ka a mag. medida: ", bg='white', fg='black').grid(row=17, column=0, sticky="w", padx=5, pady=5)
            # self.entry.grid(row=16, column=0, sticky="w", padx=5, pady=5)
            self.entry.bind("<Return>", self.on_entry_return)  
            self.correction_factor_label = tk.Label(self.subframe1_bottom, text="Coef. Conversión de Ka a mag. medida: ", textvariable=self.correction_factor_var, bg='white', fg='black')
            self.correction_factor_label.grid(row=17, column=1, sticky="w", padx=5, pady=5)
   
            # Campo de Cámara patrón
            tk.Label(self.subframe1_bottom, text="Cámara patrón:", bg='white', fg='black').grid(row=18, column=0, sticky="w", padx=5, pady=5)
            self.combo_chamber = ttk.Combobox(self.subframe1_bottom, values=["NE 2575-ns557-IR14D/014", "NE 2575-ns506-IR14D/006"])
            self.combo_chamber.grid(row=18, column=1, sticky="ew", padx=5, pady=5)
            self.combo_chamber.bind("<<ComboboxSelected>>", self.handle_chamber_selected)

            # Coeficiente de calibración
            self.calibration_coefficient_var = tk.StringVar()
            tk.Label(self.subframe1_bottom, text="Coeficiente de calibración:", bg='white', fg='black').grid(row=19, column=0, sticky="w")
            tk.Label(self.subframe1_bottom, textvariable=self.calibration_coefficient_var, bg='white', fg='black').grid(row=19, column=0, sticky="e", padx=5)

            # Factor de calibración
            self.calibration_factor_var = tk.StringVar()
            tk.Label(self.subframe1_bottom, text="Factor de calibración:", bg='white', fg='black').grid(row=19, column=1, sticky="w", padx=5)
            tk.Label(self.subframe1_bottom, textvariable=self.calibration_factor_var, bg='white', fg='black').grid(row=19, column=1, sticky="e", padx=5)

            # Asegurarse de que los widgets se expandan apropiadamente
            self.subframe1_bottom.columnconfigure(1, weight=1)

            # Frame 2
            self.frame2 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            self.frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)  # Asumimos que frame_row1 ya está usando grid

            # Título para el Frame 2
            self.title_label_frame2 = tk.Label(self.frame2, text="Instrumentación", bg='white', fg='black', font=('Helvetica', 14, 'bold'))
            self.title_label_frame2.grid(row=0, column=0, sticky="w")  # El título se extiende a lo largo de dos columnas, alineado a la izquierda

            # Campos Frame 2
            self.label_proc_ref = tk.Label(self.frame2, text="Procedimiento:", bg='white', fg='black', width=18)
            self.entry_proc_ref = tk.Entry(self.frame2, width=12)
            self.entry_proc_ref.insert(0, "P-LMRI-C-12")
            self.label_proc_ref.grid(row=1, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la izquierda
            self.entry_proc_ref.grid(row=1, column=1, sticky="w")

            self.label_electrom_ref = tk.Label(self.frame2, text="Electrómetro medidas:", bg='white', fg='black', width=18) 
            self.entry_electrom_ref = tk.Entry(self.frame2, width=12)
            self.entry_electrom_ref.insert(0, "IR14D/018")  
            self.label_electrom_ref.grid(row=2, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_electrom_ref.grid(row=2, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda
            self.label_elecppal_com = tk.Label(self.frame2, text="COM:", bg='white')
            self.label_elecppal_com.grid(row=2, column=2, sticky="w")
            opciones_elecppal_com = ["SIMU"] + [f'COM{i}' for i in range(1, 11)]
            self.elecppal_com_var = tk.StringVar(value="??")
            self.elecppal_com_optionmenu = tk.OptionMenu(self.frame2, self.elecppal_com_var, *opciones_elecppal_com)
            self.elecppal_com_optionmenu.grid(row=2, column=3, sticky="w")
            self.elecppal_com_optionmenu.configure(bg='white')

            self.label_elecmonit_ref = tk.Label(self.frame2, text="Electrómetro monitor:", bg='white', fg='black', width=18)
            self.entry_elecmonit_ref = tk.Entry(self.frame2, width=12)
            self.entry_elecmonit_ref.insert(0, "IR14D/018")  
            self.label_elecmonit_ref.grid(row=3, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_elecmonit_ref.grid(row=3, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda
            self.label_elecmonit_com = tk.Label(self.frame2, text="COM:", bg='white')
            self.label_elecmonit_com.grid(row=3, column=2, sticky="w")
            opciones_elecmonit_com = ["SIMU"] + [f'COM{i}' for i in range(1, 11)]
            self.elecmonit_com_var = tk.StringVar(value="??")
            self.elecmonit_com_optionmenu = tk.OptionMenu(self.frame2, self.elecmonit_com_var, *opciones_elecmonit_com)
            self.elecmonit_com_optionmenu.grid(row=3, column=3, sticky="w")
            self.elecmonit_com_optionmenu.configure(bg='white')

            self.label_barom_ref = tk.Label(self.frame2, text="Barómetro:", bg='white', fg='black', width=18)
            self.entry_barom_ref = tk.Entry(self.frame2, width=12)
            self.entry_barom_ref.insert(0, "IR14D/009")  
            self.label_barom_ref.grid(row=4, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_barom_ref.grid(row=4, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda
            self.label_barom_com = tk.Label(self.frame2, text="COM:", bg='white')
            self.label_barom_com.grid(row=4, column=2, sticky="w")
            opciones_barom_com = ["SIMU"] + [f'COM{i}' for i in range(1, 11)]
            self.barom_com_var = tk.StringVar(value="??")
            self.barom_com_optionmenu = tk.OptionMenu(self.frame2, self.barom_com_var, *opciones_barom_com, command=self.frame5_run)
            self.barom_com_optionmenu.grid(row=4, column=3, sticky="w")
            self.barom_com_optionmenu.configure(bg='white')

            self.label_temp_ref = tk.Label(self.frame2, text="Termómetro:", bg='white', fg='black', width=18)
            self.entry_temp_ref = tk.Entry(self.frame2, width=12)
            self.entry_temp_ref.insert(0, "IR14D/010")  
            self.label_temp_ref.grid(row=5, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_temp_ref.grid(row=5, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda
            self.label_temp_com = tk.Label(self.frame2, text="COM:", bg='white')
            self.label_temp_com.grid(row=5, column=2, sticky="w")
            opciones_temp_com = ["SIMU"] + [f'COM{i}' for i in range(1, 11)]
            self.temp_com_var = tk.StringVar(value="??")
            self.temp_com_optionmenu = tk.OptionMenu(self.frame2, self.temp_com_var, *opciones_temp_com, command=self.frame5_run_temp)
            self.temp_com_optionmenu.grid(row=5, column=3, sticky="w")
            self.temp_com_optionmenu.configure(bg='white')

            self.label_crono_ref = tk.Label(self.frame2, text="Cronómetro:", bg='white', fg='black', width=18)
            self.entry_crono_ref = tk.Entry(self.frame2, width=12)
            self.entry_crono_ref.insert(0, "IR14D/018")  
            self.label_crono_ref.grid(row=6, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_crono_ref.grid(row=6, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda

            self.label_colim_ref = tk.Label(self.frame2, text="Colimador:", bg='white', fg='black', width=18)
            self.entry_colim_ref = tk.Entry(self.frame2, width=12)
            self.entry_colim_ref.insert(0, "B80")  
            self.label_colim_ref.grid(row=7, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_colim_ref.grid(row=7, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda

            # Datos de la calibración
            self.title2_label_frame2 = tk.Label(self.frame2, text="Medidas de la Calibración", bg='white', fg='black', font=('Helvetica', 14, 'bold'))
            self.title2_label_frame2.grid(row=9, column=0, columnspan=2, sticky="w")  # El título se extiende a lo largo de dos columnas

            self.label_dist_ref = tk.Label(self.frame2, text="Distancia al foco (m):", bg='white', fg='black', width=18)
            self.entry_dist_ref = tk.Entry(self.frame2, width=12)
            self.entry_dist_ref.insert(0, "2,000")  
            self.label_dist_ref.grid(row=10, column=0, sticky="w")  # Etiqueta en la primera columna, alineada a la derecha
            self.entry_dist_ref.grid(row=10, column=1, sticky="w")  # Campo de entrada en la segunda columna, alineado a la izquierda

            # Campo de Magnitud de medida
            # self.label_fcdist_ref = tk.Label(self.frame2, text="Factor correción de distancia:", bg='white', fg='black')
            # fcdist_options = ["No", "Sí"]
            # self.combo_fcdist_ref = ttk.Combobox(self.frame2, values=fcdist_options, width=5)
            # self.combo_fcdist_ref.grid(row=10, column=0, sticky="w")
            # self.combo_fcdist_ref.grid(row=10, column=1, sticky="w", padx=5, pady=5)

            self.label_fcdist_ref = tk.Label(self.frame2, text="Factor corrección dist:", bg='white', fg='black', width=18)
            self.label_fcdist_ref.grid(row=11, column=0, sticky="w")
            # Combobox y su configuración
            fcdist_options = ["No", "Sí"]
            self.combo_fcdist_ref = ttk.Combobox(self.frame2, values=fcdist_options, width=5)
            self.combo_fcdist_ref.grid(row=11, column=1, sticky="w", padx=5, pady=5)
            self.combo_fcdist_ref.bind("<<ComboboxSelected>>", self.on_fcdist_change)
            self.data_labels = []

            #self.entry = tk.Entry(self.frame2)
            self.fcd_label = tk.Label(self.frame2, text="FCD: ", bg='white', fg='black', width=5)
            self.fcd_label.grid(row=11, column=2, sticky="w", padx=5, pady=5)
            #self.entry.bind("<Return>", self.on_entry_return)  
            self.fcd_var = tk.Entry(self.frame2, width=12)
            self.fcd_var.insert(0, "1,00")           
            self.fcd_var.grid(row=11, column=3, sticky="w", padx=5, pady=5)

            # Ajustar las configuraciones de la columna para que las etiquetas y entradas estén bien alineadas
            self.frame2.grid_columnconfigure(0, weight=1)  # Hace que la columna de las etiquetas tenga cierta expansión
            self.frame2.grid_columnconfigure(1, weight=2)  # Hace que la columna de las entradas se expanda más, para mayor espacio

            # Inicialmente ocultar todos los campos (si es necesario)
            self.title_label_frame2.grid_remove()
            self.label_proc_ref.grid_remove()
            self.entry_proc_ref.grid_remove()
            self.label_electrom_ref.grid_remove()
            self.entry_electrom_ref.grid_remove()
            self.label_elecppal_com.grid_remove()
            self.elecppal_com_optionmenu.grid_remove()
            self.label_elecmonit_ref.grid_remove()
            self.entry_elecmonit_ref.grid_remove()
            self.label_elecmonit_com.grid_remove()
            self.elecmonit_com_optionmenu.grid_remove()
            self.label_barom_ref.grid_remove()
            self.entry_barom_ref.grid_remove()
            self.label_barom_com.grid_remove()
            self.barom_com_optionmenu.grid_remove()
            self.label_temp_ref.grid_remove()
            self.entry_temp_ref.grid_remove()
            self.label_temp_com.grid_remove()
            self.temp_com_optionmenu.grid_remove()
            self.label_crono_ref.grid_remove()
            self.entry_crono_ref.grid_remove()
            self.label_colim_ref.grid_remove()
            self.entry_colim_ref.grid_remove()
            self.title2_label_frame2.grid_remove()
            self.label_dist_ref.grid_remove()
            self.entry_dist_ref.grid_remove()
            self.label_fcdist_ref.grid_remove()
            self.combo_fcdist_ref.grid_remove()
            self.fcd_label.grid_remove()
            self.fcd_var.grid_remove()

            
            # Frame 3 setup
            self.frame3 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            self.frame3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
            tk.Label(self.frame3, text="Frame 3", bg='white', fg='black').grid(row=0, column=0)

            # Frame 4 setup
            #self.frame4 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            #self.frame4.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
            #tk.Label(self.frame4, text="Frame 4", bg='white', fg='black').grid(row=0, column=0)

            # Setting up frame_row2
            self.frame_row2 = tk.Frame(self.master, borderwidth=2, relief="solid", bg='white')
            self.frame_row2.grid(row=2, column=0, sticky="ew")

            # Frame 5 setup
            self.frame5 = tk.Frame(self.frame_row2, width=400, height=400, borderwidth=2, relief="solid", bg='white')
            # self.frame5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.frame5.grid(row=0, column=0, sticky="nsew", columnspan=2)
            tk.Label(self.frame5, text="Frame 5", bg='white', fg='black').grid(row=0, column=0)
            # Ajuste de peso para las filas y columnas del frame
            self.frame5.grid_rowconfigure(0, weight=1)
            self.frame5.grid_columnconfigure(0, weight=1)

            # Frame 6 setup
            self.frame6 = tk.Frame(self.frame_row2, borderwidth=2, relief="solid", bg='white')
            self.frame6.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
            tk.Label(self.frame6, text="Frame 6", bg='white', fg='black').grid(row=0, column=0)

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

    def frame5_run(self, selection=None):
        self.running = False
        self.data_barom = []
        fig_width = 250  # Ancho deseado de la figura en píxeles
        fig_height = 250  # Altura deseada de la figura en píxeles
        dpi = 100  # Puntos por pulgada (dpi) de la figura
        self.fig_barom, self.ax_barom = plt.subplots(figsize=(fig_width / dpi, fig_height / dpi))
        self.canvas_barom = FigureCanvasTkAgg(self.fig_barom, master=self.frame5)
        self.canvas_barom.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.data_barom = []
        self.on_port_select(selection)
        self.update_graph()

    def frame5_run_temp(self, selection=None):
        self.running = False
        self.data_temp = []
        fig_width = 250  # Ancho deseado de la figura en píxeles
        fig_height = 250  # Altura deseada de la figura en píxeles
        dpi = 100  # Puntos por pulgada (dpi) de la figura
        self.fig_temp, self.ax_temp = plt.subplots(figsize=(fig_width / dpi, fig_height / dpi))
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.frame5)
        self.canvas_temp.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        self.data_temp = []
        self.on_port_select_temp(selection)
        self.update_graph_temp()

    def on_port_select(self, selection):
        self.port = selection if selection != "SIMU" else None
        self.running = True
        if selection == "SIMU":
            self.simulate_data()
        else:
            if self.port:
                self.measure_continuously()

    def on_port_select_temp(self, selection):
        self.port = selection if selection != "SIMU" else None
        self.running = True
        if selection == "SIMU":
            self.simulate_data_temp()
        else:
            if self.port:
                self.measure_continuously_temp()            

    def simulate_data(self):
        if self.running:
            new_data = random.randint(93500, 94500)
            self.data_barom.append((datetime.datetime.now(), new_data))
            self.update_graph()  # Actualiza el gráfico después de añadir nuevos datos.
            self.after(5000, self.simulate_data)  # Repite la simulación cada 5 segundos.

    def simulate_data_temp(self):
        if self.running:
            new_data = random.randint(19, 21)
            self.data_temp.append((datetime.datetime.now(), new_data))
            self.update_graph_temp()  # Actualiza el gráfico después de añadir nuevos datos.
            self.after(5000, self.simulate_data_temp)        

    def measure_continuously(self):
        if self.running:
            response = None
            try:
                with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
                    ser.write((command + '\r\n').encode('utf-8'))
                    time.sleep(1)
                    response = ''
                    while ser.in_waiting > 0:
                        response += ser.read(ser.in_waiting).decode('utf-8')
                        time.sleep(0.2)
            except serial.SerialException:
                print("Error: Unable to read from serial port")
            return response.strip()
        
    def measure_continuously_temp(self):
        if self.running:
            response = None
            try:
                with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
                    ser.write((command + '\r\n').encode('utf-8'))
                    time.sleep(1)
                    response = ''
                    while ser.in_waiting > 0:
                        response += ser.read(ser.in_waiting).decode('utf-8')
                        time.sleep(0.2)
            except serial.SerialException:
                print("Error: Unable to read from serial port")
            return response.strip()   
        
    def update_graph(self):
        self.ax_barom.clear()
        if self.data_barom:
            times, pressures = zip(*self.data_barom)
            times = [mdates.date2num(time) for time in times]
            self.ax_barom.plot(times, pressures, marker='o', linestyle='-')
            self.ax_barom.set_title("PRESIÓN", fontsize=8)
            self.ax_barom.set_xlabel("Tiempo", fontsize=5)
            self.ax_barom.set_ylabel("Presión (Pa)", fontsize=5)
            self.ax_barom.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            self.ax_barom.figure.autofmt_xdate(rotation=45)
            # Cambiar el tamaño de los ejes X e Y
            self.ax_barom.tick_params(axis='x', labelsize=5)
            self.ax_barom.tick_params(axis='y', labelsize=5)
        self.canvas_barom.draw()

    def update_graph_temp(self):
        self.ax_temp.clear()
        if self.data_temp:
            times, temperatures = zip(*self.data_temp)
            times = [mdates.date2num(time) for time in times]
            self.ax_temp.plot(times, temperatures, marker='o', linestyle='-')
            self.ax_temp.set_title("TEMPERATURA", fontsize=8)
            self.ax_temp.set_xlabel("Tiempo", fontsize=5)
            self.ax_temp.set_ylabel("Temperatura (C)", fontsize=5)
            self.ax_temp.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            self.ax_temp.figure.autofmt_xdate(rotation=45)
            # Cambiar el tamaño de los ejes X e Y
            self.ax_temp.tick_params(axis='x', labelsize=5)
            self.ax_temp.tick_params(axis='y', labelsize=5)
        self.canvas_temp.draw()     



##### START CALCULO FACTOR DE CORRECCIÓN POR DISTANCIA

    def on_fcdist_change(self, event):
        if self.combo_fcdist_ref.get() == "Sí":
            self.setup_initial_measurement_interface()
        elif self.combo_fcdist_ref.get() == "No":
            # Configura fcd_var a 1 y lo hace solo lectura
            self.fcd_var.config(state='normal')  # Cambia el estado a normal para permitir la edición
            self.fcd_var.delete(0, 'end')  # Elimina el contenido actual
            self.fcd_var.insert(0, "1.00")  # Inserta el valor '1.00'
            self.fcd_var.config(state='readonly')  # Vuelve a ponerlo como solo lectura
            
            # Llama al método calibration_mode
            self.calibration_mode()

    def setup_initial_measurement_interface(self):
        self.frame3 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
        self.frame3.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

        self.label_title = tk.Label(self.frame3, text="Medidas del factor de corrección por distancia", bg='white', fg='black', font=('Arial', 16, 'bold'))
        self.label_title.grid(row=0, column=0, columnspan=4)

        tk.Label(self.frame3, text="Tiempo (s)", font=('Arial', 8)).grid(row=1, column=0, sticky='w', padx=5)
        self.entry_time = tk.Entry(self.frame3, font=('Arial', 8), width=15)
        self.entry_time.grid(row=1, column=1, sticky='w', padx=5)
        self.entry_time.insert(0, '60')

        tk.Label(self.frame3, text="Rango de Electrómetros", font=('Arial', 8)).grid(row=1, column=2, sticky='w', padx=5)
        electrometer_range = ["LOW", "HIGH"]
        self.combo_range = ttk.Combobox(self.frame3, values=electrometer_range, width=15, font=('Arial', 8))
        self.combo_range.grid(row=1, column=3, sticky='w', padx=5)
        self.combo_range.bind("<<ComboboxSelected>>", self.update_display_range)

    def update_display_range(self, event):
        if not hasattr(self, 'start_button'):
            self.start_button = tk.Button(self.frame3, text="Iniciar Mediciones de Corriente de fuga", bg='green', fg='#71FF33', command=lambda: self.perform_measurements(0))
            self.start_button.grid(row=3, column=0, columnspan=4)

    def create_measurement_table(self, start_row):
        headers = ["Presión (hPa)", "Temperatura (°C)", "Temp. monitor (°C)", "Carga Principal (nC)", "Carga Monitor (nC)", "Int. Equipo (A)", "Int. Monitor (A)"]
        for i, header in enumerate(headers):
            label = tk.Label(self.frame3, text=header, font=('Arial', 10), bg='lightgrey', width=15)
            label.grid(row=start_row + 1, column=i, sticky='ew')  # Offset by 1 to make space for the description text
        data_labels = [[tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=15) for _ in headers] for _ in range(5)]
        for row_index, row in enumerate(data_labels):
            for col_index, label in enumerate(row):
                label.grid(row=start_row + row_index + 2, column=col_index, sticky='ew')  # Offset to start after the headers
        return data_labels

    def perform_measurements(self, tanda):
        # Incrementar el offset de inicio en función del número de tandas y de los elementos añadidos en cada tanda
        if tanda == 0:
            start_row = 4  # Para la primera tanda, empieza en la fila 4
        else:
            # Aumentar el start_row según el número de tandas previas más el espacio para las filas de promedios, decisiones y una fila adicional
            start_row = 4 + tanda * (5 + 5)  # 5 filas de medidas, 1 fila de promedio, 1 fila de desviación, 1 fila de decisiones y 1 fila adicional para separación

        description_texts = ["Medida de fugas", "Medidas a distancia lejana (m)", "Medidas a distancia cercana (m)"]
        description_label = tk.Label(self.frame3, text=description_texts[tanda],
                                    bg='black', fg='white', 
                                    font=('Helvetica', 14, 'bold'))
        description_label.grid(row=start_row, column=0, columnspan=7, sticky='wens')  # Ajustado para ocupar 6 columnas


        # Introducción para "Medidas a distancia lejana"
        if tanda == 1:
            distant_entry = tk.Entry(self.frame3, font=('Arial', 8), width=10)
            distant_entry.grid(row=start_row, column=5)
        elif tanda == 2:
            close_entry = tk.Entry(self.frame3, font=('Arial', 8), width=10)
            close_entry.grid(row=start_row, column=5)

        labels = self.create_measurement_table(start_row)
        if len(self.data_labels) <= tanda:
            self.data_labels.append(labels)
        else:
            self.data_labels[tanda] = labels

        if hasattr(self, 'start_button'):
            self.start_button.grid_remove()

        self.simulate_data(tanda, start_row)

    def simulate_data(self, tanda, start_row):
        num_medidas = 5
        data = {
            "Presión (hPa)": np.random.normal(loc=1013, scale=5, size=num_medidas),
            "Temp. equipo (°C)": np.random.normal(loc=25, scale=1, size=num_medidas),
            "Temp. monitor (°C)": np.random.uniform(low=19, high=21, size=num_medidas),
            "Carga equipo (nC)": np.random.normal(loc=10, scale=2, size=num_medidas),
            "Carga monitor (nC)": np.random.normal(loc=10, scale=2, size=num_medidas)
        }
        df = pd.DataFrame(data)

        int_ppal_values = [self.calculate_int_ppal(row) for _, row in df.iterrows()]
        int_monitor_values = [self.calculate_int_monitor(row) for _, row in df.iterrows()]

        df['Int. Equipo (A)'] = int_ppal_values
        df['Int. Monitor (A)'] = int_monitor_values

        for row_index, (_, row) in enumerate(df.iterrows()):
            for col_index, value in enumerate(row):
                self.data_labels[tanda][row_index][col_index].config(text=f"{value:.2f}")

        # Calculate and display average and standard deviation for each column
        for col_index, column_name in enumerate(df.columns):
            avg_value = np.mean(df[column_name])
            std_value = np.std(df[column_name])
            if tanda == 1 or tanda == 2:
                if column_name == "Int. Equipo (A)":
                    setattr(self, f"avg_int_equipo_tanda_{tanda}", avg_value)
                if column_name == "Int. Monitor (A)":
                    setattr(self, f"avg_int_monitor_tanda_{tanda}", avg_value)
            avg_label = tk.Label(self.frame3, text=f"Prom: {avg_value:.2f}", font=('Arial', 8), bg='lightyellow')
            avg_label.grid(row=start_row + num_medidas + 2, column=col_index, sticky='ew')

            std_label = tk.Label(self.frame3, text=f"Desv: {std_value:.2f}", font=('Arial', 8), bg='lightyellow')
            std_label.grid(row=start_row + num_medidas + 3, column=col_index, sticky='ew')

##### XANDRA START: Revisa este cálculo del FCD
        if tanda == 2:  # Print the averages after the third tanda
            print(f"Average Int. Equipo (A) in Tanda 2: {self.avg_int_equipo_tanda_1:.2f}")
            print(f"Average Int. Monitor (A) in Tanda 2: {self.avg_int_monitor_tanda_1:.2f}")
            print(f"Average Int. Equipo (A) in Tanda 3: {self.avg_int_equipo_tanda_2:.2f}")
            print(f"Average Int. Monitor (A) in Tanda 3: {self.avg_int_monitor_tanda_2:.2f}")
            # Calculate FCD value
            fcd_value = (self.avg_int_equipo_tanda_1 * self.avg_int_monitor_tanda_2) / \
                        (self.avg_int_equipo_tanda_2 * self.avg_int_monitor_tanda_1)
            self.fcd_var = tk.Entry(self.frame2, width=12, state='readonly')  # Inicializa el Entry en modo solo lectura
            self.fcd_var.insert(0, f"{fcd_value:.2f}")  # Inserta el valor formateado a dos decimales
            self.fcd_var.grid(row=11, column=3, sticky="w", padx=5, pady=5)  # Ubica el Entry en la interfaz
##### XANDRA END:

        decision_row = start_row + num_medidas + 4
        self.setup_next_tanda(decision_row, tanda)

    def setup_next_tanda(self, decision_row, tanda):
        options_label = tk.Label(self.frame3, text="Opciones posibles:", bg='#FFB233', font=('Arial', 10))
        options_label.grid(row=decision_row, column=0, sticky='w', padx=5)
        
        # Adjusting options for tanda 2
        if tanda == 2:
            options = ["Reiniciar medidas", "Calculo del FCD y continuar"]
        else:
            options = ["Reiniciar medidas", "Continuar con las medidas"]

        decision_combo = ttk.Combobox(self.frame3, values=options, width=30)
        decision_combo.grid(row=decision_row, column=1, columnspan=2, sticky='w')
        decision_combo.bind("<<ComboboxSelected>>", lambda e: self.on_decision_made(e, tanda))

    def on_decision_made(self, event, tanda):
        choice = event.widget.get()
        if choice == "Reiniciar medidas":
            # Clear all labels for the current tanda
            for label_row in self.data_labels[tanda]:
                for label in label_row:
                    label.config(text="")
            self.perform_measurements(tanda)  # Restart measurements for the current tanda
        elif choice == "Continuar con las medidas":
            self.perform_measurements(tanda + 1)  # Proceed to the next tanda
        elif choice == "Calculo del FCD y continuar" and tanda == 2:
            # Clear frame3 contents
            for widget in self.frame3.winfo_children():
                widget.destroy()
            self.calibration_mode()

##### XANDRA_START: Estos cálculos de INTENSIDAD me los he inventado. Poner la clase verdadera
    def calculate_int_ppal(self, row):
        pressure = row["Presión (hPa)"]
        temperature = row["Temp. equipo (°C)"]
        charge_ppal = row["Carga equipo (nC)"]
        return (pressure * temperature * charge_ppal) / 1000  # Convertido a Amperios

    def calculate_int_monitor(self, row):
        pressure = row["Presión (hPa)"]
        temperature = row["Temp. monitor (°C)"]
        charge_monitor = row["Carga monitor (nC)"]
        return (pressure * temperature * charge_monitor) / 1000  # Convertido a Amperios
##### XANDRA_END: Cuidado con el formato decimal.

    def run(self):
        self.mainloop()

##### FIN CALCULO DEL FACTOR DE CORRECCION POR DISTANCIA    


    def update_labels(self, event):
        option = self.combo_units.get()
        unitsrate = ""  # Inicializar con un valor por defecto
        unitsunit = ""  # Inicializar con un valor por defecto
        if option in ["Equivalente de dosis direccional H´(0,07)", "Equivalente de dosis direccional H´(3)", "Equivalente de dosis ambiental H*(10)"]:
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
        self.label_proc_ref.grid(row=1, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_proc_ref.grid(row=1, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_electrom_ref.grid(row=2, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_electrom_ref.grid(row=2, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_elecppal_com.grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.elecppal_com_optionmenu.grid(row=2, column=3, sticky="w", padx=5, pady=2)
        self.label_elecmonit_ref.grid(row=3, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_elecmonit_ref.grid(row=3, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_elecmonit_com.grid(row=3, column=2, sticky="w", padx=5, pady=2)
        self.elecmonit_com_optionmenu.grid(row=3, column=3, sticky="w", padx=5, pady=2)
        self.label_barom_ref.grid(row=4, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_barom_ref.grid(row=4, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_barom_com.grid(row=4, column=2, sticky="w", padx=5, pady=2)
        self.barom_com_optionmenu.grid(row=4, column=3, sticky="w", padx=5, pady=2)
        self.label_temp_ref.grid(row=5, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_temp_ref.grid(row=5, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_temp_com.grid(row=5, column=2, sticky="w", padx=5, pady=2)
        self.temp_com_optionmenu.grid(row=5, column=3, sticky="w", padx=5, pady=2)
        self.label_crono_ref.grid(row=6, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_crono_ref.grid(row=6, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_colim_ref.grid(row=7, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_colim_ref.grid(row=7, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.title2_label_frame2.grid(row=9, column=0, columnspan=2, sticky="w", pady=(10, 0)) 
        self.label_dist_ref.grid(row=10, column=0, sticky="w", padx=5, pady=2)  # Etiqueta alineada a la derecha
        self.entry_dist_ref.grid(row=10, column=1, sticky="w", padx=5, pady=2)  # Entrada alineada a la izquierda
        self.label_fcdist_ref.grid(row=11, column=0, sticky="w", padx=5, pady=2)
        self.combo_fcdist_ref.grid(row=11, column=1, sticky="w", padx=5, pady=2)
        self.fcd_label.grid(row=11, column=2, sticky="w", padx=5, pady=2)
        self.fcd_var.grid(row=11, column=3, sticky="w", padx=5, pady=2)

    def fetch_correction_factor(self, event):
        try:
            file_path = 't:/SIGOR/SGC/MARXA/Pruebas de desarrollo/IR14D/CoefConversion.json'
            # Leer el archivo JSON
            self.df = pd.read_json(file_path)
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return  # Salir del método si la carga falla

        # Obtener valores de calidad y medida de los comboboxes como texto
        calidad = str(self.combo_quality.get())
        medida = str(self.combo_units.get())  # Este será el nombre de la columna para la medida

        print(f"Calidad seleccionada como texto: {calidad}")
        print(f"Medida seleccionada como texto: {medida}")

        # Verificar que ambos campos están seleccionados
        if calidad and medida:
            # Filtrar el DataFrame por la calidad seleccionada
            filtered_df = self.df[self.df['Calidad'] == calidad]

            if not filtered_df.empty and medida in filtered_df.columns:
                # Extraer el factor de corrección para la calidad y medida seleccionada
                correction_factor = filtered_df.iloc[0][medida]
                # Asegurar que el separador decimal es un punto para procesarlo como float
                if ',' in correction_factor:
                    correction_factor = correction_factor.replace(',', '.')

                # Formatear el número como un string con dos decimales, manteniendo la coma como separador decimal
                correction_factor_str = "{:.3f}".format(float(correction_factor)).replace('.', ',')
                print(f"Coef Conversion: {correction_factor_str}")
                self.correction_factor_var.set(correction_factor_str)  # Actualizar la variable de control con el nuevo valor
            else:
                # Informar si no se encontraron combinaciones válidas
                print("No se encontraron datos para la combinación de calidad y medida proporcionada.")
        else:
            # Avisar si alguno de los campos no está seleccionado
            print("Debe seleccionar una calidad y una medida para buscar el factor de corrección.")

    def update_values(self, event=None):
        quality = self.combo_quality.get()
        chamber = self.combo_chamber.get()
        print(f"Calidad: {quality}")
        print(f"Cámara: {chamber}")

        if quality and chamber:
            # Determinar el coeficiente basado en las condiciones dadas
            if quality.startswith('N') or quality.startswith('L'):
                if chamber == "NE 2575-ns557-IR14D/014":
                    self.calibration_coefficient_var.set('43700')
                elif chamber == "NE 2575-ns506-IR14D/006":
                    self.calibration_coefficient_var.set('43660')
            elif quality.startswith('W'):
                if chamber == "NE 2575-ns557-IR14D/014":
                    self.calibration_coefficient_var.set('43080')
                elif chamber == "NE 2575-ns506-IR14D/006":
                    self.calibration_coefficient_var.set('43150')
        print(f"Coef Calibración: {self.calibration_coefficient_var.get()}")

    def on_entry_return(self, event):
        nuevo_valor = self.entry.get()
        self.actualizar_factor_correccion(nuevo_valor)

    def actualizar_factor_correccion(self, nuevo_valor):
        self.correction_factor_var.set(nuevo_valor)

    def update_calibration_factor(self, event):
        quality = self.combo_quality.get()
        chamber = self.combo_chamber.get()
        value = self.data.get(quality, {}).get(chamber, "N/A")  # Recupera el valor basado en la calidad y la cámara

        try:
            # Asegurarse de que 'value' es un flotante antes de formatear
            numeric_value = float(value)  # Intenta convertir el valor a float
            formatted_value = f"{numeric_value:.3f}".replace('.', ',')  # Formatea y reemplaza el punto por una coma
        except ValueError:
            # Si 'value' no puede convertirse a float, manejar como un caso especial
            formatted_value = "N/A"  # Mantener o asignar un valor por defecto que indica no disponible o no aplicable

        self.calibration_factor_var.set(formatted_value)  # Actualiza la variable de tkinter con el valor formateado

    def handle_quality_selected(self, event):
        self.fetch_correction_factor(event)
        self.update_values(event)
        self.update_calibration_factor(event)
        # Cualquier otra función que necesite ser llamada cuando se selecciona un valor.

    def handle_chamber_selected(self, event):
        self.fetch_correction_factor(event)
        self.update_values(event)
        self.update_calibration_factor(event)
        self.update_fields(event)

    def handle_final_decision(self, event):
        choice = self.decision_combo.get()
        last_row_start = len(self.data_labels) + 18

        if choice == "Reiniciar última medida":
            # Limpiar los datos de la última tanda de medidas y preparar para reingreso
            for i in range(5):
                for label in self.data_labels[-i]:
                    label.config(text="")
            self.new_distance_entry = tk.Entry(self.frame3, font=('Arial', 8), width=15)
            self.new_distance_entry.grid(row=last_row_start, column=1, sticky='w')
            self.new_distance_entry.delete(0, tk.END)
            self.new_distance_entry.insert(0, "Ingrese nueva distancia en metros")
            
            self.new_start_button = tk.Button(self.frame3, text="Iniciar Medida", bg='blue', fg='white', command=self.new_continue_measurements)
            self.new_start_button.grid(row=last_row_start + 1, column=0, columnspan=3)  # Mostrar botón para reiniciar medida

        elif choice == "Iniciar nueva tanda de 5 medidas":
            # Configurar para nuevas medidas
            self.new_distance_entry = tk.Entry(self.frame3, font=('Arial', 8), width=15)
            self.new_distance_entry.grid(row=last_row_start, column=1, sticky='w')
            self.new_distance_entry.delete(0, tk.END)
            self.new_distance_entry.insert(0, "Ingrese nueva distancia en metros")
            
            self.new_start_button = tk.Button(self.frame3, text="Iniciar Nueva Tanda", bg='blue', fg='white', command=self.new_continue_measurements)
            self.new_start_button.grid(row=last_row_start + 1, column=0, columnspan=3)  # Mostrar botón para nuevas medidas



    def calibration_mode(self):
        calibration_label = tk.Label(self.frame3, text="CALIBRACIÓN DEL EQUIPO", bg='white', fg='black', font=('Helvetica', 14, 'bold'))
        calibration_label.grid(row=0, column=0, columnspan=4, sticky='w', padx=5, pady=5)
        
   

def main():
    root = tk.Tk()
    # app = ir14dGUI(master=root)
    root.configure(bg='white')
    # frame = tk.Frame(root, bg='white')
    root.mainloop()

# Si este archivo se ejecuta como programa principal, se iniciará la GUI.
if __name__ == "__main__":
    # Crear una ventana de carga
    app = ir14dGUI()
    app.mainloop()
    
