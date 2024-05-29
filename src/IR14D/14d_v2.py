import tkinter as tk
import _tkinter
print("Cargando el programa al 5%...")
from tkinter import ttk
print("Cargando el programa al 10%...")
import tkinter.ttk as ttk
from tkinter import Label
print("Cargando el programa al 15%...")
from tkinter import Toplevel
from tkcalendar import DateEntry
import tkinter.font as tkFont
from tkinter import messagebox
print("Cargando el programa al 25%...")
import os
import pandas as pd
print("Cargando el programa al 35%...")
import openpyxl
from openpyxl.utils import get_column_letter
print("Cargando el programa al 40%...")
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
print("Cargando el programa al 50%...")
import json
from tkinter import font  # Importar el módulo de fuente
import matplotlib.pyplot as plt
print("Cargando el programa al 60%...")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np
import serial
print("Cargando el programa al 75%...")
import time
import datetime
import random
print("Cargando el programa al 90%...")
import math
import cv2
from PIL import Image, ImageTk
print("PROGRAMA EN EJECUCIÓN")


def as_text(value):
    return str(value) if value is not None else ""

class ir14dGUI(tk.Tk):
    # def __init__(self, master):
    def __init__(self):
        super().__init__()
        # self.master = master
        self.title("IR14D - PATRÓN DE RAYOS X")
        self.dataxls = {}
        self.datamed = {}
        self.datafcd = {}
        self.avg_int_ppal_patron_t0 = None
        self.avg_int_monitor_t0 = None
        self.avg_int_ppal_tanda_1 = None
        self.avg_int_monitor_tanda_2 = None
        self.avg_int_ppal_tanda_2 = None
        self.avg_int_monitor_tanda_1 = None
        self.avg_int_equipo_tanda_1 = None
        self.avg_int_equipo_tanda_2 = None
        self.avg_int_monitor_tanda_1 = None
        self.avg_int_monitor_tanda_2 = None
        self.fcd_var = tk.DoubleVar()
        self.fcd_var.set(1.0000)
        self.combo_fcdist_ref = None
        self.measure_var = tk.IntVar(value=1) 
        self.calibration_coefficient_var = tk.StringVar(value="1.0")
        self.correction_factor_var = tk.StringVar(value="1.0")
        self.canvas_barom = None
        self.fig_barom = None
        self.ax_barom = None
        self.canvas_temp = None
        self.fig_temp = None
        self.ax_temp = None

        custom_font = ("Helvetica", 12)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="black")
        style.configure("TEntry", fieldbackground="white", background="white")
        style.configure("TCombobox", fieldbackground="white", background="white")
        style.configure('Leftalign.TCombobox', justify='left') 
        style.configure('Rightalign.TCombobox', justify='right')
        style.theme_use("clam")  # Usa un tema que permita la configuración de colores
        style.configure("CustomCombobox.TCombobox", fieldbackground="#F8FEE4", background="#F8FEE4", font=custom_font)

        # self.correction_factor_str = "0.00"  # Valor inicial
        self.correction_factor_var = tk.StringVar(value="0.0")
        self.calibration_coefficient_var = tk.StringVar(value="0.0")
        
        # Font for the title
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

        # Frame for the title
        self.titulo_frame = tk.Frame(self, height=30, bg='#F8FEE4')
        self.titulo_frame.grid(row=0, column=0, sticky="ew", columnspan=4) 
        self.grid_columnconfigure(0, weight=1)
        label = tk.Label(self.titulo_frame, text="PATRONES DE RAYOS X - IR14D", font=self.title_font, bg='#F8FEE4')
        label.grid(row=0, sticky="ew")

        # Create the frames of the first row
        self.frame_row1 = tk.Frame(self.master, borderwidth=2, relief="solid", bg='white')
        self.frame_row1.grid(row=1, column=0, sticky="ew")

        self.frame1 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame_row1.grid_columnconfigure(0, weight=1)  # Make frame1 expand to fill the space

        # Subframe for top options
        self.subframe1_top = tk.Frame(self.frame1, borderwidth=2, relief="solid", bg='#F8FEE4')
        self.subframe1_top.grid(row=0, column=0, sticky="ew")
        
        # Creando una fuente personalizada
        custom_font = font.Font(family="Helvetica", size=16, weight="bold")
        # Aplicar la fuente al Label
        label = tk.Label(self.subframe1_top, text="Medida a realizar:", fg='black', bg='#F8FEE4', font=custom_font)
        label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Aplicar la fuente al Combobox
        self.option_var = tk.StringVar()
        self.option_menu = ttk.Combobox(self.subframe1_top, values=["Calibración de equipos", "Asignación de dosis"], style="CustomCombobox.TCombobox", textvariable=self.option_var)
        self.option_menu.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
##### GUARDO DATOS SERVICIO: START
        self.option_menu.bind("<FocusOut>", self.update_option_menuppal)
        # Variable para almacenar la opción principal
        self.option_menuppal = tk.StringVar()        
