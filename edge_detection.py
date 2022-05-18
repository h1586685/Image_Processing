from file import *
from image_edit import *
from tkinter import IntVar,Scale,Button
from cv2 import cvtColor,GaussianBlur,Canny,imshow,destroyWindow,filter2D,cornerHarris,imshow
from cv2 import COLOR_BGR2GRAY,BORDER_DEFAULT
from numpy import array,empty

def Canny_edge_detection(img,min_thresh,max_thresh,window = None,showing=""):
    gray = cvtColor(img, COLOR_BGR2GRAY)
    blurred = GaussianBlur(gray, (5, 5), 0)
    canny_img = Canny(blurred, min_thresh, max_thresh)
    if (showing != ""):
        show_img(window,canny_img)
    else:
        imshow("Canny Edge Detection Preview",canny_img)

def Canny_Value_Set(window,menu =None):
    if (if_loaded_img()):
        img = get_img()
        imshow("Canny Edge Detection Preview",img)

        s_min_value = IntVar()
        s_max_value = IntVar()

        Canny_window = Toplevel()
        Canny_window.grab_set()

        Canny_window.title("Canny閥值")
        scale_min = Scale(Canny_window, orient="horizontal", label="最小值:"
                       ,length =300, from_= 0, to=255, variable=s_min_value
                       ,command = lambda x=None:Canny_edge_detection(img,s_min_value.get(),s_max_value.get()))
        scale_min.pack()

        scale_max = Scale(Canny_window, orient="horizontal", label="最大值:"
                       ,length =300, from_= 0, to=255, variable=s_max_value
                       ,command = lambda x=None:Canny_edge_detection(img,s_min_value.get(),s_max_value.get()))
        scale_max.pack()
        
        Button(Canny_window, text = "確認",command = lambda : [Canny_window.destroy(),destroyWindow("Canny Edge Detection Preview")
                                                              ,menu_color_switch("GRAY",menu)
                                                              ,Canny_edge_detection(img,s_min_value.get(),s_max_value.get(),window,"true")]).pack()
        Button(Canny_window, text = "取消",command = lambda : [destroyWindow("Canny Edge Detection Preview"),Canny_window.destroy()]).pack()
    else:
        messagebox.showwarning("警告","未開啟檔案")

def Sobel_edge_detection(window,menu =""):
    sobel_kernel = array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    img = cvtColor(get_img(),COLOR_BGR2GRAY)
    menu_color_switch("GRAY",menu)
    show_img(window,filter2D(src= img,ddepth= -1, kernel = sobel_kernel , borderType= BORDER_DEFAULT))
