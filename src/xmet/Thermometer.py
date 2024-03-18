import serial
import time
import tkinter as tk
from reportlab.pdfgen import canvas
from datetime import datetime
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataCollector:
    """
    This class is responsible for collecting data from the device, storing it in memory and saving it to a PDF file.
    """
    def __init__(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=2)
        except serial.SerialException:
            print("0ºC Equipo no conectado")
            self.ser = None
        self.data = []

    def send_command(self, command):
        """
        Sends a command to the device and returns the response.
        """
        if self.ser is None:
            return "0ºC Equipo no conectado"
        self.ser.write((command + '\r\n').encode('utf-8'))
        time.sleep(0.5)  # Wait for the device's response
        response = ''
        while self.ser.in_waiting > 0:
            response += self.ser.read(self.ser.in_waiting).decode('utf-8', errors='replace')
        time.sleep(0.1)  # Additional pause if necessary
        # Replace dots with commas in the response
        formatted_response = response.replace('.', ',')
        return formatted_response.strip()

    def collect_data(self):
        """
        Collects data from the device and stores it in memory.
        """
        response = self.send_command('GET DATA')
        return (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'GET DATA', response)

    def save_to_pdf(self):
        """
        Saves the collected data to a PDF file.
        """
        c = canvas.Canvas("resultados.pdf")
        for i, (timestamp, command, response) in enumerate(self.data):
            c.drawString(100, 800 - i * 15, f"{timestamp}: Response to '{command}': {response}")
        c.save()

class App:
    """
    This class is responsible for creating the GUI and handling user interactions.
    """
    def __init__(self, root, collector):
        self.collector = collector
        self.root = root
        self.root.title("Data Collector")
        self.text = tk.Text(root)
        self.text.pack()
        self.save_button = tk.Button(root, text="Save Data", command=self.save_data)
        self.save_button.pack()
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()
        self.collecting = True
        self.fig, self.ax = plt.subplots()
        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.graph.get_tk_widget().pack()
        self.collect_data_continuously()

    def collect_data_continuously(self):
        """
        Collects data from the device and displays it in the GUI continuously.
        """
        if self.collecting:
            data = self.collector.collect_data()
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, f"{data[0]}: Response to '{data[1]}': {data[2]}\n")
            if self.collector.data:
                self.update_graph(data)
            self.root.after(1000, self.collect_data_continuously)

    def save_data(self):
        """
        Saves the current data to memory.
        """
        self.collector.data.append(self.collector.collect_data())

    def stop(self):
        """
        Stops data collection, saves the collected data to a PDF file, and closes the GUI.
        """
        self.collecting = False
        self.collector.save_to_pdf()
        self.root.quit()

    def update_graph(self, data):
        """
        Updates the graph with the latest data.
        """
        times, commands, temperatures = zip(*[(d[0], d[1], float(d[2].split(' ')[0])) for d in self.collector.data])
        self.ax.clear()
        self.ax.plot(times, temperatures)
        self.ax.set_xlabel('Time (hh:mm:ss)')
        self.ax.set_ylabel('Temperature (°C)')
        self.ax.set_title('Temperature over Time')
        self.ax.grid()
        self.graph.draw()

if __name__ == "__main__":
    collector = DataCollector('COM5', 9600)
    root = tk.Tk()
    app = App(root, collector)
    root.mainloop()