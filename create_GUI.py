from tkinter import Tk, IntVar, Canvas, Scrollbar
from tkinter.ttk import Label, Checkbutton, Button, Style, Frame, Notebook, Entry, Frame
from tkinter import messagebox as mb
#from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image
from os import getcwd, listdir, startfile
#import time
from shutil import copy
from file_operations import init_directories, read_theme, is_image, read_credentials, write_credentials, write_theme
from saucenao_caller import get_response, decode_response
from pixiv_handler import pixiv_authenticate, pixiv_login, pixiv_download
#from upload_file import get_url
#from get_source import get_source_data 

def do_sourcery():
    # For every input image a request goes out to saucenao and gets decoded (and printed, currently)
    for img in input_images_array:
        copy(cwd + '/Input/' + img, cwd + '/Sourcery/sourced_original')
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
            #pixiv_authenticate(pixiv_username, pixiv_password, credentials_array)
            decode_response(res[1])

def init_window():
    global input_images_array
    forget_all_widgets()
    y = 100
    c = 23
    sourcery_lbl.place(x = 20, y = 10)
    images_in_input_lbl.place(x = 200, y = y)
    images_in_input_count_lbl.place(x = 350, y = y)
    currently_sourcing_lbl.place(x = 200, y = y + c * 2)
    currently_sourcing_img_lbl.place(x = 350, y = y + c * 2)
    saucenao_requests_count_lbl.place(x = 350, y = y + c * 3)
    elapsed_time_lbl.place(x = 200, y = y + c * 4)
    eta_lbl.place(x = 200, y = y + c * 5)

    
    open_input_btn.place(x = 20, y = y + c * 0)
    open_sourced_btn.place(x = 20, y = y + c * 1)
    statistics_btn.place(x = 20, y = y + c * 2)
    options_btn.place(x = 20, y = y + c * 3)
    do_sourcery_btn.place(x = 380, y = 100)
    stop_btn.place(x = 200, y = y + c * 6)
    view_results_btn.place(x = 350, y = y + c * 6)

    input_images_array = listdir(cwd + "/Input")
    for img in input_images_array:
        if (not is_image(img)):
            input_images_array.remove(img)
    images_in_input_count_lbl.configure(text=str(len(input_images_array)))
    
    if esc_op:
        display_sourcery_options()
    elif esc_res:
        display_view_results()
    else:
        window.after(250, init_window)

def forget_all_widgets():
    sourcery_lbl.place_forget()
    images_in_input_lbl.place_forget()
    images_in_input_count_lbl.place_forget()
    currently_sourcing_lbl.place_forget()
    currently_sourcing_img_lbl.place_forget()
    saucenao_requests_count_lbl.place_forget()
    elapsed_time_lbl.place_forget()
    eta_lbl.place_forget()

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

    theme_lbl.place_forget()
    dark_theme_btn.place_forget()
    light_theme_btn .place_forget()
    custom_theme_btn.place_forget()
    custom_background_lbl.place_forget()
    custom_foreground_lbl.place_forget()
    custom_button_background_lbl.place_forget()
    custom_button_background_active_lbl.place_forget()
    custom_button_foreground_active_lbl.place_forget()
    custom_button_background_pressed_lbl.place_forget()
    custom_button_foreground_pressed_lbl.place_forget()
    custom_background_entry.place_forget()
    custom_foreground_entry.place_forget()
    custom_button_background_entry.place_forget()
    custom_button_background_active_entry.place_forget()
    custom_button_foreground_active_entry.place_forget()
    custom_button_background_pressed_entry.place_forget()
    custom_button_foreground_pressed_entry.place_forget()
    save_custom_theme_btn.place_forget()
    
    options_back_btn.place_forget()

    results_lbl.place_forget()
    results_frame.place_forget()

def open_input():
    try:
        startfile(cwd + "/Input")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def open_sourced():
    try:
        startfile(cwd + "/Sourced")
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def display_statistics():
    pass

def escape_options():
    global esc_op
    esc_op = True

def escape_results():
    global esc_res
    esc_res = True

def display_basic_options():
    global esc_op
    esc_op = False
    options_lbl.place(x = 50, y = 10)

    sourcery_options_btn.place(x = 50, y = 50)
    provider_options_btn.place(x = 150, y = 50)
    saucenao_options_btn.place(x = 250, y = 50)

    options_back_btn.place(x = 50, y = 500)

