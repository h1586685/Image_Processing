from tkinter import messagebox
from file import *
from cv2 import selectROI,destroyWindow,calcHist
from cv2 import COLOR_RGB2GRAY,COLOR_HSV2RGB,COLOR_HSV2BGR,COLOR_RGB2HSV,COLOR_BGR2HSV,COLOR_BGR2GRAY
import matplotlib.pyplot as plt

current_color_space="RGB"
current_img_count = 0

def ROI(window):
    global cut_img
    global cut_flag
    global current_img_count
    try:
        read_count = current_read()
        if (read_count > current_img_count): 
            current_img_count = read_count
            cut_flag = False

        if ('cut_flag' in globals() and cut_flag):
            img = cut_img
        else:
            img = get_img()
            cut_flag = True

        roi = selectROI(windowName="ROI",img = img,showCrosshair=True,fromCenter=False)
        x,y,w,h = roi
        if (x and y and w and h !=0):
            destroyWindow("ROI")
            cut_img =img [y:y+h,x:x+w]
            show_img(window,cut_img)
        else:
            destroyWindow("ROI")
            cut_flag = False

    except: messagebox.showwarning("警告","未開啟檔案")

def hist():
    try:
        img = get_img()
        if (get_color_space() == "HSV"):
            color = ('r','g','b')
        else:
            color = ('b','g','r')

        for i, col in enumerate(color):
            histr = calcHist([img],[i],None,[256],[0, 256])
            plt.plot(histr, color = col)
            plt.xlim([0, 256])
        plt.show()
    except: messagebox.showwarning("警告","未開啟檔案")

def change_color_space(window,space,menu):
    try:
        if (space == "RGB2BGR"):
            img = get_img()
            menu_color_switch("BGR",menu)
            show_img(window,img,color_space = -1)
        if (space == "BGR2RGB"):
            img = get_img(-1)
            menu_color_switch("RGB",menu)
            show_img(window,img)

        if (space == "RGB2HSV"):
            img = get_img(COLOR_RGB2HSV)
            menu_color_switch("HSV",menu)
            show_img(window,img,-1)
        if (space == "HSV2RGB"):
            img = get_img(COLOR_HSV2RGB)
            menu_color_switch("RGB",menu)
            show_img(window,img,-1)

        if (space == "BGR2HSV"):
            img = get_img(COLOR_BGR2HSV)
            menu_color_switch("HSV",menu)
            show_img(window,img,-1)
        if (space == "HSV2BGR"):
            img = get_img(COLOR_HSV2BGR)
            menu_color_switch("BGR",menu)
            show_img(window,img,-1)

        if (space == "RGB2GRAY"):
            img = get_img(-1)
            if (messagebox.askokcancel(title="警告", message="灰階化後將無法恢復")):
                menu_color_switch("GRAY",menu)
                show_img(window,img,color_space = COLOR_RGB2GRAY)
        
        if (space == "BGR2GRAY"):
            img = get_img()
            if (messagebox.askokcancel(title="警告", message="灰階化後將無法恢復")):
                menu_color_switch("GRAY",menu)
                show_img(window,img,color_space = COLOR_BGR2GRAY)

    except: messagebox.showwarning("警告","未開啟檔案")

def menu_color_switch(color_space,menu):
    global current_color_space
    if (color_space =="RGB"):
        current_color_space = "RGB"
        menu.entryconfigure(0, label="目前色彩空間 : RGB")
        menu.entryconfigure(1, state="normal")
        menu.entryconfigure(3, state="normal")
        menu.entryconfigure(7, state="normal")
        menu.entryconfigure(2, state="disabled")
        menu.entryconfigure(4, state="disabled")
        menu.entryconfigure(5, state="disabled")
        menu.entryconfigure(6, state="disabled")
        menu.entryconfigure(8, state="disabled")    
    if (color_space == "BGR"):
        current_color_space = "BGR"
        menu.entryconfigure(0, label="目前色彩空間 : BGR")
        menu.entryconfigure(2, state="normal")
        menu.entryconfigure(4, state="normal")
        menu.entryconfigure(8, state="normal")
        menu.entryconfigure(1, state="disabled")
        menu.entryconfigure(3, state="disabled")
        menu.entryconfigure(5, state="disabled")
        menu.entryconfigure(6, state="disabled")
        menu.entryconfigure(7, state="disabled")    
    if (color_space == "HSV"):
        current_color_space = "HSV"
        menu.entryconfigure(0, label="目前色彩空間 : HSV")
        menu.entryconfigure(5, state="normal")
        menu.entryconfigure(6, state="normal")
        menu.entryconfigure(1, state="disabled")
        menu.entryconfigure(2, state="disabled")
        menu.entryconfigure(3, state="disabled")
        menu.entryconfigure(4, state="disabled")
        menu.entryconfigure(7, state="disabled")
        menu.entryconfigure(8, state="disabled")

    if (color_space == "GRAY"):
        current_color_space = "GRAY"
        menu.entryconfigure(0, label="目前色彩空間 : GRAY")
        for i in range(1 ,9):
            menu.entryconfigure(i, state="disabled")

def get_color_space():
    return current_color_space