##### GUARDO DATOS SERVICIO: END        
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
            self.subframe1_bottom.grid(row=1, column=0, sticky="nsew") 
            
            # Título para el subframe
            tk.Label(self.subframe1_bottom, text="Datos del Servicio Técnico", bg='#F8FEE4', fg='black', font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

            # Campo de Referencia del Servicio Técnico
            tk.Label(self.subframe1_bottom, text="Referencia del Servicio Técnico:", bg='white', fg='black').grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.entry_ref_servicio = tk.Entry(self.subframe1_bottom)
            self.entry_ref_servicio.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START
            self.entry_ref_servicio.bind("<FocusOut>", self.save_entry_ref_servicio)     
##### GUARDO DATOS SERVICIO: END

            # Etiqueta para el campo de fecha
            tk.Label(self.subframe1_bottom, text="Fecha del Servicio:", bg='white', fg='black').grid(row=2, column=0, sticky="w", padx=5, pady=5)            
            # Campo de entrada de fecha con calendario desplegable
            self.date_entry = DateEntry(self.subframe1_bottom, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
            self.date_entry.delete(0, "end")
            self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START    
            self.date_entry.bind("<FocusOut>", self.save_date)
##### GUARDO DATOS SERVICIO: END

            # Campo de Supervisor
            tk.Label(self.subframe1_bottom, text="Supervisor/a:", bg='white', fg='black').grid(row=3, column=0, sticky="w", padx=5, pady=5)
            self.combo_supervisor = ttk.Combobox(self.subframe1_bottom, values=["Marta Borrego Ramos", "Xandra Campo Blanco", "Miguel Embid Segura"])
            self.combo_supervisor.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START
            self.combo_supervisor.bind("<FocusOut>", self.save_supervisor) 
##### GUARDO DATOS SERVICIO: END

            # Datos del Equipo a calibrar
            tk.Label(self.subframe1_bottom, text="Datos del Equipo a calibrar", bg='#F8FEE4', fg='black', font=('Helvetica', 14, 'bold')).grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)

            # Campo de Cliente
            tk.Label(self.subframe1_bottom, text="Cliente:", bg='white', fg='black').grid(row=6, column=0, sticky="w", padx=5, pady=5)
            self.entry_cliente = tk.Entry(self.subframe1_bottom)
            self.entry_cliente.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START
            self.entry_cliente.bind("<FocusOut>", self.save_entry_cliente) 
##### GUARDO DATOS SERVICIO: END


            # Campo de Dirección Cliente
            tk.Label(self.subframe1_bottom, text="Dirección Cliente:", bg='white', fg='black').grid(row=7, column=0, sticky="w", padx=5, pady=5)
            self.dir_cliente = tk.Text(self.subframe1_bottom, height=4, width=28)
            self.dir_cliente.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
            scroll = tk.Scrollbar(self.subframe1_bottom, command=self.dir_cliente.yview)
            scroll.grid(row=7, column=2, sticky='ns')
            self.dir_cliente['yscrollcommand'] = scroll.set
##### GUARDO DATOS SERVICIO: START 
            self.dir_cliente.bind("<FocusOut>", self.save_dir_cliente)       
##### GUARDO DATOS SERVICIO: END

            # Campo de Marca
            tk.Label(self.subframe1_bottom, text="Marca:", bg='white', fg='black').grid(row=8, column=0, sticky="w", padx=5, pady=5)
            self.entry_marca = tk.Entry(self.subframe1_bottom)
            self.entry_marca.grid(row=8, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START 
            self.entry_marca.bind("<FocusOut>", self.save_entry_marca)       
##### GUARDO DATOS SERVICIO: END

            # Campo de Modelo
            tk.Label(self.subframe1_bottom, text="Modelo:", bg='white', fg='black').grid(row=9, column=0, sticky="w", padx=5, pady=5)
            self.entry_modelo = tk.Entry(self.subframe1_bottom)
            self.entry_modelo.grid(row=9, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START 
            self.entry_modelo.bind("<FocusOut>", self.save_entry_modelo)       
##### GUARDO DATOS SERVICIO: END

            # Campo de NumSerie
            tk.Label(self.subframe1_bottom, text="Número de serie:", bg='white', fg='black').grid(row=10, column=0, sticky="w", padx=5, pady=5)
            self.entry_numserie = tk.Entry(self.subframe1_bottom)
            self.entry_numserie.grid(row=10, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START 
            self.entry_numserie.bind("<FocusOut>", self.save_entry_numserie)       
##### GUARDO DATOS SERVICIO: END            

            # Datos de la calibración
            tk.Label(self.subframe1_bottom, text="Datos del tipo de calibración", bg='#F8FEE4', fg='black', font=('Helvetica', 14, 'bold')).grid(row=12, column=0, columnspan=2, sticky="w", padx=5, pady=5)

            # Campo de Magnitud de medida
            tk.Label(self.subframe1_bottom, text="Magnitud de Medida:", bg='white', fg='black').grid(row=13, column=0, sticky="w", padx=5, pady=5)
            units_options = ["Equivalente de dosis direccional H´(0,07)", "Equivalente de dosis direccional H´(3)", "Equivalente de dosis ambiental H*(10)", "Exposición", "Kerma en aire", "Dosis absorbida en aire"]
            self.combo_units = ttk.Combobox(self.subframe1_bottom, values=units_options, width=35)
            self.combo_units.grid(row=13, column=1, sticky="ew", padx=5, pady=5)
            self.combo_units.bind("<<ComboboxSelected>>", self.fetch_correction_factor)
##### GUARDO DATOS SERVICIO: START 
            self.combo_units.bind("<FocusOut>", self.save_combo_units)       
##### GUARDO DATOS SERVICIO: END 

            # Etiquetas para mostrar las unidades seleccionadas
            self.label_rate = tk.Label(self.subframe1_bottom, text="Unidades de tasa: ........", bg='white', fg='black')
            self.label_rate.grid(row=14, column=0, sticky="w", padx=5, pady=5)

            self.label_unit = tk.Label(self.subframe1_bottom, text="Unidades: ........", bg='white', fg='black')
            self.label_unit.grid(row=14, column=1, sticky="w", padx=5, pady=5)

            self.combo_units.bind("<<ComboboxSelected>>", self.update_labels)
            # self.combo_units.current('')
            self.update_labels(None)

            # Cargar datos de calibración desde JSON
            with open('calibration_data.json', 'r') as json_file:
                self.data = json.load(json_file)

            # Campo de Calidad de Radiación
            tk.Label(self.subframe1_bottom, text="Calidad de radiación:", bg='white', fg='black').grid(row=16, column=0, sticky="w", padx=5, pady=5)
            self.combo_quality = ttk.Combobox(self.subframe1_bottom, values=["L-10 1 m", "L-10 2,5 m", "L-20 1 m", "L-20 2,5 m", "L-30 1 m", "L-30 2,5 m", "L-35 1 m", "L-35 2,5 m", "L-55", "L-70", "L-100", "L-125", "L-170", "L-210", "L-240", "N-10 1 m", "N-10 2,5 m", "N-15 1 m", "N-15 2,5 m", "N-20 1 m", "N-20 2,5 m", "N-25 1 m", "N-25 2,5 m", "N-30 1 m", "N-30 2,5 m", "N-40 1 m", "N-40 2,5 m", "N-60", "N-80", "N-100", "N-120", "N-150", "N-200", "N-250", "N-300", "W-30 1 m", "W-30 2,5 m", "W-40 1 m", "W-40 2,5 m", "W-60", "W-80", "W-110", "W-150", "W-200", "W-250", "W-300"])
            self.combo_quality.grid(row=16, column=1, sticky="ew", padx=5, pady=5)            
##### GUARDO DATOS SERVICIO: START 
            self.combo_quality.bind("<FocusOut>", self.save_combo_quality)       
##### GUARDO DATOS SERVICIO: END 
            self.combo_quality.bind("<<ComboboxSelected>>", self.handle_quality_selected)
                        
            self.entry = tk.Entry(self.subframe1_bottom)
            tk.Label(self.subframe1_bottom, text="Coef. Conversión de Ka a mag. medida: ", bg='white', fg='black').grid(row=17, column=0, sticky="w", padx=5, pady=5)
            # self.entry.grid(row=16, column=0, sticky="w", padx=5, pady=5)
            self.entry.bind("<Return>", self.on_entry_return)  
            self.combo_quality.bind("<<ComboboxSelected>>", self.handle_quality_selected)            
            self.correction_factor_label = tk.Label(self.subframe1_bottom, text="Coef. Conversión de Ka a mag. medida: ", textvariable=self.correction_factor_var, bg='white', fg='black')
            self.correction_factor_label.grid(row=17, column=1, sticky="w", padx=5, pady=5)
   
            # Campo de Cámara patrón
            tk.Label(self.subframe1_bottom, text="Cámara patrón:", bg='white', fg='black').grid(row=18, column=0, sticky="w", padx=5, pady=5)
            self.combo_chamber = ttk.Combobox(self.subframe1_bottom, values=["NE 2575-ns557-IR14D/014", "NE 2575-ns506-IR14D/006"])
            self.combo_chamber.grid(row=18, column=1, sticky="ew", padx=5, pady=5)
##### GUARDO DATOS SERVICIO: START 
            self.combo_chamber.bind("<FocusOut>", self.save_combo_chamber)       
##### GUARDO DATOS SERVICIO: END             
            self.combo_chamber.bind("<<ComboboxSelected>>", self.handle_chamber_selected)         

            # Coeficiente de calibración
            self.calibration_coefficient_var = tk.StringVar()
            tk.Label(self.subframe1_bottom, text="Coeficiente de calibración:", bg='white', fg='black').grid(row=19, column=0, sticky="w")
            tk.Label(self.subframe1_bottom, textvariable=self.calibration_coefficient_var, bg='white', fg='black').grid(row=19, column=0, sticky="e", padx=5)

            # Factor de calibración
            self.calibration_factor_var = tk.StringVar()
            tk.Label(self.subframe1_bottom, text="Factor de calibración:", bg='white', fg='black').grid(row=19, column=1, sticky="w", padx=5)
            tk.Label(self.subframe1_bottom, textvariable=self.calibration_factor_var, bg='white', fg='black').grid(row=19, column=1, sticky="e", padx=5)

            # Factor de Atenuación del Aire
            self.fcaa_var = tk.StringVar()
            tk.Label(self.subframe1_bottom, text="Factor de atenuación del aire:", bg='white', fg='black').grid(row=20, column=0, sticky="w", padx=5)
            tk.Label(self.subframe1_bottom, textvariable=self.fcaa_var, bg='white', fg='black').grid(row=20, column=0, sticky="e", padx=5)

            # Asegurarse de que los widgets se expandan apropiadamente
            self.subframe1_bottom.columnconfigure(1, weight=1)

            # Frame 2
            self.frame2_row1 = tk.Frame(self)
            self.frame2_row1.grid(row=1, column=1, sticky="nsew")

            self.frame2 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            self.frame2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)  # Asumimos que frame_row1 ya está usando grid

            # Configurar las columnas del frame_row1
            self.frame2_row1.grid_columnconfigure(1, minsize=20*8)  # Aproximadamente 8 píxeles por carácter, ajustar según la fuente

            # Título para el Frame 2
            self.title_label_frame2 = tk.Label(self.frame2, text="Instrumentación", bg='#F8FEE4', fg='black', font=('Helvetica', 14, 'bold'))
            self.title_label_frame2.grid(row=0, column=0, columnspan=4, sticky="w")  

            # Campos Frame 2
            # Procedimiento
            self.label_proc = tk.Label(self.frame2, text="Procedimiento", bg='white', fg='black', width=11)
            self.label_proc.grid(row=1, column=0, sticky="w", padx=(5, 0))  # Etiqueta alineada a la izquierda
            self.combo_proc = ttk.Combobox(self.frame2, values=["P-LMRI-C-12", "P-LMRI-C-13", "P-LMRI-C-26"], width=13)  
            self.combo_proc.grid(row=1, column=1, sticky="e", padx=(0, 5))        
##### GUARDO DATOS FRAME 2: START 
            self.combo_proc.bind("<FocusOut>", self.save_combo_proc)       
##### GUARDO DATOS FRAME 2: END 
               
            # Electrómetro de medida
            self.label_electrom_ref = tk.Label(self.frame2, text="Electr. Ppal", bg='white', fg='black', width=11)
            self.label_electrom_ref.grid(row=2, column=0, sticky="w", padx=(5, 0))  # Etiqueta alineada a la izquierda
            self.combo_electrom_ref = ttk.Combobox(self.frame2, values=["IR14D-18", "IR14D-28", "IR14D-41"], width=8)
            self.combo_electrom_ref.grid(row=2, column=1, sticky="e", padx=(0, 5))       
##### GUARDO DATOS FRAME 2: START 
            self.combo_electrom_ref.bind("<FocusOut>", self.save_combo_electrom_ref)       
##### GUARDO DATOS FRAME 2: END
            # self.label_elecppal_com = tk.Label(self.frame2, text="Puerto Elec.PPal:", bg='white')
            #self.label_elecppal_com.grid(row=2, column=1, sticky="w", padx=(5, 0))
            # opciones_elecppal_com = ["SIMU"] + [f'COM{i}' for i in range(1, 11)]
            # self.elecppal_com_var = tk.StringVar(value="??")
            # self.elecppal_com_optionmenu = tk.OptionMenu(self.frame2, self.elecppal_com_var, *opciones_elecppal_com)
            # self.elecppal_com_optionmenu.grid(row=2, column=2, sticky="w", padx=(0, 5))
            # self.elecppal_com_optionmenu.configure(bg='white')

            # Electrómetro Monitor
            self.label_elecmonit_ref = tk.Label(self.frame2, text="Electr. Monitor", bg='white', fg='black', width=11)
            self.label_elecmonit_ref.grid(row=3, column=0, sticky="w", padx=(5, 0))  # Etiqueta alineada a la izquierda
            self.combo_elecmonit_ref = ttk.Combobox(self.frame2, values=["IR14D-18", "IR14D-28", "IR14D-41"], width=8)
            self.combo_elecmonit_ref.grid(row=3, column=1, sticky="e", padx=(0, 5))       
##### GUARDO DATOS FRAME 2: START 
            self.combo_elecmonit_ref.bind("<FocusOut>", self.save_combo_elecmonit_ref)       
##### GUARDO DATOS FRAME 2: END
            # self.label_elecmonit_com = tk.Label(self.frame2, text="Puerto Elec.Mon:", bg='white')
            # self.label_elecmonit_com.grid(row=3, column=1, sticky="w", padx=(5, 0))
            # opciones_elecmonit_com = ["SIMU"] + [f'COM{i}' for i in range(1, 11)]
            # self.elecmonit_com_var = tk.StringVar(value="??")
            # self.elecmonit_com_optionmenu = tk.OptionMenu(self.frame2, self.elecmonit_com_var, *opciones_elecmonit_com)
            # self.elecmonit_com_optionmenu.grid(row=3, column=2, sticky="w", padx=(0, 5))
            # self.elecmonit_com_optionmenu.configure(bg='white')

            # Barómetro
            self.label_barom_ref = tk.Label(self.frame2, text="Barómetro", bg='white', fg='black', width=11)
            self.label_barom_ref.grid(row=4, column=0, sticky="w", padx=(5, 0))
            self.combo_barom_ref = ttk.Combobox(self.frame2, values=["IR14D-09", "IR14D-30", "SIMU"], width=8)
            self.combo_barom_ref.grid(row=4, column=1, sticky="e", padx=(0, 5))
            self.combo_barom_ref.bind("<FocusOut>", self.save_combo_barom_ref)
            self.combo_barom_ref.bind("<<ComboboxSelected>>", self.on_combo_barom_ref_select)

            # Termómetro
            self.label_temp_ref = tk.Label(self.frame2, text="Termómetro", bg='white', fg='black', width=11)
            self.label_temp_ref.grid(row=5, column=0, sticky="w", padx=(5, 0))  # Etiqueta alineada a la izquierda
            self.combo_temp_ref = ttk.Combobox(self.frame2, values=["IR14D-10", "IR14D-32", "SIMU"], width=8)
            self.combo_temp_ref.grid(row=5, column=1, sticky="e", padx=(0, 5))      
##### GUARDO DATOS FRAME 2: START 
            self.combo_temp_ref.bind("<FocusOut>", self.save_combo_temp_ref)       
##### GUARDO DATOS FRAME 2: END
            self.combo_temp_ref.bind("<<ComboboxSelected>>", self.on_combo_temp_ref_select)

            # Cronómetro
            self.label_crono_ref = tk.Label(self.frame2, text="Cronómetro", bg='white', fg='black', width=11)
            self.label_crono_ref.grid(row=6, column=0, sticky="w", padx=(5, 0))  # Etiqueta alineada a la izquierda
            self.combo_crono_ref = ttk.Combobox(self.frame2, values=["IR14D-19", "IR14D-18", "IR14D-28"], width=8)
            self.combo_crono_ref.grid(row=6, column=1, sticky="e", padx=(0, 5))      
##### GUARDO DATOS FRAME 2: START 
            self.combo_crono_ref.bind("<FocusOut>", self.save_combo_crono_ref)       
##### GUARDO DATOS FRAME 2: END

            # Colimador
            self.label_colim_ref = tk.Label(self.frame2, text="Colimador", bg='white', fg='black', width=11)
            self.label_colim_ref.grid(row=7, column=0, sticky="w", padx=(5, 0))  # Etiqueta alineada a la izquierda
            self.combo_colim_ref = ttk.Combobox(self.frame2, values=["B20", "B40", "B60", "B80", "B100"], width=8)
            self.combo_colim_ref.grid(row=7, column=1, sticky="e", padx=(0, 5))      
##### GUARDO DATOS FRAME 2: START 
            self.combo_colim_ref.bind("<FocusOut>", self.save_combo_colim_ref)       
##### GUARDO DATOS FRAME 2: END

            # Datos de la calibración
            self.title2_label_frame2 = tk.Label(self.frame2, text="Medidas previas", bg='#F8FEE4', fg='black', font=('Helvetica', 14, 'bold'))
            self.title2_label_frame2.grid(row=9, column=0, columnspan=4, sticky="w")  # El título se extiende a lo largo de dos columnas

            # Distancia de irradiación
            self.label_dist_ref = tk.Label(self.frame2, text="Distancia al foco (m):", bg='white', fg='black', width=18)
            self.entry_dist_ref = tk.Entry(self.frame2, width=8, validate="key", validatecommand=(self.register(self.validate_number), "%P"))
            self.label_dist_ref.grid(row=10, column=0, sticky="w", padx=(5, 0))  # Etiqueta en la primera columna, alineada a la izquierda
            self.entry_dist_ref.grid(row=10, column=1, sticky="e", padx=(0, 5))
##### GUARDO DATOS FRAME 2: START 
            self.entry_dist_ref.bind("<FocusOut>", self.save_entry_dist_ref)       
##### GUARDO DATOS FRAME 2: END

            # Campo de Factor correción de distancia
            # Etiqueta para el combobox
            self.label_fcdist_ref = tk.Label(self.frame2, text="Factor corrección dist:", bg='white', fg='black', width=18)
            self.label_fcdist_ref.grid(row=11, column=0, sticky="w")
            fcdist_options = ["No", "Sí"]
            self.combo_fcdist_ref = ttk.Combobox(self.frame2, values=fcdist_options, width=5)
            self.combo_fcdist_ref.grid(row=11, column=1, sticky="w", padx=5, pady=5)
            self.combo_fcdist_ref.bind("<<ComboboxSelected>>", self.on_fcdist_change)

            # Factor correción de distancia
            self.fcd_label = tk.Label(self.frame2, text="FCD:")
            self.fcd_label.grid(row=12, column=0, sticky="w")           
            self.fcd_value_label = tk.Label(self.frame2, textvariable=self.fcd_var, bg='white', fg='black', width=5)
            self.fcd_value_label.grid(row=12, column=1, sticky="e")
            self.data_labels = []

            # Etiqueta Corrección electrómetro
            self.fcelec_label = tk.Label(self.frame2, text="Factor corr. rango electr.:", bg='white')
            self.fcelec_label.grid(row=13, column=0, sticky="w")
            self.fcelec_var = tk.StringVar(value='Seleccione Rango')
            self.fcelec_value_label = tk.Label(self.frame2, textvariable=self.fcelec_var, bg='white', fg='black', width=18)
            self.fcelec_value_label.grid(row=13, column=1, sticky="e")

            # Ajustar las configuraciones de la columna para que las etiquetas y entradas estén bien alineadas
            self.frame2.grid_columnconfigure(0, weight=1)  # Hace que la columna de las etiquetas tenga cierta expansión
            self.frame2.grid_columnconfigure(1, weight=2)  # Hace que la columna de las entradas se expanda más, para mayor espacio

            # Inicialmente ocultar todos los campos (si es necesario)
            self.title_label_frame2.grid_remove()
            self.label_proc.grid_remove()
            self.combo_proc.grid_remove()
            self.label_electrom_ref.grid_remove()
            self.combo_electrom_ref.grid_remove()
            # self.label_elecppal_com.grid_remove()
            # self.elecppal_com_optionmenu.grid_remove()
            self.label_elecmonit_ref.grid_remove()
            self.combo_elecmonit_ref.grid_remove()
            # self.label_elecmonit_com.grid_remove()
            # self.elecmonit_com_optionmenu.grid_remove()
            self.label_barom_ref.grid_remove()
            self.combo_barom_ref.grid_remove()
            # self.label_barom_com.grid_remove()
            # self.barom_com_optionmenu.grid_remove()
            self.label_temp_ref.grid_remove()
            self.combo_temp_ref.grid_remove()
            # self.label_temp_com.grid_remove()
            # self.temp_com_optionmenu.grid_remove()
            self.label_crono_ref.grid_remove()
            self.combo_crono_ref.grid_remove()
            self.label_colim_ref.grid_remove()
            self.combo_colim_ref.grid_remove()
            self.title2_label_frame2.grid_remove()
            self.label_dist_ref.grid_remove()
            self.entry_dist_ref.grid_remove()
            self.label_fcdist_ref.grid_remove()
            self.combo_fcdist_ref.grid_remove()
            self.fcd_label.grid_remove()
            self.fcd_value_label.grid_remove()
            self.fcelec_label.grid_remove()
            self.fcelec_value_label.grid_remove()
            
            # Frame 3 setup
            self.frame3 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
            self.frame3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
            # tk.Label(self.frame3, text="Frame 3", bg='white', fg='black').grid(row=0, column=0)

            # Setting up frame_row2
            self.frame_row2 = tk.Frame(self.master, borderwidth=2, relief="solid", bg='white')
            self.frame_row2.grid(row=2, column=0, sticky="ew")

            # Frame 5 setup
            self.frame5 = tk.Frame(self.frame_row2, width=400, height=400, borderwidth=2, relief="solid", bg='white')
            # self.frame5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.frame5.grid(row=0, column=0, sticky="nsew", columnspan=2)
            # tk.Label(self.frame5, text="Frame 5", bg='white', fg='black').grid(row=0, column=0)
            # Ajuste de peso para las filas y columnas del frame
            self.frame5.grid_rowconfigure(0, weight=1)
            self.frame5.grid_columnconfigure(0, weight=1)
            self.frame5.grid_remove()

            # Frame 6 setup
            self.frame6 = tk.Frame(self.frame_row2, borderwidth=2, relief="solid", bg='white')
            self.frame6.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
            self.setup_treeview()
            self.frame6.grid_remove()  # Oculta el frame6 inicialmente

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

 
    def validate_number(self, P):
        # Permite solo números decimales en la entrada
        if P == "" or P.isdigit():
            return True
        elif P.count('.') == 1 and P.replace('.', '').isdigit() and P.index('.') != 0:
            return True
        return False
##### GUARDANDO DATOS: START
### FRAME 1: START
    def update_option_menuppal(self, event=None):  # Puede ser llamado con o sin evento
        new_value = self.option_var.get()
        if new_value:  # Verifica si new_value no está vacío
            self.option_menuppal.set(new_value)
            self.dataxls['Tipo de Servicio'] = new_value
        
    def save_entry_ref_servicio(self, event):
        self.dataxls["Referencia del Servicio Técnico"] = [self.entry_ref_servicio.get()]
        pass         

    def save_date(self, event):
        self.dataxls["Fecha"] = [self.date_entry.get()]
        pass

    def save_supervisor(self, event):
        self.dataxls["Supervisor"] = [self.combo_supervisor.get()]
        pass

    def save_entry_cliente(self, event):
        self.dataxls["Cliente"] = [self.entry_cliente.get()]
        pass

    def save_dir_cliente(self, event):
        self.dataxls["Dirección"] = [self.dir_cliente.get("1.0", "end-1c")]
        pass

    def save_entry_marca(self, event):
        self.dataxls["Marca"] = [self.entry_marca.get()]
        pass

    def save_entry_modelo(self, event):
        self.dataxls["Modelo"] = [self.entry_modelo.get()]
        pass

    def save_entry_numserie(self, event):
        self.dataxls["Número de serie"] = [self.entry_numserie.get()]
        pass

    def save_combo_units(self, event):
        self.dataxls["Magnitud de Medida"] = [self.combo_units.get()]
        pass

    def save_label_rate(self, unitsrate):
        self.dataxls["Unidades de tasa de la Magnitud de Medida"] = [unitsrate]
        pass

    def save_label_unit(self, unitsunit):
        self.dataxls["Unidades de la Magnitud de Medida"] = [unitsunit]
        pass

    def save_combo_quality(self, event):
        self.dataxls["Calidad"] = [self.combo_quality.get()]
        pass

    def save_correction_factor(self, event):
        self.dataxls["Factor de corrección"] = [self.correction_factor_var.get()]
        pass

    def save_combo_chamber(self, event):
        self.dataxls["Cámara patrón"] = [self.combo_chamber.get()]
        pass

    def save_calibration_coefficient(self, event):
        self.dataxls["Coeficiente de calibración"] = [self.calibration_coefficient_var.get()]

        pass

    def save_calibration_factor(self, event):
        self.dataxls["Factor de calibración"] = [self.calibration_factor_var.get()]
        pass

    def save_fcaa(self, event):
        self.dataxls["Factor de Atenuación del Aire"] = [self.fcaa_var.get()]   
        pass
### FRAME 1: END
### FRAME 2: START
    def save_combo_proc(self, event):
        self.dataxls["Procedimiento utilizado"] = [self.combo_proc.get()]
        pass

    def save_combo_electrom_ref(self, event):
        self.dataxls["Electrómetro Medidas"] = [self.combo_electrom_ref.get()]
        pass

    def save_combo_elecmonit_ref(self, event):
        self.dataxls["Electrómetro Monitor"] = [self.combo_elecmonit_ref.get()]
        pass

    def save_combo_barom_ref(self, event):
        self.dataxls["Barómetro"] = [self.combo_barom_ref.get()]
        pass

    def save_combo_temp_ref(self, event):
        self.dataxls["Termómetro"] = [self.combo_temp_ref.get()]
        pass

    def save_combo_crono_ref(self, event):
        self.dataxls["Cronómetro"] = [self.combo_crono_ref.get()]
        pass
    
    def save_combo_colim_ref(self, event):
        self.dataxls["Colimador"] = [self.combo_colim_ref.get()]
        # print(self.dataxls)

    def save_entry_dist_ref(self, event):
        self.datamed["Distancia de irradiación"] = [self.entry_dist_ref.get()]
        pass

    def save_entry_time_patron(self, event):
        self.datamed["Tiempo de irradiación"] = [self.entry_time_patron.get()]
        if self.entry_time_patron.get().strip():
            self.label_Irx_patron.grid()
            self.entry_Irx_patron.grid()
        pass

    def save_entry_Irx_patron(self, event):
        self.datamed["Intensidad de irradiación"] = [self.entry_Irx_patron.get()]
        if self.entry_Irx_patron.get().strip():
            self.label_combo_range.grid()
            self.combo_range.grid()
        pass

    def save_combo_range_patron(self, event):
        self.datamed["Rango Electrómetro"] = [self.combo_range.get()]
        pass

    def save_felec_var(self, *args):
        self.datamed["Factor rango electrómetro"] = [self.fcelec_var.get()]
        pass

    def save_fcd_var(self, *args):
        try:
            value_fcd = self.fcd_var.get()
            print(f"Valor actual de fcd_var: {value_fcd}")
            self.datamed["Factor corrección distancia"] = [value_fcd]
        except _tkinter.TclError as e:
             #print(f"Error al obtener el valor de fcd_var: {e}")
            self.datamed["Factor corrección distancia"] = [1.0000] 
            pass
        
### FRAME 2: END
### DATOS FACTOR CORRECION DISTANCIA: START
    def save_entry_time_fcd(self, event):
        self.datafcd["Tiempo de irradiación FCD"] = [self.entry_time_fcd.get()]
        pass

    def save_entry_fcd(self, event):
        self.datafcd["Intensidad de irradiación FCD"] = [self.entry_fcd.get()]
        pass

    def save_combo_range_fcd(self, event):
        self.datafcd["Rango Electrómetro FCD"] = [self.combo_range_fcd.get()]
        # print(self.datafcd)
        pass

    def save_and_check_time_entry(self, event):
        self.save_entry_time_fcd(event)
        if self.entry_time_fcd.get().strip():
            self.label_fcd.grid()
            self.entry_fcd.grid()

    def save_and_check_intensity_entry(self, event):
        self.save_entry_fcd(event)
        if self.entry_fcd.get().strip():
            self.label_combo_range_fcd.grid()
            self.combo_range_fcd.grid()
### DATOS FACTOR CORRECION DISTANCIA: END
##### GUARDANDO DATOS: END

##### FRAME6 START:
    def setup_treeview(self):
        self.tree = ttk.Treeview(self.frame6, height=4, show='headings')
        self.tree.grid(row=1, column=0, sticky="nsew", columnspan=11)
        self.tree.bind("<Motion>", self.check_mouse_position)

        column_headers = [
            "Rango (Sv)",
            "Kerma aire (Gy/s)",
            f"{self.combo_quality.get()} Patrón (Sv/h)",
            f"{self.combo_quality.get()} Patrón (Sv)",
            "Equipo (Sv/h)",
            "Incertidumbre Tasa",
            "Integrada (Sv)",
            "Factor calibración (Tasa)",
            "Incertidumbre Tasa (k=2)",
            "Factor calibración (Integrada)",
            "Incertidumbre Integrada (k=2)",
            "Incertidumbre Kerma aire (k=2)",
            "Incertidumbre magnitud de medida (k=2)"
        ]
        self.columns = [f'col{i+1}' for i in range(len(column_headers))]
        self.tree['columns'] = self.columns

        for i, header in enumerate(column_headers):
            self.tree.heading(self.columns[i], text=header, anchor='w')
            self.tree.column(self.columns[i], width=100, minwidth=50, anchor='w', stretch=tk.NO)

    def check_mouse_position(self, event):
        # Detectar si el cursor está sobre algún cabecero
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            column = self.tree.identify_column(event.x)
            idx = int(column.replace('#', '')) - 1
            header = self.tree.heading(self.columns[idx])['text']
            # Muestra el texto del cabecero en una etiqueta emergente
            self.show_tooltip(header, event.x_root, event.y_root)

    def show_tooltip(self, text, x, y):
        # Destruye cualquier tooltip anterior
        if hasattr(self, 'tooltip_window'):
            self.tooltip_window.destroy()
        # Crea una nueva ventana emergente como tooltip
        self.tooltip_window = tk.Toplevel()
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=text, justify=tk.LEFT, background="yellow", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack()

##### FRAME6 END
    def on_combo_barom_ref_select(self, *args):
        self.frame5.grid(row=0, column=0, sticky="nsew", columnspan=2)
        selected_value = self.combo_barom_ref.get()
        if selected_value == "SIMU":
            self.frame5_run()

    def frame5_run(self, selection=None):
        self.running = False
        self.data_barom = []
        
        fig_width = 250  # Ancho deseado de la figura en píxeles
        fig_height = 250  # Altura deseada de la figura en píxeles
        dpi = 100  # Puntos por pulgada (dpi) de la figura

        # Inicialización del gráfico y del canvas
        self.fig_barom, self.ax_barom = plt.subplots(figsize=(fig_width / dpi, fig_height / dpi))
        if self.canvas_barom is None:
            self.canvas_barom = FigureCanvasTkAgg(self.fig_barom, master=self.frame5)
            self.canvas_barom.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        else:
            self.canvas_barom.figure = self.fig_barom
            self.canvas_barom.draw()
        
        self.running = True
        self.simulate_data_barom()
    
    def simulate_data_barom(self):
        if self.running:
            new_data = random.uniform(93.500, 94.500)
            self.data_barom.append((datetime.datetime.now(), new_data))
            self.update_graph()  # Update graph after adding new data
            self.after(5000, self.simulate_data_barom)
    
    def update_graph(self):
        self.ax_barom.clear()
        if self.data_barom:
            times, pressures = zip(*self.data_barom)
            times = [mdates.date2num(time) for time in times]
            self.ax_barom.plot(times, pressures, marker='+', linestyle='-')
            self.ax_barom.set_title("PRESIÓN", fontsize=8)
            self.ax_barom.set_xlabel("Tiempo", fontsize=5)
            self.ax_barom.set_ylabel("Presión (Pa)", fontsize=5)
            
            # Auto locator and formatter for dynamic adjustment of time display
            locator = mdates.AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(locator)
            self.ax_barom.xaxis.set_major_locator(locator)
            self.ax_barom.xaxis.set_major_formatter(formatter)
            
            self.ax_barom.figure.autofmt_xdate(rotation=45)
            self.ax_barom.tick_params(axis='x', labelsize=5)
            self.ax_barom.tick_params(axis='y', labelsize=5)
        self.canvas_barom.draw()
    
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

    def on_combo_temp_ref_select(self, *args):
        self.frame5.grid(row=0, column=0, sticky="nsew", columnspan=2)
        selected_value = self.combo_temp_ref.get()
        if selected_value == "SIMU":
            self.frame5_run_temp()

    def frame5_run_temp(self, selection=None):
        self.running = False
        self.data_temp = []
        
        fig_width_t = 250  # Ancho deseado de la figura en píxeles
        fig_height_t = 250  # Altura deseada de la figura en píxeles
        dpi_t = 100  

        # Inicialización del gráfico y del canvas
        self.fig_temp, self.ax_temp = plt.subplots(figsize=(fig_width_t / dpi_t, fig_height_t / dpi_t))
        if self.canvas_temp is None:
            self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.frame5)
            self.canvas_temp.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        else:
            self.canvas_temp.figure = self.fig_temp
            self.canvas_temp.draw()
        
        self.running = True
        self.simulate_data_temp()

    def simulate_data_temp(self):
        if self.running:
            new_data_temp = random.uniform(19.0, 21.0)
            self.data_temp.append((datetime.datetime.now(), new_data_temp))
            self.update_graph_temp()  # Update graph after adding new data
            self.after(5000, self.simulate_data_temp)

    def update_graph_temp(self):
        self.ax_temp.clear()
        if self.data_temp:
            times, temperatures = zip(*self.data_temp)
            times = [mdates.date2num(time) for time in times]
            self.ax_temp.plot(times, temperatures, marker='+', linestyle='-')
            self.ax_temp.set_title("TEMPERATURA", fontsize=8)
            self.ax_temp.set_xlabel("Tiempo", fontsize=5)
            self.ax_temp.set_ylabel("Temperatura (C)", fontsize=5)
            
            # Auto locator and formatter for dynamic adjustment of time display
            locator = mdates.AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(locator)
            self.ax_temp.xaxis.set_major_locator(locator)
            self.ax_temp.xaxis.set_major_formatter(formatter)
            
            self.ax_temp.figure.autofmt_xdate(rotation=45)
            self.ax_temp.tick_params(axis='x', labelsize=5)
            self.ax_temp.tick_params(axis='y', labelsize=5)
        self.canvas_temp.draw()
                   
        
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
    

##### START CALCULO FACTOR DE CORRECCIÓN POR DISTANCIA
    def on_fcdist_change(self, event):
        selection = self.combo_fcdist_ref.get()
        if selection == "No":
            self.fcd_var.set(1.0000)
            self.save_fcd_var()
            self.calibration_mode()
        elif selection == "Sí":
            self.fcd_var.set(self.setup_initial_measurement_interface())
            self.save_fcd_var()

    def setup_initial_measurement_interface(self):
        self.frame3 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
        self.frame3.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

        self.label_title = tk.Label(self.frame3, text="Medidas del FACTOR DE CORRECCIÓN POR DISTANCIA", bg='#12461E', fg='white', font=('Arial', 16, 'bold'))
        self.label_title.grid(row=0, column=0, columnspan=7)

        # Tiempo de irradiación
        self.label_time_fcd = tk.Label(self.frame3, text="Tiempo (s)", font=('Arial', 8), bg='lightgray')
        self.entry_time_fcd = tk.Entry(self.frame3, width=8, bg='#F8FEE4', validate="key", validatecommand=(self.frame3.register(self.validate_number), "%P"))
        self.label_time_fcd.grid(row=1, column=0, sticky="w", padx=(10, 0))
        self.entry_time_fcd.grid(row=1, column=1, sticky="w", padx=(0, 5))
        self.entry_time_fcd.bind("<FocusOut>", self.save_and_check_time_entry)

        # Intensidad de irradiación (oculto inicialmente)
        self.label_fcd = tk.Label(self.frame3, text="Intensidad (A)", font=('Arial', 8), bg='lightgray')
        self.entry_fcd = tk.Entry(self.frame3, width=8, bg='#F8FEE4', validate="key", validatecommand=(self.frame3.register(self.validate_number), "%P"))
        self.label_fcd.grid(row=1, column=2, sticky="w", padx=(5, 0))
        self.entry_fcd.grid(row=1, column=3, sticky="w", padx=(0, 5))
        self.label_fcd.grid_remove()
        self.entry_fcd.grid_remove()
        self.entry_fcd.bind("<FocusOut>", self.save_and_check_intensity_entry)

        # Rango del electrómetro (oculto inicialmente)
        self.label_combo_range_fcd = tk.Label(self.frame3, text="Rango de Electrómetros", font=('Arial', 8), bg='lightgray')
        electrometer_range_fcd = ["LOW", "HIGH"]
        self.combo_range_fcd = ttk.Combobox(self.frame3, values=electrometer_range_fcd, width=15, font=('Arial', 8))
        self.label_combo_range_fcd.grid(row=1, column=4, sticky='w', padx=5)
        self.combo_range_fcd.grid(row=1, column=5, sticky='w', padx=(0, 5))
        self.label_combo_range_fcd.grid_remove()
        self.combo_range_fcd.grid_remove()
        self.combo_range_fcd.bind("<<ComboboxSelected>>", self.update_fcelec_var)

    def update_fcelec_var(self, event):
        # Obtener el valor seleccionado del ComboBox
        selected_range_fcd = self.combo_range_fcd.get()
        # print("selected_range_fcd   ", selected_range_fcd)
##### GUARDO DATOS FRAME 2: START 
        self.combo_range_fcd.bind("<FocusOut>", self.save_combo_range_fcd)     
##### GUARDO DATOS FRAME 2: END  
        # Actualizar la variable en función de la selección
        if selected_range_fcd == "LOW":
            self.fcelec_var.set("1.001")
        elif selected_range_fcd == "HIGH":
            self.fcelec_var.set("1.002")
##### GUARDO DATOS FRAME 2: START 
        self.save_felec_var(self.fcelec_var.get())       
##### GUARDO DATOS FRAME 2: END
        self.update_display_range()

    def update_display_range(self):
        if not hasattr(self, 'start_button'):
            self.start_button = tk.Button(self.frame3, text="Iniciar Mediciones de Corriente de fuga FCD", bg='green', fg='white', command=lambda: self.perform_measurements(0))
            self.start_button.grid(row=3, column=0, columnspan=4)

    def create_measurement_table(self, start_row):
        headers = ["Presión (kPa)", "Temperatura (°C)", "Temp. monitor (°C)", "Carga Principal (nC)", "Carga Monitor (nC)", "Int. Equipo (A)", "Int. Monitor (A)"]
        for i, header in enumerate(headers):
            label = tk.Label(self.frame3, text=header, font=('Arial', 10), bg='lightgrey', width=15)
            label.grid(row=start_row + 1, column=i, sticky='ew')  # Offset by 1 to make space for the description text
        data_labels = [[tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=15) for _ in headers] for _ in range(5)]
        for row_index, row in enumerate(data_labels):
            for col_index, label in enumerate(row):
                label.grid(row=start_row + row_index + 2, column=col_index, sticky='ew')  # Offset to start after the headers
        return data_labels

    def perform_measurements(self, tanda):
        if tanda == 0:
            start_row = 4
        else:
            start_row = 4 + tanda * (5 + 5)

        description_texts = ["Medida de fugas", "Medidas a distancia lejana (m)", "Medidas a distancia cercana (m)"]
        description_label = tk.Label(self.frame3, text=description_texts[tanda], bg='black', fg='white', font=('Helvetica', 14, 'bold'))
        description_label.grid(row=start_row, column=0, columnspan=2, sticky='wens')

        if tanda in [1, 2]:  # Only tanda 1 and 2 require distance inputs
            if tanda == 1:
                distance_label = tk.Label(self.frame3, text="Distancia lejana (m):", font=('Arial', 11), bg='#2F55B9', fg='white')
                distance_entry = tk.Entry(self.frame3, font=('Arial', 11), width=10)
                distance_label.grid(row=start_row, column=3)
                distance_entry.grid(row=start_row, column=4)
                self.wait_for_entry(distance_entry)
            elif tanda == 2:
                close_label = tk.Label(self.frame3, text="Distancia corta (m):", font=('Arial', 11), bg='#2F55B9', fg='white')
                close_entry = tk.Entry(self.frame3, font=('Arial', 11), width=10)
                close_label.grid(row=start_row, column=3)
                close_entry.grid(row=start_row, column=4)
                self.wait_for_entry(close_entry)

        labels = self.create_measurement_table(start_row)
        if len(self.data_labels) <= tanda:
            self.data_labels.append(labels)
        else:
            self.data_labels[tanda] = labels

        if hasattr(self, 'start_button'):
            self.start_button.grid_remove()

        self.simulate_data(tanda, start_row)

    def wait_for_entry(self, entry_widget):
        def on_entry_confirm(event):
            self.entry_var.set(1)  # Set the variable to resume execution
        self.entry_var = tk.IntVar()
        entry_widget.bind("<Return>", on_entry_confirm)  # Bind the Return key to confirm entry
        self.frame3.wait_variable(self.entry_var)

    def simulate_data(self, tanda, start_row):
        num_medidas = 5
        # Ajustar rangos de carga según la tanda
        carga_min_mon, carga_max_mon = 0, 0  # Valores predeterminados

        if tanda == 0:
            carga_min, carga_max = 8.0e-14, 2.0e-13
        elif tanda == 1:
            carga_min, carga_max = 1.60e-10, 1.62e-10
            carga_min_mon, carga_max_mon = 3.10e-10, 3.2e-10
        elif tanda == 2:
            carga_min, carga_max = 7.80e-10, 7.82e-10
            carga_min_mon, carga_max_mon = 3.10e-10, 3.2e-10

        data = {
            "Presión (kPa)": np.random.normal(loc=93, scale=1, size=num_medidas),
            "Temp. equipo (°C)": np.random.normal(loc=25, scale=1, size=num_medidas),
            "Temp. monitor (°C)": np.random.uniform(low=19, high=21, size=num_medidas),
            "Carga equipo (nC)": np.random.uniform(low=carga_min, high=carga_max, size=num_medidas),
            "Carga monitor (nC)": np.random.uniform(low=carga_min_mon, high=carga_max_mon, size=num_medidas)
        }
        df = pd.DataFrame(data)

        int_ppal_values = [self.calculate_int_ppal(row, tanda) for _, row in df.iterrows()]
        int_monitor_values = [self.calculate_int_monitor(row, tanda) for _, row in df.iterrows()]

        df['Int. Equipo (A)'] = int_ppal_values
        df['Int. Monitor (A)'] = int_monitor_values

        # Save average values for each tanda
        if tanda == 0:
            self.avg_int_ppal_t0 = np.mean(df['Int. Equipo (A)'])
            self.avg_int_monitor_t0 = np.mean(df['Int. Monitor (A)'])
        elif tanda == 1:
            self.avg_int_ppal_tanda_1 = np.mean(df['Int. Equipo (A)'])
            self.avg_int_monitor_tanda_1 = np.mean(df['Int. Monitor (A)'])
        elif tanda == 2:
            self.avg_int_ppal_tanda_2 = np.mean(df['Int. Equipo (A)'])
            self.avg_int_monitor_tanda_2 = np.mean(df['Int. Monitor (A)'])

        # Configurando el texto de cada celda con formato científico
        for row_index, (_, row) in enumerate(df.iterrows()):
            for col_index, value in enumerate(row):
                self.data_labels[tanda][row_index][col_index].config(text=f"{value:.5e}")

        # Calcular y mostrar promedio y desviación con formato científico
        for col_index, column_name in enumerate(df.columns):
            avg_value = np.mean(df[column_name])
            std_value = np.std(df[column_name])
            avg_label = tk.Label(self.frame3, text=f"Prom: {avg_value:.5e}", font=('Arial', 8), bg='lightyellow')
            avg_label.grid(row=start_row + num_medidas + 2, column=col_index, sticky='ew')
            std_label = tk.Label(self.frame3, text=f"Desv: {std_value:.5e}", font=('Arial', 8), bg='lightyellow')
            std_label.grid(row=start_row + num_medidas + 3, column=col_index, sticky='ew')

        decision_row = start_row + num_medidas + 4
        self.setup_next_tanda(decision_row, tanda)

    def setup_next_tanda(self, decision_row, tanda):
        options_label = tk.Label(self.frame3, text="Opciones posibles:", bg='#FFB233', font=('Arial', 10))
        options_label.grid(row=decision_row, column=0, sticky='w', padx=5)
        
        if tanda == 2:
            options = ["Reiniciar medidas", "Calculo del FCD y continuar"]
            # Ensure that required attributes are not None before calculation
            if self.avg_int_ppal_tanda_1 is not None and self.avg_int_monitor_tanda_2 is not None and \
            self.avg_int_ppal_tanda_2 is not None and self.avg_int_monitor_tanda_1 is not None:
                fcd_value = (self.avg_int_ppal_tanda_1 * self.avg_int_monitor_tanda_2) / \
                            (self.avg_int_ppal_tanda_2 * self.avg_int_monitor_tanda_1)
                self.fcd_var.set(f"{fcd_value:.4f}")
                self.save_fcd_var(self.fcd_var)
                self.frame6.grid()
            else:
                print("Required measurements are not available for FCD calculation")
                # You may want to handle this situation differently, e.g., by disabling options or alerting the user
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
            # Hide the custom table
            self.calibration_mode()

    def calculate_int_ppal(self, row, tanda):
        pressure = row["Presión (kPa)"]
        temperature = row["Temp. equipo (°C)"]
        charge_ppal = row["Carga equipo (nC)"]
        time_seconds = float(self.entry_time_fcd.get())  # Asegúrate de que esto sea convertido correctamente de la UI

        if tanda == 0:
            resultado = (charge_ppal / time_seconds) * (101.325 / 293.15) * (273.15 + temperature) / pressure
            return resultado
        else:
            resultados = ((charge_ppal / time_seconds) - self.avg_int_ppal_t0) * (101.325 / 293.15) * (273.15 + temperature) / pressure
            return resultados

    def calculate_int_monitor(self, row, tanda):
        pressure = row["Presión (kPa)"]
        temp_monitor = row["Temp. monitor (°C)"]
        charge_monitor = row["Carga monitor (nC)"]
        time_seconds = float(self.entry_time_fcd.get())

        if tanda == 0:
            return (charge_monitor / time_seconds) * (101.325 / 293.15) * (273.15 + temp_monitor) / pressure
        else:
            return ((charge_monitor / time_seconds) - self.avg_int_monitor_t0) * (101.325 / 293.15) * (273.15 + temp_monitor) / pressure
        
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
##### GUARDO DATOS SERVICIO: START  
        self.save_label_rate(unitsrate)      
        self.save_label_unit(unitsunit)        
##### GUARDO DATOS SERVICIO: END 
        pass

    def update_fields(self, event=None):
        # Mostrar los campos y el título cuando se actualicen o se llame a este método
        self.title_label_frame2.grid(row=0, column=0, columnspan=2, sticky="w")  # Mostrar el título con expansión a lo largo del eje horizontal
        # Configuración de las etiquetas y entradas usando grid
        self.label_proc.grid(row=1, column=0, sticky="w", padx=(5, 0))  
        self.combo_proc.grid(row=1, column=1, sticky="e", padx=(0, 5))  
        self.label_electrom_ref.grid(row=2, column=0, sticky="w", padx=(5, 0))  
        self.combo_electrom_ref.grid(row=2, column=1, sticky="e", padx=(0, 5))  
        # self.label_elecppal_com.grid(row=2, column=1, sticky="w", padx=(5, 0))
        # self.elecppal_com_optionmenu.grid(row=2, column=2, sticky="w", padx=(0, 5))
        self.label_elecmonit_ref.grid(row=3, column=0, sticky="w", padx=(5, 0))  
        self.combo_elecmonit_ref.grid(row=3, column=1, sticky="e", padx=(0, 5))  
        # self.label_elecmonit_com.grid(row=3, column=1, sticky="w", padx=(5, 0))
        # self.elecmonit_com_optionmenu.grid(row=3, column=2, sticky="w", padx=(0, 5))
        self.label_barom_ref.grid(row=4, column=0, sticky="w", padx=(5, 0))  
        self.combo_barom_ref.grid(row=4, column=1, sticky="e", padx=(0, 5))   
        # self.label_barom_com.grid(row=4, column=1, sticky="w", padx=(5, 0))
        # self.barom_com_optionmenu.grid(row=4, column=2, sticky="w", padx=(0, 5))
        self.label_temp_ref.grid(row=5, column=0, sticky="w", padx=(5, 0))   
        self.combo_temp_ref.grid(row=5, column=1, sticky="e", padx=(0, 5))  
        # self.label_temp_com.grid(row=5, column=1, sticky="w", padx=(5, 0))
        # self.temp_com_optionmenu.grid(row=5, column=2, sticky="w", padx=(0, 5))
        self.label_crono_ref.grid(row=6, column=0, sticky="w", padx=(5, 0)) 
        self.combo_crono_ref.grid(row=6, column=1, sticky="e", padx=(0, 5))
        self.label_colim_ref.grid(row=7, column=0, sticky="w", padx=(5, 0))   
        self.combo_colim_ref.grid(row=7, column=1, sticky="e", padx=(0, 5))  
        self.title2_label_frame2.grid(row=9, column=0, columnspan=2, sticky="w", pady=(10, 0)) 
        self.label_dist_ref.grid(row=10, column=0, sticky="w", padx=(5, 0)) 
        self.entry_dist_ref.grid(row=10, column=1, sticky="e", padx=(0, 5)) 
        self.label_fcdist_ref.grid(row=11, column=0, sticky="w", padx=(5, 0))
        self.combo_fcdist_ref.grid(row=11, column=1, sticky="e", padx=(0, 5))
        self.fcd_label.grid(row=12, column=0, sticky="w", padx=5, pady=2)
        self.fcd_value_label.grid(row=12, column=1, sticky="e", padx=5, pady=2)
        self.fcelec_label.grid(row=13, column=0, sticky="w", padx=5, pady=2)
        self.fcelec_value_label.grid(row=13, column=1, sticky="e", padx=5, pady=2)


    def fetch_correction_factor(self, event):
        try:
            file_path = 't:/SIGOR/SGC/MARXAN/Pruebas de desarrollo/IR14D/CoefConversion.json'
            # Leer el archivo JSON
            self.df = pd.read_json(file_path)
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return  # Salir del método si la carga falla

        # Limpiar los nombres de las columnas para eliminar posibles espacios extra
        self.df.columns = [col.strip() for col in self.df.columns]

        # Obtener valores de calidad y medida de los comboboxes como texto
        calidad = str(self.combo_quality.get()).strip()
        medida = str(self.combo_units.get()).strip()

        # Verificar que ambos campos están seleccionados
        if calidad and medida:
            # Filtrar el DataFrame por la calidad seleccionada
            filtered_df = self.df[self.df['Calidad'] == calidad]

            if not filtered_df.empty and medida in filtered_df.columns:
                # Extraer el factor de corrección para la calidad y medida seleccionada
                correction_factor = filtered_df.iloc[0][medida]
                # Asegurar que el valor es un número flotante y formatearlo a tres decimales
                if isinstance(correction_factor, (int, float)):
                    correction_factor_str = "{:.3f}".format(correction_factor)
                else:
                    # Intentar convertir y formatear en caso de que el valor sea una cadena
                    try:
                        correction_factor_str = "{:.3f}".format(float(correction_factor))
                    except ValueError:
                        correction_factor_str = correction_factor  # Usar valor original si la conversión falla

                self.correction_factor_var.set(correction_factor_str)  # Actualizar la variable de control con el nuevo valor
##### GUARDO DATOS SERVICIO: START 
                self.save_correction_factor(self.correction_factor_var)       
##### GUARDO DATOS SERVICIO: END  
            else:
                # Informar si no se encontraron combinaciones válidas
                print("No se encontraron datos para la combinación de calidad y medida proporcionada.")
        else:
            # Avisar si alguno de los campos no está seleccionado
            print("Debe seleccionar una calidad y una medida para buscar el factor de corrección.")

    def update_values(self, event=None):
        quality = self.combo_quality.get()
        chamber = self.combo_chamber.get()

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
##### GUARDO DATOS SERVICIO: START 
            self.save_calibration_coefficient(self.calibration_coefficient_var)   
##### GUARDO DATOS SERVICIO: END 


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
            formatted_value = f"{numeric_value:.3f}"
        except ValueError:
            # Si 'value' no puede convertirse a float, manejar como un caso especial
            formatted_value = "N/A"  # Mantener o asignar un valor por defecto que indica no disponible o no aplicable

        self.calibration_factor_var.set(formatted_value)  # Actualiza la variable de tkinter con el valor formateado
##### GUARDO DATOS SERVICIO: START 
        # self.save_calibration_factor(self.calibration_factor_var)     
##### GUARDO DATOS SERVICIO: END 

    def update_fcaa(self, event):
        calidadfcaa = self.combo_quality.get()  # Obtener la calidad seleccionada

        # Abrir y leer el archivo JSON
        with open('CoefAtenAire.json', 'r') as file:
            data_fcaa = json.load(file)

        # Inicializar fcaa_var con un valor por defecto en caso de no encontrar una coincidencia
        self.fcaa_var.set("Valor por defecto")

        # Buscar en la lista de objetos el que coincide con la calidad seleccionada
        for entry in data_fcaa:
            if entry["Calidad"] == calidadfcaa:
                self.fcaa_var.set(entry["Coef. Aten. aire"])  # Actualiza la variable de Tkinter con el valor
##### GUARDO DATOS SERVICIO: START 
                self.save_fcaa(self.fcaa_var.get())        
##### GUARDO DATOS SERVICIO: END
                pass

    def handle_quality_selected(self, event):
        self.fetch_correction_factor(event)
        self.update_values(event)
        self.update_calibration_factor(event)
        self.update_fcaa(event)
        pass

    def handle_chamber_selected(self, event):
        self.fetch_correction_factor(event)
        self.update_values(event)
        self.update_calibration_factor(event)
##### GUARDO DATOS SERVICIO: START 
        self.save_calibration_factor(event)     
##### GUARDO DATOS SERVICIO: END 
        self.update_fields(event)
        pass

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

##### START CALIBRACION EQUIPOS
    def calibration_mode(self):
        self.frame3 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid", bg='white')
        self.frame3.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

        calibration_label = tk.Label(self.frame3, text="CALIBRACIÓN DEL EQUIPO", bg='#12461E', fg='white', font=('Helvetica', 14, 'bold'))
        calibration_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        measure_label = tk.Label(self.frame3, text=f"Medida nº: {self.measure_var.get()}", bg='#12461E', fg='white', font=('Helvetica', 14, 'bold'))
        measure_label.grid(row=0, column=4, sticky='e', padx=5, pady=5)

        # Tiempo de irradiación
        self.label_time_patron = tk.Label(self.frame3, text="Tiempo (s)", font=('Arial', 8), bg='lightgray')
        self.entry_time_patron = tk.Entry(self.frame3, width=8, bg='#F8FEE4', validate="key", validatecommand=(self.register(self.validate_number), "%P"))
        self.label_time_patron.grid(row=1, column=0, sticky="w", padx=(5, 0))  # Etiqueta en la primera columna, alineada a la izquierda
        self.entry_time_patron.grid(row=1, column=1, sticky="w", padx=(0, 15))
        self.entry_time_patron.bind("<FocusOut>", self.save_entry_time_patron)
        self.entry_time_patron.bind("<Return>", self.save_entry_time_patron)

        # Intesidad de irradiación
        self.label_Irx_patron = tk.Label(self.frame3, text="Intensidad (A)", font=('Arial', 8), bg='lightgray')
        self.entry_Irx_patron = tk.Entry(self.frame3, width=8, bg='#F8FEE4', validate="key", validatecommand=(self.register(self.validate_number), "%P"))
        self.label_Irx_patron.grid(row=1, column=2, sticky="w", padx=(5, 0))  # Etiqueta en la primera columna, alineada a la izquierda
        self.entry_Irx_patron.grid(row=1, column=3, sticky="w", padx=(0, 15))
        self.entry_Irx_patron.bind("<FocusOut>", self.save_entry_Irx_patron)
        self.entry_Irx_patron.bind("<Return>", self.save_entry_Irx_patron)

        # Ocultar inicialmente los campos de intensidad
        self.label_Irx_patron.grid_remove()
        self.entry_Irx_patron.grid_remove()

        # Rango del electrómetro
        self.label_combo_range = tk.Label(self.frame3, text="Rango de Electrómetros", font=('Arial', 8), bg='lightgray')
        self.label_combo_range.grid(row=1, column=4, sticky='w', padx=5)
        electrometer_range = ["LOW", "HIGH"]
        self.combo_range = ttk.Combobox(self.frame3, values=electrometer_range, width=15, font=('Arial', 8))
        self.combo_range.grid(row=1, column=5, sticky='w', padx=(0, 5))
        self.combo_range.bind("<<ComboboxSelected>>", self.on_select_patron)

        # Ocultar inicialmente los campos de rango del electrómetro
        self.label_combo_range.grid_remove()
        self.combo_range.grid_remove()
       
    def on_select_patron(self, event):
        # Evento que se dispara cuando se selecciona una opción en el Combobox
        selected_range = self.combo_range.get()
        # Actualizar la variable en función de la selección
        self.combo_range.bind("<FocusOut>", self.save_combo_range_patron)        
        if selected_range == "LOW":
            self.fcelec_var.set("1.001")           
        elif selected_range == "HIGH":
            self.fcelec_var.set("1.002")

        self.save_felec_var(self.fcelec_var.get())       

        self.update_display_range_patron()

    def update_display_range_patron(self):
        self.start_button = tk.Button(self.frame3, text="Iniciar Mediciones de Corriente de fuga", bg='green', fg='#71FF33', command=lambda: self.perform_measurements_patron(0))
        self.start_button.grid(row=3, column=0, columnspan=4)

    def perform_measurements_patron(self, tanda):
        self.set_calibration_values()  # Asegúrate de que los valores estén configurados correctamente
        start_row = 4 if tanda == 0 else 4 + tanda * (5 + 5)

        description_texts = ["Medida de fugas", "Medidas del equipo patrón", "Medidas del equipo del cliente"]
        description_label = tk.Label(self.frame3, text=description_texts[tanda],
                                     bg='black', fg='white', font=('Helvetica', 14, 'bold'))
        description_label.grid(row=start_row, column=0, columnspan=8, sticky='wens')

        # Asegurarse de que self.data_labels tenga suficiente espacio
        while len(self.data_labels) <= tanda:
            self.data_labels.append([[] for _ in range(7)])

        if tanda == 2:
            self.create_measurement_table_tanda_two(start_row, tanda)
        else:
            labels = self.create_measurement_table_patron(start_row, tanda)
            self.data_labels[tanda] = labels
            if hasattr(self, 'start_button'):
                self.start_button.grid_remove()
            if tanda != 2:
                self.simulate_data_patron(tanda, start_row)

    def set_calibration_values(self):
        try:
            self.calibration_coefficient = float(self.calibration_coefficient_var.get())
            self.correction_factor = float(self.correction_factor_var.get())
            self.fcd_value = float(self.fcd_var.get())
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Invalid calibration variables: {e}")

    def create_measurement_table_tanda_two(self, start_row, tanda):
        headers = ["Tasa de fondo (Sv/h)", "Presión (kPa)", "Temperatura (C)", "Lectura equipo (Sv/h)", 
                "Lectura corregida dosis (Sv/h)", "Tasa dosis integrada (Sv)", "Lectura corregida tasa"]
        
        # Inicializar self.data_labels[tanda] con listas vacías para cada columna
        self.data_labels[tanda] = [[] for _ in range(len(headers))]

        # Añadir solo la columna "Tasa de fondo (Sv/h)" en la primera etapa
        for col_index in range(1):
            label = tk.Label(self.frame3, text=headers[col_index], font=('Arial', 10), bg='lightgrey', width=20)
            label.grid(row=start_row + 1, column=col_index, sticky='ew')
        
        # Crear entradas para "Tasa de fondo (Sv/h)"
        for row_index in range(5):
            entry = tk.Entry(self.frame3, font=('Arial', 8), bg='white', width=20)
            entry.grid(row=start_row + row_index + 2, column=0, sticky='ew')
            entry.bind("<Return>", lambda e, r=row_index: self.on_background_rate_entry(e, start_row, r, tanda))
            self.data_labels[tanda][0].append(entry)

    def on_background_rate_entry(self, event, start_row, row_index, tanda):
        entry_widget = event.widget
        entry_widget.config(state='readonly')

        # Check if all 5 measurements are entered
        if all(self.data_labels[tanda][0][i].get() != "" for i in range(5)):
            self.calculate_background_rate(start_row, tanda)

    def calculate_background_rate(self, start_row, tanda):
        background_rates = [float(self.data_labels[tanda][0][i].get()) for i in range(5)]
        avg_background_rate = np.mean(background_rates)
        std_background_rate = np.std(background_rates)

        avg_label = tk.Label(self.frame3, text=f"Prom: {avg_background_rate:.5e}", font=('Arial', 8), bg='lightyellow')
        avg_label.grid(row=start_row + 7, column=0, sticky='ew')
        std_label = tk.Label(self.frame3, text=f"Desv: {std_background_rate:.5e}", font=('Arial', 8), bg='lightyellow')
        std_label.grid(row=start_row + 8, column=0, sticky='ew')

        self.background_rate = avg_background_rate
        self.setup_next_columns(start_row, tanda, 1)

    def setup_next_columns(self, start_row, tanda, stage):
        if stage == 1:
            # Añadir las columnas "Presión (kPa)", "Temperatura (C)", "Lectura equipo (Sv/h)", "Lectura corregida dosis (Sv/h)"
            headers = ["Presión (kPa)", "Temperatura (C)", "Lectura equipo (Sv/h)", "Lectura corregida dosis (Sv/h)"]
            start_col = 1  # Empezar desde la siguiente columna después de "Tasa de fondo (Sv/h)"

            for i, header in enumerate(headers):
                label = tk.Label(self.frame3, text=header, font=('Arial', 10), bg='lightgrey', width=20)
                label.grid(row=start_row + 1, column=start_col + i, sticky='ew')

            for row_index in range(5):
                pressure_label = tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=20)
                temperature_label = tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=20)
                reading_entry = tk.Entry(self.frame3, font=('Arial', 8), bg='white', width=20)
                corrected_dose_label = tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=20)

                pressure_label.grid(row=start_row + row_index + 2, column=1, sticky='ew')
                temperature_label.grid(row=start_row + row_index + 2, column=2, sticky='ew')
                reading_entry.grid(row=start_row + row_index + 2, column=3, sticky='ew')
                corrected_dose_label.grid(row=start_row + row_index + 2, column=4, sticky='ew')

                reading_entry.bind("<Return>", lambda e, r=row_index: self.on_equipment_reading_entry(e, start_row, r, tanda))

                self.data_labels[tanda][1].append(pressure_label)
                self.data_labels[tanda][2].append(temperature_label)
                self.data_labels[tanda][3].append(reading_entry)
                self.data_labels[tanda][4].append(corrected_dose_label)

            self.tanda_stage = 1  # Mover a la siguiente etapa
        elif stage == 2:
            # Añadir las columnas "Tasa dosis integrada (Sv)", "Lectura corregida tasa"
            headers = ["Tasa dosis integrada (Sv)", "Lectura corregida tasa"]
            start_col = 5  # Empezar desde la siguiente columna después de las existentes

            for i, header in enumerate(headers):
                label = tk.Label(self.frame3, text=header, font=('Arial', 10), bg='lightgrey', width=20)
                label.grid(row=start_row + 1, column=start_col + i, sticky='ew')

            for row_index in range(5):
                integrated_dose_entry = tk.Entry(self.frame3, font=('Arial', 8), bg='white', width=20)
                corrected_rate_label = tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=20)

                integrated_dose_entry.grid(row=start_row + row_index + 2, column=5, sticky='ew')
                corrected_rate_label.grid(row=start_row + row_index + 2, column=6, sticky='ew')

                integrated_dose_entry.bind("<Return>", lambda e, r=row_index: self.on_integrated_dose_entry(e, start_row, r, tanda))

                self.data_labels[tanda][5].append(integrated_dose_entry)
                self.data_labels[tanda][6].append(corrected_rate_label)

            self.tanda_stage = 2  # Mover a la etapa final

    def on_equipment_reading_entry(self, event, start_row, row_index, tanda):
        entry_widget = event.widget
        entry_widget.config(state='readonly')

        # Simulate pressure and temperature, calculate corrected dose
        pressure = np.random.normal(loc=1013, scale=5)
        temperature = np.random.normal(loc=25, scale=1)
        equipment_reading = float(entry_widget.get())
        corrected_dose = (equipment_reading - self.background_rate) * (101.325 / 293.15) * (273.15 + temperature) / pressure

        self.data_labels[tanda][1][row_index].config(text=f"{pressure:.5e}")
        self.data_labels[tanda][2][row_index].config(text=f"{temperature:.5e}")
        self.data_labels[tanda][4][row_index].config(text=f"{corrected_dose:.5e}")

        # Check if all 5 measurements are entered
        if all(self.data_labels[tanda][3][i].get() != "" for i in range(5)):
            self.calculate_corrected_doses(start_row, tanda)

    def calculate_corrected_doses(self, start_row, tanda):
        pressures = [float(self.data_labels[tanda][1][i].cget("text")) for i in range(5)]
        temperatures = [float(self.data_labels[tanda][2][i].cget("text")) for i in range(5)]
        readings = [float(self.data_labels[tanda][3][i].get()) for i in range(5)]
        corrected_doses = [float(self.data_labels[tanda][4][i].cget("text")) for i in range(5)]

        avg_pressure = np.mean(pressures)
        std_pressure = np.std(pressures)
        avg_temperature = np.mean(temperatures)
        std_temperature = np.std(temperatures)
        avg_reading = np.mean(readings)
        std_reading = np.std(readings)
        avg_corrected_dose = np.mean(corrected_doses)
        std_corrected_dose = np.std(corrected_doses)

        # Mostrar promedio y desviación de Presión
        avg_label_pressure = tk.Label(self.frame3, text=f"Prom: {avg_pressure:.5e}", font=('Arial', 8), bg='lightyellow')
        avg_label_pressure.grid(row=start_row + 7, column=1, sticky='ew')
        std_label_pressure = tk.Label(self.frame3, text=f"Desv: {std_pressure:.5e}", font=('Arial', 8), bg='lightyellow')
        std_label_pressure.grid(row=start_row + 8, column=1, sticky='ew')

        # Mostrar promedio y desviación de Temperatura
        avg_label_temperature = tk.Label(self.frame3, text=f"Prom: {avg_temperature:.5e}", font=('Arial', 8), bg='lightyellow')
        avg_label_temperature.grid(row=start_row + 7, column=2, sticky='ew')
        std_label_temperature = tk.Label(self.frame3, text=f"Desv: {std_temperature:.5e}", font=('Arial', 8), bg='lightyellow')
        std_label_temperature.grid(row=start_row + 8, column=2, sticky='ew')

        # Mostrar promedio y desviación de Lectura equipo (Sv/h)
        avg_label_reading = tk.Label(self.frame3, text=f"Prom: {avg_reading:.5e}", font=('Arial', 8), bg='lightyellow')
        avg_label_reading.grid(row=start_row + 7, column=3, sticky='ew')
        std_label_reading = tk.Label(self.frame3, text=f"Desv: {std_reading:.5e}", font=('Arial', 8), bg='lightyellow')
        std_label_reading.grid(row=start_row + 8, column=3, sticky='ew')

        # Mostrar promedio y desviación de Lectura corregida dosis (Sv/h)
        avg_label_corrected_dose = tk.Label(self.frame3, text=f"Prom: {avg_corrected_dose:.5e}", font=('Arial', 8), bg='lightyellow')
        avg_label_corrected_dose.grid(row=start_row + 7, column=4, sticky='ew')
        std_label_corrected_dose = tk.Label(self.frame3, text=f"Desv: {std_corrected_dose:.5e}", font=('Arial', 8), bg='lightyellow')
        std_label_corrected_dose.grid(row=start_row + 8, column=4, sticky='ew')

        self.avg_pressure = avg_pressure
        self.avg_temperature = avg_temperature
        self.setup_next_columns(start_row, tanda, 2)


    def setup_final_columns(self, start_row, tanda):
        # Remove previous entries
        for row in self.data_labels[tanda]:
            for widget in row:
                widget.grid_remove()

        # Set up final columns
        headers = ["Tasa dosis integrada (Sv)", "Lectura corregida tasa"]
        for i, header in enumerate(headers):
            label = tk.Label(self.frame3, text=header, font=('Arial', 10), bg='lightgrey', width=20)
            label.grid(row=start_row + 1, column=i, sticky='ew')
        
        self.data_labels[tanda] = [[tk.Entry(self.frame3, font=('Arial', 8), bg='white', width=20) if i == 0 else tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=20)
                                    for i in range(len(headers))] for _ in range(5)]
        
        for row_index, row in enumerate(self.data_labels[tanda]):
            for col_index, widget in enumerate(row):
                widget.grid(row=start_row + row_index + 2, column=col_index, sticky='ew')
                if isinstance(widget, tk.Entry):
                    widget.bind("<Return>", lambda e, r=row_index: self.on_integrated_dose_entry(e, start_row, r, tanda))
        
        self.tanda_stage = 2  # Move to final stage

    def on_integrated_dose_entry(self, event, start_row, row_index, tanda):
        entry_widget = event.widget
        entry_widget.config(state='readonly')

        integrated_dose = float(entry_widget.get())
        corrected_rate = (integrated_dose * 101.325 / self.avg_pressure * (273.15 + self.avg_temperature) / 293.15 -
                        self.background_rate) / 3600 * float(self.entry_time_patron.get()) * 5

        self.data_labels[tanda][6][row_index].config(text=f"{corrected_rate:.5e}")

        # Check if all 5 measurements are entered
        if all(self.data_labels[tanda][6][i].cget("text") != "" for i in range(5)):
            self.calculate_final_results(start_row, tanda)

    def calculate_final_results(self, start_row, tanda):
        integrated_doses = [float(self.data_labels[tanda][5][i].get()) for i in range(5)]
        corrected_rates = [float(self.data_labels[tanda][6][i].cget("text")) for i in range(5)]

        avg_integrated_dose = np.mean(integrated_doses)
        std_integrated_dose = np.std(integrated_doses)
        avg_corrected_rate = np.mean(corrected_rates)
        std_corrected_rate = np.std(corrected_rates)

        avg_label_integrated_dose = tk.Label(self.frame3, text=f"Prom: {avg_integrated_dose:.5e}", font=('Arial', 8), bg='lightyellow')
        avg_label_integrated_dose.grid(row=start_row + 7, column=5, sticky='ew')
        std_label_integrated_dose = tk.Label(self.frame3, text=f"Desv: {std_integrated_dose:.5e}", font=('Arial', 8), bg='lightyellow')
        std_label_integrated_dose.grid(row=start_row + 8, column=5, sticky='ew')

        avg_label_corrected_rate = tk.Label(self.frame3, text=f"Prom: {avg_corrected_rate:.5e}", font=('Arial', 8), bg='lightyellow')
        avg_label_corrected_rate.grid(row=start_row + 7, column=6, sticky='ew')
        std_label_corrected_rate = tk.Label(self.frame3, text=f"Desv: {std_corrected_rate:.5e}", font=('Arial', 8), bg='lightyellow')
        std_label_corrected_rate.grid(row=start_row + 8, column=6, sticky='ew')

        # Finalize and move to next step if needed
        self.setup_next_tanda_patron(start_row + 9, tanda)

    def create_measurement_table_patron(self, start_row, tanda):
        headers = ["Presión (kPa)", "Temperatura (°C)", "Temp. monitor (°C)", "Carga Principal (nC)", "Carga Monitor (nC)", "Int. Equipo (A)", "Int. Monitor (A)"]
        if tanda in [1, 2]:  # Añadir columna "Kair" solo para tanda 2 y 3
            headers.append("Kair")

        for i, header in enumerate(headers):
            label = tk.Label(self.frame3, text=header, font=('Arial', 10), bg='lightgrey', width=15)
            label.grid(row=start_row + 1, column=i, sticky='ew')

        data_labels = [[tk.Entry(self.frame3, font=('Arial', 8), bg='white', width=15) if tanda == 2 and i == 3 else tk.Label(self.frame3, text="", font=('Arial', 8), bg='white', width=15)
                        for i in range(len(headers))] for _ in range(5)]

        for row_index, row in enumerate(data_labels):
            for col_index, entry_or_label in enumerate(row):
                entry_or_label.grid(row=start_row + row_index + 2, column=col_index, sticky='ew')
                if isinstance(entry_or_label, tk.Entry):
                    entry_or_label.bind("<Return>", lambda e, r=row_index: self.on_manual_charge_entry(e, start_row, r, tanda))

        return data_labels 
    
    def simulate_manual_data(self, charge_value, tanda):
        pressure = np.random.normal(loc=1013, scale=5)  # Simular presión
        temperature = np.random.normal(loc=25, scale=1)  # Simular temperatura del equipo
        temp_monitor = np.random.uniform(low=19, high=21)  # Simular temperatura del monitor
        charge_monitor = np.random.normal(loc=10, scale=2)  # Simular carga de monitor

        # Usar tanda en los cálculos
        int_equipo = self.calculate_int_ppal_patron({
            "Presión (kPa)": pressure,
            "Temp. equipo (°C)": temperature,
            "Carga equipo (nC)": charge_value
        }, tanda)

        int_monitor = self.calculate_int_monitor_patron({
            "Presión (kPa)": pressure,
            "Temp. monitor (°C)": temp_monitor,
            "Carga monitor (nC)": charge_monitor
        }, tanda)

        return {
            "Presión (kPa)": pressure,
            "Temperatura (°C)": temperature,
            "Temp. monitor (°C)": temp_monitor,
            "Carga monitor (nC)": charge_monitor,
            "Carga equipo (nC)": charge_value,
            "Int. Equipo (A)": int_equipo,
            "Int. Monitor (A)": int_monitor
        }

    def update_data_labels_tanda_two(self, simulated_data, start_row, row_index, tanda):
        row_labels = self.data_labels[tanda][row_index]
        # Formatear y actualizar cada campo relevante
        row_labels[0].config(text=f"{float(simulated_data['Presión (kPa)']):.5e}")
        row_labels[1].config(text=f"{float(simulated_data['Temperatura (°C)']):.5e}")
        row_labels[2].config(text=f"{float(simulated_data['Temp. monitor (°C)']):.5e}")
        row_labels[3].config(text=f"{float(simulated_data['Carga equipo (nC)']):.5e}")  # Carga principal
        row_labels[4].config(text=f"{float(simulated_data['Carga monitor (nC)']):.5e}")
        row_labels[5].config(text=f"{float(simulated_data['Int. Equipo (A)']):.5e}")  # Intensidad del equipo
        row_labels[6].config(text=f"{float(simulated_data['Int. Monitor (A)']):.5e}")  # Intensidad del monitor

        if tanda in [1, 2]:  # Solo actualizar la columna "Kair" para tandas 2 y 3
            kair_value = simulated_data['Int. Equipo (A)'] * float(self.calibration_coefficient_var.get()) * float(self.correction_factor_var.get()) * float(self.fcd_var.get())
            row_labels[7].config(text=f"{kair_value:.5e}")  # Actualizar el valor de Kair


    def simulate_data_patron(self, tanda, start_row):
        num_medidas = 5
        data = {
            "Presión (kPa)": [],
            "Temp. equipo (°C)": [],
            "Temp. monitor (°C)": [],
            "Carga equipo (nC)": [],
            "Carga monitor (nC)": []
        }

        # Generación de datos de prueba con las especificaciones indicadas
        for _ in range(num_medidas):
            data["Presión (kPa)"].append(np.random.normal(loc=93, scale=1))
            data["Temp. equipo (°C)"].append(np.random.normal(loc=20, scale=1))
            data["Temp. monitor (°C)"].append(np.random.normal(loc=20, scale=1))

            if tanda == 0:
                carga_min, carga_max = 8.0e-14, 2.0e-13
            elif tanda == 1:
                carga_min, carga_max = 3.50e-12, 4.50e-12
            elif tanda == 2:
                carga_min, carga_max = 3.50e-12, 4.50e-12
            
            data["Carga equipo (nC)"].append(np.random.uniform(low=carga_min, high=carga_max))
            data["Carga monitor (nC)"].append(np.random.uniform(low=carga_min, high=carga_max))

        # Verificación de consistencia de longitud
        length_check = len(set(len(lst) for lst in data.values())) == 1
        if not length_check:
            raise ValueError("Inconsistent data lengths in 'data' dictionary")

        if tanda == 2:
            data["Carga equipo (nC)"] = [float(self.data_labels[tanda][row_index][3].cget("text")) for row_index in range(num_medidas)]
        df = pd.DataFrame(data)
        df['Int. Equipo (A)'] = [self.calculate_int_ppal_patron(row, tanda) for _, row in df.iterrows()]
        df['Int. Monitor (A)'] = [self.calculate_int_monitor_patron(row, tanda) for _, row in df.iterrows()]

        try:
            calibration_coefficient = float(self.calibration_coefficient_var.get())
            correction_factor = float(self.correction_factor_var.get())
            fcd_value = float(self.fcd_var.get())
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Invalid calibration variables: {e}")
            return

        if tanda in [1, 2]:
            df['Kair'] = df['Int. Equipo (A)'] * calibration_coefficient * correction_factor * fcd_value

        for row_index, (_, row) in enumerate(df.iterrows()):
            for col_index, value in enumerate(row):
                if col_index < 5:
                    self.data_labels[tanda][row_index][col_index].config(text=f"{value:.5e}")
                else:
                    self.data_labels[tanda][row_index][col_index].config(text=f"{value:.5e}")

        for col_index, column_name in enumerate(df.columns):
            avg_value = np.mean(df[column_name])
            std_value = np.std(df[column_name])
            # Aplicar formato .5e a promedios y desviaciones
            avg_label = tk.Label(self.frame3, text=f"Prom: {avg_value:.5e}", font=('Arial', 8), bg='lightyellow')
            avg_label.grid(row=start_row + num_medidas + 2, column=col_index, sticky='ew')
            std_label = tk.Label(self.frame3, text=f"Desv: {std_value:.5e}", font=('Arial', 8), bg='lightyellow')
            std_label.grid(row=start_row + num_medidas + 3, column=col_index, sticky='ew')

        if tanda == 0:
            self.avg_int_ppal_patron_t0 = np.mean(df['Int. Equipo (A)'])
            self.avg_int_monitor_t0 = np.mean(df['Int. Monitor (A)'])

        decision_row = start_row + num_medidas + 4
        self.setup_next_tanda_patron(decision_row, tanda)

    def calculate_int_ppal_patron(self, row, tanda):
        pressure = row["Presión (kPa)"]
        temperature = row["Temp. equipo (°C)"]
        charge_ppal = row["Carga equipo (nC)"]
        time_seconds = float(self.entry_time_patron.get())  # Asegúrate de que esto sea convertido correctamente de la UI

        if tanda == 0:
            return (charge_ppal / time_seconds) * (101.325 / 293.15) * (273.15 + temperature) / pressure
        else:
            return ((charge_ppal / time_seconds) - self.avg_int_ppal_patron_t0) * (101.325 / 293.15) * (273.15 + temperature) / pressure

    def calculate_int_monitor_patron(self, row, tanda):
        pressure = row["Presión (kPa)"]
        temp_monitor = row["Temp. monitor (°C)"]
        charge_monitor = row["Carga monitor (nC)"]
        time_seconds = float(self.entry_time_patron.get())

        if tanda == 0:
            return (charge_monitor / time_seconds) * (101.325 / 293.15) * (273.15 + temp_monitor) / pressure
        else:
            return ((charge_monitor / time_seconds) - self.avg_int_monitor_t0) * (101.325 / 293.15) * (273.15 + temp_monitor) / pressure

    def setup_next_tanda_patron(self, decision_row, tanda):
        options_label = tk.Label(self.frame3, text="Opciones posibles:", bg='#FFB233', font=('Arial', 10))
        options_label.grid(row=decision_row, column=0, sticky='w', padx=5)

        if tanda == 2:
            options = ["Reiniciar medidas", "Siguiente medida", "Fin de las medidas"]
            if self.avg_int_equipo_tanda_1 is not None and self.avg_int_monitor_tanda_2 is not None and \
            self.avg_int_equipo_tanda_2 is not None and self.avg_int_monitor_tanda_1 is not None:
                fcd_value = (self.avg_int_equipo_tanda_1 * self.avg_int_monitor_tanda_2) / \
                            (self.avg_int_equipo_tanda_2 * self.avg_int_monitor_tanda_1)
                self.fcd_var.set(f"{fcd_value:.4f}")
                self.save_fcd_var(self.fcd_var)
                self.frame6.grid()
            else:
                print("No se han hecho medidas para cálculo del FCD. Entonces FCD = 1")
        else:
            options = ["Reiniciar medidas", "Continuar con las medidas"]

        decision_combo = ttk.Combobox(self.frame3, values=options, width=30)
        decision_combo.grid(row=decision_row, column=1, columnspan=2, sticky='w')
        decision_combo.bind("<<ComboboxSelected>>", lambda e: self.on_decision_made_patron(e, tanda))

    def on_manual_charge_entry(self, event, start_row, row_index, tanda):
        entry_widget = event.widget
        charge_value = float(entry_widget.get())
        entry_widget.config(state='readonly')

        # Pasar también tanda como argumento
        simulated_data = self.simulate_manual_data(charge_value, tanda)
        self.update_data_labels_tanda_two(simulated_data, start_row, row_index, tanda)

        # Formateo opcional y acciones adicionales si son necesarias
        formatted_charge_value = format(charge_value, '.5e')
        if tanda == 2 and row_index == 4:
            self.simulate_data_patron(tanda, start_row)
        elif row_index < 4:
            next_entry = self.data_labels[tanda][row_index + 1][3]
            next_entry.focus_set()

    def on_decision_made_patron(self, event, tanda):
        choice = event.widget.get()
        if choice == "Reiniciar medidas":
            for label_row in self.data_labels[tanda]:
                for label in label_row:
                    label.config(text="")
            self.perform_measurements_patron(tanda)
        elif choice == "Continuar con las medidas" and self.measure_var.get() == 1 and tanda == 1:
            self.show_webcam_window()
            self.perform_measurements_patron(tanda + 1)
        elif choice == "Continuar con las medidas":
            self.perform_measurements_patron(tanda + 1)
        elif choice == "Fin de las medidas" and tanda == 2:
            pass
        elif choice == "Siguiente medida" and tanda == 2:
            # Recopilar datos y guardarlos en el diccionario
            measure_num = self.measure_var.get()
            if measure_num not in self.datamed:
                self.datamed[measure_num] = []

            for tanda_num in range(3):  # Suponiendo que hay 3 tandas
                tanda_data = []
                for row in self.data_labels[tanda_num]:
                    row_data = [label.cget("text") if isinstance(label, tk.Label) else label.get() for label in row]
                    tanda_data.append(row_data)
                self.datamed[measure_num].append(tanda_data)

            # Guardar datos iniciales en self.datamed
            initial_data = {
                "Tiempo": self.entry_time_patron.get(),
                "Intensidad": self.entry_Irx_patron.get(),
                "Rango": self.combo_range.get()
            }
            self.datamed[measure_num].append(initial_data)

            # Calcular los valores promedio de Kair, Int. Equipo y monitor de las tablas 1, 2 y 3
            avg_kair_tanda2 = np.mean([float(self.data_labels[1][i][7].cget("text")) for i in range(5)])

            avg_int_equipo_tanda1 = np.mean([float(self.data_labels[0][i][5].cget("text")) for i in range(5)])
            avg_int_monitor_tanda1 = np.mean([float(self.data_labels[0][i][6].cget("text")) for i in range(5)])
            avg_int_equipo_tanda2 = np.mean([float(self.data_labels[1][i][5].cget("text")) for i in range(5)])
            avg_int_monitor_tanda2 = np.mean([float(self.data_labels[1][i][6].cget("text")) for i in range(5)])


            print(f"Valor promedio de Kair de las tablas 2: {avg_kair_tanda2:.5e}")
            print(f"Valor de self.fcaa_var: {self.fcaa_var.get()}")
            print(f"Valor de self.correction_factor_var: {self.correction_factor_var.get()}")
            print(f"Valor de self.fcd_var: {self.fcd_var.get()}")

            print(f"Valor promedio de Int. Equipo tabla 1: {avg_int_equipo_tanda1:.5e}")
            print(f"Valor promedio de Int. Monitor tabla 1: {avg_int_monitor_tanda1:.5e}")
            print(f"Valor promedio de Int. Equipo tabla 2: {avg_int_equipo_tanda2:.5e}")
            print(f"Valor promedio de Int. Monitor tabla 2: {avg_int_monitor_tanda2:.5e}")
            self.calculo_tabla_final(avg_kair_tanda2, avg_int_equipo_tanda2)

            # Reiniciar para la siguiente medida
            for widget in self.frame3.winfo_children():
                widget.destroy()
            self.measure_var.set(self.measure_var.get() + 1)
            if self.measure_var.get() > 4:
                self.measure_var.set(1)
            self.calibration_mode()
        elif choice == "Siguiente medida":
            self.frame6.grid()

        print(self.datamed)

    def calculo_tabla_final(self, avg_kair_tanda2, avg_int_equipo_tanda2):
        try:
            kerma_aire = float(avg_kair_tanda2)
            fcaa_var_value = float(self.fcaa_var.get())
            correction_factor = float(self.correction_factor_var.get())
            fcd_value = float(self.fcd_var.get())

            patron_sv_h = kerma_aire * fcaa_var_value * correction_factor * fcd_value
            patron_sv = patron_sv_h * 5 * float(self.entry_time_patron.get())
            equipo_sv_h = avg_int_equipo_tanda2
            incert_tasa = "2.1%"
            integrada_sv = "some value"
            factor_cal_tasa = "some_value"
            incert_tasa_k2 = "some_value"
            factor_cal_integrada = "some_value"
            incert_integrada_k2 = "some_value"
            incert_kerma_aire_k2 = "some_value"
            incert_magnitud_medida_k2 = "some_value"

            treeview_values = [
                "Sv", kerma_aire, patron_sv, equipo_sv_h, incert_tasa,
                integrada_sv, factor_cal_tasa, incert_tasa_k2, factor_cal_integrada,
                incert_integrada_k2, incert_kerma_aire_k2, incert_magnitud_medida_k2
            ]

            self.tree.insert("", "end", values=treeview_values)
            self.frame6.grid()
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Invalid numeric value: {e}")


    def show_webcam_window(self):
        # Create a new top-level window
        self.webcam_window = Toplevel(self.master)
        self.webcam_window.geometry('400x400')
        self.webcam_window.title('Captura de Imagen')

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # Create a label in the window to hold the webcam video
        self.webcam_label = tk.Label(self.webcam_window)
        self.webcam_label.pack()

        # Button to capture the image
        capture_button = tk.Button(self.webcam_window, text="Capturar Imagen", command=self.capture_image)
        capture_button.pack()

        # Start the video process
        self.update_video()

    def update_video(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()
        if ret:
            # Convert the image from BGR color (which OpenCV uses) to RGB color
            cv_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(cv_rgb)
            imgtk = ImageTk.PhotoImage(image=im)
            self.webcam_label.imgtk = imgtk
            self.webcam_label.configure(image=imgtk)
        # Repeat after an interval to get the video frame
        self.webcam_label.after(10, self.update_video)

    def capture_image(self):
        # Get the current frame from the webcam
        ret, frame = self.cap.read()
        referen = self.dataxls.get('Referencia del Servicio Técnico', ['Valor no encontrado'])[0]
        print(f'Referencia: {referen}')
        if ret:
            # Generate a unique filename using self.entry_ref_servicio and the current date and time
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{referen}_{timestamp}.jpg"
            
            # Save the frame as an image file
            cv2.imwrite(filename, frame)
            
            # Print the message with the full path of the saved image
            full_path = os.path.abspath(filename)
            print(f"Imagen capturada y guardada en: {full_path}")


##### FIN CALCULO DEL FACTOR DE CORRECCION POR DISTANCIA


def main():
    app = ir14dGUI()
    app.mainloop()

# Si este archivo se ejecuta como programa principal, se iniciará la GUI.
if __name__ == "__main__":
    main()
    
