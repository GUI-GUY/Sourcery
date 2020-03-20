from os import path, listdir, remove, makedirs
from shutil import move, rmtree
from tkinter import IntVar, W, N
from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from webbrowser import open_new
from copy import deepcopy
from file_operations import is_image, gen_tagfile, resize
import global_variables as gv

class SubImageData():
    """Includes information for images in subdirectories of downloads"""
    def __init__(self, name, path, service, parent, scrollparent, img=None, var=None, master_folder='', siblings=list()):
        self.name = name
        self.path = path + '/' + name
        self.service = service
        self.par = parent
        self.scrollpar = scrollparent
        self.img_obj = img
        self.photoImg_thumb = None
        self.photoImg = None
        self.size = None
        if var == None:
            self.var = IntVar(value=0)
        else:
            self.var = var
        self.chkbtn = None
        self.thumb_chkbtn = None
        self.lbl = None
        self.lbl2 = None
        self.wxh_lbl = None
        self.type_lbl = None
        self.folder = master_folder
        self.show_btn = None

        self.siblings_array = siblings

        self.load_init = False

    def load(self):
        """
        Loads image into memory
        """
        if self.load_init:
            return
        flag = False
        if self.img_obj == None:
            flag = True
            try:
                self.img_obj = Image.open(self.path)
            except Exception as e:
                print("ERROR [0044] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0044] " + str(e))
                mb.showerror("ERROR [0044]", "ERROR CODE [0044]\nSomething went wrong while accessing an image, please restart Sourcery.")
                return
        self.size = self.img_obj.size
        self.photoImg = ImageTk.PhotoImage(resize(self.img_obj))
        
        if self.var == None:
            self.var = IntVar()
        self.chkbtn = Checkbutton(self.par, image=self.photoImg, var=self.var, style="chkbtn.TCheckbutton")
        self.chkbtn.image = self.photoImg
        self.lbl = Label(self.scrollpar, text=self.service, style='label.TLabel')
        self.lbl2 = Label(self.par, text=self.service, style='label.TLabel')
        self.wxh_lbl = Label(self.scrollpar, text=self.size, style='label.TLabel')
        self.type_lbl = Label(self.scrollpar, text=self.name[self.name.rfind(".")+1:], style='label.TLabel')
        self.show_btn = Button(self.scrollpar, command=self.show, text='Show', style='button.TLabel')

        if self.scrollpar != None:
            img_obj_thumb = deepcopy(self.img_obj)
            img_obj_thumb.thumbnail((70, 70), resample=Image.ANTIALIAS)
            self.photoImg_thumb = ImageTk.PhotoImage(img_obj_thumb)
            self.thumb_chkbtn = Checkbutton(self.scrollpar, image=self.photoImg_thumb, var=self.var, style="chkbtn.TCheckbutton")
            self.thumb_chkbtn.image = self.photoImg_thumb
            img_obj_thumb.close()

        if flag:
            self.img_obj.close()

        self.load_init = True
    
    def display_grid(self, t):
        """
        Use this for the downloaded images
        Display the preview and corresponding info on the big selector scrollframe
        """
        self.thumb_chkbtn.grid(row=t, column=0, rowspan=4)
        self.lbl.grid(row=t+0, column=1, sticky=W)
        self.wxh_lbl.grid(row=t+1, column=1, sticky=W)
        self.type_lbl.grid(row=t+2, column=1, sticky=W)
        self.show_btn.grid(row=t+3, column=1, sticky=W)
    
    def display_place(self):
        """
        Use this for the original image
        Display the corresponding info above the big selector scrollframe
        """
        self.chkbtn.place(x = int(gv.width/160*1.5), y = int(gv.height/90*4))
        self.lbl2.place(x = int(gv.width/160*3.2), y = int(gv.height/90*2))
        self.lbl.place(x = int(gv.width*0.86), y = int(gv.height/90*6.3))
        self.wxh_lbl.place(x = int(gv.width*0.90), y = int(gv.height/90*6.3))
        self.type_lbl.place(x = int(gv.width*0.94), y = int(gv.height/90*6.3))

    def show(self):
        """
        Displays the image on the screen and forgets all siblings
        """
        for sib in self.siblings_array:
            sib.forget()
        self.lbl2.place(x = int(gv.width*0.44), y = int(gv.height/90*2))
        self.chkbtn.place(x = int(gv.width*0.43), y = int(gv.height/90*4))

    def forget(self):
        self.lbl2.place_forget()
        self.chkbtn.place_forget()

    def save(self, pixiv_tags, danbooru_tags, t=-1, head_dir=''):
        #--If only one image is checked, save your image in the subfolder with the name--#
        if t == -1:
            if self.var.get() == 1:
                makedirs(gv.output_dir + '/' + self.folder, 0o777, True)#TODO try except
                self.gen_tagfile(pixiv_tags, danbooru_tags, gv.output_dir + '/' + self.folder, self.name[:self.name.rfind('.')])
                try:
                    move(self.path, gv.output_dir + '/' + self.folder + '/' + self.name)
                except Exception as e:
                    print("ERROR [0037] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0037] " + str(e))
                    #mb.showerror("ERROR [0037]", "ERROR CODE [0037]\nSomething went wrong while moving the image " + self.path_original)
            # save your images in outputdir+self.folder
        ##----##

        #--If more than one image is checked, save your image in the new head directory(full path) in the subfolder with name + t + suffix--#
        else:
            if self.var.get() == 1:
                makedirs(head_dir + '/' + self.folder, 0o777, True)#TODO try except
                self.gen_tagfile(pixiv_tags, danbooru_tags, head_dir + '/' + self.folder, self.name[:self.name.rfind('.')])
                try:
                    move(self.path, head_dir + '/' + self.folder + '/' + self.name)
                except Exception as e:
                    print("ERROR [0049] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0049] " + str(e))
                    #mb.showerror("ERROR [0049]", "ERROR CODE [0049]\nSomething went wrong while moving the image " + self.path_original)
            # save your images in outputdir+self.folder+t
        ##----##

    def get_save_status(self):
        """
        Returns True if at least on box is checked, False otherwise
        """
        if self.var.get() == 1:
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

    def self_destruct(self):
        self.photoImg = None
        self.photoImg_thumb = None
        if self.chkbtn != None:
            self.chkbtn.image = None
        if self.thumb_chkbtn != None:
            self.thumb_chkbtn.image = None