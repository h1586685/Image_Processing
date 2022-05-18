from tkinter import LEFT,RIGHT, messagebox,Scale,IntVar,DoubleVar,Button
from file import *
import cv2 as cv
import matplotlib.pyplot as plt
from numpy import float32,array

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
            if (get_img().size ==0):raise

        roi = cv.selectROI(windowName="ROI",img = img,showCrosshair=True,fromCenter=False)
        x,y,w,h = roi
        if (x and y and w and h !=0):
            cv.destroyWindow("ROI")
            cut_img =img [y:y+h,x:x+w]
            cut_flag = True
            show_img(window,cut_img)
        else:
            cv.destroyWindow("ROI")
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
            histr = cv.calcHist([img],[i],None,[256],[0, 256])
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
            img = get_img(cv.COLOR_RGB2HSV)
            menu_color_switch("HSV",menu)
            show_img(window,img,-1)
        if (space == "HSV2RGB"):
            img = get_img(cv.COLOR_HSV2RGB)
            menu_color_switch("RGB",menu)
            show_img(window,img,-1)

        if (space == "BGR2HSV"):
            img = get_img(cv.COLOR_BGR2HSV)
            menu_color_switch("HSV",menu)
            show_img(window,img,-1)
        if (space == "HSV2BGR"):
            img = get_img(cv.COLOR_HSV2BGR)
            menu_color_switch("BGR",menu)
            show_img(window,img,-1)

        if (space == "RGB2GRAY"):
            img = get_img(-1)
            if (messagebox.askokcancel(title="警告", message="灰階化後將無法恢復")):
                menu_color_switch("GRAY",menu)
                show_img(window,img,color_space = cv.COLOR_RGB2GRAY)
        
        if (space == "BGR2GRAY"):
            img = get_img()
            if (messagebox.askokcancel(title="警告", message="灰階化後將無法恢復")):
                menu_color_switch("GRAY",menu)
                show_img(window,img,color_space = cv.COLOR_BGR2GRAY)

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

