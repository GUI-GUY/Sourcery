from tkinter import Tk, IntVar, Canvas, Scrollbar, Text, END
from tkinter.ttk import Label, Button, Style, Entry, Frame
#from tkinter import messagebox as mb
#from tkinter.filedialog import askdirectory
#from functools import partial
from os import listdir, path, remove
from shutil import rmtree
from multiprocessing import Process, freeze_support, Queue, Pipe#, Semaphore
from copy import copy
from file_operations import is_image, save, open_input, open_sourced, display_statistics
from sourcery import do_sourcery
from pixiv_handler import pixiv_authenticate, pixiv_login, pixiv_fetch_illustration
from Options import Options
#from image_preloader import preload_main
from ImageData import ImageData
from ScrollFrame import ScrollFrame
from Files import Files
import global_variables as gv
import time

def magic():
    """
    Starts second process which searches for images and downloads them.
    """
    global process
    do_sourcery_btn.configure(state='disabled')
    load_from_ref_btn.configure(state='disabled')
    if __name__ == '__main__':
        gv.Files.Log.write_to_log('Starting second process for sourcing images')
        process = Process(target=do_sourcery, args=(gv.cwd, gv.input_images_array, gv.Files.Cred.saucenao_api_key, gv.Files.Conf.minsim, comm_q, comm_img_q, comm_stop_q, comm_error_q, img_data_q, duplicate_c_pipe, ))
        process.start()
        rename_option = gv.Files.Conf.rename_pixiv

def image_preloader():
    # """
    # Starts multiple processes which preload images into memory to reduce loading times and increase accessibility
    # https://www.geeksforgeeks.org/multiprocessing-python-set-2/
    # """
    # if __name__ == '__main__':
    #     process0 = Process(target=preload_main, args=(sem, 0, gv.img_data_array, ))
    #     process1 = Process(target=preload_main, args=(sem, 1, gv.img_data_array,))
    #     process2 = Process(target=preload_main, args=(sem, 2, gv.img_data_array,))
    #     process0.start()
    #     process1.start()
    #     process2.start()
    pass

def display_startpage():
    """
    Draws the basic startpage widgets.
    """
    Options.SouO.color_insert()
    forget_all_widgets()
    y = 100
    c = 23
    sourcery_lbl.place(x = 20, y = 10)
    images_in_input_lbl.place(x = 20, y = y + c * 4)
    images_in_input_count_lbl.place(x = 170, y = y + c * 4)
    currently_sourcing_lbl.place(x = 20, y = y + c * 5)
    currently_sourcing_img_lbl.place(x = 170, y = y + c * 5)
    remaining_searches_lbl.place(x = 20, y = y + c * 6)
    saucenao_requests_count_lbl.place(x = 170, y = y + c * 6.3)
    #elapsed_time_lbl.place(x = 200, y = y + c * 4)
    #eta_lbl.place(x = 200, y = y + c * 5)
    error_lbl.place(x = 20, y = y + c * 12)

    open_input_btn.place(x = 20, y = y + c * 0)
    open_sourced_btn.place(x = 20, y = y + c * 1)
    #statistics_btn.place(x = 20, y = y + c * 2)
    options_btn.place(x = 20, y = y + c * 2)
    do_sourcery_btn.place(x = 20, y = y + c * 8)
    stop_btn.place(x = 20, y = y + c * 9)
    load_from_ref_btn.place(x = 20, y = y + c * 10)
    
    results_lbl.place(x = 400, y = 60)
    save_locked_btn.place(x = 250, y = height-80)
    lock_save_btn.place(x = 450, y = height-80)
    results_ScrollFrame.display(x = 400, y = 100)
    display_info()

    test_btn = Button(master=window, text='test', command=test)
    test_btn.place(x = 800, y = 60)
    display_info_btn.place(x = 600, y = 60)
    display_logfile_btn.place(x = 700, y = 60)

    refresh_startpage(1, '')
    
