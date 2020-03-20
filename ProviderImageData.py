from os import path, listdir, remove, makedirs
from shutil import move, rmtree
from tkinter import IntVar, W, N
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
    """Includes all information on the sourced images for the given image provider"""
    def __init__(self, service, name, path, thumb_size, preview_size, dictionary, illustration, siblings_array):
        self.service = service
        self.name = name
        self.path = path
        self.thumb_size = thumb_size
        self.preview_size = preview_size
        self.dict = dictionary
        self.illustration = illustration
        self.siblings_array = siblings_array
        self.downloaded_image = None
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
        self.downloaded_lbl = Label(master=gv.res_frame, text = service, style='label.TLabel')
        try:
            self.downloaded_wxh_lbl = Label(master=gv.res_frame, text = str(len(listdir(self.path))) + " images", style='label.TLabel')
        except:
            self.downloaded_wxh_lbl = Label(master=gv.res_frame, text = "More images", style='label.TLabel')
        self.downloaded_type_lbl = Label(master=gv.res_frame, style='label.TLabel')
        self.results_tags_lbl = Label(gv.res_frame, style='label.TLabel')

        self.result_not_in_tagfile_var = IntVar(value=0)
        self.result_not_in_tagfile = Checkbutton(gv.res_frame, text='Not in Tagfile', var=self.result_not_in_tagfile_var, style='chkbtn.TCheckbutton')

        self.info_img_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.info_provider_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.info_artist_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.info_title_lbl = Label(master=gv.info_frame, style='label.TLabel')
        #self.info_imageid_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.info_url_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.info_date_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.info_caption_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.info_wxh_lbl = Label(master=gv.info_frame, style='label.TLabel')
        self.tags_pixiv_lbl = Label(master=gv.info_frame, text = 'Tags', font=('Arial Bold', 15), style='label.TLabel')
        self.tags_lbl_array = list()
        self.tags = self.get_tags_list(0)#dictionary['tags'].strip('[]\'').split('\', \'')

        if self.service == 'Pixiv':
            self.tags_lbl_array.append((Label(master=gv.info_frame, text = 'Original:', style='label.TLabel', font = ('Arial Bold', 11)), Label(master=gv.info_frame, text = 'Translated:', style='label.TLabel', font = ('Arial Bold', 11))))
            for tag in self.tags:
                if type(tag) == type(dict()):
                    self.tags_lbl_array.append((Label(master=gv.info_frame, text = tag['name'], style='label.TLabel'), Label(master=gv.info_frame, text = tag['translated_name'], style='label.TLabel')))
                else:
                    self.tags_lbl_array.append((Label(master=gv.info_frame, text = tag, style='label.TLabel'), Label(master=gv.info_frame, text = '', style='label.TLabel')))
        else:
            self.tags_lbl_array.append(Label(master=gv.info_frame, text = 'Tags:', style='label.TLabel', font = ('Arial Bold', 11)))
            for tag in self.tags:
                self.tags_lbl_array.append(Label(master=gv.info_frame, text = tag, style='label.TLabel'))

        self.source_url = None

        self.downloaded_SubImgData = None

        self.load_init = False
        self.process_results_imgs_init = False
        self.modify_results_widgets_init = False
        self.process_info_imgs_init = False
        self.process_big_imgs_init = False

    def load(self):
        """
        Loads images into memory
        """
        if self.load_init:
            return True

        if path.isfile(self.path):
            try:
                self.downloaded_image = Image.open(self.path)
            except Exception as e:
                print("ERROR [0045] " + str(e))
                #mb.showerror("ERROR [0045]", "ERROR CODE [0045]\nSomething went wrong while loading an image.")
                gv.Files.Log.write_to_log("ERROR [0045] " + str(e))
                return False
        elif path.isdir(self.path):
            try:
                self.sub_dir_array.extend(listdir(self.path))
                if len(self.sub_dir_array) == 0:
                    if self.path not in gv.delete_dirs_array:
                        gv.delete_dirs_array.append(self.path)
                for img in self.sub_dir_array:
                    self.sub_dir_img_array.append(SubImageData(img, self.path, self.service, gv.window, gv.big_frame, master_folder=self.name, siblings=self.siblings_array))#(Image.open(self.path + '/' + img), img))
                self.siblings_array.extend(self.sub_dir_img_array)
            except Exception as e:
                print("ERROR [0046] " + str(e))
                #mb.showerror("ERROR [0046]", "ERROR CODE [0046]\nSomething went wrong while loading an image.")
                gv.Files.Log.write_to_log("ERROR [0046] " + str(e))
                return False
        
        self.load_init = True
        return True

    def is_greater_than_direct_sim(self):
        if self.dict['similarity'] > int(gv.Files.Conf.direct_replace):
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

        if path.isfile(self.path):
            self.downloaded_image_thumb = deepcopy(self.downloaded_image)
        elif path.isdir(self.path):
            try:
                self.downloaded_image_thumb = Image.open(self.path + '/' + listdir(self.path)[0])
            except Exception as e:
                print("ERROR [0047] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0047] " + str(e))
                mb.showerror("ERROR [0047]", "ERROR CODE [0047]\nSomething went wrong while accessing an image, please restart Sourcery.")
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

        results_tags = ''
        for elem in gv.results_tags_danbooru:
            if elem in self.tags:
                results_tags = results_tags + elem + '\n' 
        self.results_tags_lbl.configure(text = results_tags)

        if not path.isdir(self.path):
            #self.downloaded_var.set(1)
            self.downloaded_wxh_lbl.configure(text = str(self.downloaded_image.size))
            self.downloaded_type_lbl.configure(text = self.name[self.name.rfind(".")+1:])
        
        #self.modify_big_widgets_init = False
        self.modify_results_widgets_init = True
            
    def display_results(self, t):
        """
        Displays all widgets corresponding to this image on the results frame\n
        IMPORTANT:\n
        Call load, process_results_imgs and modify_results_widgets in that order before
        """
        #self.index = int(t/3)
        self.downloaded_chkbtn.grid(column = 0, row = t+2, sticky = W)
        self.downloaded_lbl.grid(column = 2, row = t+2, sticky = W, padx = 10)
        self.downloaded_wxh_lbl.grid(column = 3, row = t+2, sticky = W, padx = 10)
        self.downloaded_type_lbl.grid(column = 4, row = t+2, sticky = W, padx = 10)
        self.results_tags_lbl.grid(column = 5, row = t+2, sticky = W, padx = 10, columnspan=2)
        self.result_not_in_tagfile.grid(column = 7, row = t+2, sticky = W, padx = 10)
        
        t += 2
        return t
        
    def display_info(self, t):
        """
        Displays all widgets corresponding to this image on the info frame\n
        IMPORTANT:\n
        Call load and process_info_imgs in that order before
        """
        self.process_info_imgs()
        self.info_img_lbl.configure(image = self.downloaded_photoImage_preview)
        self.info_provider_lbl.configure(text = str(self.service), font = ('Arial Bold', 18))
        self.info_artist_lbl.configure(text = 'by ' + str(self.dict['artist']))
        self.info_title_lbl.configure(text = str(self.dict['title']), font = ('Arial Bold', 13))
        self.info_caption_lbl.configure(text = str(self.dict['caption']))
        #self.info_imageid_lbl.configure(text = 'Image ID: ' + str(self.illust.id))
        if self.source_url != None:
            self.info_url_lbl.configure(text = self.source_url[0], foreground='#2626ff', cursor='hand2', font=('Arial', 10))     
            self.info_url_lbl.bind("<Button-1>", self.hyperlink)
        else:
            self.info_url_lbl.configure(text = 'No URL', font=('Arial', 10))
        self.info_date_lbl.configure(text = 'Uploaded on: ' + str(self.dict['create_date']), font = ('Arial', 10))
        self.info_wxh_lbl.configure(text = 'Width x Height: ' + str(self.dict['width']) + ' x ' + str(self.dict['height']), font = ('Arial', 10))

        self.info_img_lbl.grid(column = 0, row = t + 1, rowspan = 9, sticky=W+N)
        self.info_provider_lbl.grid(column = 0, row = t + 0, sticky = W)
        self.info_title_lbl.grid(column = 1, row = t + 1, sticky = W, padx = 5)
        self.info_caption_lbl.grid(column = 1, row = t + 2, sticky = W, padx = 5)
        self.info_artist_lbl.grid(column = 1, row = t + 3, sticky = W, padx = 5)
        #self.info_imageid_lbl.grid(column = 1, row = t + 4, sticky = W, padx = 5)
        self.info_date_lbl.grid(column = 1, row = t + 5, sticky = W, padx = 5)
        
        # if len(self.sub_dir_array_pixiv) < 1:#
        #     self.info_wxh_lbl.grid(column = 1, row = 6, sticky = W, padx = 5)
        # self.info_url_lbl.grid(column = 0, row = 10, columnspan = 3, sticky = W)
        self.tags_pixiv_lbl.grid(column = 0, row = 11, sticky = W)


        if self.service == 'Pixiv':
            for lbl in self.tags_lbl_array:
                if lbl[1].cget('text') == '':
                    lbl[0].grid(column = 0, row = 12 + t, sticky = W, columnspan=2)
                else:
                    lbl[0].grid(column = 0, row = 12 + t, sticky = W)
                    lbl[1].grid(column = 1, row = 12 + t, sticky = W)
                t += 1
        else:
            for lbl in self.tags_lbl_array:
                lbl.grid(column = 0, row = (12 + int(t)), sticky = W, columnspan = 2)
                t += 1

    def process_info_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if self.process_info_imgs_init:
            return

        if path.isfile(self.path):
            self.downloaded_image_preview = deepcopy(self.downloaded_image)
        elif path.isdir(self.path):
            try:
                self.downloaded_image_preview = Image.open(self.path + '/' + listdir(self.path)[0])
            except Exception as e:
                print("ERROR [0043] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0043] " + str(e))
                mb.showerror("ERROR [0043]", "ERROR CODE [0043]\nSomething went wrong while accessing an image, please restart Sourcery.")
                return
        self.downloaded_image_preview.thumbnail(self.preview_size, resample=Image.ANTIALIAS)
        self.downloaded_photoImage_preview = ImageTk.PhotoImage(self.downloaded_image_preview)
        self.downloaded_image_preview.close()

        self.process_info_imgs_init = True

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
        if path.isfile(self.path):
            self.downloaded_SubImgData.display_grid(t)
            gv.big_frame.grid_rowconfigure(3, weight = 1)
            return t + 4
        elif path.isdir(self.path):
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

        if path.isfile(self.path):
            self.downloaded_SubImgData = SubImageData(self.name, self.path, self.service, gv.window, gv.big_frame, self.downloaded_image, self.downloaded_var, siblings=self.siblings_array)#ImageTk.PhotoImage(self.downloaded_image_pixiv)
            self.downloaded_SubImgData.load()
            self.siblings_array.append(self.downloaded_SubImgData)
        elif path.isdir(self.path):
            for elem in self.sub_dir_img_array:
                elem.load()

        self.process_big_imgs_init = True

    def delete_both(self):
        """
        Returns True if self.downloaded_var is 0 and self.sub_dir_img_array[...].var is 0, otherwise False\n
        Returns True if user has not checked any images in this class to save, otherwise False
        """
        if self.downloaded_var.get() == 0:
            for img in self.sub_dir_img_array:
                if img.var.get() == 1:
                    return False
            return True
        return False

    def save(self, pixiv_tags, danbooru_tags, t=-1, head_dir=''):
        #new_dir = gv.output_dir + '/' + self.name
        #--If only one image is checked, save your image with the name--#
        if t == -1:
            if self.downloaded_var.get() == 1:
                img_name = ''
                if path.isfile(self.path):
                    img_name = self.name[:self.name.rfind('.')]
                elif path.isdir(self.path):
                    img_name = self.name
                self.gen_tagfile(pixiv_tags, danbooru_tags, gv.output_dir, img_name)
                move(self.path, gv.output_dir + '/' + self.name)
            else:
                if self.path not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.path)
                for elem in self.sub_dir_img_array:
                    elem.save(pixiv_tags, danbooru_tags)
        ##----##

        #--If more than one image is checked, save your image in the new head directory(full path) with name + t + suffix--#
        else:
            if self.downloaded_var.get() == 1:
                if path.isdir(self.path):
                    move(self.path, head_dir + '/' + self.name + '_' + str(t))
                    for img in self.sub_dir_img_array:
                        img.gen_tagfile(pixiv_tags, danbooru_tags, head_dir + '/' + self.name + '_' + str(t), img.name[:img.name.rfind('.')])
                elif path.isfile(self.path):
                    move(self.path, head_dir + '/' + self.name[:self.name.rfind('.')] + '_' + str(t) + self.name[self.name.rfind('.'):])
                    self.gen_tagfile(pixiv_tags, danbooru_tags, head_dir, self.name[:self.name.rfind('.')] + '_' + str(t))
            else:
                if self.path not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.path)
                for elem in self.sub_dir_img_array:
                    elem.save(pixiv_tags, danbooru_tags, t, head_dir)
        ##----##

        # TODO try except
        # TODO clear results screen

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

    def gen_tagfile(self, pixiv_tags, danbooru_tags, gen_dir, name):
        if self.service == 'Pixiv' and gv.Files.Conf.gen_tagfile_pixiv == '1':
            all_tags = list()
            if gv.Files.Conf.tagfile_pixiv_pixiv == '1':
                all_tags.extend(pixiv_tags)
            if gv.Files.Conf.tagfile_danbooru_pixiv == '1':
                all_tags.extend(danbooru_tags)
            gen_tagfile(all_tags, gen_dir, name)
        elif self.service == 'Danbooru' and gv.Files.Conf.gen_tagfile_danbooru == '1':
            all_tags = list()
            if gv.Files.Conf.tagfile_pixiv_danbooru == '1':
                all_tags.extend(pixiv_tags)
            if gv.Files.Conf.tagfile_danbooru_danbooru == '1':
                all_tags.extend(danbooru_tags)
            gen_tagfile(all_tags, gen_dir, name)
    
    def get_tags_list(self, not_in_file=-1):
        """
        Returns a string list of all tags of the image from the provider
        """
        if not_in_file == -1:
            not_in_file = self.result_not_in_tagfile_var.get()
        
        if not_in_file == 0:
            ret_list = list()
            if self.service == 'Pixiv':
                for tag in self.illustration.tags:
                    ret_list.append(tag)
                ret_list.append('pixiv work:' + str(self.illustration.id))
                ret_list.append('title:' + self.illustration.title)
                ret_list.append('rating:' + str(self.illustration.sanity_level))
            if self.service == 'Danbooru':
                for tag in self.illustration['tag_string_general'].strip("'").split():
                    ret_list.append(tag)
                for tag in self.illustration['tag_string_character'].strip("'").split():
                    ret_list.append('character:' + tag)
                for tag in self.illustration['tag_string_copyright'].strip("'").split():
                    ret_list.append('copyright:' + tag)
                for tag in self.illustration['tag_string_artist'].strip("'").split():
                    ret_list.append('creator:' + tag)
                for tag in self.illustration['tag_string_meta'].strip("'").split():
                    ret_list.append('meta:' + tag)
                ret_list.append('booru:danbooru')
                ret_list.append('source:' + self.illustration['source'])
                ret_list.append('rating:' + self.illustration['rating'])
                if self.illustration['pixiv_id'] != None:
                    ret_list.append('pixiv work:' + str(self.illustration['pixiv_id']))
            return ret_list

    def evaluate_weight(self, original_aspect_ratio, original_width):
        img_weight = 0
        aspect_flag = False
        filetype = self.name.split('.')[-1]
        if filetype == 'png':
            img_weight = img_weight + int(gv.Files.Conf.png_weight)
        elif filetype == 'jpg':
            img_weight = img_weight + int(gv.Files.Conf.jpg_weight)
        elif filetype == 'jfif':
            img_weight = img_weight + int(gv.Files.Conf.jfif_weight)
        elif filetype == 'gif':
            img_weight = img_weight + int(gv.Files.Conf.gif_weight)
        elif filetype == 'bmp':
            img_weight = img_weight + int(gv.Files.Conf.bmp_weight)
        else:
            img_weight = img_weight + int(gv.Files.Conf.other_weight)

        if self.service == 'Danbooru':
            img_weight = img_weight + int(gv.Files.Conf.danbooru_weight)
        elif self.service == 'Pixiv':
            img_weight = img_weight + int(gv.Files.Conf.pixiv_weight)

        if original_aspect_ratio == int(self.dict['width'])/int(self.dict['height']):
            if int(self.dict['width']) > original_width:
                img_weight = img_weight + int(gv.Files.Conf.higher_resolution_weight)
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

    def self_destruct(self):
        if self.downloaded_SubImgData != None:
            self.downloaded_SubImgData.self_destruct()
        if self.downloaded_image != None:
            self.downloaded_image.close()
        for img in self.sub_dir_img_array:
            img.self_destruct()
        self.downloaded_photoImage_thumb = None
        self.downloaded_photoImage_preview = None

        self.downloaded_chkbtn.image = None
