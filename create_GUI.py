
# __version__ = '0.1'
# __author__ = 'Cardinal Biggles'

from os import listdir, path, remove
from sys import stderr
from copy import copy
from multiprocessing import freeze_support
import time
from tkinter import Tk, IntVar, Canvas, Scrollbar, Text, END, W, simpledialog
from tkinter import Checkbutton as cb
from tkinter.ttk import Label, Button, Style, Entry, Frame
#from tkinter import messagebox as mb
#from tkinter.filedialog import askdirectory
#from functools import partial
from shutil import rmtree
from copy import deepcopy
#from distutils.util import strtobool
from threading import Thread
from file_operations import is_image, save, open_input, open_output, display_statistics, change_input, change_output
from sourcery import do_sourcery
from pixiv_handler import pixiv_fetch_illustration
from danbooru_handler import danbooru_fetch_illustration
from Options import Options
#from image_preloader import preload_main
from ImageData import ImageData
from DIllustration import DIllustration
from ScrollFrame import ScrollFrame
from Startpage import Startpage
from Files import Files
import global_variables as gv

#stderr = gv.Files.Log

def load_from_ref():
    c = simpledialog.askinteger(title='How many?', prompt='How many images would you like to load?')
    if c != None:
        ref_thread = Thread(target=load_from_ref_run, args=[c], daemon=True)
        ref_thread.start()
        Startpage_Class.do_sourcery_btn.configure(state='disabled')
        Startpage_Class.load_from_ref_btn.configure(state='disabled')

def load_from_ref_run(c):
    """
    Loads images whose info has been saved in the reference file
    """
    gv.Files.Ref.read_reference()
    #refs = deepcopy()#gv.Files.Ref.read_reference()
    gv.Files.Log.write_to_log('Loading images from reference file...')
    for ref in gv.Files.Ref.refs:
        if c == 0:
            break
        
        pixiv_info_list = list(ref['pixiv'])
        danb_info_list = list(ref['danbooru'])
        yandere_info_list = list(ref['yandere'])
        konachan_info_list = list(ref['konachan'])
        dict_list = ref['dict_list']

        pixiv_illustration_list = list()
        visited_ids = list()
        for elem in pixiv_info_list:
            if elem['id'] not in visited_ids:
                x = None
                for d in dict_list:
                    if d['service_name'] == 'Pixiv' and int(d['illust_id']) == int(elem['id']):
                        x = d
                        break
                if x != None:
                    pixiv_illustration_list.append((pixiv_fetch_illustration(ref['old_name'], int(elem['id'])), elem['new_name'], x))
                visited_ids.append(elem['id'])
        
        danb_illustration_list = list()
        visited_ids = list()
        for elem in danb_info_list:
            if elem['id'] not in visited_ids:
                x = None
                for d in dict_list:
                    if d['service_name'] == 'Danbooru' and int(d['illust_id']) == int(elem['id']):
                        x = d
                        break
                if x != None:
                    danb_illustration_list.append((danbooru_fetch_illustration(int(elem['id']), danbooru=True), elem['new_name'], x))
                visited_ids.append(elem['id'])
        
        yandere_illustration_list = list()
        visited_ids = list()
        for elem in yandere_info_list:
            if elem['id'] not in visited_ids:
                x = None
                for d in dict_list:
                    if d['service_name'] == 'Yandere' and int(d['illust_id']) == int(elem['id']):
                        x = d
                        break
                if x != None:
                    yandere_illustration_list.append((danbooru_fetch_illustration(int(elem['id']), yandere=True), elem['new_name'], x))
                visited_ids.append(elem['id'])
        
        konachan_illustration_list = list()
        visited_ids = list()
        for elem in konachan_info_list:
            if elem['id'] not in visited_ids:
                x = None
                for d in dict_list:
                    if d['service_name'] == 'Konachan' and int(d['illust_id']) == int(elem['id']):
                        x = d
                        break
                if x != None:
                    konachan_illustration_list.append((danbooru_fetch_illustration(int(elem['id']), konachan=True), elem['new_name'], x))
                visited_ids.append(elem['id'])
        
        next_img = False
        for data in gv.img_data_array:
            if str(ref['old_name']) == data.sub_dill.name and str(ref['minsim']) == gv.config.getint('SauceNAO', 'minsim'):
                next_img = True
                break
        if len(pixiv_illustration_list) == 0 and len(danb_illustration_list) == 0 and len(yandere_illustration_list) == 0 and len(konachan_illustration_list) == 0:
            next_img = True
        if not next_img:
            # dict_list is list of {"service_name": service_name, "illust_id": illust_id, "source": source}
            dill = DIllustration(ref['input_path'], [{"service":'Original', "name":str(ref['old_name']), "work_path": gv.cwd + '/Sourcery/sourced_original/' + str(ref['old_name'])}, 
            pixiv_illustration_list, danb_illustration_list, yandere_illustration_list, konachan_illustration_list], ref, ref['minsim'])
            Startpage_Class.Processing_Class.img_data_q.put(dill)
            c -= 1
        # else:
        #     gv.Files.Log.write_to_log('Image ' + str(ref['old_name']) + ' already sourced or no sources found')
    gv.Files.Log.write_to_log('Loaded images from reference file or Reference file is empty')
    Startpage_Class.do_sourcery_btn.configure(state='enabled')
    Startpage_Class.load_from_ref_btn.configure(state='enabled')

