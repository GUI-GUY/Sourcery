from tkinter import Tk, IntVar, Canvas, Scrollbar
from tkinter.ttk import Label, Checkbutton, Button, Style, Frame, Notebook, Entry, Frame
from tkinter import messagebox as mb
#from tkinter.filedialog import askdirectory
from functools import partial
from PIL import ImageTk, Image
from os import getcwd, listdir, startfile, path
#import time
from shutil import copy, move
from file_operations import init_directories, read_theme, is_image, read_credentials, write_credentials, write_theme, save
from sourcery import do_sourcery

def magic():
    do_sourcery(cwd, input_images_array, saucenao_key, saucenao_requests_count_lbl, pixiv_username, pixiv_password, credentials_array)

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
    for widget in window.winfo_children():
        widget.place_forget()

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
    enforce_style()

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

# 5.2 Resize images to fit on screen
def resize(image):
    global width
    global height

    oldwidth = image.width
    oldheight = image.height

    if oldwidth > width/3:
        newwidth = round(width/3)
        newheight = round(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    if image.height > height-320:
        newheight = height - 320
        newwidth = round(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    return image

def display_big_selector(index):
    forget_all_widgets()
    big_selector_frame.place(x = round(width/3), y = 73)
    original_image = Image.open(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[index][2] + '.' + pixiv_images_array[index][3])
    original_size = original_image.size
    original_image = resize(original_image)
    original_photoImage = ImageTk.PhotoImage(original_image)

    original_chkbtn = Checkbutton(window, image=original_photoImage, var=chkbtn_vars_array[index][0], style="chkbtn.TCheckbutton")
    original_chkbtn.image = original_photoImage
    original_chkbtn.place(x = 20, y = 73)

    cropped_name_lbl = Label(window, text = pixiv_images_array[index][2], style='label.TLabel')
    original_wxh_lbl = Label(window, text = original_size, style='label.TLabel')
    original_type_lbl = Label(window, text = pixiv_images_array[index][3], style='label.TLabel')
    cropped_name_lbl.place(x = 50, y = 50)
    original_wxh_lbl.place(x = 50, y = 500)
    original_type_lbl.place(x = 50, y = 523)

    if pixiv_images_array[index][9]:
        t = 0
        chkbtn_vars_big_array = []
        for img in pixiv_images_array[index][10]:
            chkbtn_vars_big_array.append(IntVar())
            downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[index][0] + '/' + img)
            downloaded_size = downloaded_image.size # TODO is this runtime or instant assigned in the label?
            downloaded_image = resize(downloaded_image)
            downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)

            dowloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=chkbtn_vars_big_array[int(t/4)], style="chkbtn.TCheckbutton")
            dowloaded_chkbtn.image = downloaded_photoImage
            dowloaded_chkbtn.grid(column = 0, row = t, rowspan = 4)
            downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
            dowloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
            downloaded_type_lbl = Label(frame2, text = img[img.rfind(".")+1:], style='label.TLabel')
            downloaded_lbl.grid(column = 1, row = t + 0)
            dowloaded_wxh_lbl.grid(column = 1, row = t + 1)
            downloaded_type_lbl.grid(column = 1, row = t + 2)
            t += 4
    else:
        downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[index][0])
        downloaded_size = downloaded_image.size
        downloaded_image = resize(downloaded_image)
        downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)

        dowloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=chkbtn_vars_array[index][1], style="chkbtn.TCheckbutton")
        dowloaded_chkbtn.image = downloaded_photoImage
        dowloaded_chkbtn.grid(column = 0, row = 0, rowspan = 4)
        downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
        dowloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
        downloaded_type_lbl = Label(frame2, text = pixiv_images_array[index][0][pixiv_images_array[index][0].rfind(".")+1:], style='label.TLabel')
        downloaded_lbl.grid(column = 1, row = 0)
        dowloaded_wxh_lbl.grid(column = 1, row = 1)
        downloaded_type_lbl.grid(column = 1, row = 2)

