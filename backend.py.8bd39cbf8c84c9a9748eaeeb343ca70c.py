from BRGui import Visualize, VisualizeEventListener
import numpy as np
import cv2 as cv
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

        l = int(max(5, 6))
        u = int(min(6, 6))

        ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        edges = cv.GaussianBlur(img, (21, 51), 4)
        edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(edges, l, u)

        _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
        mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

        data = mask.tolist()
        sys.setrecursionlimit(10 ** 8)
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] != 255:
                    data[i][j] = -1
                else:
                    break
            for j in range(len(data[i]) - 1, -1, -1):
                if data[i][j] != 255:
                    data[i][j] = -1
                else:
                    break
        image = np.array(data)
        image[image != -1] = 255
        image[image == -1] = 0

        mask = np.array(image, np.uint8)

        result = cv.bitwise_and(original, original, mask=mask)
        result[mask == 0] = 255
        # cv.imshow(result)

        cv.imwrite('bg.png', result)

        img = Image.open('bg.png')
        img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
                newData.append((255, 0, 0, 255))
            else:
                newData.append(item)
    
        img.putdata(newData)
        img.save("img.png", "PNG")

        self.__window.imgAfter = tk.PhotoImage(file="img.png")
        self.__window.canvas_after.create_image(50,10,image=self.__window.imgAfter)

    def on_click_btn_file(self, event: tk.Event):
        filename = askopenfilename()
        self.__window.lbl_file['text'] = filename
        self.__window.imgBefore = tk.PhotoImage(file=filename)
        self.__window.canvas_before.create_image(50,10,image=self.__window.imgBefore)

        self.Remove(file=filename)