from tkinter import Tk, W, E, IntVar
from tkinter.ttk import Label, Checkbutton, Progressbar, Button, Style, Frame, Notebook
from tkinter import messagebox as mb
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image, ImageDraw
import os
import time
from file_operations import init_directories, read_theme, is_image

from upload_file import get_url
#from get_source import get_source_data 

def meth():
    return
    for img in input_images_array:
        #print(get_source_data(cwd + "/test_images/" + img))
        url = get_url(cwd, img)
        time.sleep(1)
    print(input_images_array)

def init_window():
    global input_images_array
    forget_all_widgets()

    sourcery_lbl.place(x = 20, y = 10)
    images_in_input_lbl.place(x = 200, y = 100)
    images_in_input_count_lbl.place(x = 200, y = 120)
    currently_sourcing_lbl.place(x = 200, y = 140)
    currently_sourcing_img_lbl.place(x = 200, y = 160)
    saucenao_requests_count_lbl.place(x = 200, y = 180)
    elapsed_time_lbl.place(x = 200, y = 200)
    eta_lbl.place(x = 200, y = 220)

    method_name_or_text_here_btn.place(x = 20, y = 100)
    open_input_btn.place(x = 20, y = 120)
    open_sourced_btn.place(x = 20, y = 140)
    statistics_btn.place(x = 20, y = 160)
    options_btn.place(x = 20, y = 180)
    do_sourcery_btn.place(x = 20, y = 200)
    stop_btn.place(x = 20, y = 220)
    view_results_btn.place(x = 20, y = 240)

    input_images_array = os.listdir(cwd + "/test_images")
    for img in input_images_array:
        if (not is_image(img)):
            input_images_array.remove(img)
    images_in_input_count_lbl.configure(text=str(len(input_images_array)))
    
    if stay:
        window.after(100, init_window)
    else:
        display_sourcery_options()

def forget_all_widgets():
    sourcery_lbl.place_forget()
    images_in_input_lbl.place_forget()
    images_in_input_count_lbl.place_forget()
    currently_sourcing_lbl.place_forget()
    currently_sourcing_img_lbl.place_forget()
    saucenao_requests_count_lbl.place_forget()
    elapsed_time_lbl.place_forget()
    eta_lbl.place_forget()

    method_name_or_text_here_btn.place_forget()
    open_input_btn.place_forget()
    open_sourced_btn.place_forget()
    statistics_btn.place_forget()
    options_btn.place_forget()
    do_sourcery_btn.place_forget()
    stop_btn.place_forget()
    view_results_btn.place_forget()

    options_lbl.place_forget()

    provider_options_btn.place_forget()
    saucenao_options_btn.place_forget()
    sourcery_options_btn.place_forget()
    options_back_btn.place_forget()

def open_input():
    try:
        os.startfile(cwd + "/Input")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def open_sourced():
    try:
        os.startfile(cwd + "/Sourced")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def display_statistics():
    pass

def set_options():
    global stay
    stay = False

def display_basic_options():
    global stay
    stay = True
    options_lbl.place(x = 50, y = 10)

    sourcery_options_btn.place(x = 50, y = 50)
    provider_options_btn.place(x = 150, y = 50)
    saucenao_options_btn.place(x = 250, y = 50)

def display_sourcery_options():
    forget_all_widgets()
    display_basic_options()
    
    options_back_btn.place(x = 50, y = 150)

def display_provider_options():
    forget_all_widgets()
    display_basic_options()

    
    options_back_btn.place(x = 50, y = 150)

def display_saucenao_options():
    forget_all_widgets()
    display_basic_options()

    
    options_back_btn.place(x = 50, y = 150)

def do_sourcery():
    pass

def stop():
    pass

def display_view_results():
    pass

def enforce_style():
    colour_array = read_theme(cwd)
    window.configure(bg=colour_array[0])
    style = Style()
    style.configure("label.TLabel", foreground=colour_array[1], background=colour_array[0], font=("Arial Bold", 10))
    style.configure("button.TLabel", foreground=colour_array[1], background=colour_array[2], font=("Arial Bold", 10))
    style.map("button.TLabel",
        foreground=[('pressed', colour_array[6]), ('active', colour_array[4])],
        background=[('pressed', '!disabled', colour_array[5]), ('active', colour_array[3])]
    )

if __name__ == '__main__':
    #freeze_support()

    cwd = os.getcwd()
    window = Tk()
    window.title("Sourcery")
    window.update_idletasks()
    #window.state('zoomed')
    height = window.winfo_screenheight()
    width = window.winfo_screenwidth()
    window.geometry(str(width-500) + 'x' + str(height-500))
    #dateS =  time.strftime("20%y-%m-%d")

    # set style
    enforce_style()

    # widgets for start screen
    sourcery_lbl = Label(window, text="Sourcery", font=("Arial Bold", 50), style="label.TLabel")
    images_in_input_lbl = Label(window, text="Images in input", style="label.TLabel")
    images_in_input_count_lbl = Label(window, text="Number here", style="label.TLabel")
    currently_sourcing_lbl = Label(window, text="Currently Sourcing:", style="label.TLabel")
    currently_sourcing_img_lbl = Label(window, text="Image name here", style="label.TLabel")
    saucenao_requests_count_lbl = Label(window, text="Number here/200", style="label.TLabel")
    elapsed_time_lbl = Label(window, text="Elapsed time:", style="label.TLabel")
    eta_lbl = Label(window, text="ETA:", style="label.TLabel")

    method_name_or_text_here_btn = Button(window, text="Do the magic", command=meth, style="button.TLabel")
    open_input_btn = Button(window, text="Open Input", command=open_input, style="button.TLabel")
    open_sourced_btn = Button(window, text="Open Sourced", command=open_sourced, style="button.TLabel")
    statistics_btn = Button(window, text="Statistics", command=display_statistics, style="button.TLabel")
    options_btn = Button(window, text="Options", command=set_options, style="button.TLabel")
    do_sourcery_btn = Button(window, text="Do Sourcery", command=do_sourcery, style="button.TLabel")
    stop_btn = Button(window, text="Stop", command=stop, style="button.TLabel")
    view_results_btn = Button(window, text="View Results", command=display_view_results, style="button.TLabel")

    # widgets for options
    options_lbl = Label(window, text="Options", font=("Arial Bold", 20), style="label.TLabel")

    provider_options_btn = Button(window, text="Provider", command=display_provider_options, style="button.TLabel")
    saucenao_options_btn = Button(window, text="SauceNao", command=display_saucenao_options, style="button.TLabel")
    sourcery_options_btn = Button(window, text="Sourcery", command=display_sourcery_options, style="button.TLabel")

    

    options_back_btn = Button(window, text="Back", command=init_window, style="button.TLabel")

    # global arrays
    input_images_array = []

    stay = True
    init_directories(cwd)
    init_window()
    window.mainloop()