def test():
    print(gv.img_data_array)
    gv.Files.Log.write_to_log('this is a test')

def refresh_startpage(change, answer2):
    """
    Updates these startpage widgets:
    - Images in Input folder
    - Remaining searches on SauceNao
    - Current image that is being processed
    """
    global currently_processing
    global img_data_counter
    gv.input_images_array = listdir(gv.cwd + "/Input")
    for img in gv.input_images_array:
        if (not is_image(img)):
            gv.input_images_array.remove(img)
    images_in_input_count_lbl.configure(text=str(len(gv.input_images_array)))


    # if process.is_alive():
    #     if lock_save_btn.cget('state') != 'enabled':
    #         lock_save_btn.configure(state='enabled')
    #     if not locked and save_locked_btn.cget('state') != 'disabled':
    #         save_locked_btn.configure(state='disabled')
    # elif save_locked_btn.cget('state') != 'enabled' and lock_save_btn.cget('state') != 'disabled':
    #     save_locked_btn.configure(state='enabled')
    #     lock_save_btn.configure(state='disabled')

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
                    currently_processing = answer2
            except:
                pass
        currently_sourcing_img_lbl.configure(text=answer2)
    if answer2 == 'Stopped' or answer2 == 'Finished':
        if comm_error_q.empty():
            gv.Files.Log.write_to_log('Sourcing process was stopped or is finished')
            do_sourcery_btn.configure(state='enabled')
            load_from_ref_btn.configure(state='enabled')
            stop_btn.configure(state='enabled')
            answer2 = ''
    if not comm_error_q.empty():
        try:
            e = comm_error_q.get()
            error_lbl.configure(text=e)
            gv.Files.Log.write_to_log(e)
        except:
            pass
    if not img_data_q.empty():
        try:
            a = img_data_q.get()
            b = ImageData(a[0], a[1], a[2], a[3])
            gv.img_data_array.append(b)
        except:
            pass
    
    # Kucke ob freie plätze gefolgt von besetzten
    # wenn ja, rücke auf (erniedrige den index aller datas welche größer sind und platziere sie erneut)
    # Kucke ob es datas gibt welche keinen index haben
    # wenn eine gefunden, 
    # packe es in frühesten freien platz

    mem = False
    c = 0
    i = 0
    if (True in gv.free_space) and (False in gv.free_space):
        for space in gv.free_space:
            if space and not mem:
                mem = True
                c = i
            if not space and mem:
                x = 0
                for data in gv.img_data_array:
                    if data.index > c:
                        gv.free_space[data.index] = True
                        data.display_results((c+x)*3)
                        gv.free_space[c+x] = False
                    x += 1
                break
            i += 1
    if (True in gv.free_space):
        for data in gv.img_data_array:
            if data.index == None:
                x = 0
                for space in gv.free_space:
                    if space:
                        data.load()
                        data.process_results_imgs()
                        data.modify_results_widgets()
                        data.display_results(x*3)
                        gv.free_space[x] = False
                        break
                    x += 1
    if gv.esc_op:
        Options.display_sourcery_options()
    else:
        window.after(100, refresh_startpage, change, answer2)

def load_from_ref():
    refs = gv.Files.Ref.read_reference()
    if refs:
        pixiv_authenticate()
        gv.Files.Log.write_to_log('Loading images from reference file...')
        for ref in refs:
            illust = pixiv_fetch_illustration(ref['old_name'], ref['id_pixiv'])
            if not illust:
                continue
            next_img = False
            for data in gv.img_data_array:
                if ref['old_name'] == data.name_original:
                    if ref['id_pixiv'] == illust.id:# TODO Missing: rename option
                        next_img = True
            if next_img:
                gv.Files.Log.write_to_log('Image already loaded/sourced')
                continue
            gv.img_data_array.append(ImageData(ref['old_name'], ref['new_name_pixiv'], ['Pixiv', None, None, None, ref['minsim']], illust))# TODO what if image doesnt exist
        gv.Files.Log.write_to_log('Loaded images from reference file')
    else:
        gv.Files.Log.write_to_log('Reference file is empty')

