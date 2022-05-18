import tkinter as tk
from file import *
from image_edit import *
from Image_Processing import *
from edge_detection import *

window = tk.Tk() #main window
toolbar = tk.Menu(window) 
window.config(menu=toolbar) #fix menu on window

file_menu = tk.Menu(toolbar,tearoff=False)
file_menu.add_command(label= "開啟檔案",command = lambda: read_file(window,color_space_option))
file_menu.add_command(label= "儲存檔案",command = save_file)
file_menu.add_command(label= "檔案資訊",command = image_info)
file_menu.add_separator()
file_menu.add_command(label = "離開", command = window.destroy)

image_edit = tk.Menu(toolbar,tearoff=False)
image_edit.add_command(label="向左旋轉90度",command = lambda: rotation_img(window,get_img(),90))
image_edit.add_command(label="向右旋轉90度",command = lambda: rotation_img(window,get_img(),-90))
image_edit.add_command(label="垂直翻轉",command = lambda: flip_img(window,get_img(),0))
image_edit.add_command(label="水平翻轉",command = lambda: flip_img(window,get_img(),1))
image_edit.add_separator()
image_edit.add_command(label="平移",command = lambda: translate_img_window(window))
image_edit.add_command(label="仿射轉換",command= lambda: affine_trans_win(window))
image_edit.add_command(label="透視",command= lambda:perspective_trans(window))
image_edit.add_separator()
image_edit.add_command(label= "設定ROI",command = lambda: ROI(window))
image_edit.add_command(label= "顯示影像直方圖",command = hist)

color_space_option = tk.Menu(image_edit, tearoff=False)
color_space_option.add_command(label="目前色彩空間 : RGB",state="disable")
color_space_option.add_command(label="RGB to BGR",command = lambda: change_color_space(window,"RGB2BGR",color_space_option))
color_space_option.add_command(label="BGR to RGB",command = lambda: change_color_space(window,"BGR2RGB",color_space_option),state="disable")
color_space_option.add_command(label="RGB to HSV",command = lambda: change_color_space(window,"RGB2HSV",color_space_option))
color_space_option.add_command(label="BGR to HSV",command = lambda: change_color_space(window,"BGR2HSV",color_space_option),state="disable")
color_space_option.add_command(label="HSV to RGB",command = lambda: change_color_space(window,"HSV2RGB",color_space_option),state="disable")
color_space_option.add_command(label="HSV to BGR",command = lambda: change_color_space(window,"HSV2BGR",color_space_option),state="disable")
color_space_option.add_command(label="RGB to GRAY",command = lambda: change_color_space(window,"RGB2GRAY",color_space_option))
color_space_option.add_command(label="BGR to GRAY",command = lambda: change_color_space(window,"BGR2GRAY",color_space_option),state="disable")
image_edit.add_cascade(label="顯示或改變色彩空間" ,menu=color_space_option)

image_processing = tk.Menu(toolbar,tearoff=False)
image_processing.add_command(label= "影像二值化",command = lambda: setting_threshold_window(window,color_space_option))
image_processing.add_command(label= "直方圖等化",command = lambda: img_equalizeHist(window,color_space_option))

filter = tk.Menu(image_edit, tearoff=False)
filter.add_command(label="平均濾波器",command = lambda: img_filter(window,"averaging"))
filter.add_command(label="高斯模糊",command = lambda: img_filter(window,"gaussian_blur"))
filter.add_command(label="中值濾波",command = lambda: img_filter(window,"median_blur"))
filter.add_separator()
filter.add_command(label="浮雕濾波器",command = lambda: img_filter(window,"emboss"))
image_processing.add_cascade(label="濾波器" ,menu=filter)
image_processing.add_separator()
image_processing.add_command(label= "侵蝕",command = lambda: Erosion_img(window))
image_processing.add_command(label= "膨脹",command = lambda: Dilation_img(window))
image_processing.add_command(label= "開運算",command = lambda: MOR_OPEN(window))
image_processing.add_command(label= "閉運算",command = lambda: MOR_CLOSE(window))



edge_detection = tk.Menu(toolbar,tearoff=False)
edge_detection.add_command(label="Canny邊緣偵測",command = lambda: Canny_Value_Set(window,color_space_option))
edge_detection.add_command(label="Sobel濾波器",command = lambda: Sobel_edge_detection(window,color_space_option))

toolbar.add_cascade(label= "檔案", menu= file_menu)
toolbar.add_cascade(label= "設定", menu= image_edit)
toolbar.add_cascade(label= "影像處理", menu= image_processing)
toolbar.add_cascade(label= "邊緣偵測", menu= edge_detection)

window.title('影像處理')
window.geometry('%dx%d+%d+%d' % (700,700,0,0))

window.mainloop()