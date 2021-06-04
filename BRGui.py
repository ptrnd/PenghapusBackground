import tkinter as tk
import matplotlib as mp
import numpy as np
from tkinter import ttk

class VisualizeEventListener:
    def btn_file(self, event: tk.Event):
        pass

    def btn_save(self, event: tk.Event):
        pass

class Visualize:
    def __init__(self, backend : VisualizeEventListener):
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title('Background Remover')

        self.backend = backend

        self.init_widgets()
        self.__bind_events()

    def init_widgets(self):
        self.frame_satu = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        self.lbl_input = tk.Label(master=self.frame_satu, text='Masukkan gambar jpg : ')
        self.lbl_input.pack(pady=3)
        self.frame_satu.grid(row=0, column=0, sticky='nw')

        self.frame_dua = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        self.btn_file = tk.Button(master=self.frame_dua, text='Pilih File', width=10)
        self.btn_file.pack(pady=3)
        self.frame_dua.grid(row=0, column=1, sticky='n')

        self.frame_tiga = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        self.lbl_file = tk.Label(master=self.frame_tiga, text='nama file', width=100)
        self.lbl_file.pack(pady=3)
        self.frame_tiga.grid(row=0, column=2, sticky='ne')

        #Before
        self.frame_empat = tk.Frame(master=self.window, borderwidth=1)
        self.lbl_before = tk.Label(master=self.frame_empat, text='Before', width=10)
        self.lbl_before.pack(pady=3)
        
        self.canvas_before = tk.Canvas(master=self.frame_empat)
        self.canvas_before.pack(pady=3)
        self.imgBefore = tk.PhotoImage(file="doraemon hitam.png")
        self.canvas_before.create_image(100,100,image=self.imgBefore)

        self.frame_empat.grid(row=1, columnspan=3, sticky='nsew')

        #After
        self.frame_lima = tk.Frame(master=self.window, borderwidth=1)
        self.lbl_after = tk.Label(master=self.frame_lima, text='After', width=10)
        self.lbl_after.pack(pady=3)

        self.canvas_after = tk.Canvas(master=self.frame_lima)
        self.canvas_after.pack(pady=3)
        self.imgAfter = tk.PhotoImage(file="doraemon hitam.png")
        self.canvas_after.create_image(100,100,image=self.imgAfter)

        self.frame_lima.grid(row=2, columnspan=3, sticky='s')

    def __bind_events(self):
        self.btn_file.bind('<Button-1>', self.backend.on_click_btn_file)


    def show(self):
        self.window.mainloop()