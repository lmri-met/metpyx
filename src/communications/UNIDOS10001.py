import serial
import time
from openpyxl import Workbook

def enviar_comando(ser, comando):
    ser.write((comando + '\r\n').encode('utf-8'))
    time.sleep(0.5)  # Espera para la respuesta del dispositivo
    respuesta = ''
    while ser.in_waiting > 0:
        respuesta += ser.read(ser.in_waiting).decode('utf-8', errors='replace')
    time.sleep(0.1)  # Pausa adicional si es necesario
    # Reemplaza puntos por comas en la respuesta
    respuesta_formateada = respuesta.replace('.', ',')
    return respuesta_formateada.strip()

# Crear un nuevo libro de Excel y seleccionar la hoja activa
wb = Workbook()
ws = wb.active

puerto = 'COM5'
baudios = 9600

with serial.Serial(puerto, baudios, timeout=2) as ser:
    print("Conexión establecida con el dispositivo.")
    
    comandos = ['PTW', 'SER', '?S', '?R', 'R0', 'M2', '?C', '?F', '?U', '?W', 'G', 'H', 'V']
    for comando in comandos:
        respuesta = enviar_comando(ser, comando)
        if comando == 'V':
            partes = respuesta.split()
            if len(partes) < 3:  # Asegurar que hay al menos 3 partes
                partes += [''] * (3 - len(partes))  # Rellenar con cadenas vacías si es necesario
            # Asegura que los puntos decimales se reemplacen por comas para el comando 'V'
            partes = [parte.replace('.', ',') for parte in partes]
            ws.append(['V'] + partes)
        else:
            ws.append([comando, respuesta])
        if comando == 'G':  # Si el comando es 'G', espera 20 segundos antes del siguiente comando
            time.sleep(20)
        print(f"Respuesta a '{comando}': {respuesta}")

# Guardar el libro de Excel
wb.save("resultados.xlsx")
