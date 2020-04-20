from os import path, listdir, remove, makedirs
from shutil import move, rmtree
from threading import Lock
from tkinter import IntVar, W, N, S
from tkinter import Checkbutton as cb
from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from webbrowser import open_new
from copy import deepcopy
from file_operations import is_image, gen_tagfile
from SubImageData import SubImageData
import global_variables as gv

class ProviderImageData():
    """Includes all gui objects"""
    def __init__(self, sub_dill, dillustration, thumb_size, preview_size, siblings_array):
        self.sub_dill = sub_dill
        self.thumb_size = thumb_size
        self.preview_size = preview_size
        self.siblings_array = siblings_array
        self.downloaded_image_thumb = None
        self.downloaded_photoImage_thumb = None
        self.downloaded_photoImage_preview = None
        self.downloaded_image_preview = None
        self.sub_dir_array = list()
        self.sub_dir_img_array = list()
        self.downloaded_var = IntVar(value=0)
        self.downloaded_chkbtn = cb(master = gv.res_frame, var=self.downloaded_var,
            foreground=gv.Files.Theme.foreground, 
            background=gv.Files.Theme.background, 
            borderwidth = 1,
            highlightthickness = 1, 
            selectcolor=gv.Files.Theme.checkbutton_pressed, 
            activebackground=gv.Files.Theme.button_background_active, 
            activeforeground=gv.Files.Theme.button_foreground_active, 
            relief='flat',#default flat
            overrelief='ridge',#no default
            offrelief='flat',#default raised
            indicatoron='false')
        self.downloaded_lbl = Label(gv.res_frame, text = self.sub_dill.service, style='label.TLabel')
        try:
            self.downloaded_wxh_lbl = Label(gv.res_frame, text = str(len(listdir(self.sub_dill.path))) + " images", style='label.TLabel')
        except:
            self.downloaded_wxh_lbl = Label(gv.res_frame, text = "More images", style='label.TLabel')
        self.downloaded_type_lbl = Label(gv.res_frame, style='label.TLabel')
        self.results_tags_lbl = Label(gv.res_frame, wraplength=gv.res_frame_width/6, style='label.TLabel')
        self.size = None

        self.result_not_in_tagfile_var = IntVar(value=0)
        self.result_not_in_tagfile = Checkbutton(gv.res_frame, text='Not in Tagfile', var=self.result_not_in_tagfile_var, style='chkbtn.TCheckbutton')
        self.result_in_tagfile_var = IntVar(value=0)
        self.result_in_tagfile = Checkbutton(gv.res_frame, text='Put in Tagfile', var=self.result_in_tagfile_var, style='chkbtn.TCheckbutton')

        self.info_img_lbl = Label(gv.info_frame, style='label.TLabel')
        self.info_provider_lbl = Label(gv.info_frame, style='label.TLabel')
        self.info_artist_lbl = Label(gv.info_frame, wraplength=gv.info_frame_width*0.55, style='label.TLabel')
        self.info_title_lbl = Label(gv.info_frame, wraplength=gv.info_frame_width*0.55, style='label.TLabel')
        #self.info_imageid_lbl = Label(gv.info_frame, style='label.TLabel')
        self.info_url_lbl_list = list()
        #self.info_url_lbl = Label(gv.info_frame, style='label.TLabel')
        self.info_date_lbl = Label(gv.info_frame, style='label.TLabel')
        self.info_caption_lbl = Label(gv.info_frame, wraplength=gv.info_frame_width*0.55, style='label.TLabel')
        self.info_wxh_lbl = Label(gv.info_frame, style='label.TLabel')
        self.tags_pixiv_lbl = Label(gv.info_frame, text = 'Tags', font=('Arial Bold', 15), style='label.TLabel')
        self.tags_lbl_array = list()

        if self.sub_dill.service == 'Pixiv':
            self.tags_lbl_array.append((Label(gv.info_frame, text = 'Original:', style='label.TLabel', font = ('Arial Bold', 11)), Label(gv.info_frame, text = 'Translated:', style='label.TLabel', font = ('Arial Bold', 11))))
            for tag in self.sub_dill.tags:
                if type(tag) == type(dict()):
                    self.tags_lbl_array.append((Label(gv.info_frame, text = tag['name'], wraplength=gv.info_frame_width/2.1, style='label.TLabel'), Label(gv.info_frame, text = tag['translated_name'], wraplength=gv.info_frame_width/2.1, style='label.TLabel',)))
                else:
                    self.tags_lbl_array.append((Label(gv.info_frame, text = tag, wraplength=gv.info_frame_width/2.1, style='label.TLabel'), Label(gv.info_frame, text = '', wraplength=gv.info_frame_width/2.1, style='label.TLabel')))
        else:
            self.tags_lbl_array.append(Label(gv.info_frame, text = 'Tags:', style='label.TLabel', font = ('Arial Bold', 11)))
            for tag in self.sub_dill.tags:
                self.tags_lbl_array.append(Label(gv.info_frame, text = tag, wraplength=gv.info_frame_width/2.1, style='label.TLabel'))

        for elem in self.sub_dill.source:
            lbl = Label(gv.info_frame, text = elem, foreground='#2626ff', cursor='hand2', style='label.TLabel')
            lbl.bind("<Button-1>", self.hyperlink)
            self.info_url_lbl_list.append(lbl)

        self.downloaded_SubImgData = None
        if not self.sub_dill.is_folder:
            self.downloaded_SubImgData = SubImageData(self.sub_dill.name, self.sub_dill.path[:self.sub_dill.path.rfind('/')], self.sub_dill.service, gv.window, gv.big_frame, var=self.downloaded_var, siblings=self.siblings_array)
            
        self.big_lock = Lock()
        self.load_init = False
        self.process_results_imgs_init = False
        self.modify_results_widgets_init = False
        self.process_info_imgs_init = False
        self.process_big_imgs_init = False

    def load(self, second_try=False):
        """
        Loads images into memory
        """
        if self.load_init:
            return True

        if not self.sub_dill.is_folder:
            try:
                self.downloaded_image_thumb = Image.open(self.sub_dill.path)
            except Exception as e:
                if not second_try:
                    return self.load(True)
                else:
                    print("ERROR [0070] " + str(e))
                    #mb.showerror("ERROR [0070]", "ERROR CODE [0070]\nSomething went wrong while loading an image.")
                    gv.Files.Log.write_to_log("ERROR [0070] " + str(e))
                    return False
        else:
            try:
                self.sub_dir_array.extend(listdir(self.sub_dill.path))
                if len(self.sub_dir_array) == 0:
                    if self.sub_dill.path not in gv.delete_dirs_array:
                        gv.delete_dirs_array.append(self.sub_dill.path)
                for img in self.sub_dir_array:
                    data = SubImageData(img, self.sub_dill.path, self.sub_dill.service, gv.window, gv.big_frame, master_folder=self.sub_dill.name_no_suffix, siblings=self.siblings_array)
                    if data not in self.sub_dir_img_array:
                        self.sub_dir_img_array.append(data)
                self.siblings_array.extend(self.sub_dir_img_array)
            except Exception as e:
                if not second_try:
                    return self.load(True)
                else:
                    print("ERROR [0046] " + str(e))
                    #mb.showerror("ERROR [0046]", "ERROR CODE [0046]\nSomething went wrong while loading an image.")
                    gv.Files.Log.write_to_log("ERROR [0046] " + str(e))
                    return False
            try:
                self.downloaded_image_thumb = Image.open(self.sub_dill.path + '/' + listdir(self.sub_dill.path)[0])
            except Exception as e:
                print("ERROR [0047] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0047] " + str(e))
                mb.showerror("ERROR [0047]", "ERROR CODE [0047]\nSomething went wrong while accessing an image, please restart Sourcery.")
                return False

            self.size = deepcopy(self.downloaded_image_thumb.size)
        
        self.load_init = True
        return True

    def is_greater_than_direct_sim(self):
        if self.sub_dill.similarity > gv.config.getint('Sourcery', 'direct_replace'):
            return True
        return False

    def process_results_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        #Call load before
        """
        self.load()
        if self.process_results_imgs_init:
            return

        self.downloaded_image_thumb.thumbnail(self.thumb_size, resample=Image.ANTIALIAS)
        self.downloaded_photoImage_thumb = ImageTk.PhotoImage(self.downloaded_image_thumb)
        self.downloaded_image_thumb.close()

        self.process_results_imgs_init = True
    
    def modify_results_widgets(self):
        """
        Fills widgets with information\n
        IMPORTANT:\n
        Call load and process_results_imgs in that order before
        """
        if self.modify_results_widgets_init:
            return

        self.downloaded_chkbtn.configure(image=self.downloaded_photoImage_thumb)
        self.downloaded_chkbtn.image = self.downloaded_photoImage_thumb

        if self.sub_dill.service == 'Pixiv':
            results_tags = ''
            for elem in gv.results_tags_pixiv:
                if elem in self.sub_dill.tags:
                    results_tags = results_tags + elem + '\n' 
            self.results_tags_lbl.configure(text = results_tags)
        elif self.sub_dill.service == 'Danbooru':
            results_tags = ''
            for elem in gv.results_tags_danbooru:
                if elem in self.sub_dill.tags:
                    results_tags = results_tags + elem + '\n' 
            self.results_tags_lbl.configure(text = results_tags)
        elif self.sub_dill.service == 'Yandere':
            results_tags = ''
            for elem in gv.results_tags_yandere:
                if elem in self.sub_dill.tags:
                    results_tags = results_tags + elem + '\n' 
            self.results_tags_lbl.configure(text = results_tags)
            results_tags = ''
        elif self.sub_dill.service == 'Konachan':
            for elem in gv.results_tags_konachan:
                if elem in self.sub_dill.tags:
                    results_tags = results_tags + elem + '\n' 
            self.results_tags_lbl.configure(text = results_tags)

        if not self.sub_dill.is_folder:
            self.downloaded_wxh_lbl.configure(text = str(self.size))
            self.downloaded_type_lbl.configure(text = self.sub_dill.filetype)
        
        self.modify_results_widgets_init = True
            
    def display_results(self, t):
        """
        Displays all widgets corresponding to this image on the results frame\n
        IMPORTANT:\n
        Call load, process_results_imgs and modify_results_widgets in that order before
        """
        #self.index = int(t/3)
        self.downloaded_chkbtn.grid(column = 0, row = t+2, sticky = W)
        self.downloaded_lbl.grid(column = 2, row = t+2, sticky = W, padx = 7)
        self.downloaded_wxh_lbl.grid(column = 3, row = t+2, sticky = W, padx = 7)
        self.downloaded_type_lbl.grid(column = 4, row = t+2, sticky = W, padx = 7)
        self.results_tags_lbl.grid(column = 5, row = t+2, sticky = W, padx = 7)
        self.result_not_in_tagfile.grid(column = 6, row = t+2, sticky = W+N, padx = 7, pady = 3)
        self.result_in_tagfile.grid(column = 6, row = t+2, sticky = W+N, padx = 7, pady = 23)
        
        return t+2
        
    def display_info(self, t):
        """
        Displays all widgets corresponding to this image on the info frame\n
        IMPORTANT:\n
        Call load and process_info_imgs in that order before
        """
        self.process_info_imgs()
        self.info_img_lbl.configure(image = self.downloaded_photoImage_preview)
        self.info_provider_lbl.configure(text = self.sub_dill.service, font = ('Arial Bold', 18))
        self.info_artist_lbl.configure(text = 'by ' + self.sub_dill.creator)
        self.info_title_lbl.configure(text = self.sub_dill.title, font = ('Arial Bold', 13))
        self.info_caption_lbl.configure(text = self.sub_dill.caption)
        #self.info_imageid_lbl.configure(text = 'Image ID: ' + str(self.illust.id))
        self.info_date_lbl.configure(text = 'Uploaded on: ' + str(self.sub_dill.create_date), font = ('Arial', 10))
        self.info_wxh_lbl.configure(text = 'Width x Height: ' + str(self.sub_dill.width) + ' x ' + str(self.sub_dill.height), font = ('Arial', 10))

        self.info_img_lbl.grid(column = 0, row = t + 1, rowspan = 9, sticky=W+N)
        self.info_provider_lbl.grid(column = 0, row = t + 0, sticky = W, columnspan = 2)
        self.info_title_lbl.grid(column = 1, row = t + 1, sticky = W, padx = 5, columnspan = 2)
        self.info_caption_lbl.grid(column = 1, row = t + 2, sticky = W, padx = 5, columnspan = 2)
        self.info_artist_lbl.grid(column = 1, row = t + 3, sticky = W, padx = 5, columnspan = 2)
        #self.info_imageid_lbl.grid(column = 1, row = t + 4, sticky = W, padx = 5)
        self.info_date_lbl.grid(column = 1, row = t + 5, sticky = W, padx = 5, columnspan = 2)
        
        if len(self.sub_dir_img_array) < 1:
            self.info_wxh_lbl.grid(column = 1, row = t + 6, sticky = W, padx = 5, columnspan = 2)
        for elem in self.info_url_lbl_list:
            elem.grid(column = 0, row = t + 10, columnspan = 4, sticky = W)
            t = t+1
        self.tags_pixiv_lbl.grid(column = 0, row = 11, sticky = W)

        t = t+12

        if self.sub_dill.service == 'Pixiv':
            for lbl in self.tags_lbl_array:
                if lbl[1].cget('text') == '':
                    lbl[0].grid(column = 0, row = t, sticky = W, columnspan=3)
                else:
                    lbl[0].grid(column = 0, row = t, sticky = W, columnspan = 2)
                    lbl[1].grid(column = 2, row = t, sticky = W)
                t += 1
        else:
            second_row = False
            for lbl in self.tags_lbl_array:
                if second_row:
                    lbl.grid(column = 2, row = t, sticky = W)
                    second_row = False
                    t -= 1
                else:
                    lbl.grid(column = 0, row = t, sticky = W, columnspan = 2)
                    second_row = True
                
                t += 1
        #gv.res_frame.columnconfigure(1, weight=1)
        return t

    def process_info_imgs(self, second_try=False):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if self.process_info_imgs_init:
            return True

        if not self.sub_dill.is_folder:
            try:
                self.downloaded_image_preview = Image.open(self.sub_dill.path)
            except Exception as e:
                if not second_try:
                    return self.load(True)
                else:
                    print("ERROR [0072] " + str(e))
                    #mb.showerror("ERROR [0072]", "ERROR CODE [0072]\nSomething went wrong while loading an image.")
                    gv.Files.Log.write_to_log("ERROR [0072] " + str(e))
                    return False
        else:
            try:
                self.downloaded_image_preview = Image.open(self.sub_dill.path + '/' + listdir(self.sub_dill.path)[0])
            except Exception as e:
                if not second_try:
                    return self.load(True)
                else:
                    print("ERROR [0043] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0043] " + str(e))
                    mb.showerror("ERROR [0043]", "ERROR CODE [0043]\nSomething went wrong while accessing an image, please restart Sourcery.")
                    return False
        self.downloaded_image_preview.thumbnail(self.preview_size, resample=Image.ANTIALIAS)
        self.downloaded_photoImage_preview = ImageTk.PhotoImage(self.downloaded_image_preview)
        self.downloaded_image_preview.close()

        self.process_info_imgs_init = True
        return True

    def hyperlink(self, event):
        """
        Opens a webbrowser with a URL on click of a widget that is bound to this method
        """
        open_new(event.widget.cget("text"))

    def display_big_selector(self, t):
        """
        Displays all widgets corresponding to this image on the big selector screen\n
        IMPORTANT:\n
        Call load and process_big_imgs in that order before
        """
        if not self.sub_dill.is_folder:
            self.downloaded_SubImgData.display_grid(t)
            gv.big_frame.grid_rowconfigure(3, weight = 1)
            return t + 4
        else:
            for elem in self.sub_dir_img_array:
                elem.display_grid(t)
                gv.big_frame.grid_rowconfigure(t + 3, weight = 1)
                t += 4
            return t

    def process_big_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if self.process_big_imgs_init:
            return

        if not self.sub_dill.is_folder:
            self.downloaded_SubImgData.load()
            self.siblings_array.append(self.downloaded_SubImgData)
        else:
            for elem in self.sub_dir_img_array:
                elem.load()

        self.process_big_imgs_init = True

    def save(self, pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=-1, head_dir='', second_try=False):
        #new_dir = gv.output_dir + '/' + self.name
        #--If only one image is checked, save your image with the name--#
        if t == -1:
            if self.downloaded_var.get() == 1:
                if not self.sub_dill.is_folder:
                    if not self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gv.output_dir, self.sub_dill.name_no_suffix):
                        self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gv.output_dir, self.sub_dill.name_no_suffix)
                try:
                    move(self.sub_dill.path, gv.output_dir + '/' + self.sub_dill.name)
                except Exception as e:
                    if not second_try:
                        return self.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=t, head_dir=head_dir, second_try=True)
                    else:
                        print("ERROR [0054] " + str(e))
                        gv.Files.Log.write_to_log("ERROR [0054] " + str(e))
                        #mb.showerror("ERROR [0054]", "ERROR CODE [0054]\nSomething went wrong while moving the image " + self.sub_dill.path)
                        return False
                for img in self.sub_dir_img_array:
                    if not img.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gv.output_dir + '/' + self.sub_dill.name, img.name[:img.name.rfind('.')]):
                        img.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gv.output_dir + '/' + self.sub_dill.name, img.name[:img.name.rfind('.')])
                        
                return True
            else:
                if self.sub_dill.path not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.sub_dill.path)
                for elem in self.sub_dir_img_array:
                    if not elem.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags):
                        return False
                return True
        ##----##

        #--If more than one image is checked, save your image in the new head directory(full path) with name + t + suffix--#
        else:
            if self.downloaded_var.get() == 1:
                if self.sub_dill.is_folder:
                    try:
                        move(self.sub_dill.path, head_dir + '/' + self.sub_dill.name + '_' + str(t))
                    except Exception as e:
                        if not second_try:
                            return self.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=t, head_dir=head_dir, second_try=True)
                        else:
                            print("ERROR [0055] " + str(e))
                            gv.Files.Log.write_to_log("ERROR [0055] " + str(e))
                            #mb.showerror("ERROR [0055]", "ERROR CODE [0055]\nSomething went wrong while moving the image " + self.sub_dill.path)
                            return False
                    for img in self.sub_dir_img_array:
                        if not img.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, head_dir + '/' + self.sub_dill.name_no_suffix + '_' + str(t), img.name[:img.name.rfind('.')]):
                            img.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, head_dir + '/' + self.sub_dill.name_no_suffix + '_' + str(t), img.name[:img.name.rfind('.')])
                        
                else:
                    try:
                        move(self.sub_dill.path, head_dir + '/' + self.sub_dill.name_no_suffix + '_' + str(t) + '.' + self.sub_dill.filetype)
                    except Exception as e:
                        if not second_try:
                            return self.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=t, head_dir=head_dir, second_try=True)
                        else:
                            print("ERROR [0056] " + str(e))
                            gv.Files.Log.write_to_log("ERROR [0056] " + str(e))
                            #mb.showerror("ERROR [0056]", "ERROR CODE [0056]\nSomething went wrong while moving the image " + self.sub_dill.path)
                            return False
                    if not self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, head_dir, self.sub_dill.name_no_suffix + '_' + str(t)):
                        self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, head_dir, self.sub_dill.name_no_suffix + '_' + str(t))
                return True
            else:
                if self.sub_dill.path not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.sub_dill.path)
                for elem in self.sub_dir_img_array:
                    elem.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t, head_dir)
                return True
        ##----##

    def get_save_status(self):
        """
        Returns True if at least on box is checked, False otherwise
        """
        if self.downloaded_var.get() == 1:
            return True
        for elem in self.sub_dir_img_array:
            if elem.get_save_status():
                return True
        return False

    def gen_tagfile(self, pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gen_dir, name):
        if self.sub_dill.service == 'Pixiv' and gv.config['Pixiv']['gen_tagfile'] == '1':
            all_tags = list()
            if gv.config['Pixiv']['tagfile_pixiv'] == '1':
                all_tags.extend(pixiv_tags)
            if gv.config['Pixiv']['tagfile_danbooru'] == '1':
                all_tags.extend(danbooru_tags)
            if gv.config['Pixiv']['tagfile_yandere'] == '1':
                all_tags.extend(yandere_tags)
            if gv.config['Pixiv']['tagfile_konachan'] == '1':
                all_tags.extend(konachan_tags)
            all_tags.extend(exception_tags)
            return gen_tagfile(all_tags, gen_dir, name)
        elif self.sub_dill.service == 'Danbooru' and gv.config['Danbooru']['gen_tagfile'] == '1':
            all_tags = list()
            if gv.config['Danbooru']['tagfile_pixiv'] == '1':
                all_tags.extend(pixiv_tags)
            if gv.config['Danbooru']['tagfile_danbooru'] == '1':
                all_tags.extend(danbooru_tags)
            if gv.config['Danbooru']['tagfile_yandere'] == '1':
                all_tags.extend(yandere_tags)
            if gv.config['Danbooru']['tagfile_konachan'] == '1':
                all_tags.extend(konachan_tags)
            all_tags.extend(exception_tags)
            return gen_tagfile(all_tags, gen_dir, name)
        elif self.sub_dill.service == 'Yandere' and gv.config['Yandere']['gen_tagfile'] == '1':
            all_tags = list()
            if gv.config['Yandere']['tagfile_pixiv'] == '1':
                all_tags.extend(pixiv_tags)
            if gv.config['Yandere']['tagfile_danbooru'] == '1':
                all_tags.extend(danbooru_tags)
            if gv.config['Yandere']['tagfile_yandere'] == '1':
                all_tags.extend(yandere_tags)
            if gv.config['Yandere']['tagfile_konachan'] == '1':
                all_tags.extend(konachan_tags)
            all_tags.extend(exception_tags)
            return gen_tagfile(all_tags, gen_dir, name)
        elif self.sub_dill.service == 'Konachan' and gv.config['Konachan']['gen_tagfile'] == '1':
            all_tags = list()
            if gv.config['Konachan']['tagfile_pixiv'] == '1':
                all_tags.extend(pixiv_tags)
            if gv.config['Konachan']['tagfile_danbooru'] == '1':
                all_tags.extend(danbooru_tags)
            if gv.config['Konachan']['tagfile_yandere'] == '1':
                all_tags.extend(yandere_tags)
            if gv.config['Konachan']['tagfile_konachan'] == '1':
                all_tags.extend(konachan_tags)
            all_tags.extend(exception_tags)
            return gen_tagfile(all_tags, gen_dir, name)
    
    def get_tags_list(self, not_in_file=-1):
        """
        Returns a string list of all tags of the image from the provider\n
        except when the 'Not in Tagfile' checkbutton was ticked
        """
        if not_in_file == -1:
            not_in_file = self.result_not_in_tagfile_var.get()
        
        exception_tags = list()
        if self.result_in_tagfile_var.get() == 1:
            exception_tags = self.sub_dill.tags

        if not_in_file == 0:
            return (self.sub_dill.tags, exception_tags)

        return list()

    def evaluate_weight(self, original_aspect_ratio, original_width):
        img_weight = 0
        aspect_flag = False
        switch = {
            'png': gv.config.getint('Weight', 'png'),
            'jpg': gv.config.getint('Weight', 'jpg'),
            'jpeg': gv.config.getint('Weight', 'jpg'),
            'jfif': gv.config.getint('Weight', 'jfif'),
            'gif': gv.config.getint('Weight', 'gif'),
            'bmp': gv.config.getint('Weight', 'bmp')
        }
        img_weight += switch.get(self.sub_dill.filetype, gv.config.getint('Weight', 'other'))

        switch = {
            'Danbooru': gv.config.getint('Weight', 'danbooru'),
            'Pixiv': gv.config.getint('Weight', 'pixiv'),
            'Yandere': gv.config.getint('Weight', 'yandere'),
            'Konachan': gv.config.getint('Weight', 'konachan'),
        }
        img_weight += switch.get(self.sub_dill.service, 0)

        if original_aspect_ratio == round(int(self.sub_dill.width)/int(self.sub_dill.height), 1):
            if int(self.sub_dill.width) > original_width:
                img_weight = img_weight + gv.config.getint('Weight', 'higher_resolution')
            elif int(self.sub_dill.width) == original_width:
                img_weight = img_weight + gv.config.getint('Weight', 'higher_resolution')
                aspect_flag = True
            else:
                aspect_flag = True
        
        return img_weight, aspect_flag

    def forget_results(self):
        self.downloaded_chkbtn.grid_forget()
        self.downloaded_lbl.grid_forget()
        self.downloaded_wxh_lbl.grid_forget()
        self.downloaded_type_lbl.grid_forget()
        self.result_not_in_tagfile.grid_forget()
        self.results_tags_lbl.grid_forget()
        self.result_in_tagfile.grid_forget()

    def unload_big_imgs(self):
        if self.downloaded_SubImgData != None:
            self.downloaded_SubImgData.unload_big_imgs()
        for elem in self.sub_dir_img_array:
                elem.unload_big_imgs()
        self.process_big_imgs_init = False

    def self_destruct(self):
        if self.downloaded_SubImgData != None:
            self.downloaded_SubImgData.self_destruct()
        for img in self.sub_dir_img_array:
            img.self_destruct()
        del self.downloaded_photoImage_thumb
        del self.downloaded_photoImage_preview

        self.downloaded_chkbtn.image = None

        del self.downloaded_chkbtn
        del self.downloaded_lbl
        del self.downloaded_wxh_lbl
        del self.downloaded_type_lbl
        del self.results_tags_lbl

        del self.result_not_in_tagfile
        del self.result_in_tagfile

        del self.info_img_lbl
        del self.info_provider_lbl
        del self.info_artist_lbl
        del self.info_title_lbl
        #del self.info_imageid_lbl
        #del self.info_url_lbl
        del self.info_date_lbl
        del self.info_caption_lbl
        del self.info_wxh_lbl
        del self.tags_pixiv_lbl
        if self.sub_dill.service == 'Pixiv':
            for elem in self.tags_lbl_array:
                a = elem[0]
                del a
                b = elem[1]
                del b
        else:
            for elem in self.tags_lbl_array:
                del elem

        for elem in self.info_url_lbl_list:
            del elem
