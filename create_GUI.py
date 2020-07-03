
# __version__ = '0.1'
# __author__ = 'Cardinal Biggles'

from os import listdir, path, remove
from copy import copy, deepcopy
from multiprocessing import freeze_support
import time
from tkinter import Tk, IntVar, Canvas, Scrollbar, Text, END, W, simpledialog
from tkinter import Checkbutton as cb
from tkinter.ttk import Label, Button, Style, Entry, Frame
#from tkinter import messagebox as mb
#from tkinter.filedialog import askdirectory
#from functools import partial
from shutil import rmtree
#from distutils.util import strtobool
from threading import Thread
import logging as log
from file_operations import is_image, save, open_input, open_output, display_statistics, change_input, change_output
from sourcery import do_sourcery
from pixiv_handler import pixiv_fetch_illustration
from booru_handler import booru_fetch_illustration
from Options import Options
#from image_preloader import preload_main
from ImageData import ImageData
from DIllustration import DIllustration
from ScrollFrame import ScrollFrame
from Startpage import Startpage
from Files import Files
import global_variables as gv
#from atexit import register


def load_from_ref():
    c = simpledialog.askinteger(title='How many?', prompt='How many images would you like to load?')
    if c != None:
        ref_thread = Thread(target=load_from_ref_run, args=[c], daemon=True)
        ref_thread.start()
        #window.after(0, load_from_ref_run, c)
        Startpage_Class.do_sourcery_btn.configure(state='disabled')
        Startpage_Class.load_from_ref_btn.configure(state='disabled')

def load_from_ref_run(c):
    """
    Loads images whose info has been saved in the reference file
    """
    gv.Files.Ref.read_reference()
    loaded_counter = 0
    duplicates_counter = 0
    no_sources_counter = 0
    #refs = deepcopy()#gv.Files.Ref.read_reference()
    gv.Logger.write_to_log('Loading images from reference file...', log.INFO)
    for ref in gv.Files.Ref.refs:
        if c == 0:
            break
        
        pixiv_info_list = list(ref['pixiv'])
        danb_info_list = list(ref['danbooru'])
        yandere_info_list = list(ref['yandere'])
        konachan_info_list = list(ref['konachan'])
        if 'gelbooru' in ref:
            gelbooru_info_list = list(ref['gelbooru'])
        else:
            gelbooru_info_list = list()
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
        
        login_dict = {"gelbooru_api_key":gv.config.get('Gelbooru','api_key'), "gelbooru_user_id":gv.config.get('Gelbooru','user_id')}
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
                    
                    danb_illustration_list.append((booru_fetch_illustration(int(elem['id']), 'Danbooru', login_dict), elem['new_name'], x))
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
                    yandere_illustration_list.append((booru_fetch_illustration(int(elem['id']), 'Yandere', login_dict), elem['new_name'], x))
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
                    konachan_illustration_list.append((booru_fetch_illustration(int(elem['id']), 'Konachan', login_dict), elem['new_name'], x))
                visited_ids.append(elem['id'])
        
        gelbooru_illustration_list = list()
        visited_ids = list()
        for elem in gelbooru_info_list:
            if elem['id'] not in visited_ids:
                x = None
                for d in dict_list:
                    if d['service_name'] == 'Gelbooru' and int(d['illust_id']) == int(elem['id']):
                        x = d
                        break
                if x != None:
                    gelbooru_illustration_list.append((booru_fetch_illustration(int(elem['id']), 'Gelbooru', login_dict), elem['new_name'], x))
                visited_ids.append(elem['id'])
        
        next_img = False
        for data in gv.img_data_array:
            if str(ref['old_name']) == data.sub_dill.name and int(ref['minsim']) == gv.config.getint('SauceNAO', 'minsim'):
                next_img = True
                duplicates_counter += 1
                break
        if len(pixiv_illustration_list) == 0 and len(danb_illustration_list) == 0 and len(yandere_illustration_list) == 0 and len(konachan_illustration_list) == 0 and len(gelbooru_illustration_list) == 0:
            next_img = True
            no_sources_counter += 1
        if not next_img:
            # dict_list is list of {"service_name": service_name, "illust_id": illust_id, "source": source}
            dill = DIllustration(ref['input_path'], [{"service":'Original', "name":str(ref['old_name']), "work_path": gv.cwd + '/Sourcery/sourced_original/' + str(ref['old_name'])}, 
                pixiv_illustration_list, danb_illustration_list, yandere_illustration_list, konachan_illustration_list, gelbooru_illustration_list], ref, ref['minsim'])
            Startpage_Class.Processing_Class.img_data_q.put(dill)
            c -= 1
            loaded_counter += 1
    if len(gv.Files.Ref.refs) == 0:
        gv.Logger.write_to_log('Reference file is empty', log.INFO)
    else:
        gv.Logger.write_to_log('References: ' + str(len(gv.Files.Ref.refs)))
        gv.Logger.write_to_log('Loaded ' + str(loaded_counter) + ' images from reference file', log.INFO)
        gv.Logger.write_to_log('Skipped ' + str(duplicates_counter) + ' images because they were already loaded', log.INFO)
        gv.Logger.write_to_log('Skipped ' + str(no_sources_counter) + ' images because no sources were found', log.INFO)
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
    gv.Logger.write_to_log('Saving selected images...', log.INFO)
    if save():
        gv.Logger.write_to_log('Saved images', log.INFO)
    else:
        gv.Logger.write_to_log('Cancelled saving images', log.INFO)
    Startpage_Class.results_ScrollFrame.display(x = int(width/16*4), y = int(height/9))
    leftovers()
    Startpage_Class.save_locked_btn.configure(state='disabled')

