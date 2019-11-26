from tkinter import Tk, W, E, IntVar
from tkinter.ttk import Label, Checkbutton, Progressbar, Button
from tkinter import messagebox as mb
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image, ImageDraw
import os
import time
from get_source import get_source_data 

def meth():
    for img in input_images_array:
        print(get_source_data(cwd + "/test_images/" + img))
        time.sleep(1)
    print(input_images_array)


def is_image(img):
    """Returns True if the given images ends with a common image suffix such as .png or .jpg\n
    otherwise False"""
    if img.endswith(".png"):
        return True
    if img.endswith(".jpg"):
        return True
    if img.endswith(".jpeg"):
        return True
    if img.endswith(".jfif"):
        return True
    return False

def init_window():
    global input_images_array
    sourcery_lbl.grid(column=0, row=0, columnspan=2, sticky=W, padx=15)
    method_name_or_text_here_btn.grid(column=0, row=2, sticky=W, padx=15)

    input_images_array = os.listdir(cwd + "/test_images")
    for img in input_images_array:
        if (not is_image(img)):
            input_images_array.remove(img)

if __name__ == '__main__':
    #freeze_support()

    cwd = os.getcwd()
    window = Tk()
    window.title("Sourcery")
    window.update_idletasks()
    window.state('zoomed')
    height = window.winfo_screenheight()
    width = window.winfo_screenwidth()
    window.geometry(str(width) + 'x' + str(height))
    #dateS =  time.strftime("20%y-%m-%d")

    # widgets for start screen
    sourcery_lbl = Label(window, text="Sourcery", font=("Arial Bold", 50))
    method_name_or_text_here_btn = Button(window, text="Do stuff", command=meth)

    # global arrays
    input_images_array = []

    init_window()
    window.mainloop()