def duplicate_loop():
    if duplicate_p_pipe.poll():
        dup_list = duplicate_p_pipe.recv()
        is_dup = False
        for data in gv.img_data_array:
            if dup_list[0] == data.name_original and dup_list[1] == str(data.minsim) and dup_list[2] == str(data.rename):
                is_dup = True
                break
        duplicate_p_pipe.send(is_dup)
    window.after(10, duplicate_loop)

def display_info():
    gv.Files.Log.log_text.place_forget()
    info_ScrollFrame.display(x = (width/3)*1.85, y = 100)

def display_logfile():
    info_ScrollFrame.sub_frame.place_forget()
    gv.Files.Log.log_text.place(x = (width/3)*1.85, y = 100)

def forget_all_widgets():
    for widget in window.winfo_children():
        widget.place_forget()

def escape_options():
    """
    Sets an escape variable on 'options'-button press for refresh_startpage to stop looping.
    """
    gv.esc_op = True

def stop():
    """
    Stop further search for images and halt the second process.
    """
    global process
    if process.is_alive():
        gv.Files.Log.write_to_log('Stopping sourcing process...')
        comm_stop_q.put("Stopped")
        stop_btn.configure(state='disabled')
    #currently_sourcing_img_lbl.configure(text="Stopped")

def lock_save():
    """
    Locks in selected images to save
    """
    data_list = copy(gv.img_data_array)
    for data in data_list:
        if data.index != None:
            data.lock()
    save_locked_btn.configure(state='enabled')
    
def save_locked():
    """
    Save locked images from results page
    """
    gv.Files.Log.write_to_log('Saving selected images...')
    if save():
        gv.Files.Log.write_to_log('Saved images')
    else:
        gv.Files.Log.write_to_log('Cancelled saving images')
    leftovers()
    save_locked_btn.configure(state='disabled')

def leftovers():
    # # Delete leftovers
    # if not process.is_alive():
    #     for img in listdir(gv.cwd + '/Sourcery/sourced_original'):
    #         if gv.cwd + '/Sourcery/sourced_original' + img not in gv.delete_dirs_array:
    #             gv.delete_dirs_array.append(gv.cwd + '/Sourcery/sourced_original' + img)

    gv.Files.Log.write_to_log('Deleting empty folders, leftovers etc. ...')
    for element in gv.delete_dirs_array:
        try:
            if path.isdir(element):
                rmtree(element)
            elif path.isfile(element):
                remove(element)
        except Exception as e:
            print('ERROR [0017] ' + str(e))
            gv.Files.Log.write_to_log("ERROR [0017] " + str(e))
            #mb.showerror("ERROR", "ERROR CODE [0017]\nSomething went wrong while removing the image " + element)

    gv.delete_dirs_array.clear()
    gv.Files.Log.write_to_log('Deleted stuff')

