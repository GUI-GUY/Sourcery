from tkinter import Tk, W, E, IntVar
from tkinter.ttk import Label, Checkbutton, Progressbar, Button, Style, Frame, Notebook, Entry
from tkinter import messagebox as mb
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image, ImageDraw
import os
import time
import shutil
from file_operations import init_directories, read_theme, is_image, read_credentials
from saucenao_caller import get_response, decode_response
from pixiv_handler import pixiv_authenticate, pixiv_login, pixiv_download
#from upload_file import get_url
#from get_source import get_source_data 

def magic():
    # For every input image a request goes out to saucenao and gets decoded (and printed, currently)
    for img in input_images_array:
        shutil.copy(cwd + '/Input/' + img, cwd + '/Sourcery/sourced_original')
        res = get_response(img, cwd, saucenao_key)
        if res[0] == 403:
            # stop()
            mb.showerror('ERROR', res[1])
        elif res[0] == 2:
            # stop()
            mb.showerror('ERROR', res[1] + '\nSauceNao servers are overloaded\nor you are out of searches.\nTry again tomorrow.')
        elif res[0] == 600:
            # stop()
            mb.showerror('ERROR', res[1] + '\nSauceNao gave a response but there was a problem on their end')
        elif res[0] == 41:
            mb.showerror('ERROR', res[1])
        elif res[0] == 402:
            mb.showerror('ERROR', res[1])
        elif res[0] == 200:
            #pixiv_authenticate()
            decode_response(res[1])

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

    input_images_array = os.listdir(cwd + "/Input")
    for img in input_images_array:
        if (not is_image(img)):
            input_images_array.remove(img)
    images_in_input_count_lbl.configure(text=str(len(input_images_array)))
    
    if stay:
        window.after(250, init_window)
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

    pixiv_login_lbl.place_forget()
    pixiv_user_lbl.place_forget()
    pixiv_user_filled_lbl.place_forget()
    pixiv_user_entry.place_forget()
    pixiv_password_lbl.place_forget()
    pixiv_password_filled_lbl.place_forget()
    pixiv_password_entry.place_forget()
    pixiv_login_change_btn.place_forget()
    pixiv_login_confirm_btn.place_forget()

    saucenao_key_number_lbl.place_forget()
    saucenao_key_lbl.place_forget()
    saucenao_key_entry.place_forget()
    saucenao_key_change_btn.place_forget()
    saucenao_key_confirm_btn.place_forget()
    
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

    options_back_btn.place(x = 50, y = 500)

def display_sourcery_options():
    forget_all_widgets()
    display_basic_options()
    
    

def display_provider_options():
    forget_all_widgets()
    display_basic_options()

    pixiv_login_lbl.place(x = 50, y = 100)
    pixiv_user_lbl.place(x = 50, y = 130)
    pixiv_user_filled_lbl.place(x = 120, y = 130)
    pixiv_password_lbl.place(x = 50, y = 160)
    pixiv_password_filled_lbl.place(x = 120, y = 160)
    pixiv_login_change_btn.place(x = 50, y = 190)
    

def display_saucenao_options():
    forget_all_widgets()
    display_basic_options()
    saucenao_key_lbl.place(x = 50, y = 100)
    saucenao_key_number_lbl.place(x = 150, y = 100)
    saucenao_key_change_btn.place(x = 550, y = 100)
    
def pixiv_change_login():
    pixiv_user_filled_lbl.place_forget()
    pixiv_password_filled_lbl.place_forget()
    pixiv_login_change_btn.place_forget()
    pixiv_user_entry.place(x = 120, y = 130)
    pixiv_password_entry.place(x = 120, y = 160)
    pixiv_login_confirm_btn.place(x = 50, y = 190)
    pixiv_user_entry.delete(0, len(pixiv_username))
    pixiv_password_entry.delete(0, len(pixiv_password))
    pixiv_user_entry.insert(0, pixiv_username)
    pixiv_password_entry.insert(0, pixiv_password)

def pixiv_set_login():
    global pixiv_username
    global pixiv_password
    pixiv_user_entry.place_forget()
    pixiv_password_entry.place_forget()
    pixiv_login_confirm_btn.place_forget()
    pixiv_user_filled_lbl.place(x = 120, y = 130)
    pixiv_password_filled_lbl.place(x = 120, y = 160)
    pixiv_login_change_btn.place(x = 50, y = 190)
    pixiv_username = pixiv_user_entry.get()
    pixiv_password = pixiv_password_entry.get()
    pixiv_user_filled_lbl.configure(text=pixiv_username)
    pixiv_password_filled_lbl.configure(text=pixiv_password)

def saucenao_change_key():
    saucenao_key_change_btn.place_forget()
    saucenao_key_number_lbl.place_forget()
    saucenao_key_confirm_btn.place(x = 550, y = 100)
    saucenao_key_entry.place(x = 150, y = 100)
    saucenao_key_entry.delete(0, len(saucenao_key))
    saucenao_key_entry.insert(0, saucenao_key)
    


def saucenao_set_key():
    global saucenao_key
    saucenao_key = saucenao_key_entry.get()
    saucenao_key_confirm_btn.place_forget()
    saucenao_key_entry.place_forget()
    saucenao_key_change_btn.place(x = 550, y = 100)
    saucenao_key_number_lbl.configure(text=saucenao_key)
    saucenao_key_number_lbl.place(x = 150, y = 100)

    

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

    method_name_or_text_here_btn = Button(window, text="Do the magic", command=magic, style="button.TLabel")
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

    credentials_array = read_credentials(cwd)
    pixiv_username = credentials_array[1]
    pixiv_password = credentials_array[2]
    pixiv_login_lbl = Label(window, text="Pixiv Login", style="label.TLabel")
    pixiv_user_lbl = Label(window, text="Username", style="label.TLabel")
    pixiv_user_filled_lbl = Label(window, width=50, text=pixiv_username, style="button.TLabel")
    pixiv_user_entry = Entry(window, width=52, style="button.TLabel")
    pixiv_password_lbl = Label(window, text="Password", style="label.TLabel")
    pixiv_password_filled_lbl = Label(window, width=50, text=pixiv_password, style="button.TLabel")
    pixiv_password_entry = Entry(window, width=52, style="button.TLabel")
    pixiv_login_change_btn = Button(window, text="Change", command=pixiv_change_login, style="button.TLabel")
    pixiv_login_confirm_btn = Button(window, text="Confirm", command=pixiv_set_login, style="button.TLabel")

    saucenao_key = credentials_array[0]
    saucenao_key_lbl = Label(window, text="SauceNao API-Key", style="label.TLabel")
    saucenao_key_number_lbl = Label(window, width=50, text=saucenao_key, style="button.TLabel")
    saucenao_key_entry = Entry(window, width=52, style="button.TLabel")
    saucenao_key_change_btn = Button(window, text="Change", command=saucenao_change_key, style="button.TLabel")
    saucenao_key_confirm_btn = Button(window, text="Confirm", command=saucenao_set_key, style="button.TLabel")

    options_back_btn = Button(window, text="Back", command=init_window, style="button.TLabel")

    # global arrays
    input_images_array = []

    stay = True
    init_directories(cwd)
    init_window()
    window.mainloop()