def display_view_results():
    global esc_res
    esc_res = False
    forget_all_widgets()
    results_lbl.place(x = 50, y = 20)
    options_back_btn.place(x = 50, y = 500)
    save_and_back_btn.place(x = 150, y = 500)
    save_and_refresh_btn.place(x = 250, y = 500)
    results_frame.place(x = 50, y = 100)

    thumb_size = (70,70)
    pixiv_dir_array = listdir(cwd + '/Sourcery/sourced_progress/pixiv')
    pixiv_sub_dir_array = []
    sourced_original_array = listdir(cwd + '/Sourcery/sourced_original')
    # TODO delete non images
    for t in range(len(sourced_original_array)):
        sourced_original_array[t] = sourced_original_array[t].rpartition('.')
    
    t = 0
    for img in pixiv_dir_array:
        # If input is empty, delete every element
        if len(sourced_original_array) == 0:
            delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
            continue
        flag = False # IsDirectory flag
        pointdex = img.rfind(".")
        if pointdex == -1:
            cropped = img
        else:
            cropped = img[:pointdex] # deletes the suffix
        suffix = ''
        sub = ''
        if path.isfile(cwd + '/Sourcery/sourced_progress/pixiv/' + img):
            for image in sourced_original_array:
                if image[0] == cropped:
                    suffix = image[2]
                    break
            if suffix == '':
                delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                continue
            try:
                original_image = Image.open(cwd + '/Sourcery/sourced_original/' + cropped + '.' + suffix) 
                downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
        elif path.isdir(cwd + '/Sourcery/sourced_progress/pixiv/' + img):
            flag = True
            try:
                pixiv_sub_dir_array = listdir(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                if len(pixiv_sub_dir_array) == 0:
                    delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                    continue
                pathname = ''
                for image in sourced_original_array:
                    if image[0] == img:
                        pathname = cwd + '/Sourcery/sourced_original/' + image[0] + image[1] + image[2]
                        suffix = image[2]
                        break
                if suffix == '':
                    delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                    continue
                sub = pixiv_sub_dir_array[0]
                original_image = Image.open(pathname)
                downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + img + '/' + pixiv_sub_dir_array[0])
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)

        original_size = original_image.size
        downloaded_size = downloaded_image.size

        original_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)
        downloaded_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)

        original_photoImage = ImageTk.PhotoImage(original_image)
        downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)

        original_chkbtn = Checkbutton(frame, image=original_photoImage, var=chkbtn_vars_array[int(t/3)][0], style="chkbtn.TCheckbutton")
        dowloaded_chkbtn = Checkbutton(frame, image=downloaded_photoImage, var=chkbtn_vars_array[int(t/3)][1], style="chkbtn.TCheckbutton")
        original_chkbtn.image = original_photoImage
        dowloaded_chkbtn.image = downloaded_photoImage
        original_chkbtn.grid(column = 0, row = t+1)
        dowloaded_chkbtn.grid(column = 0, row = t+2)
        cropped_name_lbl = Label(frame, text = cropped, style='label.TLabel')
        original_lbl = Label(frame, text = "original", style='label.TLabel')
        original_wxh_lbl = Label(frame, text = str(original_size), style='label.TLabel')
        original_type_lbl = Label(frame, text = suffix, style='label.TLabel')
        downloaded_lbl = Label(frame, text = "pixiv", style='label.TLabel')
        cropped_name_lbl.grid(column = 1, row = t, columnspan=3)
        original_lbl.grid(column = 2, row = t+1)
        original_wxh_lbl.grid(column = 3, row = t+1)
        original_type_lbl.grid(column = 4, row = t+1)
        downloaded_lbl.grid(column = 2, row = t+2)
        if flag:
            downloaded_wxh_lbl = Label(frame, text = "More images", style='label.TLabel')
            downloaded_type_lbl = Label(frame, text = "More images", style='label.TLabel')
        else:
            downloaded_wxh_lbl = Label(frame, text = str(downloaded_size), style='label.TLabel')
            downloaded_type_lbl = Label(frame, text = img[img.rfind(".")+1:], style='label.TLabel')
        downloaded_wxh_lbl.grid(column = 3, row = t+2)
        downloaded_type_lbl.grid(column = 4, row = t+2)
        big_selector_partial = partial(display_big_selector, int(t/3))
        big_selector_btn = Button(frame, text='View in Big Selector', command=big_selector_partial, style='button.TLabel')
        big_selector_btn.grid(column = 5, row = t+2)

        pixiv_images_array.append([img, sub, cropped, suffix, cropped_name_lbl, original_image, original_photoImage, downloaded_image, downloaded_photoImage, flag, pixiv_sub_dir_array])
        if t > 32:
            break
        t += 3

