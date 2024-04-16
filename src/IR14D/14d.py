import tkinter as tk
from tkinter import Label

class CustomGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Ejemplo Completo de GUI con Frames y Títulos")

        # Frame para el título, si quieres añadir un frame específico para eso
        self.titulo_frame = tk.Frame(self.master, height=30, width=1300)
        self.titulo_frame.pack(fill="x")
        Label(self.titulo_frame, text="Título Principal de la Ventana").pack()

        # Crear los frames de la primera fila
        self.frame_row1 = tk.Frame(self.master, borderwidth=2, relief="solid")
        self.frame_row1.pack(fill="x")

        # Frame 1 con dos subframes
        self.frame1 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid")
        self.frame1.pack(side="left", expand=True, fill="both")
        
        self.subframe1_top = tk.Frame(self.frame1, borderwidth=2, relief="solid", height=150)
        self.subframe1_top.pack(fill="x", expand=True)
        Label(self.subframe1_top, text="Subframe Superior").pack()

        self.subframe1_bottom = tk.Frame(self.frame1, borderwidth=2, relief="solid", height=150)
        self.subframe1_bottom.pack(fill="x", expand=True)
        Label(self.subframe1_bottom, text="Subframe Inferior").pack()

        # Frame 2, 3, 4 en la primera fila
        self.frame2 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid")
        self.frame2.pack(side="left", expand=True, fill="both")
        Label(self.frame2, text="Frame 2").pack()

        self.frame3 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid")
        self.frame3.pack(side="left", expand=True, fill="both")
        Label(self.frame3, text="Frame 3").pack()

        self.frame4 = tk.Frame(self.frame_row1, borderwidth=2, relief="solid")
        self.frame4.pack(side="left", expand=True, fill="both")
        Label(self.frame4, text="Frame 4").pack()

        # Crear los frames de la segunda fila
        self.frame_row2 = tk.Frame(self.master, borderwidth=2, relief="solid")
        self.frame_row2.pack(fill="x")
        
        self.frame5 = tk.Frame(self.frame_row2, borderwidth=2, relief="solid")
        self.frame5.pack(side="left", expand=True, fill="both")
        Label(self.frame5, text="Frame 5").pack()

        self.frame6 = tk.Frame(self.frame_row2, borderwidth=2, relief="solid")
        self.frame6.pack(side="left", expand=True, fill="both")
        Label(self.frame6, text="Frame 6").pack()

def main():
    root = tk.Tk()
    app = CustomGUI(root)
    root.mainloop()

# Si este archivo se ejecuta como programa principal, se iniciará la GUI.
if __name__ == "__main__":
    main()
