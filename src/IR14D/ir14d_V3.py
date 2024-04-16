import sys
import numpy as np
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QApplication)
from PyQt5.QtGui import QImage, QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from datetime import datetime, timedelta

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CALIBRACIÓN - ASIGNACIÓN DE DOSIS. IR-14D")
        self.initUI()
        self.cap = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def initUI(self):
        layout = QVBoxLayout()

        # Marco de título
        self.titulo_label = QLabel("CALIBRACIÓN - ASIGNACIÓN DE DOSIS. IR-14D", self)
        self.titulo_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titulo_label)

        # Layout de entrada de datos
        datos_layout = QHBoxLayout()
        layout.addLayout(datos_layout)

        # Panel de entrada de datos
        self.entrada_datos_panel = self.crearPanelEntradaDatos()
        datos_layout.addWidget(self.entrada_datos_panel)

        # Panel de la cámara
        self.imagen_label = QLabel(self)
        self.actualizar_imagen(cv2.imread("placeholder.png"))  # Imagen de placeholder
        datos_layout.addWidget(self.imagen_label)

        # Panel de gráficos
        self.grafico_panel = self.crearPanelGrafico()
        datos_layout.addWidget(self.grafico_panel)

        self.setLayout(layout)

    def crearPanelEntradaDatos(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Agregar widgets aquí
        layout.addWidget(QLabel("DATOS DE ENTRADA"))

        # Ejemplo de entrada de datos
        self.nombre_edit = QLineEdit()
        layout.addWidget(self.nombre_edit)

        return panel

    def crearPanelGrafico(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)
        self.ax1 = self.figure.add_subplot(111)
        self.ax2 = self.ax1.twinx()

        self.actualizar_grafica()

        return panel

    def actualizar_grafica(self):
        # Lógica para actualizar la gráfica
        self.ax1.clear()
        self.ax2.clear()

        # Genera algunos datos de ejemplo
        data_x = [datetime.now() + timedelta(seconds=i) for i in range(10)]
        data_y1 = np.random.randint(0, 100, size=10)
        data_y2 = np.random.randint(0, 100, size=10)

        self.ax1.plot(data_x, data_y1, 'r-')
        self.ax2.plot(data_x, data_y2, 'b-')

        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.figure.autofmt_xdate()

        self.canvas.draw()

    def actualizar_imagen(self, frame):
        if frame is None:
            # Manejar el caso de que frame sea None, por ejemplo, mostrando una imagen de error o un mensaje
            print("Error: No se pudo cargar la imagen.")
            return
        
        # Convertir imagen de CV2 a QPixmap para mostrarla en QLabel
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
        self.imagen_label.setPixmap(QPixmap.fromImage(p))

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.actualizar_imagen(frame)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
