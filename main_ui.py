import tkinter as tk
from file import *
from image_edit import *
from Image_Processing import *

window = tk.Tk() #main window
toolbar = tk.Menu(window) 
window.config(menu=toolbar) #fix menu on window

file_menu = tk.Menu(toolbar,tearoff=False)
file_menu.add_command(label= "開啟檔案",command = lambda: read_file(window,color_space_option))
file_menu.add_command(label= "儲存檔案",command = save_file)
file_menu.add_separator()
file_menu.add_command(label = "離開", command = window.destroy)

image_edit = tk.Menu(toolbar,tearoff=False)
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
image_processing.add_command(label= "影像二值化",command = lambda: setting_threshold_window(window))
image_processing.add_command(label= "直方圖等化",command = lambda: img_equalizeHist(window,color_space_option))

toolbar.add_cascade(label= "檔案", menu= file_menu)
toolbar.add_cascade(label= "設定", menu= image_edit)
toolbar.add_cascade(label= "影像處理", menu= image_processing)

window.title('影像處理')
window.geometry('%dx%d+%d+%d' % (700,700,0,0))

window.mainloop()