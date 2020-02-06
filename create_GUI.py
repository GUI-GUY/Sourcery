from tkinter import Tk, IntVar, Canvas, Scrollbar
from tkinter.ttk import Label, Checkbutton, Button, Style, Entry, Frame
#from tkinter import messagebox as mb
#from tkinter.filedialog import askdirectory
from functools import partial
from os import listdir
from multiprocessing import Process, freeze_support, Queue
from file_operations import init_directories, init_configs, read_theme, is_image, read_credentials, write_credentials, write_theme, save, open_input, open_sourced, display_statistics, write_to_log
from sourcery import do_sourcery
from display_thread import display_view_results2, display_big_selector2
from pixiv_handler import pixiv_login
from global_variables import * #(potential problem with visibility?)

def magic():
    """
    Starts second process which searches for images and downloads them.
    """
    global process
    do_sourcery_btn.configure(state='disabled')
    if __name__ == '__main__':
        process = Process(target=do_sourcery, args=(cwd, input_images_array, credentials_array[0], comm_q, comm_img_q, comm_stop_q, comm_error_q, ))
        process.start()

def display_startpage():
    """
    Draws the basic startpage widgets.
    """
    forget_all_widgets()
    y = 100
    c = 23
    sourcery_lbl.place(x = 20, y = 10)
    images_in_input_lbl.place(x = 200, y = y)
    images_in_input_count_lbl.place(x = 350, y = y)
    currently_sourcing_lbl.place(x = 200, y = y + c * 2)
    currently_sourcing_img_lbl.place(x = 350, y = y + c * 2)
    remaining_searches_lbl.place(x = 200, y = y + c * 3)
    saucenao_requests_count_lbl.place(x = 350, y = y + c * 3.3)
    #elapsed_time_lbl.place(x = 200, y = y + c * 4)
    #eta_lbl.place(x = 200, y = y + c * 5)
    error_lbl.place(x = 550, y = y + c * 2)

    open_input_btn.place(x = 20, y = y + c * 0)
    open_sourced_btn.place(x = 20, y = y + c * 1)
    #statistics_btn.place(x = 20, y = y + c * 2)
    options_btn.place(x = 20, y = y + c * 2)
    do_sourcery_btn.place(x = 550, y = 100)
    stop_btn.place(x = 700, y = 100)
    view_results_btn.place(x = 350, y = y + c * 6)
    
    refresh_startpage()
    
def refresh_startpage():
    """
    Updates these startpage widgets:
    - Images in Input folder
    - Remaining searches on SauceNao
    - Current image that is being processed
    """
    global currently_processing
    global input_images_array
    input_images_array = listdir(cwd + "/Input")
    for img in input_images_array:
        if (not is_image(img)):
            input_images_array.remove(img)
    images_in_input_count_lbl.configure(text=str(len(input_images_array)))

    answer1 = 201
    if not comm_q.empty():
        try:
            answer1 = comm_q.get()
            saucenao_requests_count_lbl.configure(text=str(answer1) + "/200")
        except:
            pass
    if not comm_img_q.empty():
        if answer1 < 1:
            answer2 = "Out of requests"
        else:
            try:
                answer2 = comm_img_q.get()
                if answer2 != currently_processing:
                    if currently_processing != '':
                        safe_to_show_array.append(currently_processing)
                    currently_processing = answer2
                    pointdex = currently_processing.rfind(".")
                if pointdex != -1:
                    currently_processing = currently_processing[:pointdex] # deletes the suffix
            except:
                pass
        if answer2 == 'Stopped' or answer2 == 'Finished':
            do_sourcery_btn.configure(state='enabled')
            stop_btn.configure(state='enabled')
        currently_sourcing_img_lbl.configure(text=answer2)
    if not comm_error_q.empty():
        try:
            e = comm_error_q.get()
            error_lbl.configure(text=e)
            write_to_log('Multiprocess Error: ' + e)
        except:
            pass
    if esc_op:
        display_sourcery_options()
    elif esc_res:
        display_view_results()
    else:
        window.after(100, refresh_startpage)

def forget_all_widgets():
    for widget in window.winfo_children():
        widget.place_forget()

def escape_options():
    """
    Sets an escape variable on 'options'-button press for refresh_startpage to stop looping.
    """
    global esc_op
    esc_op = True

def escape_results():
    """
    Sets an escape variable on 'view results'-button press for refresh_startpage to stop looping.
    """
    global esc_res
    esc_res = True

