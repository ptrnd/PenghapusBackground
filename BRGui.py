import tkinter as tk
import matplotlib as mp
import numpy as np
import time
from tkinter import ttk

class VisualizeEventListener:
    def btn_file(self, event: tk.Event):
        pass

    def btn_save(self, event: tk.Event):
        pass

    def btn_process(self, event: tk.Event):
        pass

class Visualize:
    def __init__(self, backend : VisualizeEventListener):
        self.window = tk.Tk()
        self.window.geometry('800x400')
        self.window.title('Background Remover')

        self.backend = backend

        self.init_widgets()
        self.__bind_events()

    def init_widgets(self):
        
        # tombol memasukkan gambar
        self.frame_input_img = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        self.lbl_input = tk.Label(master=self.frame_input_img, text='Masukkan gambar jpg : ')
        self.lbl_input.pack(pady=1, anchor="w")
        
        self.btn_file = tk.Button(master=self.frame_input_img, text='Pilih File', width=10)
        self.btn_file.pack(pady=1, anchor="w", side='left')

        self.lbl_file = tk.Label(master=self.frame_input_img, text='nama file')
        self.lbl_file.pack(pady=1, anchor="w")
        self.frame_input_img.grid(row=0, column=0, sticky='w')


        # Setting warna BG
        self.frame_input_bg = tk.Frame(master=self.window, borderwidth=1)  # , relief=tk.RAISED)
        
        self.lbl_red = tk.Label(master=self.frame_input_bg, text='Red : ')
        self.lbl_red.pack(pady=1,anchor="n", side='left')
        self.n_red = tk.Entry(master=self.frame_input_bg, width=10)
        self.n_red.pack(pady=1,side='left')

        self.lbl_green = tk.Label(master=self.frame_input_bg, text='Green : ')
        self.lbl_green.pack(pady=1,anchor="n", side='left')
        self.n_green = tk.Entry(master=self.frame_input_bg, width=10)
        self.n_green.pack(pady=1,side='left')

        self.lbl_blue = tk.Label(master=self.frame_input_bg, text='Blue : ')
        self.lbl_blue.pack(pady=1,anchor="n", side='left')
        self.n_blue = tk.Entry(master=self.frame_input_bg, width=10)
        self.n_blue.pack(pady=1)

        self.n_blue.insert(tk.END, "0")
        self.n_red.insert(tk.END, "0")
        self.n_green.insert(tk.END, "0")

        self.frame_input_bg.grid(row=0, column=1, sticky='e')
        
        #btn Proses
        self.frame_setting = tk.Frame(master=self.window, borderwidth=1)

        # self.lbl_max = tk.Label(master=self.frame_setting, text='Max : ')
        # self.lbl_max.pack(pady=1,anchor="n", side='left')
        # self.n_max = tk.Entry(master=self.frame_setting, width=10)
        # self.n_max.pack(pady=1, side='left')

        # self.lbl_min = tk.Label(master=self.frame_setting, text='Min : ')
        # self.lbl_min.pack(pady=1,anchor="n", side='left')
        # self.n_min = tk.Entry(master=self.frame_setting, width=10)
        # self.n_min.pack(pady=1,side='left')

        self.lbl_file_name = tk.Label(master=self.frame_setting, text='Simpan dengan Nama : ')
        self.lbl_file_name.pack(pady=1,anchor="n", side='left')
        self.input_name = tk.Entry(master=self.frame_setting, width=20)
        self.input_name.pack(pady=1,side='left')

        self.input_name.insert(tk.END, "result.png")

        self.btn_process = tk.Button(master=self.frame_setting, text='Proses and Save')
        self.btn_process.pack(padx=10)
        self.frame_setting.grid(row=1, column=0, sticky='e', pady=3,  columnspan=2)


        self.frame_img = tk.Frame(master=self.window, borderwidth=1)
        self.frame_img.grid(row=2,column=0, columnspan=2)

        # Before
        # label "sebelum"
        self.frame_before = tk.Frame(master=self.frame_img, borderwidth=1)
        self.lbl_before = tk.Label(master=self.frame_before, text='Before', width=10)
        self.lbl_before.pack(pady=1)

        # gambar sebelum backgroundnya dihapus
        self.canvas_before = tk.Canvas(master=self.frame_before)
        self.canvas_before.pack(side='top')
        self.imgBefore = tk.PhotoImage(file="init.png")
        self.imgBefore = self.imgBefore.subsample(2)
        self.canvas_before.create_image(200,100,image=self.imgBefore)

        self.frame_before.grid(row=0, column=0, sticky='n')

        #After
        # label "setelah"
        self.frame_after = tk.Frame(master=self.frame_img, borderwidth=1)
        self.lbl_after = tk.Label(master=self.frame_after, text='After', width=10)
        self.lbl_after.pack(pady=1)

        # gambar setelah backgroundnya dihapus
        self.canvas_after = tk.Canvas(master=self.frame_after)
        self.canvas_after.pack()
        self.imgAfter = tk.PhotoImage(file="init.png")
        self.imgAfter = self.imgAfter.subsample(2)
        self.canvas_after.create_image(200,100,image=self.imgAfter)
        self.frame_after.grid(row=0, column=1, sticky='n')


    # method tombol untuk memasukkan file
    def __bind_events(self):
        self.btn_file.bind('<Button-1>', self.backend.on_click_btn_file)
        self.btn_process.bind('<Button-1>', self.backend.on_click_btn_process)


    def show(self):
        self.window.mainloop()