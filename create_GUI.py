
# __version__ = '0.1'
# __author__ = 'Cardinal Biggles'

from os import listdir, path, remove
from sys import stderr
from copy import copy
import time
from tkinter import Tk, IntVar, Canvas, Scrollbar, Text, END, W
from tkinter import Checkbutton as cb
from tkinter.ttk import Label, Button, Style, Entry, Frame
#from tkinter import messagebox as mb
#from tkinter.filedialog import askdirectory
#from functools import partial
from shutil import rmtree
#from distutils.util import strtobool
from multiprocessing import Process, freeze_support, Queue, Pipe, Lock, Semaphore
from file_operations import is_image, save, open_input, open_output, display_statistics, change_input, change_output
from sourcery import do_sourcery
from pixiv_handler import pixiv_fetch_illustration
from danbooru_handler import danbooru_fetch_illustration
from Options import Options
#from image_preloader import preload_main
from ImageData import ImageData
from ScrollFrame import ScrollFrame
from Files import Files
import global_variables as gv

stderr = gv.Files.Log

def magic():
    """
    Starts second process which searches for images and downloads them.
    """
    global process
    global input_images_array
    do_sourcery_btn.configure(state='disabled')
    load_from_ref_btn.configure(state='disabled')
    if __name__ == '__main__':
        gv.Files.Log.write_to_log('Starting second process for sourcing images')
        input_lock.acquire()
        process = Process(target=do_sourcery, args=(gv.cwd, input_images_array, gv.Files.Cred.saucenao_api_key, gv.Files.Conf.minsim, gv.input_dir, comm_q, comm_img_q, comm_stop_q, comm_error_q, img_data_q, duplicate_c_pipe, ))
        process.start()
        input_lock.release()

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
    Options_Class.SouO.color_insert()
    forget_all_widgets()
    x = int(height/160*2)
    y = int(height/9)
    c = 22

    sourcery_lbl.place(x = x, y = int(height/160))
    sub_frame_startpage.place(x = x, y = y  + c * 6)

    change_input_btn.place(x = x, y = y + c * 0)
    open_input_btn.place(x = x, y = y + c * 1)
    change_output_btn.place(x = x, y = y + c * 2)
    open_output_btn.place(x = x, y = y + c * 3)
    options_btn.place(x = x, y = y + c * 4)
    
    results_lbl.place(x = int(width/16*4), y = int(height/90*6))
    save_locked_btn.place(x = int(width*0.48), y = int(height*0.9))
    lock_save_btn.place(x = int(width*0.4), y = int(height*0.9))
    results_ScrollFrame.display(x = int(width/16*4), y = int(height/9))
    display_info()

    test_btn = Button(master=window, text='test', command=test)
    test_btn.place(x = 800, y = 60)
    display_info_btn.place(x = int(width*0.7), y = int(height/90*6))
    display_logfile_btn.place(x = int(width*0.8), y = int(height/90*6))

    refresh_startpage(1, '')
    
def test():
    global input_images_array
    print(gv.img_data_array)
    print(input_images_array)
    gv.Files.Log.write_to_log('this is a test')

def list_input(directory_list, directory, depth):
    add = list()
    for elem in directory_list:
        if path.isfile(directory + '/' + elem) or depth == 0:
            add.append(directory + '/' + elem)
        elif path.isdir(directory + '/' + elem):
            add.extend(list_input(listdir(directory + '/' + elem), directory + '/' + elem, depth-1))
    return add

