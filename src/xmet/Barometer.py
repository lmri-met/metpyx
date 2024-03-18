import serial
import time
from reportlab.pdfgen import canvas
import tkinter as tk
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Barometer:
    """
    A class used to represent a Barometer

    ...

    Attributes
    ----------
    port : str
        a formatted string to determine the port to connect to the barometer
    baudrate : int
        the baudrate for the serial connection
    measurement : str
        the current measurement from the barometer
    running : bool
        a flag to control the continuous measurement

    Methods
    -------
    send_command(command)
        Sends a command to the barometer and returns the response.
    measure_continuously()
        Continuously measures the barometer until the running flag is set to False.
    """

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.measurement = None
        self.running = True

    def send_command(self, command):
        """Sends a command to the barometer and returns the response."""
        try:
            with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
                ser.write((command + '\r\n').encode('utf-8'))
                time.sleep(1)
                response = ''
                while ser.in_waiting > 0:
                    response += ser.read(ser.in_waiting).decode('utf-8')
                    time.sleep(0.2)
                return response.strip()
        except serial.SerialException:
            return None

    def measure_continuously(self):
        """Continuously measures the barometer until the running flag is set to False."""
        while self.running:
            self.measurement = self.send_command('ATM?')
            time.sleep(5)

class Window:
    """
    A class used to represent a Window for the barometer measurements

    ...

    Attributes
    ----------
    barometer : Barometer
        the barometer to measure
    measurements : list
        a list to store the measurements
    thread : Thread
        a thread to run the continuous measurement in

    Methods
    -------
    create()
        Creates the window and starts the continuous measurement.
    record_single_measurement()
        Records a single measurement from the barometer.
    stop_recording()
        Stops the recording, saves the measurements to a PDF, and destroys the window.
    update_label()
        Updates the label in the window with the current measurement from the barometer.
    """

    def __init__(self, barometer):
        self.barometer = barometer
        self.measurements = []
        self.thread = Thread(target=self.barometer.measure_continuously)

    def create(self):
        """Creates the window and starts the continuous measurement."""
        self.window = tk.Tk()
        self.label = tk.Label(self.window, text="Data will be displayed here")
        self.label.pack()
        self.record_button = tk.Button(self.window, text="Record Measurement", command=self.record_single_measurement)
        self.record_button.pack()
        self.stop_button = tk.Button(self.window, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()

        # Create a Figure and a dynamic matplotlib Plot
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.graph = FigureCanvasTkAgg(self.fig, master=self.window)
        self.graph.get_tk_widget().pack()
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)

        self.update_label()
        self.thread.start()  # Start the continuous measurement in a separate thread
        self.window.mainloop()

    def animate(self, i):
        """Updates the plot with new data."""
        self.ax.clear()
        self.ax.plot([float(m.split(': ')[-1]) for m in self.measurements])  # Extract the measurements from the strings
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Measurement')

    def record_single_measurement(self):
        """Records a single measurement from the barometer."""
        current_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        barometer_measurement = self.barometer.measurement
        if barometer_measurement:
            text = f"{current_datetime} - Barometer measurement: {barometer_measurement}"
        else:
            text = f"{current_datetime} - 0 Not connected"
        self.measurements.append(text)

    def stop_recording(self):
        """Stops the recording, saves the measurements to a PDF, and destroys the window."""
        self.barometer.running = False
        c = canvas.Canvas("T:/SIGOR/SGC/MARXA/Pruebas de desarrollo/barometer_measurements.pdf")
        for i, measurement in enumerate(self.measurements):
            c.drawString(100, 750 - i * 15, measurement)
        c.save()
        self.window.destroy()

    def update_label(self):
        """Updates the label in the window with the current measurement from the barometer."""
        try:
            current_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            barometer_measurement = self.barometer.measurement
            if barometer_measurement:
                text = f"{current_datetime} - Barometer measurement: {barometer_measurement}"
            else:
                text = f"{current_datetime} - 0 Not connected"
            self.label.config(text=text)
            self.label.after(5000, self.update_label)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        barometer = Barometer('COM5', 9600)
        Window(barometer).create()
    except Exception as e:
        print(f"An error occurred: {e}")