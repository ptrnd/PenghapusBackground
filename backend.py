from BRGui import Visualize, VisualizeEventListener
import numpy as np
import cv2 as cv
import time
from matplotlib import pyplot as plt
import sys
from PIL import Image

import tkinter as tk
from tkinter.filedialog import askopenfilename


# from google.colab.patches import cv2_imshow

class Backend(VisualizeEventListener):
    def __init__(self):
        self.__window = None

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window: Visualize):
        self.__window = window

    def Remove(self, file):
        img = cv.imread(file, cv.IMREAD_UNCHANGED)
        original = img.copy()

        # buat edge conture (garis di samping gambar)
        ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        edges = cv.GaussianBlur(img, (21, 51), 4)
        edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(edges, 6, 6)

        # memperbesar tebal garis
        _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
        mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

        # mengisi area dalam
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

        # memperhalus sudut
        # closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        # mask = cv.morphologyEx(mask, cv.MORPH_ERODE, kernel)

        # clipping (memasukkan gambar di area putih)
        result = cv.bitwise_and(original, original, mask=mask)
        result[mask == 0] = 255
        # cv.imshow(result)

        cv.imwrite('hasil.png', result)

        img = Image.open('hasil.png')
        img.convert("RGBA")
        datas = img.getdata()

        # background
        newData = []
        for item in datas:
            if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        # save gambar
        img.putdata(newData)
        img.save("img.png", "PNG")

        self.__window.imgAfter = tk.PhotoImage(file="img.png")
        self.__window.imgAfter = self.__window.imgAfter.subsample(3)
        self.__window.canvas_after.create_image(50,10,image=self.__window.imgAfter, anchor = "nw")

    def on_click_btn_file(self, event: tk.Event):
        filename = askopenfilename()
        time.sleep(2)
        # menampilkan gambar asli di bagian "before"
        self.__window.lbl_file['text'] = filename
        self.__window.imgBefore = tk.PhotoImage(file=filename)
        self.__window.imgBefore = self.__window.imgBefore.subsample(3)
        self.__window.canvas_before.create_image(50,10,image=self.__window.imgBefore,anchor = "nw")

        self.Remove(file=filename)
