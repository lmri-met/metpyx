import cv2
import os
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from datetime import datetime
from threading import Thread

class Camera:
    """
    A class used to represent a Camera.

    ...

    Attributes
    ----------
    camera_index : int
        a integer representing the index of the camera to use
    cap : cv2.VideoCapture
        a VideoCapture object to capture video from the camera
    c : canvas.Canvas
        a Canvas object to create a PDF file
    image_counter : int
        a counter to keep track of the number of images captured
    is_capturing : bool
        a flag to indicate whether the camera is capturing images
    output_dir : str
        a string representing the directory to save images and PDF file

    Methods
    -------
    capture(image_name)
        Captures an image from the camera and saves it to the output directory.
    release()
        Releases the camera and destroys all windows.
    run()
        Starts capturing video from the camera and displays a GUI for capturing images.
    """

    def __init__(self, camera_index=0, output_dir="."):
        """
        Constructs all the necessary attributes for the Camera object.

        Parameters
        ----------
            camera_index : int, optional
                The index of the camera to use (default is 0)
            output_dir : str, optional
                The directory to save images and PDF file (default is ".")
        """

        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        self.c = canvas.Canvas(os.path.join(output_dir, "images.pdf"), pagesize=landscape(letter))
        self.image_counter = 0
        self.is_capturing = True
        self.output_dir = output_dir

    def capture(self, image_name):
        """
        Captures an image from the camera and saves it to the output directory.

        Parameters
        ----------
            image_name : str
                The name of the image file

        Returns
        -------
            str
                The path of the image file, or None if there was an error capturing the image
        """

        ret, frame = self.cap.read()
        if not ret:
            print("Error capturing frame")
            return None

        image_path = os.path.join(self.output_dir, f"{image_name}.png")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img.save(image_path)
        return image_path

    def release(self):
        """Releases the camera and destroys all windows."""

        self.cap.release()

    def run(self):
        """
        Starts capturing video from the camera and displays a GUI for capturing images.
        When the "Capture" button is clicked, an image is captured and added to a PDF file.
        When the "Stop" button is clicked, the PDF file is saved and the program exits.
        """

        width, height = landscape(letter)
        image_width = width / 2
        image_height = height / 2

        def update_image():
            ret, frame = self.cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            if self.is_capturing:
                lmain.after(10, update_image)

        def capture_image():
            image_path = self.capture(f"image_{self.image_counter}")
            if image_path:
                x = (self.image_counter % 2) * image_width
                y = (self.image_counter // 2) * image_height
                self.c.drawImage(image_path, x, y + 20, image_width, image_height - 20)
                timestamp = datetime.now()
                timestamp_str = f"Date: {timestamp.strftime('%d/%m/%Y')}; Time: {timestamp.strftime('%H:%M:%S')}"
                self.c.setFont('Helvetica', 14)
                self.c.drawString(x, y, timestamp_str)
                if self.image_counter % 4 == 3:
                    self.c.showPage()
                self.image_counter += 1
                tk.messagebox.showinfo("Info", "Captura realizada")

        def stop_capture():
            if self.image_counter % 4 != 3:
                self.c.showPage()
            self.c.save()
            self.is_capturing = False
            self.release()
            cv2.destroyAllWindows()
            root.quit()

        root = tk.Tk()
        root.title("CAMERA")
        lmain = tk.Label(root)
        lmain.pack()
        btn_capture = tk.Button(root, text="Capture", command=capture_image)
        btn_capture.pack(side="left")
        btn_stop = tk.Button(root, text="Stop", command=stop_capture)
        btn_stop.pack(side="right")

        update_thread = Thread(target=update_image)
        update_thread.start()

        root.mainloop()

if __name__ == "__main__":
    camera = Camera(output_dir="T:\\SIGOR\\SGC\\MARXA\\Pruebas de desarrollo\\Camara")
    camera.run()