def forget_all_widgets():
    for widget in window.winfo_children():
        widget.place_forget()

def lock_save():
    """
    Locks in selected images(ImageData) to save
    """
    data_list = copy(gv.img_data_array)
    for data in data_list:
        if data.display_results_init:
            data.lock()
    Startpage_Class.save_locked_btn.configure(state='enabled')
    
def save_locked():
    """
    Save locked images from results page
    """
    gv.Files.Log.write_to_log('Saving selected images...')
    if save():
        gv.Files.Log.write_to_log('Saved images')
    else:
        gv.Files.Log.write_to_log('Cancelled saving images')
    Startpage_Class.results_ScrollFrame.display(x = int(width/16*4), y = int(height/9))
    leftovers()
    Startpage_Class.save_locked_btn.configure(state='disabled')

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
            try:
                elem.configure(
                    foreground=gv.Files.Theme.foreground, 
                    background=gv.Files.Theme.background, 
                    selectcolor=gv.Files.Theme.checkbutton_pressed, 
                    activebackground=gv.Files.Theme.button_background_active, 
                    activeforeground=gv.Files.Theme.button_foreground_active, 
                )
            except:
                pass
    for elem in gv.res_frame.winfo_children():
        if type(elem) == type(cb()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.foreground, 
                    background=gv.Files.Theme.background, 
                    selectcolor=gv.Files.Theme.checkbutton_pressed, 
                    activebackground=gv.Files.Theme.button_background_active, 
                    activeforeground=gv.Files.Theme.button_foreground_active, 
                )
            except:
                pass
    for elem in gv.big_frame.winfo_children():
        if type(elem) == type(cb()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.foreground, 
                    background=gv.Files.Theme.background, 
                    selectcolor=gv.Files.Theme.checkbutton_pressed, 
                    activebackground=gv.Files.Theme.button_background_active, 
                    activeforeground=gv.Files.Theme.button_foreground_active, 
                )
            except:
                pass
    for elem in Options_Class.ProO.DanO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.foreground, 
                    background=gv.Files.Theme.background, 
                    font=("Arial Bold", 10)
                )
            except:
                pass
    for elem in Options_Class.ProO.PixO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.foreground, 
                    background=gv.Files.Theme.background, 
                    font=("Arial Bold", 10)
                )
            except:
                pass
    for elem in Options_Class.ProO.YanO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.foreground, 
                    background=gv.Files.Theme.background, 
                    font=("Arial Bold", 10)
                )
            except:
                pass
    for elem in Options_Class.ProO.KonO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.foreground, 
                    background=gv.Files.Theme.background, 
                    font=("Arial Bold", 10)
                )
            except:
                pass
        
    gv.Files.Log.log_text.configure(foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
    
    #style.configure("scroll.Vertical.TScrollbar", foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.button_background, throughcolor=gv.Files.Theme.button_background, activebackground=gv.Files.Theme.button_background)
    Startpage_Class.results_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    Startpage_Class.info_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    Startpage_Class.big_selector_ScrollFrame.canvas.configure(background=gv.Files.Theme.background)
    Startpage_Class.canvas_startpage.configure(background=gv.Files.Theme.background)
    Options_Class.ProO.PixO.scrollpar.canvas.configure(background=gv.Files.Theme.background)
    Options_Class.ProO.DanO.scrollpar.canvas.configure(background=gv.Files.Theme.background)
    Options_Class.ProO.Weight.scrollpar.canvas.configure(background=gv.Files.Theme.background)

if __name__ == '__main__':
    freeze_support()

    window = gv.window = Tk()
    window.title("Sourcery")
    #window.update_idletasks()
    window.state('zoomed')
    height = gv.height = window.winfo_screenheight()
    width = gv.width = window.winfo_screenwidth()
    #window.geometry(str(width-500) + 'x' + str(height-500))
    #dateS =  time.strftime("20%y-%m-%d")

    gv.Files.Log.log_text = Text(window, height=int(gv.height*7/9/16), width=int(gv.width/3/7))
    gv.Files.Log.init_log()
    gv.Files.Log.write_to_log('Initialising variables...')

    Options_Class = Options(window, enforce_style)
    Startpage_Class = Startpage(window, Options_Class, load_from_ref, lock_save, save_locked)
    gv.display_startpage = Startpage_Class.display_startpage
    
    enforce_style() 

    startpage_update_thread = Thread(target=Startpage_Class.refresh_startpage, daemon=True, name="startpage_update")

    gv.Files.Log.write_to_log('Variables initialised')
    Startpage_Class.Processing_Class.duplicate_loop()
    Startpage_Class.Processing_Class.terminate_loop()
    startpage_update_thread.start()
    Startpage_Class.display_startpage()
    
    window.mainloop()