def enforce_style():
    """
    Changes style of all widgets to the currently selected theme.
    """
    #gv.Files.Theme.read_theme()
    window.configure(bg=gv.Files.Theme.background)
    style = Style()
    style.configure("label.TLabel", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
    style.configure("button.TLabel", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.button_background, font=("Arial Bold", 10))
    style.map("button.TLabel",
        foreground=[('pressed', gv.Files.Theme.button_foreground_pressed), ('active', gv.Files.Theme.button_foreground_active)],
        background=[('pressed', '!disabled', gv.Files.Theme.button_background_pressed), ('disabled', 'lime green'), ('active', gv.Files.Theme.button_background_active)]
    )
    style.configure("frame.TFrame", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background)
    style.configure("chkbtn.TCheckbutton", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, borderwidth = 0, highlightthickness = 10, selectcolor=gv.Files.Theme.button_background, activebackground=gv.Files.Theme.button_background, activeforeground=gv.Files.Theme.button_background, disabledforeground=gv.Files.Theme.button_background, highlightcolor=gv.Files.Theme.button_background, font=("Arial Bold", 10))
    gv.Files.Log.log_text.configure(foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
    #style.configure("scroll.Vertical.TScrollbar", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.button_background, throughcolor=gv.Files.Theme.button_background, activebackground=gv.Files.Theme.button_background)
    results_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    info_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    big_selector_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)

if __name__ == '__main__':
    freeze_support()

    window = Tk()
    window.title("Sourcery")
    window.update_idletasks()
    window.state('zoomed')
    height = gv.height = window.winfo_screenheight()
    width = gv.width = window.winfo_screenwidth()
    results_frame_height = int(height-200)
    results_frame_width = int(width/3)
    info_frame_height = int(height-200)
    info_frame_width = int(width/3)
    big_selector_frame_height = int(height-200) # height-620
    big_selector_frame_width = int(width*0.13) - 25 # width-620
    #window.geometry(str(width-500) + 'x' + str(height-500))
    #dateS =  time.strftime("20%y-%m-%d")

    # set style
    results_ScrollFrame = ScrollFrame(window, results_frame_width, results_frame_height)
    info_ScrollFrame = ScrollFrame(window, info_frame_width, info_frame_height)
    big_selector_ScrollFrame = ScrollFrame(window, big_selector_frame_width, big_selector_frame_height)

    gv.Files.Log.log_text = Text(master=window, height=int(info_frame_height/16), width=int(info_frame_width/7))
    gv.Files.Log.init_log()
    gv.Files.Log.write_to_log('Initialising variables...')

    enforce_style()
    
    Options = Options(window, display_startpage, enforce_style)

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
    #view_results_btn = Button(window, text="View Results", command=escape_results, style="button.TLabel")
    display_info_btn = Button(window, text="display_info", command=display_info, style="button.TLabel")
    display_logfile_btn = Button(window, text="display_logfile", command=display_logfile, style="button.TLabel")
    load_from_ref_btn = Button(window, text="Load from Reference File", command=load_from_ref, style="button.TLabel")
    

    # widgets for options
    options_lbl = Label(window, text="Options", font=("Arial Bold", 20), style="label.TLabel")
    options_back_btn = Button(window, text="Back", command=display_startpage, style="button.TLabel")

    # widgets for results
    results_lbl = Label(window, text="Results", font=("Arial Bold", 20), style="label.TLabel")

    lock_save_btn = Button(window, text="Lock selected", command=lock_save, style="button.TLabel")
    save_locked_btn = Button(window, text="Save selected images", command=save_locked, state = 'disabled', style="button.TLabel")

    img_data_counter = 0
    rename_option = False

    gv.frame = results_ScrollFrame.frame
    gv.frame2 = big_selector_ScrollFrame.frame
    gv.frame3 = info_ScrollFrame.frame
    gv.window = window
    gv.big_selector_frame = big_selector_ScrollFrame.sub_frame
    gv.big_selector_canvas = big_selector_ScrollFrame.canvas
    for i in range(12):
        gv.free_space.append(True)
    #gv.display_view_results = display_view_results
    gv.display_startpage = display_startpage
    currently_processing = ''
    gv.esc_op = False # Escape variable for options
    esc_res = False # Escape variable for results
    loop_esc = True
    process = Process()
    comm_q = Queue() # Queue for 'Remaining searches'
    comm_img_q = Queue() # Queue for 'Currently Sourcing'
    comm_stop_q = Queue() # Queue for stop signal
    comm_error_q = Queue() # Queue for error messages
    img_data_q = Queue() # Queue for ImageData classes
    duplicate_p_pipe, duplicate_c_pipe = Pipe()
    #sem = Semaphore(12)
    #image_preloader()
    gv.Files.Log.write_to_log('Variables initialised')
    duplicate_loop()
    display_startpage()
    window.mainloop()