#def new_save_system():
    # call before leftovers
    # takes list with tuples: (src, dest, Error1=None/False, Error2=None/False)
    # copies for every elem in list from src to dst, 
    # if error, write in Error1 and try again, 
    # if error, write in Error2 and remove from delete_dirs_array

def leftovers(delete_list=None):
    """
    Deletes files and folders scheduled to be deleted indicated by delete_dirs_array
    """
    # # Delete leftovers
    # if not process.is_alive():
    #     for img in listdir(gv.cwd + '/Sourcery/sourced_original'):
    #         if gv.cwd + '/Sourcery/sourced_original' + img not in gv.delete_dirs_array:
    #             gv.delete_dirs_array.append(gv.cwd + '/Sourcery/sourced_original' + img)

    gv.Logger.write_to_log('Deleting empty folders, leftovers etc. ...', log.INFO)
    if delete_list == None:
        delete_list = gv.delete_dirs_array
    for element in delete_list:
        try:
            if path.isdir(element):
                rmtree(element)
            elif path.isfile(element):
                remove(element)
        except Exception as e:
            print('ERROR [0017] ' + str(e))
            gv.Logger.write_to_log("ERROR [0017] " + str(e), log.ERROR)
            #mb.showerror("ERROR", "ERROR CODE [0017]\nSomething went wrong while removing the image " + element)

    delete_list.clear()
    gv.Logger.write_to_log('Deleted stuff', log.INFO)