def display_basic_options():
    """
    Draws options widgets that are shown on all options pages.
    """
    global esc_op
    esc_op = False
    options_lbl.place(x = 50, y = 10)

    sourcery_options_btn.place(x = 50, y = 50)
    provider_options_btn.place(x = 150, y = 50)
    saucenao_options_btn.place(x = 250, y = 50)

    options_back_btn.place(x = 50, y = 500)

def display_sourcery_options():
    """
    Draw options for Sourcery Application:
    - Themes
    """
    forget_all_widgets()
    display_basic_options()
    y = 100
    c = 23
    x1 = 50
    x2 = 240
    theme_lbl.place(x = x1, y = y-5)
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
    global current_theme
    current_theme = "Dark Theme"
    write_theme(current_theme, custom_array)
    enforce_style()

def change_to_light_theme():
    global current_theme
    current_theme = "Light Theme"
    write_theme(current_theme, custom_array)
    enforce_style()

def change_to_custom_theme():
    global current_theme
    current_theme = "Custom Theme"
    write_theme(current_theme, custom_array)
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
    e = write_theme(current_theme, custom_array)
    if e == None:
        write_to_log('Saved custom theme successfully')

def display_provider_options():
    """
    Draw options (login) for all image providers:
    - Pixiv 
    """
    forget_all_widgets()
    display_basic_options()
    y = 100
    c = 23
    pixiv_login_lbl.place(x = 50, y = y)
    pixiv_user_lbl.place(x = 50, y = y + c * 1)
    pixiv_user_filled_lbl.place(x = 120, y = y + c * 1)
    pixiv_password_lbl.place(x = 50, y = y + c * 2)
    pixiv_password_filled_lbl.place(x = 120, y = y + c * 2)
    pixiv_login_change_btn.place(x = 50, y = y + c * 4)
    pixiv_warning_lbl.place(x = 50, y = y + c * 3)
    
def display_saucenao_options():
    """
    Draw options (API-Key) for SauceNao:
    """
    forget_all_widgets()
    display_basic_options()
    saucenao_key_lbl.place(x = 50, y = 100)
    saucenao_key_number_lbl.place(x = 180, y = 100)
    saucenao_key_change_btn.place(x = 550, y = 100)
    
def pixiv_change_login():
    """
    Unlock login widget for pixiv, so that you can change your login data. 
    """
    y = 100
    c = 23
    pixiv_user_filled_lbl.place_forget()
    pixiv_password_filled_lbl.place_forget()
    pixiv_login_change_btn.place_forget()
    pixiv_user_entry.place(x = 120, y = y + c * 1)
    pixiv_password_entry.place(x = 120, y = y + c * 2)
    pixiv_login_confirm_btn.place(x = 50, y = y + c * 4)
    pixiv_login_confirm_nosave_btn.place(x = 180, y = y + c * 4)
    pixiv_user_entry.delete(0, len(credentials_array[1]))
    pixiv_password_entry.delete(0, len(credentials_array[2]))
    pixiv_user_entry.insert(0, credentials_array[1])
    pixiv_password_entry.insert(0, credentials_array[2])

def pixiv_set_login(save):
    """
    Save pixiv login data and revert the widgets to being uneditable.
    """
    y = 100
    c = 23
    pixiv_user_entry.place_forget()
    pixiv_password_entry.place_forget()
    pixiv_login_confirm_btn.place_forget()
    pixiv_login_confirm_nosave_btn.place_forget()
    pixiv_user_filled_lbl.place(x = 120, y = y + c * 1)
    pixiv_password_filled_lbl.place(x = 120, y = y + c * 2)
    pixiv_login_change_btn.place(x = 50, y = y + c * 4)
    credentials_array[1] = pixiv_user_entry.get()
    credentials_array[2] = pixiv_password_entry.get()
    if save:
        e = write_credentials(credentials_array)
    else:
        pixiv_login()
        credentials_array[1] = ''
        credentials_array[2] = ''
        e = write_credentials(credentials_array)
    if e == None:
        write_to_log('Changed pixiv login data successfully')
    pixiv_user_filled_lbl.configure(text=credentials_array[1])
    pixiv_password_filled_lbl.configure(text=credentials_array[2])

