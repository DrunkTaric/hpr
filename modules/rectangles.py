import cv2
import math
import numpy as np
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('settings.json')

class rectangle:
    def __init__(self, x, y, h, w):
        self.own_x = x
        self.own_y = y
        self.own_h = h
        self.own_w = w
        self.close_x = 0
        self.close_y = 0
        self.close_h = 0
        self.close_w = 0
        self.distance = 0
    def Distance(self, rec):
        return math.sqrt((rec.own_x - self.own_x) ** 2 + (rec.own_y - self.own_y) ** 2) #ref https://www.cuemath.com/euclidean-distance-formula/

class filter:
    def __init__(self, data = []):
        self.input = data
        
    def start_process(self):
        self.remove_interfering_rectangles()
        self.remove_threshold_dots()
        
    def is_rectangle_inside_another(self, r1, r2):
        return (
                (r1.own_x <= r2.own_x) and #x1 < x2
                (r2.own_x <= (r1.own_x + r1.own_w)) and #x2 < x1 + w1
                ((r2.own_x + r2.own_w) >= r1.own_x) and #x2 + w2 > x1
                ((r2.own_x + r2.own_w) <= (r1.own_x + r1.own_w)) and #x2 + w2 < x1 + w1
                (r1.own_y < r2.own_y) and #y1 < y2
                ((r2.own_y + r2.own_h) <= (r1.own_y + r1.own_h)) #y2 + h2 < y1 + h1
            )
        
    def remove_interfering_rectangles(self):
        remove = []
        for i in self.input:
            for x in self.input:
                if self.is_rectangle_inside_another(i, x):
                    if (i.own_h * i.own_w) > (x.own_h * x.own_w): remove.append(x) #getting the smallest rectangle and removing it
                    else: remove.append(i)
        for i in list(dict.fromkeys(remove)):
            self.input.remove(i)
             
    def remove_threshold_dots(self):
        for i in self.input:
            if (i.own_h * i.own_w) < 200:
                self.input.remove(i)

class process: 
    def __init__(self, data = []):
        self.input = data
        self.rectagles = []

    def start_process(self):
        self.make_rectangles()
        self.filter = filter(self.rectagles)
        self.filter.start_process()
        self.rectagles = self.filter.input
        
    def make_rectangles(self):
        for i in self.input:
            self.rectagles.append(self.shape_rectangle(i))
            
    def make_rectangle(self, xL, xH, yL, yH):
        return rectangle(xL, yL, yH - yL, xH - xL)
    
    def shape_rectangle(self, array):
        x_high, y_high, x_low, y_low, edit = 0, 0, 0, 0, True
        for lines in array:
            for pos in lines:
                x, y = pos[0], pos[1]
                if edit: x_high, y_high, x_low, y_low, edit = x, y, x, y, False
                if x_high < x: x_high = x
                if y_high < y: y_high = y
                if x_low > x: x_low = x
                if y_low > y: y_low = y
        return self.make_rectangle(x_low, x_high, y_low, y_high)

class main:
    def __init__(self, src):
        self.src = src
        self.src_img = cv2.imread(self.src)
        self.resized_img = cv2.resize(self.src_img.copy(), (4000, 1500), interpolation = cv2.INTER_AREA)
        self.src_gray = cv2.cvtColor(self.src_img.copy(), cv2.COLOR_BGR2GRAY)
        self.resized_gray = cv2.cvtColor(self.resized_img.copy(), cv2.COLOR_BGR2GRAY)
        self.src_bilateral = cv2.bilateralFilter(self.src_img.copy(), 3, 50, 50)
        self.src_bilateral = cv2.bilateralFilter(self.resized_img.copy(), 3, 50, 50)
        self.src_thresh = cv2.threshold(self.src_gray.copy(), 127, 255, cv2.THRESH_BINARY_INV)[1]
        self.resized_thresh = cv2.threshold(self.resized_gray.copy(), 127, 255, cv2.THRESH_BINARY_INV)[1]
        self.src_dilated = cv2.dilate(self.src_thresh.copy(), np.ones((5 ,100), np.uint8), iterations=1)
        self.resized_dilated = cv2.dilate(self.resized_thresh.copy(), np.ones((5 ,100), np.uint8), iterations=1)
        self.src_morph = cv2.morphologyEx(self.src_thresh.copy(), cv2.MORPH_OPEN, np.ones((2, 2)))
        self.resized_morph = cv2.morphologyEx(self.resized_thresh.copy(), cv2.MORPH_OPEN, np.ones((2, 2)))
    
    def start_process(self):
        self.ctrs, self.heir = cv2.findContours(self.resized_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.process = process(self.ctrs)
        self.process.start_process()
        self.output = self.process.rectagles