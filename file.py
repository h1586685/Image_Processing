from tkinter import Toplevel, filedialog,Label,messagebox,W
from PIL import ImageTk, Image
from cv2 import cvtColor,COLOR_BGR2RGB,COLOR_RGB2BGR,imdecode
from numpy import asarray,fromfile,uint8
from os.path import dirname,basename
from os import stat

read_count = 0

def show_img(window,img,color_space = COLOR_BGR2RGB):
    global loaded_img
    global panel
    global current_show_img
    global img_h,img_w
    
    # image & window resize
    img_h,img_w =img.shape[:2]
    window.geometry('%dx%d'%(img_w,img_h)) 
    
    # transform 2 RGB
    # if color space == -1->default using show image with BGR (tk window using RGB)
    if (color_space != -1):
        img = cvtColor(img, color_space)

    #load image on tk
    current_show_img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=current_show_img)

    #checking if already loaded image
    if ('loaded_img' in globals()):
        panel.configure(image = imgtk,height = img_h, width = img_w)
    else:
        panel = Label(window, image = imgtk,height = img_h, width = img_w)
        loaded_img = True

    panel.pack(fill = "none", expand = "false")
    window.mainloop()

def read_file(window,menu = ""):
    global read_count
    global load_img
    global image_path

    if ('loaded_img' in globals()):
        read_count += 1
        if (menu != ""):
            menu.entryconfigure(0, label="目前色彩空間 : RGB")
            menu.entryconfigure(1, state="normal")
            menu.entryconfigure(3, state="normal")
            menu.entryconfigure(7, state="normal")
            menu.entryconfigure(2, state="disabled")
            menu.entryconfigure(4, state="disabled")
            menu.entryconfigure(5, state="disabled")
            menu.entryconfigure(6, state="disabled")
            menu.entryconfigure(8, state="disabled")

    image_path = filedialog.askopenfilename(filetypes=[("jpg","*.jpg"),("png","*.png"),("gif","*.gif"),("All files", "*")])
    if (image_path != ""):
        #Use numpy reading the file/path including chinese characters
        #and then use the cv.imdecode reading the image from stream
        load_img = imdecode(fromfile(image_path,dtype=uint8),-1)
        show_img(window,load_img)

def save_file():
    if ('load_img' in globals()):
        try:
            if (get_img().size != 0):
                current_show_img.save(filedialog.asksaveasfilename(defaultextension=".jpg"
                ,filetypes=[("jpg","*.jpg"),("png","*.png"),("gif","*.gif"),("All files", "*")]
                ,initialdir= "./"
                ,title="儲存影像"))
        except: return
    else:  messagebox.showwarning("警告","未開啟檔案")

def image_info():
    if (if_loaded_img()):
        #show the image info on top-level window
        image_info_window = Toplevel()
        image_info_window.grab_set()

        # "sticky=W" <- the "W" is import from tkinter
        image_info_window.title("檔案資訊")
        Label(image_info_window, text = "檔案名稱：").grid(row = 0, column = 0,sticky=W)
        filename_label = Label(image_info_window, text = basename(image_path))
        filename_label.grid(row = 0, column = 1,sticky=W)

        Label(image_info_window, text = "檔案路徑：").grid(row = 1, column = 0,sticky=W)
        only_filepath = Label(image_info_window, text = dirname(image_path))
        only_filepath.grid(row = 1, column = 1,sticky=W)

        Label(image_info_window, text = "圖片尺寸：").grid(row = 2, column = 0,sticky=W)
        only_filepath = Label(image_info_window, text = str(img_w) + "x" + str(img_h))
        only_filepath.grid(row = 2, column = 1,sticky=W)

        Label(image_info_window, text = "原始圖片大小：").grid(row = 3, column = 0,sticky=W)
        only_filepath = Label(image_info_window, text = str(round(stat(image_path).st_size/1e+6,3)) + "MB")
        only_filepath.grid(row = 3, column = 1,sticky=W)

    else:
        messagebox.showwarning("警告","未開啟檔案")

#get the image from tk for opencv using(tk = RGB,opencv = BGR)
def get_img(color_space = COLOR_RGB2BGR):
    try:
        img = asarray(current_show_img)
        # transform 2 BGR
        # if color space == -1->default using show image with RGB (opencv using BGR)
        if (color_space != -1):
            img = cvtColor(img, color_space)
        return img
    except:
        pass

def current_read():
    return read_count

def if_loaded_img():
    try:
        return loaded_img
    except:
        return False

def get_img_size():
    return img_h,img_w