import tkinter as tk
from file import *
from cv2 import equalizeHist,cvtColor,threshold,filter2D,GaussianBlur,medianBlur
from cv2 import THRESH_BINARY,COLOR_BGR2GRAY,BORDER_DEFAULT
from image_edit import *
import numpy as np

def setting_threshold_window(window,menu = ""):
    if (if_loaded_img()):
        threshold = tk.Toplevel()
        threshold.grab_set()
        threshold.title("設定門檻")

        tk.Label(threshold, text = "最小值").grid(row = 0, column = 0)
        min = tk.Entry(threshold, width = 7)
        min.grid(row = 0, column = 1,padx=10)

        tk.Label(threshold, text = "最大值").grid(row =1, column = 0)
        max = tk.Entry(threshold, width = 7)
        max.grid(row = 1, column = 1,padx=10)

        tk.Button(threshold, text = "確認",command = lambda : img_thresholding(window,threshold,min.get(),max.get(),menu)).grid(row = 2, column = 0,padx=21)
        tk.Button(threshold, text = "取消",command = threshold.destroy).grid(row = 2, column = 1,)
    else:
        messagebox.showwarning("警告","未開啟檔案")
            
def img_equalizeHist(window,menu = ""):
    try:
        img = cvtColor(get_img(),COLOR_BGR2GRAY)
        if (messagebox.askokcancel(title="警告", message="直方圖等化後將無法恢復")):
            if (menu != ""):
                menu_color_switch("GRAY",menu)
            img = equalizeHist(img)
            show_img(window,img)
    except:
        messagebox.showwarning("警告","未開啟檔案")

def img_thresholding(window,setting_window,min,max,menu = ""):
    setting_window.destroy()
    try:
        img = cvtColor(get_img(),COLOR_BGR2GRAY)
        if (menu != ""):
                menu_color_switch("GRAY",menu)
        min = int(min);max = int(max)
        img = threshold(img, int(min), int(max), THRESH_BINARY)[1]
        show_img(window,img,-1)
    except ValueError:
        messagebox.showwarning("警告","請輸入數字")
    except NameError:
        messagebox.showwarning("警告","未開啟檔案")

def img_filter(window,filter_name,menu =""):
    try:
        img = get_img()
        if (filter_name == "averaging"):
            #kernel size = 3*3,get the average value from kernel 
            kernel_size = np.ones((3,3),np.float32)/9

            #after filter image will get same image depth when ddepth's value = -1
            show_img(window,filter2D(src= img,ddepth= -1, kernel = kernel_size , borderType= BORDER_DEFAULT))
        if (filter_name == "gaussian_blur"):
            show_img(window,GaussianBlur(img, (3,3) ,0,borderType=BORDER_DEFAULT))
        if (filter_name == "median_blur"):
            #medianBlur(image,kernel size)
            show_img(window,medianBlur(img,5,BORDER_DEFAULT))
        if (filter_name == "emboss"):
            emboss_kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
            show_img(window,filter2D(src= img,ddepth= -1, kernel = emboss_kernel , borderType= BORDER_DEFAULT))
        if (filter_name == "sobel"):
            sobel_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            img = cvtColor(img,COLOR_BGR2GRAY)
            menu_color_switch("GRAY",menu)
            show_img(window,filter2D(src= img,ddepth= -1, kernel = sobel_kernel , borderType= BORDER_DEFAULT))
    except:
        messagebox.showwarning("警告","未開啟檔案")