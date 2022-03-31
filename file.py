from tkinter import filedialog,Label,messagebox
from PIL import ImageTk, Image
from cv2 import imread,cvtColor,COLOR_BGR2RGB,COLOR_RGB2BGR,imdecode
from numpy import asarray,fromfile,uint8

read_count = 0

def show_img(window,img,color_space = COLOR_BGR2RGB):
    global loaded_img
    global panel
    global current_show_img
    
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

    try:
        #using numpy get the file/path include chinese characters
        load_img = imdecode(fromfile(filedialog.askopenfilename(
            filetypes=[("jpg","*.jpg"),("png","*.png"),("gif","*.gif"),("All files", "*")]),dtype=uint8),-1)
        show_img(window,load_img)
    except: return

def save_file():
    if ('load_img' in globals()):
        try:
            if (get_img().size != 0):
                current_show_img.save(filedialog.asksaveasfilename(defaultextension=".jpg"
                ,filetypes=[("jpg","*.jpg"),("png","*.png"),("gif","*.gif"),("All files", "*")]
                ,initialdir= "./"
                ,title="儲存影像"))

                # imwrite(filedialog.asksaveasfilename(defaultextension=".jpg"
                # ,filetypes=[("jpg","*.jpg"),("png","*.png"),("gif","*.gif"),("All files", "*")]
                # ,initialdir= "./"
                # ,title="儲存影像")
                # ,load_img)
        except: return
    else:  messagebox.showwarning("警告","未開啟檔案")

#get the image from tk for opencv using(tk = RGB,opencv = BGR)
def get_img(color_space = COLOR_RGB2BGR):
    img = asarray(current_show_img)
    # transform 2 BGR
    # if color space == -1->default using show image with RGB (opencv using BGR)
    if (color_space != -1):
        img = cvtColor(img, color_space)
    return img

def current_read():
    return read_count

def if_loaded_img():
    try:
        return loaded_img
    except:
        return False