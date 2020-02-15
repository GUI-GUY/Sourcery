from os import path, listdir
from tkinter import IntVar, W
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from tkinter import messagebox as mb
from copy import deepcopy
#from file_operations import is_image
import global_variables as gv

class ImageData():
    """PixivOptions"""
    def __init__(self, name, img_data_array, illust):
        self.name_original = name
        self.name_pixiv = str(illust.id)
        self.set_name_pixiv()
        # print('illus ID: ' + str(illust.id))
        # print('illus title' + illust.title)
        # self.service = img_data_array[0]
        # self.illust_id = img_data_array[1]
        # self.member_id = img_data_array[2]
        # self.source_url = img_data_array[3]
        self.path_original = gv.cwd + '/Sourcery/sourced_original/' + self.name_original
        self.path_pixiv = gv.cwd + '/Sourcery/sourced_progress/pixiv/' + self.name_pixiv
        # print("or: " + self.path_original)
        # print("pix: " + self.path_pixiv)
        self.original_image = None
        self.downloaded_image_pixiv = None
        self.sub_dir_array_pixiv = list()
        self.sub_dir_img_array_pixiv = list()
        self.thumb_size = (70,70)
        self.original_image_thumb = None
        self.original_photoImage_thumb = None
        self.downloaded_image_pixiv_thumb = None
        self.downloaded_photoImage_pixiv_thumb = None
        self.original_var = IntVar(value=0)
        self.original_chkbtn = Checkbutton(gv.frame, var=self.original_var, style="chkbtn.TCheckbutton")
        self.original_lbl = Label(gv.frame, text = "original", style='label.TLabel')
        self.original_wxh_lbl = Label(gv.frame, style='label.TLabel')
        self.original_type_lbl = Label(gv.frame, style='label.TLabel')
        self.original_cropped_lbl = Label(gv.frame, style='label.TLabel')
        self.downloaded_var = IntVar(value=1)
        self.downloaded_chkbtn = Checkbutton(gv.frame, var=self.downloaded_var, style="chkbtn.TCheckbutton")
        self.downloaded_lbl = Label(gv.frame, text = "pixiv", style='label.TLabel')
        self.downloaded_wxh_lbl = Label(gv.frame, text = "More images", style='label.TLabel')
        self.downloaded_type_lbl = Label(gv.frame, text = "More images", style='label.TLabel')
        self.big_selector_btn = Button(gv.frame, text='View in Big Selector', style='button.TLabel')

    def set_name_pixiv(self):
        """
        Sets correct name for pixiv
        """
        dir = listdir(gv.cwd + '/Sourcery/sourced_progress/pixiv/')
        for elem in dir:
            test = elem.rsplit('.', 1)
            if self.name_pixiv == test[0]:
                self.name_pixiv = elem

    def load(self):
        """
        Loads images into memory
        """
        original_image = Image.open(gv.cwd + '/Sourcery/sourced_original/' + self.name_original)
        if path.isfile(self.path_pixiv):
            try:
                self.original_image = Image.open(self.path_original)
                self.downloaded_image_pixiv = Image.open(self.path_pixiv)
            except Exception as e:
                print("ERROR [0031] " + str(e))
                mb.showerror("ERROR [0031]", "ERROR CODE [0031]\nSomething went wrong while loading an image.")
                gv.Files.Log.write_to_log("ERROR [0031] " + str(e))
        elif path.isdir(self.path_pixiv):
            try:
                self.sub_dir_array_pixiv.extend(listdir(self.path_pixiv))
                if len(self.sub_dir_array_pixiv) == 0:
                    if self.path_pixiv not in gv.delete_dirs_array:
                        gv.delete_dirs_array.append(self.path_pixiv)
                        #gv.safe_to_show_array.remove(cropped)
                #gv.chkbtn_vars_array[int(t/3)][0].set(1)
                #gv.chkbtn_vars_array[int(t/3)][1].set(0)
                self.original_image = Image.open(self.path_original)
                for img in self.sub_dir_array_pixiv:
                    self.sub_dir_img_array_pixiv.append(Image.open(self.path_pixiv + '/' + img))
            except Exception as e:
                print("ERROR [0032] " + str(e))
                mb.showerror("ERROR [0032]", "ERROR CODE [0032]\nSomething went wrong while loading an image.")
                gv.Files.Log.write_to_log("ERROR [0032] " + str(e))
                
    def display_results(self, t):
        """
        Displays all widgets corresponding to this image\n
        IMPORTANT:\n
        Call load, process_results_imgs and modify_widgets in that order before
        """
        self.original_chkbtn.grid(column = 0, row = t+1)
        self.original_lbl.grid(column = 2, row = t+1, sticky = W, padx = 10)
        self.original_wxh_lbl.grid(column = 3, row = t+1, sticky = W, padx = 10)
        self.original_type_lbl.grid(column = 4, row = t+1, sticky = W, padx = 10)
        self.original_cropped_lbl.grid(column = 1, row = t, columnspan=3, sticky = W, padx = 10)
        self.downloaded_chkbtn.grid(column = 0, row = t+2)
        self.downloaded_lbl.grid(column = 2, row = t+2, sticky = W, padx = 10)
        self.downloaded_wxh_lbl.grid(column = 3, row = t+2, sticky = W, padx = 10)
        self.downloaded_type_lbl.grid(column = 4, row = t+2, sticky = W, padx = 10)
        self.big_selector_btn.grid(column = 5, row = t+2, sticky = W, padx = 10)

        
    def process_results_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        self.original_image_thumb = deepcopy(self.original_image)
        self.original_image_thumb.thumbnail(self.thumb_size, resample=Image.ANTIALIAS)
        self.original_photoImage_thumb = ImageTk.PhotoImage(self.original_image_thumb)
        self.original_image_thumb.close()

        if path.isfile(self.path_pixiv):
            self.downloaded_image_pixiv_thumb = deepcopy(self.downloaded_image_pixiv)
        elif path.isdir(self.path_pixiv):
            self.downloaded_image_pixiv_thumb = deepcopy(self.sub_dir_img_array_pixiv[0])
        self.downloaded_image_pixiv_thumb.thumbnail(self.thumb_size, resample=Image.ANTIALIAS)
        self.downloaded_photoImage_pixiv_thumb = ImageTk.PhotoImage(self.downloaded_image_pixiv_thumb)
        self.downloaded_image_pixiv_thumb.close()

    def modify_widgets(self):
        """
        Fills widgets with information\n
        IMPORTANT:\n
        Call load and process_results_imgs in that order before
        """
        self.original_chkbtn.configure(image=self.original_photoImage_thumb)
        self.original_chkbtn.image = self.original_photoImage_thumb
        self.original_wxh_lbl.configure(text = str(self.original_image.size))
        self.original_type_lbl.configure(text = self.name_original[self.name_original.rfind('.')+1:])
        self.original_cropped_lbl.configure(text = self.name_original[:self.name_original.rfind('.')])
        self.downloaded_chkbtn.configure(image=self.downloaded_photoImage_pixiv_thumb)
        self.downloaded_chkbtn.image = self.downloaded_photoImage_pixiv_thumb
        #big_selector_partial = partial(display_big_selector, int(t/3))
        self.big_selector_btn.configure(command=self.display_big_selector)
        if path.isdir(self.path_pixiv):
            self.downloaded_chkbtn.configure(state = 'disabled')
        else:
            self.downloaded_wxh_lbl.configure(text = str(self.downloaded_image_pixiv.size))# downloaded_wxh_lbl
            self.downloaded_type_lbl.configure(text = self.name_pixiv[self.name_pixiv.rfind(".")+1:])# downloaded_type_lbl
            self.downloaded_chkbtn.configure(state = 'enabled')

    def display_big_selector(self):
        pass


    def image_opener(self, img, cropped, t, sourced_original_array, pixiv_sub_dir_array):
        dir_flag = False
        sub = ''
        if path.isfile(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img):
            for image in sourced_original_array:
                if image[0] == cropped:
                    suffix = image[2]
                    break
            if suffix == '':
                if gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                    gv.safe_to_show_array.remove(cropped)
                return None,None,None,None,None, True
            try:
                original_image = Image.open(gv.cwd + '/Sourcery/sourced_original/' + cropped + '.' + suffix) 
                downloaded_image = Image.open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img)
            except Exception as e:
                print("ERROR [0005] " + str(e))
                mb.showerror("ERROR [0005]", "ERROR CODE [0005]\nSomething went wrong while loading an image, please go back and try again.")
                gv.Files.Log.write_to_log("ERROR [0005] " + str(e))
                return
        elif path.isdir(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img):
            dir_flag = True
            try:
                pixiv_sub_dir_array.extend(listdir(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img))
                if len(pixiv_sub_dir_array) == 0:
                    if gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img not in gv.delete_dirs_array:
                        gv.delete_dirs_array.append(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                        gv.safe_to_show_array.remove(cropped)
                    return None,None,None,None,None, True
                pathname = ''
                for image in sourced_original_array:
                    if image[0] == img:
                        pathname = gv.cwd + '/Sourcery/sourced_original/' + image[0] + image[1] + image[2]
                        suffix = image[2]
                        break
                if suffix == '':
                    if gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img not in gv.delete_dirs_array:
                        gv.delete_dirs_array.append(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                        gv.safe_to_show_array.remove(cropped)
                    return None,None,None,None,None, True
                gv.chkbtn_vars_array[int(t/3)][0].set(1)
                gv.chkbtn_vars_array[int(t/3)][1].set(0)
                sub = pixiv_sub_dir_array[0]
                original_image = Image.open(pathname)
                downloaded_image = Image.open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img + '/' + pixiv_sub_dir_array[0])
            except Exception as e:
                print("ERROR [0006] " + str(e))
                mb.showerror("ERROR [0006]", "ERROR CODE [0006]\nSomething went wrong while loading an image, please go back and try again.")
                gv.Files.Log.write_to_log("ERROR [0006] " + str(e))
                return
        return original_image, downloaded_image, suffix, sub, dir_flag, False
            