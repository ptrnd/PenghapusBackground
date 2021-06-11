from Gui import Gui, GuiEventListener
import numpy as np
import cv2 as cv
import time
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
        img = cv.imread(file, cv.IMREAD_UNCHANGED)
        original = img.copy()

        

        ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        edges = cv.GaussianBlur(img, (3, 3), 0)
        edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)

        l, thresh_im = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
        u = 0.5*l
        edges = cv.Canny(edges, l, u)

        _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
        mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

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

        result = cv.bitwise_and(original, original, mask=mask)
        result[mask == 0] = 255

        cv.imwrite('tmp/hasil.png', result)
        img = Image.open('tmp/hasil.png')
        img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
                newData.append((int(self.__window.n_red.get()), 
                                int(self.__window.n_green.get()), 
                                int(self.__window.n_blue.get()), 255))
            else:
                newData.append(item)

        print(int(self.__window.n_red.get()),self.__window.n_green.get(),int(self.__window.n_blue.get()))
        img.putdata(newData)
        img.save("result/"+self.__window.input_name.get(), "PNG")

        self.__window.imgAfter = tk.PhotoImage(file="result/"+self.__window.input_name.get())
        self.__window.imgAfter = self.__window.imgAfter.subsample(2)
        self.__window.canvas_after.create_image(50,10,image=self.__window.imgAfter, anchor = "nw")

    def on_click_btn_file(self, event: tk.Event):
        filename = askopenfilename()
        time.sleep(2)
        self.__window.lbl_file['text'] = filename
        self.__window.imgBefore = tk.PhotoImage(file=filename)
        self.__window.imgBefore = self.__window.imgBefore.subsample(2)
        self.__window.canvas_before.create_image(50,10,image=self.__window.imgBefore,anchor = "nw")

    def on_click_btn_process(self, event: tk.Event):
        self.Remove(file=self.__window.lbl_file['text'])

