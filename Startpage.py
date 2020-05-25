from os import listdir, path, remove
from shutil import rmtree
from multiprocessing import Lock
from threading import Thread, enumerate as enu
import time
from tkinter import Tk, IntVar, Canvas, Scrollbar, Text, END, W, simpledialog
from tkinter import Checkbutton as cb
from tkinter.ttk import Label, Button, Style, Entry, Frame, Checkbutton
import logging as log
from ScrollFrame import ScrollFrame
from Files import Files
from ImageData import ImageData
from Processing import Processing
from file_operations import is_image
from file_operations import is_image, save, open_input, open_output, display_statistics, change_input, change_output
import global_variables as gv


class Startpage():
    """Includes all startpage widgets and methods"""
    def __init__(self, window, options_class, load_from_ref, lock_save, save_locked):
        self.Processing_Class = Processing(self)
        self.Options_Class = options_class
        self.Options_Class.options_back_btn.configure(command=self.display_startpage)
        self.window = window
        self.input_images_array = list()

        startpage_frame_height = int(gv.height/3)
        startpage_frame_width = int(gv.width/5)
        gv.res_frame_height = results_frame_height = int(gv.height*7/9)
        gv.res_frame_width = results_frame_width = int(gv.width/3)
        gv.info_frame_height = info_frame_height = int(gv.height*7/9)
        gv.info_frame_width = info_frame_width = int(gv.width/3)
        gv.big_frame_height = big_selector_frame_height = int(gv.height*7/9)
        gv.big_frame_width = big_selector_frame_width = int(gv.width*0.12)

        self.results_ScrollFrame = ScrollFrame(window, gv.res_frame_width, gv.res_frame_height)
        self.info_ScrollFrame = gv.info_ScrollFrame = ScrollFrame(window, gv.info_frame_width, gv.info_frame_height)
        self.big_selector_ScrollFrame = ScrollFrame(window, gv.big_frame_width, gv.big_frame_height)

        gv.res_frame = self.results_ScrollFrame.frame
        gv.big_frame = self.big_selector_ScrollFrame.frame
        gv.info_frame = self.info_ScrollFrame.frame
        gv.big_selector_frame = self.big_selector_ScrollFrame.sub_frame
        gv.big_selector_canvas = self.big_selector_ScrollFrame.canvas

        theme = gv.Files.Theme.theme['General']['current']
        self.sub_frame_startpage = Frame(window, width=startpage_frame_width, height=startpage_frame_height, style="frame.TFrame")
        self.canvas_startpage = Canvas(self.sub_frame_startpage, width=startpage_frame_width, height=startpage_frame_height, background=gv.Files.Theme.theme[theme]['background'], highlightthickness=0)
        self.frame_startpage = Frame(self.canvas_startpage, width=startpage_frame_width, height=startpage_frame_height, style="frame.TFrame")
        self.canvas_startpage.pack(side="left")
        self.canvas_startpage.create_window((0,0),window=self.frame_startpage,anchor='nw')

        # widgets for start screen
        self.sourcery_lbl = Label(window, text="Sourcery", font=("Arial Bold", 50), style="label.TLabel")
        self.images_in_input_lbl = Label(self.frame_startpage, text="Images in Input folder:", style="label.TLabel")
        self.images_in_input_count_lbl = Label(self.frame_startpage, text="Number here", style="label.TLabel")
        self.currently_sourcing_lbl = Label(self.frame_startpage, text="Currently Sourcing:", style="label.TLabel")
        self.currently_sourcing_img_lbl = Label(self.frame_startpage, text="None", wraplength=startpage_frame_width/2.4, style="label.TLabel")
        self.remaining_searches_lbl = Label(self.frame_startpage, text="Remaining SauceNao\nsearches today:", style="label.TLabel")
        self.saucenao_requests_count_lbl = Label(self.frame_startpage, text="???/200", style="label.TLabel")
        #self.elapsed_time_lbl = Label(self.frame_startpage, text="Elapsed time:", style="label.TLabel")
        #self.eta_lbl = Label(self.frame_startpage, text="ETA:", style="label.TLabel")
        self.error_lbl = Label(self.frame_startpage, text="", wraplength=startpage_frame_width-10, style="label.TLabel")

        self.change_input_btn = Button(window, text="Change Input", command=change_input, style="button.TLabel")
        self.open_input_btn = Button(window, text="Open Input", command=open_input, style="button.TLabel")
        self.change_output_btn = Button(window, text="Change Output", command=change_output, style="button.TLabel")
        self.open_output_btn = Button(window, text="Open Output", command=open_output, style="button.TLabel")
        #self.statistics_btn = Button(window, text="Statistics", command=display_statistics, style="button.TLabel")
        self.options_btn = Button(window, text="Options", command=self.Options_Class.display_sourcery_options, style="button.TLabel")
        self.do_sourcery_btn = Button(self.frame_startpage, text="Get Sources", command=self.Processing_Class.magic, style="button.TLabel")
        self.stop_btn = Button(self.frame_startpage, text="Stop", command=self.Processing_Class.stop, style="button.TLabel")
        #self.view_results_btn = Button(window, text="View Results", command=escape_results, style="button.TLabel")
        self.display_info_btn = Button(window, text="Image Info", command=self.display_info, style="button.TLabel")
        self.display_logfile_btn = Button(window, text="Log", command=self.display_logfile, style="button.TLabel")
        self.load_from_ref_btn = Button(self.frame_startpage, text="Load from Reference File", command=load_from_ref, style="button.TLabel")
        
        
        self.frame_startpage.columnconfigure(2, weight=1)

        # widgets for results
        self.results_lbl = Label(window, text="Results", font=("Arial Bold", 20), style="label.TLabel")
        self.lock_save_btn = Button(window, text="Lock selected", command=lock_save, style="button.TLabel")
        self.save_locked_btn = Button(window, text="Save selected images", command=save_locked, state = 'disabled', style="button.TLabel")
        def c():
            gv.config['DEFAULT']['jump_log'] = str(self.jump_log_var.get())
        self.jump_log_var = IntVar(value=gv.config.getint('DEFAULT', 'jump_log'))
        theme = gv.Files.Theme.theme['General']['current']
        self.jump_log_chkbtn = cb(window, text="Jump to newest entry", var=self.jump_log_var, command=c,
            foreground=gv.Files.Theme.theme[theme]['foreground'], 
            background=gv.Files.Theme.theme[theme]['background'], 
            borderwidth = 1,
            highlightthickness = 0, 
            selectcolor=gv.Files.Theme.theme[theme]['checkbutton_pressed'], 
            activebackground=gv.Files.Theme.theme[theme]['button_background_active'], 
            activeforeground=gv.Files.Theme.theme[theme]['button_foreground_active'], 
            relief='flat',#default flat
            overrelief='ridge',#no default
            offrelief='flat',#default raised
            indicatoron='false')# sunken, raised, groove, ridge, flat, style="chkbtn.TCheckbutton")

        self.index = 0
        self.input_lock = Lock()

    def display_startpage(self):
        """
        Draws the basic startpage widgets.
        """
        self.Options_Class.SouO.color_insert()
        self.forget_all_widgets()
        x = int(gv.height/160*2)
        y = int(gv.height/9)
        c = 22

        self.sourcery_lbl.place(x = x, y = int(gv.height/160))
        self.sub_frame_startpage.place(x = x, y = y  + c * 6)

        #self.change_input_btn.place(x = x, y = y + c * 0)
        self.open_input_btn.place(x = x, y = y + c * 1)
        #self.change_output_btn.place(x = x, y = y + c * 2)
        self.open_output_btn.place(x = x, y = y + c * 2)
        self.options_btn.place(x = x, y = y + c * 3)
        
        self.images_in_input_lbl.grid(row=0, column=0, sticky=W)
        self.images_in_input_count_lbl.grid(row=0, column=1, sticky=W, padx = 10)
        self.currently_sourcing_lbl.grid(row=1, column=0, sticky=W)
        self.currently_sourcing_img_lbl.grid(row=1, column=1, sticky=W, padx = 10)
        self.remaining_searches_lbl.grid(row=2, column=0, sticky=W)
        self.saucenao_requests_count_lbl.grid(row=2, column=1, sticky=W, padx = 10)
        #self.elapsed_time_lbl.grid(row= 5, column= 0)
        #self.eta_lbl.grid(row= 5, column= 0)
        self.error_lbl.grid(row=7, column=0, columnspan=3, sticky=W)

        self.do_sourcery_btn.grid(row= 3, column= 0, sticky=W, pady = 1)
        self.stop_btn.grid(row= 4, column= 0, sticky=W, pady = 1)
        self.load_from_ref_btn.grid(row= 5, column= 0, sticky=W, pady = 1, columnspan=2)

        self.results_lbl.place(x = int(gv.width/16*4), y = int(gv.height/90*6))
        self.save_locked_btn.place(x = int(gv.width*0.48), y = int(gv.height*0.9))
        self.lock_save_btn.place(x = int(gv.width*0.4), y = int(gv.height*0.9))
        self.results_ScrollFrame.display(x = int(gv.width/16*4), y = int(gv.height/9))

        self.display_logfile()

        self.display_info_btn.place(x = int(gv.width*0.7), y = int(gv.height/90*6))
        self.display_logfile_btn.place(x = int(gv.width*0.8), y = int(gv.height/90*6))

    def list_input(self, directory_list, directory, depth):
        add = list()
        for elem in directory_list:
            if path.isfile(directory + '/' + elem) or depth == 0:
                add.append(directory + '/' + elem)
            elif path.isdir(directory + '/' + elem):
                add.extend(list_input(listdir(directory + '/' + elem), directory + '/' + elem, depth-1))
        return add

    def count_input(self):
        self.input_lock.acquire()
        try:
            self.input_images_array = self.list_input(listdir(gv.input_dir), gv.input_dir, gv.config.getint('Sourcery', 'input_search_depth'))
            self.input_images_array.extend(listdir(gv.input_dir))
        except Exception as e:
            print('ERROR [0040] ' + str(e))
            gv.Files.Log.write_to_log('ERROR [0040] ' + str(e), log.ERROR)
            #mb.showerror("ERROR [0040]", "ERROR CODE [0040]\nSomething went wrong while accessing a the 'Input' folder, please restart Sourcery.")
        delete = list()
        for img in self.input_images_array:
            if (not is_image(img)) or not path.isfile(img):
                delete.append(img)
        for elem in delete:
            if elem in self.input_images_array:
                self.input_images_array.remove(elem)
        self.input_lock.release()
        def update(text):
            self.images_in_input_count_lbl.configure(text=text)
        self.window.after(0, update, str(len(self.input_images_array)))

    def make_image_data(self):
        if not self.Processing_Class.img_data_q.empty():
            b = None
            try:
                b = ImageData(self.Processing_Class.img_data_q.get(False), self.index)
                self.index += 1
                gv.img_data_array.append(b)
            except Exception as e:
                if b in gv.img_data_array:
                    gv.img_data_array.remove(b)
                print("ERROR [0060] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0060] " + str(e), log.ERROR)
                #mb.showerror("ERROR [0060]", "ERROR CODE [0060]\nImage data could not be loaded, skipped.")
        self.window.after(100, self.make_image_data)
            
    def load_image_data(self):
        for data in gv.img_data_array:
            if not data.placed and gv.imgpp_sem.acquire(False):
                load = data.load()
                if not load:
                    data.self_destruct()
                    gv.img_data_array.remove(data)
                    gv.Files.Log.write_to_log('Problem while loading images, skipped', log.INFO)
                elif load:
                    data.init_widgets()
                    data.process_results_imgs()
                    data.modify_results_widgets()
                    x = data.display_results(gv.last_occupied_result+1)
                    if x == -1:# This means direct replace has triggered
                        gv.Files.Log.write_to_log('Saving image:' + data.sub_dill.name + '...' , log.INFO)
                        if data.save():
                            gv.Files.Log.write_to_log('Successfully saved image', log.INFO)
                            data.self_destruct()
                        else:
                            gv.Files.Log.write_to_log('Did not save image', log.INFO)# TODO delete reference
                        gv.img_data_array.remove(data)
                    else:
                        gv.last_occupied_result = x
                    data.placed = True
        self.window.after(100, self.load_image_data)

    def get_processing_status(self, answer2='', currently_processing=''):
        answer1 = (201, 200)
        try:
            answer1 = self.Processing_Class.comm_q.get(False)
            self.saucenao_requests_count_lbl.configure(text=str(answer1[0]) + "/" + str(answer1[1]))
        except:
            pass
        if not self.Processing_Class.comm_img_q.empty():
            if answer1[0] < 1:
                answer2 = "Out of requests"
            else:
                try:
                    answer2 = self.Processing_Class.comm_img_q.get(False)
                    if answer2 != currently_processing:
                        currently_processing = answer2
                except:
                    pass
            self.currently_sourcing_img_lbl.configure(text=answer2)
        if answer2 == 'Stopped' or answer2 == 'Finished':
            if self.Processing_Class.comm_error_q.empty():
                gv.Files.Log.write_to_log('Sourcing process was stopped or is finished', log.INFO)
                self.do_sourcery_btn.configure(state='enabled')
                self.load_from_ref_btn.configure(state='enabled')
                self.stop_btn.configure(state='enabled')
                answer2 = ''
        try:
            e = self.Processing_Class.comm_error_q.get(False)
            if e.startswith('DELETE'):
                try:
                    if path.isdir(e[6:]):
                        rmtree(e[6:])
                    elif path.isfile(e[6:]):
                        remove(e[6:])
                except Exception as e:
                    print('ERROR [0067] ' + str(e))
                    gv.Files.Log.write_to_log("ERROR [0067] " + str(e), log.ERROR)
                    #mb.showerror("ERROR", "ERROR CODE [0067]\nSomething went wrong while removing the image " + element)
            else:
                self.error_lbl.configure(text=e)
                gv.Files.Log.write_to_log(e, log.ERROR)
        except:
            pass
        self.window.after(100, self.get_processing_status, answer2, currently_processing)
        #return answer2, currently_processing

    def jump_log(self):
        if gv.config.getboolean('DEFAULT', 'jump_log'):
            gv.Files.Log.log_text.yview_moveto(1)
        self.window.after(100, self.jump_log)

    def refresh_startpage(self):
        """
        Updates these startpage widgets:
        - Images in Input folder
        - Remaining searches on SauceNao
        - Current image that is being processed
        Creates ImageData classes from the information the magic process gives
        Displays all results
        """
        self.window.after(1, self.jump_log)
        self.window.after(1, self.get_processing_status)
        self.window.after(1, self.make_image_data)
        self.window.after(1, self.load_image_data)

        def update():
            while True:
                self.count_input()
                time.sleep(0.3)
        Thread(target=update, daemon=True, name="startpage_update").start()

    def display_info(self):
        gv.Files.Log.log_text.place_forget()
        self.info_ScrollFrame.display(x = (gv.width/3)*1.85, y = 100)

    def display_logfile(self):
        self.info_ScrollFrame.sub_frame.place_forget()
        gv.Files.Log.log_text.place(x = int(gv.width/3)*1.85, y = int(gv.height/9))
        self.jump_log_chkbtn.place(x = int(gv.width/3)*1.85, y = int(gv.height/90*80))

    def forget_all_widgets(self):
        for widget in self.window.winfo_children():
            widget.place_forget()