def display_sourcery_options():
    forget_all_widgets()
    display_basic_options()
    y = 100
    c = 23
    x1 = 50
    x2 = 240
    theme_lbl.place(x = x1, y = y)
    dark_theme_btn.place(x = x1, y = y + c * 1)
    light_theme_btn .place(x = x1, y = y + c * 2)
    custom_theme_btn.place(x = x1, y = y + c * 3)
    custom_background_lbl.place(x = x1, y = y + c * 4)
    custom_foreground_lbl.place(x = x1, y = y + c * 5)
    custom_button_background_lbl.place(x = x1, y = y + c * 6)
    custom_button_background_active_lbl.place(x = x1, y = y + c * 7)
    custom_button_foreground_active_lbl.place(x = x1, y = y + c * 8)
    custom_button_background_pressed_lbl.place(x = x1, y = y + c * 9)
    custom_button_foreground_pressed_lbl.place(x = x1, y = y + c * 10)
    custom_background_entry.place(x = x2, y = y + c * 4)
    custom_foreground_entry.place(x = x2, y = y + c * 5)
    custom_button_background_entry.place(x = x2, y = y + c * 6)
    custom_button_background_active_entry.place(x = x2, y = y + c * 7)
    custom_button_foreground_active_entry.place(x = x2, y = y + c * 8)
    custom_button_background_pressed_entry.place(x = x2, y = y + c * 9)
    custom_button_foreground_pressed_entry.place(x = x2, y = y + c * 10)
    save_custom_theme_btn.place(x = x1, y = y + c * 11)

def change_to_dark_theme():
    write_theme(cwd, "Dark Theme", custom_array)
    enforce_style()

def change_to_light_theme():
    write_theme(cwd, "Light Theme", custom_array)
    enforce_style()

def change_to_custom_theme():
    write_theme(cwd, "Custom Theme", custom_array)
    enforce_style()

def save_custom_theme():
    global custom_array
    custom_array[0] = custom_background_entry.get()
    custom_array[1] = custom_foreground_entry.get()
    custom_array[2] = custom_button_background_entry.get()
    custom_array[3] = custom_button_background_active_entry.get()
    custom_array[4] = custom_button_foreground_active_entry.get()
    custom_array[5] = custom_button_background_pressed_entry.get()
    custom_array[6] = custom_button_foreground_pressed_entry.get()

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
    credentials_array[1] = pixiv_username
    credentials_array[2] = pixiv_password
    write_credentials(cwd, credentials_array)

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
    credentials_array[0] = saucenao_key
    write_credentials(cwd, credentials_array)
    saucenao_key_confirm_btn.place_forget()
    saucenao_key_entry.place_forget()
    saucenao_key_change_btn.place(x = 550, y = 100)
    saucenao_key_number_lbl.configure(text=saucenao_key)
    saucenao_key_number_lbl.place(x = 150, y = 100)

def stop():
    pass

def display_view_results():
    global esc_res
    esc_res = False
    forget_all_widgets()
    results_lbl.place(x = 50, y = 20)
    options_back_btn.place(x = 50, y = 500)
    results_frame.place(x = 50, y = 100)
    
    

    
    # pixiv_dir_array = listdir(cwd + '/Sourcery/sourced_progress/pixiv')
    # pixiv_images = []
    # for img in pixiv_dir_array:
    #     try:
    #         pixiv_images.append(Image.open(cwd + '/Sourcery/sourced_original/' + img)), (Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + img))
    #     except Exception as e:
    #         print(e)
    #         mb.showerror("ERROR", e)

    # for tup in pixiv_images:
    #     tup[0] = tup[0].thumbnail()
    #     tup[1] = tup[1].thumbnail()

    # for t in range(0,len(txtversions)):
    #     photoImages[t] = ImageTk.PhotoImage(images[t])
    #     imgpanels[t].configure(image = photoImages[t])
    #     imgpanels[t].grid(column=t+3 , row=2)

def myfunction(event):
    results_canvas.configure(scrollregion=results_canvas.bbox("all"),width=200,height=200)


def enforce_style():
    global colour_array, custom_array
    colour_array, custom_array = read_theme(cwd)
    window.configure(bg=colour_array[0])
    style = Style()
    style.configure("label.TLabel", foreground=colour_array[1], background=colour_array[0], font=("Arial Bold", 10))
    style.configure("button.TLabel", foreground=colour_array[1], background=colour_array[2], font=("Arial Bold", 10))
    style.map("button.TLabel",
        foreground=[('pressed', colour_array[6]), ('active', colour_array[4])],
        background=[('pressed', '!disabled', colour_array[5]), ('active', colour_array[3])]
    )
    style.configure("frame.TFrame", foreground=colour_array[1], background=colour_array[0])
    #style.configure("scroll.Vertical.TScrollbar", foreground=colour_array[1], background=colour_array[2], throughcolor=colour_array[2], activebackground=colour_array[2])
    results_canvas.configure(background=colour_array[0])