def refresh_startpage(change, answer2):
    """
    Updates these startpage widgets:
    - Images in Input folder
    - Remaining searches on SauceNao
    - Current image that is being processed
    Creates ImageData classes from the information the magic process gives
    Displays all results
    """
    global input_images_array
    
    input_lock.acquire()
    try:
        input_images_array = list_input(listdir(gv.input_dir), gv.input_dir, int(gv.Files.Conf.input_search_depth))
        input_images_array.extend(listdir(gv.input_dir))
    except Exception as e:
        print('ERROR [0040] ' + str(e))
        gv.Files.Log.write_to_log('ERROR [0040] ' + str(e))
        #mb.showerror("ERROR [0040]", "ERROR CODE [0040]\nSomething went wrong while accessing a the 'Input' folder, please restart Sourcery.")
    delete = list()
    for img in input_images_array:
        if (not is_image(img)) or not path.isfile(img):
            delete.append(img)
    for elem in delete:
        if elem in input_images_array:
            input_images_array.remove(elem)
    input_lock.release()
    images_in_input_count_lbl.configure(text=str(len(input_images_array)))

    answer1 = (201, 200)
    if not comm_q.empty():
        try:
            answer1 = comm_q.get()
            saucenao_requests_count_lbl.configure(text=str(answer1[0]) + "/" + str(answer1[1]))
        except:
            pass
    if not comm_img_q.empty():
        if answer1[0] < 1: # TypeError: '<' not supported between instances of 'tuple' and 'int'
            answer2 = "Out of requests"
        else:
            try:
                answer2 = comm_img_q.get()
                global currently_processing
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
            #print('a')
            global index
            b = ImageData(a[0], a[1], a[2], a[3], a[4], a[5], a[6], index)
            index += 1
            gv.img_data_array.append(b)
            #print('b')
        except Exception as e:
            if b in gv.img_data_array:
                gv.img_data_array.remove(b)
            print("ERROR [0055] " + str(e))
            gv.Files.Log.write_to_log("ERROR [0055] " + str(e))
            #mb.showerror("ERROR [0055]", "ERROR CODE [0055]\nImage data could not be loaded, skipped.")
    
    for data in gv.img_data_array:
        if not data.placed:
            load = data.load()
            if  not load:
                data.self_destruct()
                gv.img_data_array.remove(data)
                gv.Files.Log.write_to_log('Problem while loading images, skipped')
            elif load:
                if gv.imgpp_sem.acquire(False):
                    data.process_results_imgs()
                    data.modify_results_widgets()
                    x = data.display_results(gv.last_occupied_result+1)
                    if x == -1:# This means direct replace has triggered
                        gv.Files.Log.write_to_log('Attempting to save image:' + data.name_original + '...' )
                        if data.save():
                            gv.Files.Log.write_to_log('Successfully saved image')
                            data.self_destruct()
                        else:
                            gv.Files.Log.write_to_log('Did not save image')# TODO delete reference
                        gv.img_data_array.remove(data)
                    else:
                        gv.last_occupied_result = x
                    data.placed = True

    window.after(100, refresh_startpage, change, answer2)

def load_from_ref():
    """
    Loads images whose info has been saved in the reference file
    """
    refs = gv.Files.Ref.read_reference()
    if refs:
        gv.Files.Log.write_to_log('Loading images from reference file...')
        for ref in refs:

            pixiv_info_list = list(ref['pixiv'])

            danb_info_list = list(ref['danbooru'])

            yandere_info_list = list(ref['yandere'])

            konachan_info_list = list(ref['konachan'])

            dict_list = ref['dict_list']

            pixiv_illustration_list = list()
            visited_ids = list()
            for elem in pixiv_info_list:
                if elem['id'] not in visited_ids:
                    pixiv_illustration_list.append((pixiv_fetch_illustration(ref['old_name'], elem['id']), elem['new_name']))
                    visited_ids.append(elem['id'])
            
            danb_illustration_list = list()
            visited_ids = list()
            for elem in danb_info_list:
                if elem['id'] not in visited_ids:
                    danb_illustration_list.append((danbooru_fetch_illustration(elem['id'], danbooru=True), elem['new_name']))
                    visited_ids.append(elem['id'])
            
            yandere_illustration_list = list()
            visited_ids = list()
            for elem in yandere_info_list:
                if elem['id'] not in visited_ids:
                    yandere_illustration_list.append((danbooru_fetch_illustration(elem['id'], yandere=True), elem['new_name']))
                    visited_ids.append(elem['id'])
            
            konachan_illustration_list = list()
            visited_ids = list()
            for elem in konachan_info_list:
                if elem['id'] not in visited_ids:
                    konachan_illustration_list.append((danbooru_fetch_illustration(elem['id'], konachan=True), elem['new_name']))
                    visited_ids.append(elem['id'])
            
            next_img = False
            for data in gv.img_data_array:
                if str(ref['old_name']) == data.name_original and str(ref['minsim']) == gv.Files.Conf.minsim:
                    next_img = True
                    break
            if next_img:
                gv.Files.Log.write_to_log('Image ' + str(ref['old_name']) + ' already sourced')
                continue
            # # dict_list is list of {"service_name": service_name, "illust_id": illust_id, "source": source}

            global index
            gv.img_data_array.append(ImageData(ref['old_name'], ref['input_path'], dict_list, pixiv_illustration_list, danb_illustration_list, yandere_illustration_list, konachan_illustration_list, index))
            index += 1
        gv.Files.Log.write_to_log('Loaded images from reference file')
    else:
        gv.Files.Log.write_to_log('Reference file is empty')

