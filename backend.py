from Gui import Gui, GuiEventListener
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from PIL import Image

import tkinter as tk
from tkinter.filedialog import askopenfilename


# from google.colab.patches import cv2_imshow

class Backend(GuiEventListener):
    def __init__(self):
        self.__window = None

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window: Gui):
        self.__window = window

    def Remove(self, file):
        # Membaca file gambar
        img = cv.imread(file)
        original = img.copy()

        # deteksi edge object
        blur = cv.GaussianBlur(img, (3, 3), 0)
        gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
        l, thresh_im = cv.threshold(gray, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
        u = 0.5*l
        edges = cv.Canny(gray, l, u)

        # melakukan morphologu close
        _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
        mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

        # membuat gabar object maskin
        data =   mask.tolist()
        for i in  range(len(data)):
            for j in  range(len(data[i])):
                if data[i][j] !=  255:
                    data[i][j] =  -1
                else:
                    break
            for j in  range(len(data[i])-1, -1, -1):
                if data[i][j] !=  255:
                    data[i][j] =  -1
                else:
                    break                    
        image = np.array(data)
        image[image !=  -1] =  255
        image[image ==  -1] =  0
        mask = np.array(image, np.uint8)

        kernel = np.ones((5,5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_ERODE, kernel)


        # Melakukan maskin terhadap gambar ori dengan gambar maskin
        result = cv.bitwise_and(original, original, mask=mask)
        result[mask == 0] = 255

        # Menyimpan hasil maskin
        cv.imwrite('tmp/mask.png', result)
        img = Image.open('tmp/mask.png')
        img.convert("RGBA")
        datas = img.getdata()

        # Ubah warna backGround
        # warna putih di anggap background
        newData = []
        for item in datas:
            if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
                newData.append((int(self.__window.n_red.get()), 
                                int(self.__window.n_green.get()), 
                                int(self.__window.n_blue.get()), 255))
            else:
                newData.append(item)
        img.putdata(newData)

        #simpan Gambar
        img.save("result/"+self.__window.input_name.get(), "PNG")

        #tampilkan Hasil di gui
        self.__window.imgAfter = tk.PhotoImage(file="result/"+self.__window.input_name.get())
        self.__window.imgAfter = self.__window.imgAfter.subsample(2)
        self.__window.canvas_after.create_image(50,10,image=self.__window.imgAfter, anchor = "nw")

    def on_click_btn_file(self, event: tk.Event):
        filename = askopenfilename()
        self.__window.lbl_file['text'] = filename
        self.__window.imgBefore = tk.PhotoImage(file=filename)
        self.__window.imgBefore = self.__window.imgBefore.subsample(2)
        self.__window.canvas_before.create_image(50,10,image=self.__window.imgBefore,anchor = "nw")

    def on_click_btn_process(self, event: tk.Event):
        self.Remove(file=self.__window.lbl_file['text'])