def enforce_style():
    """
    Changes style of all widgets to the currently selected theme.
    """
    #gv.Files.Theme.theme[theme]['read_theme()
    theme = gv.Files.Theme.theme['General']['current']
    window.configure(bg=gv.Files.Theme.theme[theme]['background'])
    style = Style()
    style.configure("label.TLabel", foreground=gv.Files.Theme.theme[theme]['foreground'], background=gv.Files.Theme.theme[theme]['background'], font=("Arial Bold", 10))
    style.configure("button.TLabel", foreground=gv.Files.Theme.theme[theme]['foreground'], background=gv.Files.Theme.theme[theme]['button_background'], font=("Arial Bold", 10))
    style.map("button.TLabel",
        foreground=[('pressed', gv.Files.Theme.theme[theme]['button_foreground_pressed']), ('active', gv.Files.Theme.theme[theme]['button_foreground_active'])],
        background=[('pressed', '!disabled', gv.Files.Theme.theme[theme]['button_background_pressed']), ('disabled', 'black'), ('active', gv.Files.Theme.theme[theme]['button_background_active'])]
    )
    style.configure("frame.TFrame", foreground=gv.Files.Theme.theme[theme]['foreground'], background=gv.Files.Theme.theme[theme]['background'])
    style.configure("optmen.TMenubutton", 
        foreground=gv.Files.Theme.theme[theme]['foreground'], 
        background=gv.Files.Theme.theme[theme]['button_background'], 
        activebackground=gv.Files.Theme.theme[theme]['button_background'],
        activeforeground=gv.Files.Theme.theme[theme]['foreground'], 
        highlightbackground=gv.Files.Theme.theme[theme]['button_background'],
        highlightcolor=gv.Files.Theme.theme[theme]['foreground'], 
        borderwidth=0, 
        font=("Arial Bold", 10))
    style.configure("chkbtn.TCheckbutton", 
        foreground=gv.Files.Theme.theme[theme]['foreground'], 
        background=gv.Files.Theme.theme[theme]['background'], 
        borderwidth = 0, 
        highlightthickness = 10, 
        font=("Arial Bold", 10)) # sunken, raised, groove, ridge, flat
    for elem in window.winfo_children():
        if type(elem) == type(cb()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.theme[theme]['foreground'], 
                    background=gv.Files.Theme.theme[theme]['background'], 
                    selectcolor=gv.Files.Theme.theme[theme]['checkbutton_pressed'], 
                    activebackground=gv.Files.Theme.theme[theme]['button_background_active'], 
                    activeforeground=gv.Files.Theme.theme[theme]['button_foreground_active'], 
                )
            except:
                pass
    for elem in gv.res_frame.winfo_children():
        if type(elem) == type(cb()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.theme[theme]['foreground'], 
                    background=gv.Files.Theme.theme[theme]['background'], 
                    selectcolor=gv.Files.Theme.theme[theme]['checkbutton_pressed'], 
                    activebackground=gv.Files.Theme.theme[theme]['button_background_active'], 
                    activeforeground=gv.Files.Theme.theme[theme]['button_foreground_active'], 
                )
            except:
                pass
    for elem in gv.big_frame.winfo_children():
        if type(elem) == type(cb()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.theme[theme]['foreground'], 
                    background=gv.Files.Theme.theme[theme]['background'], 
                    selectcolor=gv.Files.Theme.theme[theme]['checkbutton_pressed'], 
                    activebackground=gv.Files.Theme.theme[theme]['button_background_active'], 
                    activeforeground=gv.Files.Theme.theme[theme]['button_foreground_active'], 
                )
            except:
                pass
    for elem in Options_Class.ProO.DanO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.theme[theme]['foreground'], 
                    background=gv.Files.Theme.theme[theme]['background'], 
                    font=("Arial Bold", 10)
                )
            except:
                pass
    for elem in Options_Class.ProO.PixO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.theme[theme]['foreground'], 
                    background=gv.Files.Theme.theme[theme]['background'], 
                    font=("Arial Bold", 10)
                )
            except:
                pass
    for elem in Options_Class.ProO.YanO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.theme[theme]['foreground'], 
                    background=gv.Files.Theme.theme[theme]['background'], 
                    font=("Arial Bold", 10)
                )
            except:
                pass
    for elem in Options_Class.ProO.KonO.scrollpar_frame.winfo_children():
        if type(elem) == type(Text()):
            try:
                elem.configure(
                    foreground=gv.Files.Theme.theme[theme]['foreground'], 
                    background=gv.Files.Theme.theme[theme]['background'], 
                    font=("Arial Bold", 10)
                )
            except:
                pass
        
    gv.Logger.log_text.configure(foreground=gv.Files.Theme.theme[theme]['foreground'], background=gv.Files.Theme.theme[theme]['background'], font=("Arial Bold", 10))
    
    #style.configure("scroll.Vertical.TScrollbar", foreground=gv.Files.Theme.theme[theme]['foreground'], background=gv.Files.Theme.theme[theme]['button_background'], throughcolor=gv.Files.Theme.theme[theme]['button_background'], activebackground=gv.Files.Theme.theme[theme]['button_background'])
    Startpage_Class.results_ScrollFrame.canvas.configure(background=gv.Files.Theme.theme[theme]['background'])
    Startpage_Class.info_ScrollFrame.canvas.configure(background=gv.Files.Theme.theme[theme]['background'])
    Startpage_Class.big_selector_ScrollFrame.canvas.configure(background=gv.Files.Theme.theme[theme]['background'])
    Startpage_Class.canvas_startpage.configure(background=gv.Files.Theme.theme[theme]['background'])
    Options_Class.ProO.PixO.scrollpar.canvas.configure(background=gv.Files.Theme.theme[theme]['background'])
    Options_Class.ProO.DanO.scrollpar.canvas.configure(background=gv.Files.Theme.theme[theme]['background'])
    Options_Class.ProO.Weight.scrollpar.canvas.configure(background=gv.Files.Theme.theme[theme]['background'])

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

    gv.Logger.log_text = Text(window, height=int(gv.height*7/9/16), width=int(gv.width/3/7))
    gv.Logger.init_log()
    log.info('Initialising variables...')

    Options_Class = Options(window, enforce_style, leftovers)
    Startpage_Class = gv.Startpage_Class = Startpage(window, Options_Class, load_from_ref, lock_save, save_locked)
    gv.display_startpage = Startpage_Class.display_startpage
    
    enforce_style() 

    log.info('Variables initialised')
    Startpage_Class.Processing_Class.duplicate_loop()
    Startpage_Class.Processing_Class.terminate_loop()
    Startpage_Class.refresh_startpage()
    Startpage_Class.display_startpage()
    window.mainloop()