def rotation_img(window=None,input_img=[],angle=None):
    try:
        #https://stackoverflow.com/questions/43892506/opencv-python-rotate-image-without-cropping-sides
        height, width = input_img.shape[:2]
        # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
        image_center = (width/2, height/2)

        rotation_mart = cv.getRotationMatrix2D(image_center, angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mart[0,0]) 
        abs_sin = abs(rotation_mart[0,1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center and adding the new image center coordinates
        rotation_mart[0, 2] += bound_w/2 - image_center[0]
        rotation_mart[1, 2] += bound_h/2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated_mat = cv.warpAffine(input_img, rotation_mart, (bound_w, bound_h))
        if (window !=None):
            show_img(window,rotated_mat)

    except: messagebox.showwarning("警告","未開啟檔案")

def flip_img(window,input_img =[],angle =0):
    try:
        img = cv.flip(input_img,angle)
        show_img(window,img)
    except: messagebox.showwarning("警告","未開啟檔案")

def translate_img(img,img_w,img_h,x,y,showing=""):
    M = float32([[1,0,x],[0,1,y]])
    af_tran_img = cv.warpAffine(img,M,(img_w,img_h))
    if (showing != ""):
        cv.imshow(showing,af_tran_img)
    else:
        return af_tran_img

def translate_img_window(window):
    try:
        prev_img = get_img()
        img_h,img_w = get_img_size()
        cv.imshow("Translate Preview",prev_img)

        s_h_value = IntVar()
        s_w_value = IntVar()

        translate = Toplevel()
        translate.grab_set()
        translate.title("影像平移")
        scale_h = Scale(translate, orient="horizontal", label="水平位移:"
                       ,length =300, from_= -img_w, to=img_w, variable=s_h_value
                       ,command = lambda x =None: translate_img(prev_img,img_w,img_h,s_h_value.get(),s_w_value.get(),"Translate Preview"))
        scale_h.pack()
        
        scale_w = Scale(translate, orient="horizontal", label="垂直位移:"
                       ,length =300, from_= -img_h, to=img_h, variable=s_w_value
                       ,command = lambda x =None: translate_img(prev_img,img_w,img_h,s_h_value.get(),s_w_value.get(),"Translate Preview"))
        scale_w.pack()
        Button(translate, text = "確認"
        ,command = lambda :[translate.destroy(),cv.destroyWindow("Translate Preview")
        ,show_img(window,translate_img(prev_img,img_w,img_h,s_h_value.get(),s_w_value.get(),""))]).pack(side=LEFT,ipadx=20, padx=40)
        Button(translate, text = "取消",command = lambda :[translate.destroy()
        ,cv.destroyWindow("Translate Preview")]).pack(side=RIGHT,ipadx=20, padx=40)

    except:
        messagebox.showwarning("警告","未開啟檔案")

def affine_trans(img,warp_arg1=0,warp_arg2=1,warp_arg3=1,warp_arg4=0,warp_arg5=1,warp_arg6=0
                ,angle=360,scale=0.0,x=0,y=0,showing=""):

    img_h,img_w = get_img_size()
    #get three points of the image to derive the affine transform relation
    srcTri = array( [[0, 0], [img_w - 1, 0], [0, img_h - 1]] ).astype(float32)
    #affine point
    dstTri = array( [[img_h*warp_arg1, img_w*warp_arg2],
                     [img_w*warp_arg3, img_h*warp_arg4], 
                     [img_w*warp_arg5, img_h*warp_arg6]] ).astype(float32)
    warp_mat = cv.getAffineTransform(srcTri, dstTri)
    
    #warpAffine(input image,output image,output size)
    warp_dst = cv.warpAffine(img, warp_mat, (img_w, img_h))

    center = (img_w//2, img_h//2)
    rot_mat = cv.getRotationMatrix2D( center, angle, scale )
    warp_rotate_dst = cv.warpAffine(warp_dst, rot_mat, (img_w, img_h))

    M = float32([[1,0,x],[0,1,y]])
    warp_rotate_dst = cv.warpAffine(warp_rotate_dst,M,(img_w,img_h))
    
    if (showing != ""):
        cv.imshow(showing,warp_rotate_dst)
    else:
        return warp_rotate_dst

def affine_trans_win(window):
    try:
        global affine_img
        affine_img = get_img()
        cv.imshow("Affine Translate Preview",affine_img)

        s_h_value = IntVar()
        s_w_value = IntVar()
        s_rotation_value = IntVar()
        s_scaling_value = DoubleVar()
        s_warp_value1 = DoubleVar()
        s_warp_value2 = DoubleVar()
        s_warp_value3 = DoubleVar()
        s_warp_value4 = DoubleVar()
        s_warp_value5 = DoubleVar()
        s_warp_value6 = DoubleVar()

        affine = Toplevel()
        affine.grab_set()
        affine.title("仿射變換")
        scale_warp1 = Scale(affine, orient="horizontal", label="剪切1:"
                       ,length =300, from_= 0, to=1,resolution =0.05 , variable=s_warp_value1
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_warp1.pack()

        scale_warp2 = Scale(affine, orient="horizontal", label="剪切2:"
                       ,length =300, from_= 0, to=1,resolution =0.05 , variable=s_warp_value2
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_warp2.pack()

        scale_warp3 = Scale(affine, orient="horizontal", label="剪切3:"
                       ,length =300, from_= 0, to=1,resolution =0.05 , variable=s_warp_value3
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_warp3.pack()

        scale_warp4 = Scale(affine, orient="horizontal", label="剪切4:"
                       ,length =300, from_= 0, to=1,resolution =0.05 , variable=s_warp_value4
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_warp4.pack()

        scale_warp5 = Scale(affine, orient="horizontal", label="剪切5:"
                       ,length =300, from_= 0, to=1,resolution =0.05 ,variable=s_warp_value5
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_warp5.pack()

        scale_warp6 = Scale(affine, orient="horizontal", label="剪切6:"
                       ,length =300, from_= 0, to=1,resolution =0.05 , variable=s_warp_value6
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_warp6.pack()

        scale_rotation = Scale(affine, orient="horizontal", label="旋轉角度:"
                       ,length =300, from_= 0, to=360,resolution =1 , variable=s_rotation_value
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_rotation.pack()

        scale_scaling = Scale(affine, orient="horizontal", label="縮放倍率:"
                       ,length =300, from_= 0, to=1,resolution =0.05 , variable=s_scaling_value
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_scaling.pack()

        scale_h = Scale(affine, orient="horizontal", label="垂直位移:"
                       ,length =300, from_= -get_img_size()[1], to=get_img_size()[1], variable=s_h_value
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_h.pack()
        
        scale_w = Scale(affine, orient="horizontal", label="水平位移:"
                       ,length =300, from_= -get_img_size()[0], to=get_img_size()[0], variable=s_w_value
                       ,command = lambda x =None: affine_trans(affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get(),"Affine Translate Preview"))
        scale_w.pack()

        Button(affine, text = "確認"
        ,command = lambda :[affine.destroy(),cv.destroyWindow("Affine Translate Preview"),show_img(window,affine_trans(
                        affine_img,s_warp_value1.get(),s_warp_value2.get(),s_warp_value3.get()
                       ,s_warp_value4.get(),s_warp_value5.get(),s_warp_value6.get()
                       ,s_rotation_value.get(),s_scaling_value.get(),s_w_value.get(),s_h_value.get()))]).pack(side=LEFT,ipadx=20, padx=40)
        Button(affine, text = "取消",command = lambda :[affine.destroy(),cv.destroyWindow("Affine Translate Preview")]).pack(side=RIGHT,ipadx=20, padx=40)

    except:
        messagebox.showwarning("警告","未開啟檔案")

def get_points(event,x,y,flag,param):
    if (event == cv.EVENT_LBUTTONDBLCLK and len(pts)<4):
        pts.append((x,y))
        cv.imshow("Perspective",cv.circle(pers_img, (x,y), radius=3, color=(0, 0, 255), thickness=-1))

def perspective_trans(window):
    global pts
    global pers_img
    pts = []
    pers_img = get_img()
    cv.imshow("Perspective",pers_img)
    cv.setMouseCallback("Perspective",get_points)
    while(1):
        if (cv.waitKey(13) == 13):
            cv.destroyWindow("Perspective")
            if (len(pts)>=4):
                pts1 = float32([[pts[0][0],pts[0][1]],[pts[1][0],pts[1][1]],[pts[2][0],pts[2][1]],[pts[3][0],pts[3][1]]])
                pts2 = float32([[0,0],[300,0],[0,300],[300,300]])
                M = cv.getPerspectiveTransform(pts1,pts2)
                dst = cv.warpPerspective(get_img(),M,(300,300))
                show_img(window,dst)
            break
        

