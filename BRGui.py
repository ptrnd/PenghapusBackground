import tkinter as tk
import matplotlib as mp
import numpy as np

from tkinter.filedialog import askopenfilename
from tkinter import ttk


class Visualize:

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title('Background Remover')
        self.init_widgets()

    def init_widgets(self):
        self.frame_satu = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        self.lbl_input = tk.Label(master=self.frame_satu, text='Masukkan gambar jpg : ')
        self.lbl_input.pack(pady=3)
        self.frame_satu.grid(row=0, column=0, sticky='nw')

        self.frame_dua = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        self.btn_file = tk.Button(master=self.frame_dua, text='Pilih File', width=10)
        self.btn_file.pack(pady=3)
        self.btn_file.bind('<Button-1>', self.on_click_btn_file)
        self.frame_dua.grid(row=0, column=1, sticky='n')

        self.frame_tiga = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        self.lbl_file = tk.Label(master=self.frame_tiga, text='nama file', width=10)
        self.lbl_file.pack(pady=3)
        self.frame_tiga.grid(row=0, column=2, sticky='ne', width=100)

        self.frame_empat = tk.Frame(master=self.window, borderwidth=1)
        self.lbl_before = tk.Label(master=self.frame_empat, text='Before', width=10)
        self.lbl_before.pack(pady=3)
        self.frame_empat.grid(row=1, columnspan=3, sticky='nsew')

        self.frame_lima = tk.Frame(master=self.window, borderwidth=1)
        self.lbl_after = tk.Label(master=self.frame_lima, text='After', width=10)
        self.lbl_after.pack(pady=3)
        self.frame_lima.grid(row=2, columnspan=3, sticky='s')

    def on_click_btn_file(self, event: tk.Event):
        filename = askopenfilename()
        self.lbl_file['text'] = filename

    def show(self):
        self.window.mainloop()