def save_and_back():
    save(cwd, chkbtn_vars_array, pixiv_images_array, delete_dirs_array, frame)
    init_window()

def save_and_refresh():
    save(cwd, chkbtn_vars_array, pixiv_images_array, delete_dirs_array, frame)
    display_view_results()


def myfunction(event):
    results_canvas.configure(scrollregion=results_canvas.bbox("all"), width=width-620, height=height-620)

def myfunction2(event):
    big_selector_canvas.configure(scrollregion=big_selector_canvas.bbox("all"), width=(width/3)*2 - 50, height=height-125)

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
    style.configure("chkbtn.TCheckbutton", foreground=colour_array[1], background=colour_array[0], borderwidth = 0, highlightthickness = 10, selectcolor=colour_array[2], activebackground=colour_array[2], activeforeground=colour_array[2], disabledforeground=colour_array[2], highlightcolor=colour_array[2])
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
    do_sourcery_btn = Button(window, text="Do Sourcery", command=magic, style="button.TLabel")
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

    results_frame = Frame(window, width=width-620, height=height-620, style="frame.TFrame")
    results_canvas = Canvas(results_frame, width=width-620, height=height-620, background=colour_array[0], highlightthickness=0)
    frame = Frame(results_canvas, width=width-620, height=height-620, style="frame.TFrame")
    results_scrollbar = Scrollbar(results_frame, orient="vertical", command=results_canvas.yview)
    results_canvas.configure(yscrollcommand=results_scrollbar.set)
    #https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
    results_scrollbar.pack(side="right",fill="y")
    results_canvas.pack(side="left")
    results_canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>",myfunction)

    save_and_back_btn = Button(window, text="Save & Back", command=save_and_back, style="button.TLabel")
    save_and_refresh_btn = Button(window, text="Save & Refresh", command=save_and_refresh, style="button.TLabel")

    # widgets for big_selector
    big_selector_frame = Frame(window, width=width-620, height=height-620, style="frame.TFrame")
    big_selector_canvas = Canvas(big_selector_frame, width=width-620, height=height-620, background=colour_array[0], highlightthickness=0)
    frame2 = Frame(big_selector_canvas, width=width-620, height=height-620, style="frame.TFrame")
    big_selector_scrollbar = Scrollbar(big_selector_frame, orient="vertical", command=big_selector_canvas.yview)
    big_selector_canvas.configure(yscrollcommand=big_selector_scrollbar.set)

    big_selector_scrollbar.pack(side="right",fill="y")
    big_selector_canvas.pack(side="left")
    big_selector_canvas.create_window((0,0),window=frame2,anchor='nw')
    frame2.bind("<Configure>",myfunction2)

    # global arrays
    input_images_array = []
    pixiv_images_array = []
    delete_dirs_array = []
    chkbtn_vars_array = []
    for i in range(12):
        chkbtn_vars_array.append(((IntVar()), (IntVar())))
        chkbtn_vars_array[i][0].set(0)
        chkbtn_vars_array[i][1].set(1)
    
    esc_op = False
    esc_res = False
    init_directories(cwd)
    init_window()
    window.mainloop()