def saucenao_change_key():
    """
    Unlock API-Key widget for SauceNao, so that you can change your API-Key. 
    """
    saucenao_key_change_btn.place_forget()
    saucenao_key_number_lbl.place_forget()
    saucenao_key_confirm_btn.place(x = 550, y = 100)
    saucenao_key_entry.place(x = 180, y = 100)
    saucenao_key_entry.delete(0, len(credentials_array[0]))
    saucenao_key_entry.insert(0, credentials_array[0])
    
def saucenao_set_key():
    """
    Save SauceNao API-Key and revert the widget to being uneditable.
    """
    credentials_array[0] = saucenao_key_entry.get()
    e = write_credentials(credentials_array)
    if e == None:
        write_to_log('Changed SauceNao API-Key successfully')
    saucenao_key_confirm_btn.place_forget()
    saucenao_key_entry.place_forget()
    saucenao_key_change_btn.place(x = 550, y = 100)
    saucenao_key_number_lbl.configure(text=credentials_array[0])
    saucenao_key_number_lbl.place(x = 180, y = 100)

def stop():
    """
    Stop further search for images and halt the second process.
    """
    global process
    if process.is_alive():
        comm_stop_q.put("Stopped")
        stop_btn.configure(state='disabled')
    #currently_sourcing_img_lbl.configure(text="Stopped")

def display_big_selector(index):
    forget_all_widgets()
    big_selector_frame.place(x = round(width*0.515), y = 20)
    big_selector_canvas.yview_moveto(0)
    window.after(10, display_big_selector2, index, window, frame2, display_view_results)

def display_view_results():
    global esc_res
    esc_res = False
    forget_all_widgets()
    results_lbl.place(x = 50, y = 20)
    options_back_btn.place(x = 50, y = height-80)
    save_and_back_btn.place(x = 150, y = height-80)
    save_and_refresh_btn.place(x = 250, y = height-80)
    results_frame.place(x = 50, y = 100)
    results_canvas.yview_moveto(0)

    for x in range(len(big_ref_array)):
        try:
            big_ref_array[0].place_forget()
        except:
            pass
        try:
            big_ref_array[0].image = None
        except:
            pass
        del big_ref_array[0]

    window.after(10, display_view_results2, frame, display_big_selector)

def save_and_back():
    """
    Save selected images from results page and go back to startpage.
    """
    save(chkbtn_vars_array, chkbtn_vars_big_array, pixiv_images_array, delete_dirs_array, safe_to_show_array, frame, process)
    display_startpage()

def save_and_refresh():
    """
    Save selected images from results page and show the next dozen.
    """
    save(chkbtn_vars_array, chkbtn_vars_big_array, pixiv_images_array, delete_dirs_array, safe_to_show_array, frame, process)
    refresh()

def refresh():
    global currently_processing
    # Get all images processed while on results screen and put them in safe_to_show_array
    if not comm_img_q.empty():
        answer2 = comm_img_q.get()
        if answer2 != currently_processing:
            if currently_processing != '':
                safe_to_show_array.append(currently_processing)
            currently_processing = answer2
            pointdex = currently_processing.rfind(".")
            if pointdex != -1:
                currently_processing = currently_processing[:pointdex] # deletes the suffix
        window.after(1, refresh)
    else:
        for elem in chkbtn_vars_array:
            elem[0].set(0)
            elem[1].set(1)
        display_view_results()

def myfunction(event):
    """
    Setup scroll region for results screen.
    """
    results_canvas.configure(scrollregion=results_canvas.bbox("all"), width=results_frame_width, height=results_frame_height)

def myfunction2(event):
    """
    Setup scroll region for big selector screen.
    """
    big_selector_canvas.configure(scrollregion=big_selector_canvas.bbox("all"), width=big_selector_frame_width, height=big_selector_frame_height)

def enforce_style():
    """
    Changes style of all widgets to the currently selected theme.
    """
    global colour_array, custom_array, current_theme
    colour_array, custom_array, current_theme = read_theme()
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

def bound_to_mousewheel(event):
    results_canvas.bind_all("<MouseWheel>", on_mousewheel)
    # # with Windows OS
    # root.bind("<MouseWheel>", mouse_wheel)
    # # with Linux OS
    # root.bind("<Button-4>", mouse_wheel)
    # root.bind("<Button-5>", mouse_wheel)  

def unbound_to_mousewheel(event):
    results_canvas.unbind_all("<MouseWheel>") 