if __name__ == '__main__':
    #freeze_support()

    cwd = getcwd()
    window = Tk()
    window.title("Sourcery")
    window.update_idletasks()
    #window.state('zoomed')
    height = window.winfo_screenheight()
    width = window.winfo_screenwidth()
    window.geometry(str(width-500) + 'x' + str(height-500))
    #dateS =  time.strftime("20%y-%m-%d")

    # set style
    colour_array = []
    custom_array = []
    results_canvas=Canvas(window)
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

    open_input_btn = Button(window, text="Open Input", command=open_input, style="button.TLabel")
    open_sourced_btn = Button(window, text="Open Sourced", command=open_sourced, style="button.TLabel")
    statistics_btn = Button(window, text="Statistics", command=display_statistics, style="button.TLabel")
    options_btn = Button(window, text="Options", command=escape_options, style="button.TLabel")
    do_sourcery_btn = Button(window, text="Do Sourcery", command=do_sourcery, style="button.TLabel")
    stop_btn = Button(window, text="Stop", command=stop, style="button.TLabel")
    view_results_btn = Button(window, text="View Results", command=escape_results, style="button.TLabel")

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

    theme_lbl = Label(window, text="Theme", font=("Arial Bold", 14), style="label.TLabel")
    dark_theme_btn = Button(window, text="Dark Theme", command=change_to_dark_theme, style="button.TLabel")
    light_theme_btn = Button(window, text="Light Theme", command=change_to_light_theme, style="button.TLabel")
    custom_theme_btn = Button(window, text="Custom Theme", command=change_to_custom_theme, style="button.TLabel")
    custom_background_lbl = Label(window, text="Background", style="label.TLabel")
    custom_foreground_lbl = Label(window, text="Foreground", style="label.TLabel")
    custom_button_background_lbl = Label(window, text="Button Background", style="label.TLabel")
    custom_button_background_active_lbl = Label(window, text="Button Background Active", style="label.TLabel")
    custom_button_foreground_active_lbl = Label(window, text="Button Foreground Active", style="label.TLabel")
    custom_button_background_pressed_lbl = Label(window, text="Button Background Pressed", style="label.TLabel")
    custom_button_foreground_pressed_lbl = Label(window, text="Button Foreground Pressed", style="label.TLabel")
    custom_background_entry = Entry(window, width=30, style="button.TLabel")
    custom_foreground_entry = Entry(window, width=30, style="button.TLabel")
    custom_button_background_entry = Entry(window, width=30, style="button.TLabel")
    custom_button_background_active_entry = Entry(window, width=30, style="button.TLabel")
    custom_button_foreground_active_entry = Entry(window, width=30, style="button.TLabel")
    custom_button_background_pressed_entry = Entry(window, width=30, style="button.TLabel")
    custom_button_foreground_pressed_entry = Entry(window, width=30, style="button.TLabel")
    save_custom_theme_btn = Button(window, text="Save Custom Theme", command=save_custom_theme, style="button.TLabel")

    custom_background_entry.insert(0, custom_array[0])
    custom_foreground_entry.insert(0, custom_array[1])
    custom_button_background_entry.insert(0, custom_array[2])
    custom_button_background_active_entry.insert(0, custom_array[3])
    custom_button_foreground_active_entry.insert(0, custom_array[4])
    custom_button_background_pressed_entry.insert(0, custom_array[5])
    custom_button_foreground_pressed_entry.insert(0, custom_array[6])

    options_back_btn = Button(window, text="Back", command=init_window, style="button.TLabel")

    # widgets for results
    results_lbl = Label(window, text="Results", font=("Arial Bold", 14), style="label.TLabel")

    results_frame=Frame(window, width=1520, height=1520, style="frame.TFrame")
    results_canvas=Canvas(results_frame, width=1520, height=1520, background=colour_array[0], highlightthickness=0)
    frame=Frame(results_canvas, width=1520, height=1520, style="frame.TFrame")
    results_scrollbar=Scrollbar(results_frame, orient="vertical", command=results_canvas.yview)
    results_canvas.configure(yscrollcommand=results_scrollbar.set)

    results_scrollbar.pack(side="right",fill="y")
    results_canvas.pack(side="left")
    results_canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>",myfunction)

#     for i in range(50):
#        Label(frame,text=i, style="label.TLabel").grid(row=i+1,column=0)
#        Label(frame,text="my text"+str(i), style="label.TLabel").grid(row=i,column=1)
#        Label(frame,text=".................1..............2..............3...............4......", style="label.TLabel").grid(row=i,column=2)
    
    # global arrays
    input_images_array = []

    esc_op = False
    esc_res = False
    init_directories(cwd)
    init_window()
    window.mainloop()