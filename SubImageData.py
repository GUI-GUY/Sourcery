from os import path, listdir, remove, makedirs
from shutil import move, rmtree
from tkinter import IntVar, W, N, E, S, ACTIVE, NORMAL
from tkinter import Checkbutton as cb
from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from webbrowser import open_new
from copy import deepcopy
from file_operations import is_image, gen_tagfile, resize
import global_variables as gv

class SubImageData():
    """Includes information for images in subdirectories of downloads"""
    def __init__(self, name, path, service, parent, scrollparent, folder_var=None, var=None, master_folder='', siblings=list()):
        self.name = name
        self.path = path + '/' + name
        self.service = service
        self.par = parent
        self.scrollpar = scrollparent
        self.img_obj = None
        self.photoImg_thumb = None
        self.photoImg = None
        self.size = None
        if var == None:
            self.var = IntVar(value=0)
        else:
            self.var = var
        self.folder_var = folder_var
        
        self.folder = master_folder

        self.siblings_array = siblings

        self.is_displayed = False
        self.load_init = False
    
    def init_widgets(self):
        def folder_toggle():
            if self.var.get() == 0:
                self.folder_var.set(0)
        self.chkbtn = cb(self.par, var=self.var, command= folder_toggle,
            foreground=gv.Files.Theme.foreground, 
            background=gv.Files.Theme.background, 
            borderwidth = 1,
            highlightthickness = 6, 
            selectcolor=gv.Files.Theme.checkbutton_pressed, 
            activebackground=gv.Files.Theme.button_background_active, 
            activeforeground=gv.Files.Theme.button_foreground_active, 
            relief='flat',#default flat
            overrelief='ridge',#no default
            offrelief='flat',#default raised
            indicatoron='false')# sunken, raised, groove, ridge, flat, style="chkbtn.TCheckbutton"
        self.thumb_chkbtn = cb(self.scrollpar, var=self.var, command= folder_toggle,
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
        self.lbl = Label(self.scrollpar, text=self.service, style='label.TLabel')
        self.lbl2 = Label(self.par, text=self.service, style='label.TLabel')
        self.wxh_lbl = Label(self.scrollpar, style='label.TLabel')
        self.type_lbl = Label(self.scrollpar, style='label.TLabel')
        self.show_btn = Button(self.scrollpar, command=self.show, text='Show', style='button.TLabel')


    def load(self, second_try=False):
        """
        Loads image into memory
        """
        if self.load_init:
            return True

        try:
            self.img_obj = Image.open(self.path)
        except Exception as e:
            if not second_try:
                return self.load(True)
            else:
                print("ERROR [0044] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0044] " + str(e))
                mb.showerror("ERROR [0044]", "ERROR CODE [0044]\nSomething went wrong while accessing an image, please restart Sourcery.")
                return False
        self.size = deepcopy(self.img_obj.size)
        self.img_obj = resize(self.img_obj)
        self.photoImg = ImageTk.PhotoImage(self.img_obj)
        try:
            self.img_obj.close()
        except:
            pass
        self.img_obj = None
        
        def assign():
            self.chkbtn.configure(image=self.photoImg)
            self.chkbtn.image = self.photoImg
            self.wxh_lbl.configure(text=self.size)
            self.type_lbl.configure(text=self.name[self.name.rfind(".")+1:])
        self.par.after(1, assign)

        if self.scrollpar != None:
            try:
                img_obj_thumb = Image.open(self.path)
            except Exception as e:
                if not second_try:
                    return self.load(True)
                else:
                    print("ERROR [0071] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0071] " + str(e))
                    mb.showerror("ERROR [0071]", "ERROR CODE [0071]\nSomething went wrong while accessing an image, please restart Sourcery.")
                    return False
            #img_obj_thumb = deepcopy(self.img_obj)
            img_obj_thumb.thumbnail((70, 70), resample=Image.ANTIALIAS)
            self.photoImg_thumb = ImageTk.PhotoImage(img_obj_thumb)
            try:
                img_obj_thumb.close()
            except:
                pass
            def assign2():
                self.thumb_chkbtn.configure(image=self.photoImg_thumb)
                self.thumb_chkbtn.image = self.photoImg_thumb
            self.thumb_chkbtn.after(1, assign2)

        self.load_init = True
        return True
    
    def display_grid(self, t):
        """
        Use this for the downloaded images
        Display the preview and corresponding info on the big selector scrollframe
        """
        self.thumb_chkbtn.grid(row=t, column=0, rowspan=4, sticky=W+E+N+S)
        self.lbl.grid(row=t+0, column=1, sticky=W+E)
        self.wxh_lbl.grid(row=t+1, column=1, sticky=W+E)
        self.type_lbl.grid(row=t+2, column=1, sticky=W+E)
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
        self.is_displayed = True
        self.lbl2.place(x = int(gv.width*0.44), y = int(gv.height/90*2))
        self.chkbtn.place(x = int(gv.width*0.43), y = int(gv.height/90*4))
        try:
            self.thumb_chkbtn.configure(background=gv.Files.Theme.selected_background)
        except:
            pass
        self.lbl.configure(background=gv.Files.Theme.selected_background)
        self.wxh_lbl.configure(background=gv.Files.Theme.selected_background)
        self.type_lbl.configure(background=gv.Files.Theme.selected_background)
        self.show_btn.configure(state=ACTIVE)
        gv.window.bind("<d>", lambda e: self.var.set(not self.var.get()))

    def forget(self):
        self.lbl2.place_forget()
        self.chkbtn.place_forget()
        try:
            self.thumb_chkbtn.configure(background=gv.Files.Theme.background)
        except:
            pass
        self.lbl.configure(background=gv.Files.Theme.background)
        self.wxh_lbl.configure(background=gv.Files.Theme.background)
        self.type_lbl.configure(background=gv.Files.Theme.background)
        self.show_btn.configure(state=NORMAL)
        self.is_displayed = False

    def save(self, pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=-1, head_dir='', second_try=False):
        #--If only one image is checked, save your image in the subfolder with the name--#
        if t == -1:
            if self.var.get() == 1:
                try:
                    makedirs(gv.output_dir + '/' + self.folder, 0o777, True)
                except Exception as e:
                    if not second_try:
                        return self.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=t, head_dir=head_dir, second_try=True)
                    else:
                        print("ERROR [0051] " + str(e))
                        gv.Files.Log.write_to_log("ERROR [0051] " + str(e))
                        #mb.showerror("ERROR [0051]", "ERROR CODE [0051]\nSomething went wrong while creating the folder" + gv.output_dir + '/' + self.folder)
                        return False
                if not self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gv.output_dir + '/' + self.folder, self.name[:self.name.rfind('.')]):
                    self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gv.output_dir + '/' + self.folder, self.name[:self.name.rfind('.')])
                try:
                    move(self.path, gv.output_dir + '/' + self.folder + '/' + self.name)
                except Exception as e:
                    if not second_try:
                        return self.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=t, head_dir=head_dir, second_try=True)
                    else:
                        print("ERROR [0037] " + str(e))
                        gv.Files.Log.write_to_log("ERROR [0037] " + str(e))
                        #mb.showerror("ERROR [0037]", "ERROR CODE [0037]\nSomething went wrong while moving the image " + self.path_original)
                        return False
            return True
            # save your images in outputdir+self.folder
        ##----##

        #--If more than one image is checked, save your image in the new head directory(full path) in the subfolder with name + t + suffix--#
        else:
            if self.var.get() == 1:
                try:
                    makedirs(head_dir + '/' + self.folder, 0o777, True)
                except Exception as e:
                    if not second_try:
                        return self.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=t, head_dir=head_dir, second_try=True)
                    else:
                        print("ERROR [0052] " + str(e))
                        gv.Files.Log.write_to_log("ERROR [0052] " + str(e))
                        #mb.showerror("ERROR [0052]", "ERROR CODE [0051]\nSomething went wrong while creating the folder" + head_dir + '/' + self.folder)
                        return False
                if not self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, head_dir + '/' + self.folder, self.name[:self.name.rfind('.')]):
                    self.gen_tagfile(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, head_dir + '/' + self.folder, self.name[:self.name.rfind('.')])
             
                try:
                    move(self.path, head_dir + '/' + self.folder + '/' + self.name)
                except Exception as e:
                    if not second_try:
                        return self.save(pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, t=t, head_dir=head_dir, second_try=True)
                    else:
                        print("ERROR [0049] " + str(e))
                        gv.Files.Log.write_to_log("ERROR [0049] " + str(e))
                        #mb.showerror("ERROR [0049]", "ERROR CODE [0049]\nSomething went wrong while moving the image " + self.path)
                        return False
            return True
            # save your images in outputdir+self.folder+t
        ##----##

    def get_save_status(self):
        """
        Returns True if at least one box is checked, False otherwise
        """
        if self.var.get() == 1:
            return True
        return False

    def gen_tagfile(self, pixiv_tags, danbooru_tags, yandere_tags, konachan_tags, exception_tags, gen_dir, name):
        p_pos = name.rfind('_p')
        all_tags = list()
        if p_pos != -1:
            all_tags.append('page:' + name[p_pos+2:])
        if self.service == 'Pixiv' and gv.config['Pixiv']['gen_tagfile'] == '1':
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
        elif self.service == 'Danbooru' and gv.config['Danbooru']['gen_tagfile'] == '1':
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
        elif self.service == 'Yandere' and gv.config['Yandere']['gen_tagfile'] == '1':
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
        elif self.service == 'Konachan' and gv.config['Konachan']['gen_tagfile'] == '1':
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

    def unload_big_imgs(self):
        if self.chkbtn != None:
            self.chkbtn.configure(image=None)
            self.chkbtn.image = None
        if self.thumb_chkbtn != None:
            self.thumb_chkbtn.configure(image=None)
            self.thumb_chkbtn.image = None
        self.photoImg_thumb = None
        self.photoImg = None
        self.load_init = False

    def self_destruct(self):
        if self.chkbtn != None:
            self.chkbtn.configure(image=None)
            self.chkbtn.image = None
        if self.thumb_chkbtn != None:
            self.thumb_chkbtn.configure(image=None)
            self.thumb_chkbtn.image = None
        del self.photoImg_thumb
        del self.photoImg
        self.chkbtn.destroy()
        self.thumb_chkbtn.destroy()
        self.lbl.destroy()
        self.lbl2.destroy()
        self.wxh_lbl.destroy()
        self.type_lbl.destroy()
        self.show_btn.destroy()