def duplicate_loop():
    """
    Looks if a requested image has already been sourced with the same options and notifies the magic process
    """
    if duplicate_p_pipe.poll():
        dup_dict = duplicate_p_pipe.recv()
        is_dup = False
        for data in gv.img_data_array: # {'img_name': img, 'minsim': minsim, 'rename_pixiv': gv.Files.Conf.rename_pixiv, 'rename_danbooru': gv.Files.Conf.rename_danbooru}
            if str(dup_dict['img_name']) == data.name_original and str(dup_dict['minsim']) == str(data.minsim):
                is_dup = True
                break
        duplicate_p_pipe.send(is_dup)
    window.after(1, duplicate_loop)

def display_info():
    gv.Files.Log.log_text.place_forget()
    info_ScrollFrame.display(x = (width/3)*1.85, y = 100)

def display_logfile():
    info_ScrollFrame.sub_frame.place_forget()
    gv.Files.Log.log_text.place(x = (width/3)*1.85, y = int(height/9))

def forget_all_widgets():
    for widget in window.winfo_children():
        widget.place_forget()

def stop():
    """
    Stop further search for images and halt the magic process.
    """
    global process
    if process.is_alive():
        gv.Files.Log.write_to_log('Stopping sourcing process...')
        comm_stop_q.put("Stopped")
        stop_btn.configure(state='disabled')
    #currently_sourcing_img_lbl.configure(text="Stopped")

