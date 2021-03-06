from os import path, listdir, remove, makedirs
from threading import Thread, Lock
from time import sleep
from shutil import move, rmtree
from tkinter import IntVar, W, N
from tkinter import Checkbutton as cb
from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from webbrowser import open_new
from copy import deepcopy
import logging as log
from file_operations import is_image, gen_tagfile
from ProviderImageData import ProviderImageData
from SubImageData import SubImageData
import global_variables as gv

class ImageData():
    """Includes all information on the sourced images"""
    def __init__(self, dillustration, index):
        self.thumb_size = (70,70)
        self.preview_size = (200, 200)
        self.siblings_array = list()
        self.service_list = list()
        self.pixiv_list = list()
        for elem in dillustration.pixiv_subdillustration:
            self.pixiv_list.append(ProviderImageData(elem, dillustration, self.thumb_size, self.preview_size, self.siblings_array))
        self.danbooru_list = list()
        for elem in dillustration.danbooru_subdillustration:
            self.danbooru_list.append(ProviderImageData(elem, dillustration, self.thumb_size, self.preview_size, self.siblings_array))
        self.yandere_list = list()
        for elem in dillustration.yandere_subdillustration:
            self.yandere_list.append(ProviderImageData(elem, dillustration, self.thumb_size, self.preview_size, self.siblings_array))
        self.konachan_list = list()
        for elem in dillustration.konachan_subdillustration:
            self.konachan_list.append(ProviderImageData(elem, dillustration, self.thumb_size, self.preview_size, self.siblings_array))
        self.gelbooru_list = list()
        for elem in dillustration.gelbooru_subdillustration:
            self.gelbooru_list.append(ProviderImageData(elem, dillustration, self.thumb_size, self.preview_size, self.siblings_array))

        self.sub_dill = dillustration.original_sub
        self.dill = dillustration

        self.service_list.append(self.pixiv_list)
        self.service_list.append(self.danbooru_list)
        self.service_list.append(self.yandere_list)
        self.service_list.append(self.konachan_list)
        self.service_list.append(self.gelbooru_list)
        
        self.size = None
        
        self.original_image_thumb = None
        self.original_photoImage_thumb = None

        self.original_chkbtn = None
        self.original_lbl = None
        self.original_wxh_lbl = None
        self.original_type_lbl = None
        self.original_cropped_lbl = None

        self.big_selector_btn = None
        self.info_btn = None      
        self.back_btn = None
        self.next_btn = None
        self.prev_btn = None

        self.index = index
        self.prev_imgdata = None
        self.next_imgdata = None
        self.placed = False

        self.original_var = IntVar(value=0)
        #self.original_SubImgData = None
        self.original_SubImgData = SubImageData(self.sub_dill.name, self.sub_dill.path[:self.sub_dill.path.rfind('/')], 'Input', gv.window, None, var=self.original_var)
        self.big_lock = Lock()
        self.big_active = False

        self.load_init = False
        self.display_results_init = False
        self.process_results_imgs_init = False
        self.process_big_imgs_init = False
        self.modify_results_widgets_init = False
        self.process_info_imgs_init = False
        self.locked = False

    def init_widgets(self):
        theme = gv.Files.Theme.theme['General']['current']
        self.original_chkbtn = cb(gv.res_frame, var=self.original_var,
            foreground=gv.Files.Theme.theme[theme]['foreground'], 
            background=gv.Files.Theme.theme[theme]['background'], 
            borderwidth = 1, 
            selectcolor=gv.Files.Theme.theme[theme]['checkbutton_pressed'], 
            activebackground=gv.Files.Theme.theme[theme]['button_background_active'], 
            activeforeground=gv.Files.Theme.theme[theme]['button_foreground_active'], 
            relief='flat',#default flat
            overrelief='ridge',#no default
            offrelief='flat',#default raised
            indicatoron='false')# sunken, raised, groove, ridge, flat)
        self.original_lbl = Label(gv.res_frame, text = "Input", style='label.TLabel')
        self.original_wxh_lbl = Label(gv.res_frame, style='label.TLabel')
        self.original_type_lbl = Label(gv.res_frame, style='label.TLabel')
        self.original_cropped_lbl = Label(gv.res_frame, style='label.TLabel')
        self.original_cropped_big_lbl = Label(gv.res_frame, style='label.TLabel')

        self.big_selector_btn = Button(gv.res_frame, command=self.display_big_selector, text='Big Selector', style='button.TLabel')
        self.info_btn = Button(gv.res_frame, command=self.display_info, text='More Info', style='button.TLabel')        
        self.back_btn = Button(gv.window, text = 'Back', command = self.display_view_results, style = 'button.TLabel')
        self.next_btn = Button(gv.window, text = 'Next', style = 'button.TLabel')
        self.prev_btn = Button(gv.window, text = 'Previous', style = 'button.TLabel')

        self.original_SubImgData.init_widgets()
        
        for service in self.service_list:
            for elem in service:
                elem.init_widgets()
        
    def forget_all_widgets(self):
        for widget in gv.window.winfo_children():
            widget.place_forget()
        for widget in gv.big_frame.winfo_children():
            widget.grid_forget()

    def load(self):
        """
        Loads images into memory
        """
        if self.load_init:
            return True

        try:
            self.original_image_thumb = Image.open(self.sub_dill.path)
        except Exception as e:
                print("ERROR [0069] " + str(e))
                #mb.showerror("ERROR [0069]", "ERROR CODE [0069]\nSomething went wrong while loading an image.")
                gv.Logger.write_to_log("ERROR [0069] " + str(e), log.ERROR)
                return False
        
        if self.original_image_thumb == None:
            return False
        self.size = (self.original_image_thumb.width, self.original_image_thumb.height)
        for service in self.service_list:
            for elem in service:
                elem.load()

        self.load_init = True
        return True

    def process_results_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if self.process_results_imgs_init:
            return
        
        self.original_image_thumb.thumbnail(self.thumb_size, resample=Image.ANTIALIAS)
        self.original_photoImage_thumb = ImageTk.PhotoImage(self.original_image_thumb)
        self.original_image_thumb.close()

        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    elem.process_results_imgs()

        self.process_results_imgs_init = True

    def modify_results_widgets(self):
        """
        Fills widgets with information\n
        IMPORTANT:\n
        Call load and process_results_imgs in that order before
        """
        if self.modify_results_widgets_init:
            return
        self.original_chkbtn.configure(image=self.original_photoImage_thumb)
        self.original_chkbtn.image = self.original_photoImage_thumb
        self.original_wxh_lbl.configure(text = str(self.size))
        self.original_type_lbl.configure(text = self.sub_dill.filetype)
        self.original_cropped_lbl.configure(text = self.sub_dill.name_no_suffix)
        self.original_cropped_big_lbl.configure(text = self.sub_dill.name_no_suffix)

        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    elem.modify_results_widgets()

        gv.res_frame.columnconfigure(0, weight=1)
        gv.res_frame.columnconfigure(1, weight=1)
        gv.res_frame.columnconfigure(2, weight=1)
        gv.res_frame.columnconfigure(3, weight=1)
        gv.res_frame.columnconfigure(4, weight=1)
        gv.res_frame.columnconfigure(5, weight=2)
        #self.modify_big_widgets_init = False
        self.modify_results_widgets_init = True

    def display_view_results(self, event=None):
        self.forget_all_widgets()
        if self.prev_imgdata != None:
            z = Thread(target=self.prev_imgdata.unload_big_imgs, name=self.prev_imgdata.sub_dill.name_no_suffix, daemon=True)
            z.start()
        if self.next_imgdata != None:
            y = Thread(target=self.next_imgdata.unload_big_imgs, name=self.next_imgdata.sub_dill.name_no_suffix, daemon=True)
            y.start()
        x = Thread(target=self.unload_big_imgs, name=self.sub_dill.name_no_suffix, daemon=True)
        x.start()

        gv.window.bind("<Up>", '')
        gv.window.bind("<w>", '')
        gv.window.bind("<Down>", '')
        gv.window.bind("<s>", '')
        gv.window.bind("<a>", '')
        gv.window.bind("<d>", '')
        gv.window.bind("<e>", '')
        gv.window.bind("<q>", '')
        gv.window.bind("<BackSpace>", '')
        gv.window.bind("<Left>", '')
        gv.window.bind("<Right>", '')
        gv.display_startpage()

    def display_results(self, t):
        """
        Displays all widgets corresponding to this image on the results frame\n
        IMPORTANT:\n
        Call load, process_results_imgs and modify_results_widgets in that order before
        """
        #TODO display_results_init skip?
        flag = False
        if gv.config['Pixiv']['direct_replace'] == '1':
            for elem in self.pixiv_list:
                if elem.load_init:
                    if elem.is_greater_than_direct_sim():
                        flag = True
        if gv.config['Danbooru']['direct_replace'] == '1':
            for elem in self.danbooru_list:
                if elem.load_init:
                    if elem.is_greater_than_direct_sim():
                        flag = True
        if gv.config['Yandere']['direct_replace'] == '1':
            for elem in self.yandere_list:
                if elem.load_init:
                    if elem.is_greater_than_direct_sim():
                        flag = True
        if gv.config['Konachan']['direct_replace'] == '1':
            for elem in self.konachan_list:
                if elem.load_init:
                    if elem.is_greater_than_direct_sim():
                        flag = True
        if gv.config['Gelbooru']['direct_replace'] == '1':
            for elem in self.gelbooru_list:
                if elem.load_init:
                    if elem.is_greater_than_direct_sim():
                        flag = True

        if flag:
            if gv.config['Pixiv']['direct_replace'] == '1':
                for elem in self.pixiv_list:
                    if elem.load_init:
                        if elem.is_greater_than_direct_sim():
                            elem.downloaded_var.set(1)
                        else:
                            elem.downloaded_var.set(0)
            if gv.config['Danbooru']['direct_replace'] == '1':
                for elem in self.danbooru_list:
                    if elem.load_init:
                        if elem.is_greater_than_direct_sim():
                            elem.downloaded_var.set(1)
                        else:
                            elem.downloaded_var.set(0)
            if gv.config['Yandere']['direct_replace'] == '1':
                for elem in self.yandere_list:
                    if elem.load_init:
                        if elem.is_greater_than_direct_sim():
                            elem.downloaded_var.set(1)
                        else:
                            elem.downloaded_var.set(0)
            if gv.config['Konachan']['direct_replace'] == '1':
                for elem in self.konachan_list:
                    if elem.load_init:
                        if elem.is_greater_than_direct_sim():
                            elem.downloaded_var.set(1)
                        else:
                            elem.downloaded_var.set(0)
            if gv.config['Gelbooru']['direct_replace'] == '1':
                for elem in self.gelbooru_list:
                    if elem.load_init:
                        if elem.is_greater_than_direct_sim():
                            elem.downloaded_var.set(1)
                        else:
                            elem.downloaded_var.set(0)
            return -1
        
        aspect_flag = True # True if original image has the highest resolution
        highest_weight = (None, 0)

        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    weight, a_flag = elem.evaluate_weight(round(self.size[0]/self.size[1], 1), self.size[0])
                    if not a_flag:
                        aspect_flag = False
                    if weight > highest_weight[1]:
                        highest_weight = (elem, weight)
        
        original_weight = self.evaluate_weight()

        if aspect_flag:
            original_weight = original_weight + gv.config.getint('Weight', 'higher_resolution')
        if original_weight > highest_weight[1]:
            self.original_var.set(1)
        else:
            highest_weight[0].downloaded_var.set(1)

        #self.index = int(t/4)
        self.original_chkbtn.grid(column = 0, row = t+1, sticky = W)
        self.original_lbl.grid(column = 2, row = t+1, sticky = W, padx = 7)
        self.original_wxh_lbl.grid(column = 3, row = t+1, sticky = W, padx = 7)
        self.original_type_lbl.grid(column = 4, row = t+1, sticky = W, padx = 7)
        self.info_btn.grid(column = 6, row = t+1, sticky = W, padx = 7)
        self.original_cropped_lbl.grid(column = 1, row = t, columnspan=6, sticky = W, padx = 7)
        self.big_selector_btn.grid(column = 5, row = t+1, sticky = W, padx = 7)

        t += 1

        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    t = elem.display_results(t+1)

        self.display_results_init = True
        return t

    def evaluate_weight(self):
        img_weight = 0
        filetype = self.sub_dill.filetype
        switch = {
            'png': gv.config.getint('Weight', 'png'),
            'jpg': gv.config.getint('Weight', 'jpg'),
            'jpeg': gv.config.getint('Weight', 'jpg'),
            'jfif': gv.config.getint('Weight', 'jfif'),
            'gif': gv.config.getint('Weight', 'gif'),
            'bmp': gv.config.getint('Weight', 'bmp')
        }
        img_weight += switch.get(filetype, gv.config.getint('Weight', 'other'))

        img_weight += gv.config.getint('Weight', 'original')
        
        return img_weight

    def lock(self):
        """
        Locks in the image so that it can be saved safely
        """
        self.locked = True
        self.original_cropped_lbl.configure(background = 'green')

    def display_info(self):
        """
        Displays all widgets corresponding to this image on the info frame\n
        IMPORTANT:\n
        Call load before
        """
        for widget in gv.info_frame.winfo_children():
            widget.grid_forget()
        
        gv.Logger.log_text.place_forget()
        gv.info_ScrollFrame.display(x = (gv.width/3)*1.85, y = 100)

        t = 0

        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    t = elem.display_info(t)
        
    def display_big_selector(self, event=None):
        """
        Displays all widgets corresponding to this image on the big selector page\n
        IMPORTANT:\n
        Call load before
        """
        
        self.modify_big_widgets()
        
        def down(event=None):
            show_next = False
            breakout = False
            for service in self.service_list:
                for elem in service:
                    if show_next:
                        if elem.downloaded_SubImgData != None:
                            elem.downloaded_SubImgData.show()
                        breakout = True
                        break
                    elif elem.downloaded_SubImgData != None and elem.downloaded_SubImgData.is_displayed:
                        show_next = True
                    else:
                        for data in elem.sub_dir_img_array:
                            if show_next:
                                data.show()
                                breakout = True
                                break
                            elif data.is_displayed:
                                show_next = True
                    if breakout:
                        break
                if breakout:
                    break
        
        def up(event=None):
            breakout = False
            last = None
            for service in self.service_list:
                for elem in service:
                    if elem.downloaded_SubImgData != None:
                        if elem.downloaded_SubImgData.is_displayed:
                            if last != None:
                                last.show()
                            breakout = True
                            break
                        else:
                            last = elem.downloaded_SubImgData
                    else:
                        for data in elem.sub_dir_img_array:
                            if data.is_displayed:
                                if last != None:
                                    last.show()
                                breakout = True
                                break
                            last = data
                    
                    if breakout:
                        break
                if breakout:
                    break

        gv.window.bind("<Up>", up)
        gv.window.bind("<w>", up)
        gv.window.bind("<Down>", down)
        gv.window.bind("<s>", down)
        gv.window.bind("<BackSpace>", self.display_view_results)
        gv.window.bind("<a>", lambda e: self.original_var.set(not self.original_var.get()))
        self.big_active = True
        self.forget_all_widgets()
        gv.big_selector_frame.place(x = round(gv.width*0.86), y = int(gv.height/90*9))
        gv.big_selector_canvas.yview_moveto(0)
        self.back_btn.place(x = round(gv.width*0.86), y = int(gv.height/90*4))
        self.prev_btn.place(x = round(gv.width*0.90), y = int(gv.height/90*4))
        self.next_btn.place(x = round(gv.width*0.94), y = int(gv.height/90*4))
        self.display_big_selector_imgs()
        x = Thread(target=self.process_big_imgs, name=self.sub_dill.name_no_suffix, daemon=True)
        x.start()

    def process_big_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if not self.process_big_imgs_init:
            self.original_SubImgData.load()
            
            for service in self.service_list:
                for elem in service:
                    if elem.load_init:
                        elem.process_big_imgs()
            self.process_big_imgs_init = True
        
    def display_big_selector_imgs(self):
        if not self.big_active:
            return
        t = 0
        self.original_SubImgData.display_place()
        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    t = elem.display_big_selector(t)

        # Show image chosen by weight system
        breakout = False
        for service in self.service_list:
            for elem in service:
                if elem.downloaded_SubImgData != None and elem.downloaded_SubImgData.var.get() == 1:
                    elem.downloaded_SubImgData.show()
                    breakout = True
                    break
                elif elem.downloaded_var.get() == 1:
                    elem.sub_dir_img_array[0].show()
                    breakout = True
                    break
                else:
                    for data in elem.sub_dir_img_array:
                        if data.var.get() == 1:
                            data.show()
                            breakout = True
                            break
                if breakout:
                    break
            if breakout:
                    break

        if self.next_imgdata != None:
            self.next_imgdata.big_active = False
            gv.window.bind("<Right>", self.next_imgdata.display_big_selector)
            gv.window.bind("<e>", self.next_imgdata.display_big_selector)
        if self.prev_imgdata != None:
            self.prev_imgdata.big_active = False
            gv.window.bind("<Left>", self.prev_imgdata.display_big_selector)
            gv.window.bind("<q>", self.prev_imgdata.display_big_selector)

    def unload_big_imgs(self):
        self.original_SubImgData.unload_big_imgs()
        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    elem.unload_big_imgs()
        self.process_big_imgs_init = False
    
    def modify_big_widgets(self):
        """
        Sets up next and previous buttons for the big selector screen\n
        """
        flag_next = False
        flag_prev = False
        saved_index_smaller = (None, -1)
        saved_index_bigger = (None, -1)
        for data in gv.img_data_array:
            if data.display_results_init and data.index < self.index and data.index > saved_index_smaller[1]:
                saved_index_smaller = (data, data.index)
            if data.display_results_init and data.index > self.index and (data.index < saved_index_bigger[1] or saved_index_bigger[1] == -1):
                saved_index_bigger = (data, data.index)
        if saved_index_smaller[1] > -1:
            self.prev_btn.configure(state='enabled', command = saved_index_smaller[0].display_big_selector)
            self.prev_imgdata = saved_index_smaller[0]
        else:
            self.prev_btn.configure(state='disabled', command=None)
            self.prev_imgdata = None
        if saved_index_bigger[1] > -1:
            self.next_btn.configure(state='enabled', command = saved_index_bigger[0].display_big_selector)
            self.next_imgdata = saved_index_bigger[0]
        else:
            self.next_btn.configure(state='disabled', command=None)
            self.next_imgdata = None
        
        if self.prev_imgdata != None:
            t = Thread(target=self.prev_imgdata.process_big_imgs, name=self.prev_imgdata.sub_dill.name_no_suffix, daemon=True)
            t.start()
            if self.prev_imgdata.prev_imgdata != None:
                z = Thread(target=self.prev_imgdata.prev_imgdata.unload_big_imgs, name=self.prev_imgdata.prev_imgdata.sub_dill.name_no_suffix, daemon=True)
                z.start()
                if self.prev_imgdata.prev_imgdata.prev_imgdata != None:
                    q = Thread(target=self.prev_imgdata.prev_imgdata.prev_imgdata.unload_big_imgs, name=self.prev_imgdata.prev_imgdata.prev_imgdata.sub_dill.name_no_suffix, daemon=True)
                    q.start()
        if self.next_imgdata != None:
            x = Thread(target=self.next_imgdata.process_big_imgs, name=self.next_imgdata.sub_dill.name_no_suffix, daemon=True)
            x.start()
            if self.next_imgdata.next_imgdata != None:
                y = Thread(target=self.next_imgdata.next_imgdata.unload_big_imgs, name=self.next_imgdata.next_imgdata.sub_dill.name_no_suffix, daemon=True)
                y.start()
                if self.next_imgdata.next_imgdata.next_imgdata != None:
                    e = Thread(target=self.next_imgdata.next_imgdata.next_imgdata.unload_big_imgs, name=self.next_imgdata.next_imgdata.next_imgdata.sub_dill.name_no_suffix, daemon=True)
                    e.start()
       
    def save(self, second_try=False, save_counter=0):
        """
        "Saves" own checked images and schedules the unchecked images to be deleted 
        """
        exception_tags = list()
        pixiv_tags = list()
        for elem in self.pixiv_list:
            tags = elem.get_tags_list()
            pixiv_tags.extend(tags[0])
            exception_tags.extend(tags[1])

        danbooru_tags = list()
        for elem in self.danbooru_list:
            tags = elem.get_tags_list()
            danbooru_tags.extend(tags[0])
            exception_tags.extend(tags[1])

        yandere_tags = list()
        for elem in self.yandere_list:
            tags = elem.get_tags_list()
            yandere_tags.extend(tags[0])
            exception_tags.extend(tags[1])

        konachan_tags = list()
        for elem in self.konachan_list:
            tags = elem.get_tags_list()
            konachan_tags.extend(tags[0])
            exception_tags.extend(tags[1])

        gelbooru_tags = list()
        for elem in self.gelbooru_list:
            tags = elem.get_tags_list()
            gelbooru_tags.extend(tags[0])
            exception_tags.extend(tags[1])

        counter = 0
        for service in self.service_list:
            counter += len(service)
        
        if counter == 1 and gv.config['Original']['single_source_in_tagfile'] == '1':
            exception_tags.extend(pixiv_tags)
            exception_tags.extend(danbooru_tags)
            exception_tags.extend(yandere_tags)
            exception_tags.extend(konachan_tags)
            exception_tags.extend(gelbooru_tags)

        if not second_try:
            #--Does the user want to save more than one image?...--#
            save_counter = 0
            
            for service in self.service_list:
                for elem in service:
                    if elem.load_init:
                        if save_counter > 1:
                            break
                        if elem.get_save_status():
                            save_counter += 1
            if self.original_var.get() == 1:
                save_counter += 1
            ##----##
                
            if save_counter == 0:
                if gv.config['Sourcery']['delete_input'] == '1':
                    if not mb.askyesno('Delete all?', 'Delete all images(INcluding image in input folder) related to:\n' + self.sub_dill.name + '\n'):
                        return False
                else:
                    if not mb.askyesno('Delete all?', 'Delete all images(EXcluding image in input folder) related to:\n' + self.sub_dill.name + '\n'):
                        return False

        #--...If yes, make a head directory(new_dir, full path) with the original name and save all checked images in it--#
        if save_counter > 1:
            new_dir = gv.output_dir + '/' + self.sub_dill.name_no_suffix
            try:
                makedirs(new_dir, 0o777, True)
            except Exception as e:
                if not second_try:
                    return self.save(True, save_counter)
                else:
                    print("ERROR [0061] " + str(e))
                    gv.Logger.write_to_log("ERROR [0061] " + str(e), log.ERROR)
                    #mb.showerror("ERROR [0061]", "ERROR CODE [0061]\nSomething went wrong while creating the output folder)
                    return False
            t = 0
            if self.original_var.get() == 1:
                new_img_name = self.sub_dill.name_no_suffix + '_' + str(t) + '.' + self.sub_dill.filetype
                if not self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, gelbooru_tags, exception_tags, new_dir, self.sub_dill.name_no_suffix + '_' + str(t)):
                    self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, gelbooru_tags, exception_tags, new_dir, self.sub_dill.name_no_suffix + '_' + str(t))
                
                try:
                    move(self.sub_dill.path, new_dir + '/' + new_img_name)
                except Exception as e:
                    if not second_try:
                        return self.save(True, save_counter)
                    else:
                        print("ERROR [0013] " + str(e))
                        gv.Logger.write_to_log("ERROR [0013] " + str(e), log.ERROR)
                        #mb.showerror("ERROR [0013]", "ERROR CODE [0013]\nSomething went wrong while moving the image " + self.sub_dill.path)
                        return False
                t += 1
            else:
                if self.sub_dill.path not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.sub_dill.path)
            for service in self.service_list:
                for elem in service:
                    if elem.load_init:
                        elem.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, gelbooru_tags, exception_tags, t, new_dir)
                        t += 1
        ##----##

        #--...If no, go through all saves, the only one that is checked will be in there--#
        else:
            try:
                makedirs(gv.output_dir, 0o777, True)
            except Exception as e:
                if not second_try:
                    return self.save(True, save_counter)
                else:
                    print("ERROR [0062] " + str(e))
                    gv.Logger.write_to_log("ERROR [0062] " + str(e), log.ERROR)
                    #mb.showerror("ERROR [0062]", "ERROR CODE [0062]\nSomething went wrong while creating the output folder)
                    return False
            if self.original_var.get() == 1:
                if not self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, gelbooru_tags, exception_tags, gv.output_dir, self.sub_dill.name_no_suffix):
                    self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, gelbooru_tags, exception_tags, gv.output_dir, self.sub_dill.name_no_suffix)
                try:
                    move(self.sub_dill.path, gv.output_dir + '/' + self.sub_dill.name)
                except Exception as e:
                    if not second_try:
                        return self.save(True, save_counter)
                    else:
                        print("ERROR [0048] " + str(e))
                        gv.Logger.write_to_log("ERROR [0048] " + str(e), log.ERROR)
                        #mb.showerror("ERROR [0048]", "ERROR CODE [0048]\nSomething went wrong while moving the image " + self.path_original)
                        return False
            else:
                if self.sub_dill.path not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.sub_dill.path)
            for service in self.service_list:
                for elem in service:
                    if elem.load_init:
                        if not elem.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, gelbooru_tags, exception_tags):
                            return False
        ##----##

        self.forget_results()

        for widget in gv.info_frame.winfo_children():
            widget.grid_forget()

        if gv.config['Sourcery']['delete_input'] == '1':
            gv.delete_dirs_array.append(self.dill.input_path)
        try:
            gv.Files.Ref.refs.remove(self.dill.reference)
            gv.Files.Ref.write_reference()
        except:
            pass
        return True

    def gen_tagfile(self, pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, gelbooru_tags, exception_tags, gen_dir, name):
        if gv.config['Original']['gen_tagfile'] == '1':
            all_tags = list()
            if gv.config['Original']['tagfile_pixiv'] == '1':
                all_tags.extend(pixiv_tags)
            if gv.config['Original']['tagfile_danbooru'] == '1':
                all_tags.extend(danbooru_tags)
            if gv.config['Original']['tagfile_yandere'] == '1':
                all_tags.extend(yandere_tags)
            if gv.config['Original']['tagfile_konachan'] == '1':
                all_tags.extend(konachan_tags)
            if gv.config['Original']['tagfile_gelbooru'] == '1':
                all_tags.extend(gelbooru_tags)
            all_tags.extend(exception_tags)
            return gen_tagfile(all_tags, gen_dir, name)

    def forget_results(self):
        self.original_chkbtn.grid_forget()
        self.original_lbl.grid_forget()
        self.original_wxh_lbl.grid_forget()
        self.original_type_lbl.grid_forget()
        self.info_btn.grid_forget()
        self.original_cropped_lbl.grid_forget()
        self.big_selector_btn.grid_forget()

        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    elem.forget_results()

    def self_destruct(self):
        if self.original_SubImgData != None:
            self.original_SubImgData.self_destruct()
        self.original_photoImage_thumb = None

        if self.original_chkbtn != None:
            self.original_chkbtn.configure(image=None)
            self.original_chkbtn.image = None

        for service in self.service_list:
            for elem in service:
                if elem.load_init:
                    elem.self_destruct()
        
        del self.original_image_thumb
        del self.original_photoImage_thumb

        if self.original_chkbtn != None:
            self.original_chkbtn.destroy()
        if self.original_lbl != None:
            self.original_lbl.destroy()
        if self.original_wxh_lbl != None:
            self.original_wxh_lbl.destroy()

        if self.original_type_lbl != None:
            self.original_type_lbl.destroy()
        if self.original_cropped_lbl != None:
            self.original_cropped_lbl.destroy()

        if self.big_selector_btn != None:
            self.big_selector_btn.destroy()
        if self.info_btn != None:
            self.info_btn.destroy()
        if self.back_btn != None:
            self.back_btn.destroy()
        if self.next_btn != None:
            self.next_btn.destroy()
        if self.prev_btn != None:
            self.prev_btn.destroy()