def on_mousewheel(event):
    results_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def bound_to_mousewheel2(event):
    big_selector_canvas.bind_all("<MouseWheel>", on_mousewheel2)   

def unbound_to_mousewheel2(event):
    big_selector_canvas.unbind_all("<MouseWheel>") 

def on_mousewheel2(event):
    big_selector_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == '__main__':
    freeze_support()
    
    window = Tk()
    window.title("Sourcery")
    window.update_idletasks()
    window.state('zoomed')
    height = window.winfo_screenheight()
    width = window.winfo_screenwidth()
    results_frame_height = height-200
    results_frame_width = width-200
    big_selector_frame_height = height-100 # height-620
    big_selector_frame_width = round(width*0.48) - 25 # width-620
    #window.geometry(str(width-500) + 'x' + str(height-500))
    #dateS =  time.strftime("20%y-%m-%d")

    # set style
    results_canvas = Canvas(window)
    enforce_style()

    # widgets for start screen
    sourcery_lbl = Label(window, text="Sourcery", font=("Arial Bold", 50), style="label.TLabel")
    images_in_input_lbl = Label(window, text="Images in input", style="label.TLabel")
    images_in_input_count_lbl = Label(window, text="Number here", style="label.TLabel")
    currently_sourcing_lbl = Label(window, text="Currently Sourcing:", style="label.TLabel")
    currently_sourcing_img_lbl = Label(window, text="None", style="label.TLabel")
    remaining_searches_lbl = Label(window, text="Remaining SauceNao\nsearches today:", style="label.TLabel")
    saucenao_requests_count_lbl = Label(window, text="???/200", style="label.TLabel")
    #elapsed_time_lbl = Label(window, text="Elapsed time:", style="label.TLabel")
    #eta_lbl = Label(window, text="ETA:", style="label.TLabel")
    error_lbl = Label(window, text="Errors will be displayed here", style="label.TLabel")

    open_input_btn = Button(window, text="Open Input", command=open_input, style="button.TLabel")
    open_sourced_btn = Button(window, text="Open Sourced", command=open_sourced, style="button.TLabel")
    #statistics_btn = Button(window, text="Statistics", command=display_statistics, style="button.TLabel")
    options_btn = Button(window, text="Options", command=escape_options, style="button.TLabel")
    do_sourcery_btn = Button(window, text="Do Sourcery", command=magic, style="button.TLabel")
    stop_btn = Button(window, text="Stop", command=stop, style="button.TLabel")
    view_results_btn = Button(window, text="View Results", command=escape_results, style="button.TLabel")

    # widgets for options
    options_lbl = Label(window, text="Options", font=("Arial Bold", 20), style="label.TLabel")

    provider_options_btn = Button(window, text="Provider", command=display_provider_options, style="button.TLabel")
    saucenao_options_btn = Button(window, text="SauceNao", command=display_saucenao_options, style="button.TLabel")
    sourcery_options_btn = Button(window, text="Sourcery", command=display_sourcery_options, style="button.TLabel")

    pixiv_login_lbl = Label(window, text="Pixiv Login", style="label.TLabel")
    pixiv_user_lbl = Label(window, text="Username", style="label.TLabel")
    pixiv_user_filled_lbl = Label(window, width=50, text=credentials_array[1], style="button.TLabel")
    pixiv_user_entry = Entry(window, width=52, style="button.TLabel")
    pixiv_password_lbl = Label(window, text="Password", style="label.TLabel")
    pixiv_password_filled_lbl = Label(window, width=50, text=credentials_array[2], style="button.TLabel")
    pixiv_password_entry = Entry(window, width=52, style="button.TLabel")
    pixiv_login_change_btn = Button(window, text="Change", command=pixiv_change_login, style="button.TLabel")
    pixiv_login_confirm_btn = Button(window, text="Confirm & Save", command=partial(pixiv_set_login, True), style="button.TLabel")
    pixiv_login_confirm_nosave_btn = Button(window, text="Confirm & Don't Save", command=partial(pixiv_set_login, False), style="button.TLabel")
    pixiv_warning_lbl = Label(window, width=50, text='THIS WILL BE SAVED IN PLAINTEXT!!!', style="label.TLabel")

    saucenao_key_lbl = Label(window, text="SauceNao API-Key", style="label.TLabel")
    saucenao_key_number_lbl = Label(window, width=50, text=credentials_array[0], style="button.TLabel")
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

    current_theme = 'Dark Theme'
    custom_background_entry.insert(0, custom_array[0])
    custom_foreground_entry.insert(0, custom_array[1])
    custom_button_background_entry.insert(0, custom_array[2])
    custom_button_background_active_entry.insert(0, custom_array[3])
    custom_button_foreground_active_entry.insert(0, custom_array[4])
    custom_button_background_pressed_entry.insert(0, custom_array[5])
    custom_button_foreground_pressed_entry.insert(0, custom_array[6])

    options_back_btn = Button(window, text="Back", command=display_startpage, style="button.TLabel")

    # widgets for results
    results_lbl = Label(window, text="Results", font=("Arial Bold", 14), style="label.TLabel")

    results_frame = Frame(window, width=results_frame_width, height=results_frame_height, style="frame.TFrame")
    results_canvas = Canvas(results_frame, width=results_frame_width, height=results_frame_height, background=colour_array[0], highlightthickness=0)
    frame = Frame(results_canvas, width=results_frame_width, height=results_frame_height, style="frame.TFrame")
    results_scrollbar = Scrollbar(results_frame, orient="vertical", command=results_canvas.yview)
    results_canvas.configure(yscrollcommand=results_scrollbar.set)
    #https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
    results_scrollbar.pack(side="right",fill="y")
    results_canvas.pack(side="left")
    results_canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>", myfunction)

    save_and_back_btn = Button(window, text="Save & Back", command=save_and_back, style="button.TLabel")
    save_and_refresh_btn = Button(window, text="Save & Refresh", command=save_and_refresh, style="button.TLabel")

    # widgets for big_selector
    big_selector_frame = Frame(window, width=big_selector_frame_width, height=big_selector_frame_width, style="frame.TFrame")
    big_selector_canvas = Canvas(big_selector_frame, width=big_selector_frame_width, height=big_selector_frame_width, background=colour_array[0], highlightthickness=0)
    frame2 = Frame(big_selector_canvas, width=big_selector_frame_width, height=big_selector_frame_width, style="frame.TFrame")
    big_selector_scrollbar = Scrollbar(big_selector_frame, orient="vertical", command=big_selector_canvas.yview)
    big_selector_canvas.configure(yscrollcommand=big_selector_scrollbar.set)

    big_selector_scrollbar.pack(side="right",fill="y")
    big_selector_canvas.pack(side="left")
    big_selector_canvas.create_window((0,0),window=frame2,anchor='nw')
    frame2.bind("<Configure>", myfunction2)

    # results_canvas.bind_all("<MouseWheel>", on_mousewheel)
    frame.bind('<Enter>', bound_to_mousewheel)
    frame.bind('<Leave>', unbound_to_mousewheel)
    frame2.bind('<Enter>', bound_to_mousewheel2)
    frame2.bind('<Leave>', unbound_to_mousewheel2)
    
    safe_to_show_array.extend(listdir(cwd + '/Sourcery/sourced_original/'))
    tt=0
    for img in safe_to_show_array:
        pointdex = img.rfind(".")
        if pointdex != -1:
            safe_to_show_array[tt] = img[:pointdex] # deletes the suffix
        tt += 1
    for i in range(12):
        results_12_tuple_widgets_array.append(([Checkbutton(frame, style="chkbtn.TCheckbutton"), Label(frame, text = "original", style='label.TLabel'), Label(frame, style='label.TLabel'), Label(frame, style='label.TLabel'), Label(frame, style='label.TLabel')], [Checkbutton(frame, style="chkbtn.TCheckbutton"), Label(frame, text = "pixiv", style='label.TLabel'), Label(frame, text = "More images", style='label.TLabel'), Label(frame, text = "More images", style='label.TLabel'), Button(frame, text='View in Big Selector', style='button.TLabel')]))
    for i in range(12):
        chkbtn_vars_array.append(((IntVar()), (IntVar())))
        chkbtn_vars_array[i][0].set(0)
        chkbtn_vars_array[i][1].set(1)

    currently_processing = ''
    esc_op = False # Escape variable for options
    esc_res = False # Escape variable for results
    process = Process()
    comm_q = Queue() # Queue for 'Remaining searches'
    comm_img_q = Queue() # Queue for 'Currently Sourcing'
    comm_stop_q = Queue() # Queue for stop signal
    comm_error_q = Queue() # Queue for error messages
    display_startpage()
    window.mainloop()