def lock_save():
    """
    Locks in selected images(ImageData) to save
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
    """
    Deletes files and folders scheduled to be deleted indicated by delete_dirs_array
    """
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
        background=[('pressed', '!disabled', gv.Files.Theme.button_background_pressed), ('disabled', 'black'), ('active', gv.Files.Theme.button_background_active)]
    )
    style.configure("frame.TFrame", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background)
    style.configure("optmen.TMenubutton", 
        foreground=gv.Files.Theme.foreground, 
        background=gv.Files.Theme.button_background, 
        activebackground=gv.Files.Theme.button_background,
        activeforeground=gv.Files.Theme.foreground, 
        highlightbackground=gv.Files.Theme.button_background,
        highlightcolor=gv.Files.Theme.foreground, 
        borderwidth=0, 
        font=("Arial Bold", 10))
    style.configure("chkbtn.TCheckbutton", 
        foreground=gv.Files.Theme.foreground, 
        background=gv.Files.Theme.background, 
        borderwidth = 0, 
        highlightthickness = 10, 
        font=("Arial Bold", 10)) # sunken, raised, groove, ridge, flat
    for elem in window.winfo_children():
        if type(elem) == type(cb()):
            elem.configure(
                foreground=gv.Files.Theme.foreground, 
                background=gv.Files.Theme.background, 
                selectcolor=gv.Files.Theme.checkbutton_pressed, 
                activebackground=gv.Files.Theme.button_background_active, 
                activeforeground=gv.Files.Theme.button_foreground_active, 
            )
    for elem in gv.res_frame.winfo_children():
        if type(elem) == type(cb()):
            elem.configure(
                foreground=gv.Files.Theme.foreground, 
                background=gv.Files.Theme.background, 
                selectcolor=gv.Files.Theme.checkbutton_pressed, 
                activebackground=gv.Files.Theme.button_background_active, 
                activeforeground=gv.Files.Theme.button_foreground_active, 
            )
    for elem in gv.big_frame.winfo_children():
        if type(elem) == type(cb()):
            elem.configure(
                foreground=gv.Files.Theme.foreground, 
                background=gv.Files.Theme.background, 
                selectcolor=gv.Files.Theme.checkbutton_pressed, 
                activebackground=gv.Files.Theme.button_background_active, 
                activeforeground=gv.Files.Theme.button_foreground_active, 
            )
    for elem in Options_Class.ProO.DanO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            elem.configure(
                foreground=gv.Files.Theme.foreground, 
                background=gv.Files.Theme.background, 
                font=("Arial Bold", 10)
            )
    for elem in Options_Class.ProO.PixO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            elem.configure(
                foreground=gv.Files.Theme.foreground, 
                background=gv.Files.Theme.background, 
                font=("Arial Bold", 10)
            )
        
    gv.Files.Log.log_text.configure(foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
    
    #style.configure("scroll.Vertical.TScrollbar", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.button_background, throughcolor=gv.Files.Theme.button_background, activebackground=gv.Files.Theme.button_background)
    results_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    info_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    big_selector_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    canvas_startpage.configure(background=gv.Files.Theme.background)
    Options_Class.ProO.PixO.scrollpar.canvas.configure(background=gv.Files.Theme.background)
    Options_Class.ProO.DanO.scrollpar.canvas.configure(background=gv.Files.Theme.background)
    Options_Class.ProO.Weight.scrollpar.canvas.configure(background=gv.Files.Theme.background)

if __name__ == '__main__':
    freeze_support()

    window = Tk()
    window.title("Sourcery")
    window.update_idletasks()
    window.state('zoomed')
    height = gv.height = window.winfo_screenheight()
    width = gv.width = window.winfo_screenwidth()
    results_frame_height = int(height*7/9)
    results_frame_width = int(width/3)
    info_frame_height = int(height*7/9)
    info_frame_width = int(width/3)
    big_selector_frame_height = int(height*7/9) # height-620
    big_selector_frame_width = int(width*0.12) # width-620
    #window.geometry(str(width-500) + 'x' + str(height-500))
    #dateS =  time.strftime("20%y-%m-%d")

    # set style
    results_ScrollFrame = ScrollFrame(window, results_frame_width, results_frame_height)
    info_ScrollFrame = ScrollFrame(window, info_frame_width, info_frame_height)
    gv.info_ScrollFrame = info_ScrollFrame
    big_selector_ScrollFrame = ScrollFrame(window, big_selector_frame_width, big_selector_frame_height)

    gv.res_frame = results_ScrollFrame.frame
    gv.big_frame = big_selector_ScrollFrame.frame
    gv.info_frame = info_ScrollFrame.frame


    gv.Files.Log.log_text = Text(master=window, height=int(info_frame_height/16), width=int(info_frame_width/7))
    gv.Files.Log.init_log()
    gv.Files.Log.write_to_log('Initialising variables...')

    sub_frame_startpage = Frame(window, width=width/5, height=height/5, style="frame.TFrame")
    canvas_startpage = Canvas(sub_frame_startpage, width=width/5, height=height/5, background=gv.Files.Theme.background, highlightthickness=0)
    frame_startpage = Frame(canvas_startpage, width=width/5, height=height/5, style="frame.TFrame")
    canvas_startpage.pack(side="left")
    canvas_startpage.create_window((0,0),window=frame_startpage,anchor='nw')

    Options_Class = Options(window, display_startpage, enforce_style)

    enforce_style()
    

    # widgets for start screen
    sourcery_lbl = Label(window, text="Sourcery", font=("Arial Bold", 50), style="label.TLabel")
    images_in_input_lbl = Label(frame_startpage, text="Images in Input folder:", style="label.TLabel")
    images_in_input_count_lbl = Label(frame_startpage, text="Number here", style="label.TLabel")
    currently_sourcing_lbl = Label(frame_startpage, text="Currently Sourcing:", style="label.TLabel")
    currently_sourcing_img_lbl = Label(frame_startpage, text="None", style="label.TLabel")
    remaining_searches_lbl = Label(frame_startpage, text="Remaining SauceNao\nsearches today:", style="label.TLabel")
    saucenao_requests_count_lbl = Label(frame_startpage, text="???/200", style="label.TLabel")
    #elapsed_time_lbl = Label(frame_startpage, text="Elapsed time:", style="label.TLabel")
    #eta_lbl = Label(frame_startpage, text="ETA:", style="label.TLabel")
    error_lbl = Label(frame_startpage, text="", style="label.TLabel")

    images_in_input_lbl.grid(row=0, column=0, sticky=W)
    images_in_input_count_lbl.grid(row=0, column=1, sticky=W, padx = 10)
    currently_sourcing_lbl.grid(row=1, column=0, sticky=W)
    currently_sourcing_img_lbl.grid(row=1, column=1, sticky=W, padx = 10)
    remaining_searches_lbl.grid(row=2, column=0, sticky=W)
    saucenao_requests_count_lbl.grid(row=2, column=1, sticky=W, padx = 10)
    #elapsed_time_lbl.grid(row= 5, column= 0)
    #eta_lbl.grid(row= 5, column= 0)
    error_lbl.grid(row=7, column=0, columnspan=3, sticky=W)

    change_input_btn = Button(window, text="Change Input", command=change_input, style="button.TLabel")
    open_input_btn = Button(window, text="Open Input", command=open_input, style="button.TLabel")
    change_output_btn = Button(window, text="Change Output", command=change_output, style="button.TLabel")
    open_output_btn = Button(window, text="Open Output", command=open_output, style="button.TLabel")
    #statistics_btn = Button(window, text="Statistics", command=display_statistics, style="button.TLabel")
    options_btn = Button(window, text="Options", command=Options_Class.display_sourcery_options, style="button.TLabel")
    do_sourcery_btn = Button(frame_startpage, text="Get Sources", command=magic, style="button.TLabel")
    stop_btn = Button(frame_startpage, text="Stop", command=stop, style="button.TLabel")
    #view_results_btn = Button(window, text="View Results", command=escape_results, style="button.TLabel")
    display_info_btn = Button(window, text="Image Info", command=display_info, style="button.TLabel")
    display_logfile_btn = Button(window, text="Log", command=display_logfile, style="button.TLabel")
    load_from_ref_btn = Button(frame_startpage, text="Load from Reference File", command=load_from_ref, style="button.TLabel")
    
    do_sourcery_btn.grid(row= 3, column= 0, sticky=W, pady = 1)
    stop_btn.grid(row= 4, column= 0, sticky=W, pady = 1)
    load_from_ref_btn.grid(row= 5, column= 0, sticky=W, pady = 1, columnspan=2)

    frame_startpage.columnconfigure(2, weight=1)

    # widgets for results
    results_lbl = Label(window, text="Results", font=("Arial Bold", 20), style="label.TLabel")
    lock_save_btn = Button(window, text="Lock selected", command=lock_save, style="button.TLabel")
    save_locked_btn = Button(window, text="Save selected images", command=save_locked, state = 'disabled', style="button.TLabel")

    
    gv.window = window
    gv.big_selector_frame = big_selector_ScrollFrame.sub_frame
    gv.big_selector_canvas = big_selector_ScrollFrame.canvas
    for i in range(int(gv.Files.Conf.imgpp)):
        gv.free_space.append(True)
    gv.display_startpage = display_startpage
    currently_processing = ''
    process = Process()
    comm_q = Queue() # Queue for 'Remaining searches'
    comm_img_q = Queue() # Queue for 'Currently Sourcing'
    comm_stop_q = Queue() # Queue for stop signal
    comm_error_q = Queue() # Queue for error messages
    img_data_q = Queue() # Queue for ImageData information
    duplicate_p_pipe, duplicate_c_pipe = Pipe()
    input_images_array = list()
    input_lock = Lock()
    #sem = Semaphore(12)
    gv.imgpp_sem = Semaphore(int(gv.Files.Conf.imgpp))
    #image_preloader()
    index = 0
    gv.Files.Log.write_to_log('Variables initialised')
    duplicate_loop()
    display_startpage()
    window.mainloop()