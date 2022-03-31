import tkinter as tk
from file import *
from cv2 import equalizeHist,cvtColor,threshold
from cv2 import THRESH_BINARY,COLOR_BGR2GRAY
from image_edit import *

def setting_threshold_window(window):
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

        tk.Button(threshold, text = "確認",command = lambda : img_thresholding(window,threshold,min.get(),max.get())).grid(row = 2, column = 0,padx=21)
        tk.Button(threshold, text = "取消",command = threshold.destroy).grid(row = 2, column = 1,)
    else:
        messagebox.showwarning("警告","未開啟檔案")
            
def img_equalizeHist(window,menu = ""):
    try:
        img = cvtColor(get_img(),COLOR_BGR2GRAY)
        if (messagebox.askokcancel(title="警告", message="影像二值化後將無法恢復")):
            if (menu != ""):
                menu_color_switch("GRAY",menu)
            img = equalizeHist(img)
            show_img(window,img)
    except:
        messagebox.showwarning("警告","未開啟檔案")

def img_thresholding(window,setting_window,min,max):
    setting_window.destroy()
    try:
        img = cvtColor(get_img(),COLOR_BGR2GRAY)
        min = int(min);max = int(max)
        img = threshold(img, int(min), int(max), THRESH_BINARY)[1]
        show_img(window,img,-1)
    except ValueError:
        messagebox.showwarning("警告","請輸入數字")
    except NameError:
        messagebox.showwarning("警告","未開啟檔案")