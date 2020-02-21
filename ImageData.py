from os import path, listdir, remove
from shutil import move, rmtree
from tkinter import IntVar, W, N
#from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from webbrowser import open_new
from copy import deepcopy
from file_operations import is_image
import global_variables as gv

class ImageData():
    """PixivOptions"""
    def __init__(self, old_name, new_name, img_data_array, illust):
        self.name_original = old_name
        self.name_pixiv = new_name
        self.set_name_pixiv()
        self.illust = illust
        self.service = img_data_array[0]
        # self.illust_id = img_data_array[1]
        # self.member_id = img_data_array[2]
        self.source_url = img_data_array[3]
        self.path_original = gv.cwd + '/Sourcery/sourced_original/' + self.name_original
        self.path_pixiv = gv.cwd + '/Sourcery/sourced_progress/pixiv/' + self.name_pixiv
        self.original_image = None
        self.downloaded_image_pixiv = None
        self.sub_dir_array_pixiv = list()
        self.sub_dir_img_array_pixiv = list()
        self.thumb_size = (70,70)
        self.preview_size = (200, 200)
        self.original_image_thumb = None
        self.original_photoImage_thumb = None
        self.downloaded_image_pixiv_thumb = None
        self.downloaded_photoImage_pixiv_thumb = None
        self.downloaded_image_pixiv_preview = None
        self.downloaded_photoImage_pixiv_preview = None
        self.original_var = IntVar(value=0)
        self.original_chkbtn = Checkbutton(master=gv.frame, var=self.original_var, style="chkbtn.TCheckbutton")
        self.original_lbl = Label(master=gv.frame, text = "original", style='label.TLabel')
        self.original_wxh_lbl = Label(master=gv.frame, style='label.TLabel')
        self.original_type_lbl = Label(master=gv.frame, style='label.TLabel')
        self.original_cropped_lbl = Label(master=gv.frame, style='label.TLabel')
        self.downloaded_pixiv_var = IntVar(value=1)
        self.downloaded_chkbtn = Checkbutton(master=gv.frame, var=self.downloaded_pixiv_var, style="chkbtn.TCheckbutton")
        self.downloaded_lbl = Label(master=gv.frame, text = "pixiv", style='label.TLabel')
        self.downloaded_wxh_lbl = Label(master=gv.frame, text = "More images", style='label.TLabel')#TODO how many instead of more
        self.downloaded_type_lbl = Label(master=gv.frame, text = "More images", style='label.TLabel')
        self.big_selector_btn = Button(master=gv.frame, command=self.display_big_selector, text='View in Big Selector', style='button.TLabel')

        self.info_btn = Button(master=gv.frame, command=self.display_info, text='More Info', style='button.TLabel')
        
        self.info_img_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.info_provider_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.info_artist_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.info_title_lbl = Label(master=gv.frame3, style='label.TLabel')
        #self.info_imageid_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.info_url_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.info_date_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.info_caption_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.info_wxh_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.tags_pixiv_lbl = Label(master=gv.frame3, style='label.TLabel')
        self.tags_lbl_array = list()
        

        self.tags_lbl_array.append((Label(master=gv.frame3, text = 'Original:', style='label.TLabel', font = ('Arial Bold', 11)), Label(master=gv.frame3, text = 'Translated:', style='label.TLabel', font = ('Arial Bold', 11))))
        for tag in illust.tags:
            self.tags_lbl_array.append((Label(master=gv.frame3, text = tag['name'], style='label.TLabel'), Label(master=gv.frame3, text = tag['translated_name'], style='label.TLabel')))

        self.back_btn = Button(gv.window, text = 'Back', command = self.display_view_results, style = 'button.TLabel')
        self.next_btn = Button(gv.window, text = 'Next', style = 'button.TLabel')
        self.prev_btn = Button(gv.window, text = 'Prev', style = 'button.TLabel')
        self.index = None

        self.original_SubImgData = None
        self.downloaded_SubImgData_pixiv = None

        self.load_init = False
        self.process_results_imgs_init = False
        self.process_big_imgs_init = False
        self.modify_results_widgets_init = False
        self.modify_big_widgets_init = False
        self.process_info_imgs_init = False

    def set_name_pixiv(self):
        """
        Sets correct name for pixiv
        """
        dir = listdir(gv.cwd + '/Sourcery/sourced_progress/pixiv/')
        for elem in dir:
            if is_image(elem):
                test = elem.rsplit('.', 1)
                if self.name_pixiv == test[0]:
                    self.name_pixiv = elem

    def forget_all_widgets(self):
        for widget in gv.window.winfo_children():
            widget.place_forget()
        for widget in gv.frame2.winfo_children():
            widget.grid_forget()

    def load(self):
        """
        Loads images into memory
        """
        if self.load_init:
            return
        self.original_image = Image.open(self.path_original)
        if path.isfile(self.path_pixiv):
            try:
                self.downloaded_image_pixiv = Image.open(self.path_pixiv)
            except Exception as e:
                print("ERROR [0031] " + str(e))
                #mb.showerror("ERROR [0031]", "ERROR CODE [0031]\nSomething went wrong while loading an image.")
                gv.Files.Log.write_to_log("ERROR [0031] " + str(e))
        elif path.isdir(self.path_pixiv):
            try:
                self.sub_dir_array_pixiv.extend(listdir(self.path_pixiv))
                if len(self.sub_dir_array_pixiv) == 0:
                    if self.path_pixiv not in gv.delete_dirs_array:
                        gv.delete_dirs_array.append(self.path_pixiv)
                for img in self.sub_dir_array_pixiv:
                    self.sub_dir_img_array_pixiv.append(SubImageData(img, self.path_pixiv, 'pixiv', gv.frame2, master_folder=self.name_pixiv))#(Image.open(self.path_pixiv + '/' + img), img))
            except Exception as e:
                print("ERROR [0032] " + str(e))
                #mb.showerror("ERROR [0032]", "ERROR CODE [0032]\nSomething went wrong while loading an image.")
                gv.Files.Log.write_to_log("ERROR [0032] " + str(e))
        self.load_init = True

    def display_view_results(self):
        self.forget_all_widgets()
        gv.display_startpage()
        #gv.display_view_results()

    def display_results(self, t):
        """
        Displays all widgets corresponding to this image\n
        IMPORTANT:\n
        Call load, process_results_imgs and modify_results_widgets in that order before
        """
        self.index = int(t/3)
        self.original_chkbtn.grid(column = 0, row = t+1, sticky = W)
        self.original_lbl.grid(column = 2, row = t+1, sticky = W, padx = 10)
        self.original_wxh_lbl.grid(column = 3, row = t+1, sticky = W, padx = 10)
        self.original_type_lbl.grid(column = 4, row = t+1, sticky = W, padx = 10)
        self.info_btn.grid(column = 5, row = t+1, sticky = W, padx = 10)
        self.original_cropped_lbl.grid(column = 1, row = t, columnspan=3, sticky = W, padx = 10)
        self.downloaded_chkbtn.grid(column = 0, row = t+2, sticky = W)
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
        if self.process_results_imgs_init:
            return
        self.original_image_thumb = deepcopy(self.original_image)
        self.original_image_thumb.thumbnail(self.thumb_size, resample=Image.ANTIALIAS)
        self.original_photoImage_thumb = ImageTk.PhotoImage(self.original_image_thumb)
        self.original_image_thumb.close()

        if path.isfile(self.path_pixiv):
            self.downloaded_image_pixiv_thumb = deepcopy(self.downloaded_image_pixiv)
        elif path.isdir(self.path_pixiv):
            self.downloaded_image_pixiv_thumb = Image.open(self.path_pixiv + '/' + listdir(self.path_pixiv)[0])
        self.downloaded_image_pixiv_thumb.thumbnail(self.thumb_size, resample=Image.ANTIALIAS)
        self.downloaded_photoImage_pixiv_thumb = ImageTk.PhotoImage(self.downloaded_image_pixiv_thumb)
        self.downloaded_image_pixiv_thumb.close()

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
        self.original_wxh_lbl.configure(text = str(self.original_image.size))
        self.original_type_lbl.configure(text = self.name_original[self.name_original.rfind('.')+1:])
        self.original_cropped_lbl.configure(text = self.name_original[:self.name_original.rfind('.')])
        
        self.downloaded_chkbtn.configure(image=self.downloaded_photoImage_pixiv_thumb)
        self.downloaded_chkbtn.image = self.downloaded_photoImage_pixiv_thumb

        if path.isdir(self.path_pixiv):
            self.original_var.set(1)
            self.downloaded_pixiv_var.set(0)
        else:
            self.downloaded_wxh_lbl.configure(text = str(self.downloaded_image_pixiv.size))
            self.downloaded_type_lbl.configure(text = self.name_pixiv[self.name_pixiv.rfind(".")+1:])
            
        
        #self.modify_big_widgets_init = False
        self.modify_results_widgets_init = True

    def display_info(self):
        for widget in gv.frame3.winfo_children():
            widget.grid_forget()

        self.process_info_imgs()
        self.info_img_lbl.configure(image = self.downloaded_photoImage_pixiv_preview)
        self.info_provider_lbl.configure(text = str(self.service), font = ('Arial Bold', 18))
        self.info_artist_lbl.configure(text = 'by ' + str(self.illust.user.name))
        self.info_title_lbl.configure(text = str(self.illust.title), font = ('Arial Bold', 13))
        self.info_caption_lbl.configure(text = str(self.illust.caption))
        #self.info_imageid_lbl.configure(text = 'Image ID: ' + str(self.illust.id))
        if self.source_url != None:
            self.info_url_lbl.configure(text = self.source_url[0], foreground='#2626ff', cursor='hand2', font=('Arial', 10))     
            self.info_url_lbl.bind("<Button-1>", self.hyperlink)
        else:
            self.info_url_lbl.configure(text = 'No URL', font=('Arial', 10))
        self.info_date_lbl.configure(text = 'Uploaded on: ' + str(self.illust.create_date), font = ('Arial', 10))
        self.info_wxh_lbl.configure(text = 'Width x Height: ' + str(self.illust.width) + ' x ' + str(self.illust.height), font = ('Arial', 10))
        self.tags_pixiv_lbl.configure(text = 'Tags', font=('Arial Bold', 15))
        self.info_img_lbl.grid(column = 0, row = 1, rowspan = 9, sticky=W+N)
        self.info_provider_lbl.grid(column = 0, row = 0, sticky = W)
        self.info_title_lbl.grid(column = 1, row = 1, sticky = W, padx = 5)
        self.info_caption_lbl.grid(column = 1, row = 2, sticky = W, padx = 5)
        self.info_artist_lbl.grid(column = 1, row = 3, sticky = W, padx = 5)
        #self.info_imageid_lbl.grid(column = 1, row = 4, sticky = W, padx = 5)
        self.info_date_lbl.grid(column = 1, row = 5, sticky = W, padx = 5)
        
        self.info_wxh_lbl.grid(column = 1, row = 6, sticky = W, padx = 5)#TODO don't do this when more images
        self.info_url_lbl.grid(column = 0, row = 10, columnspan = 3, sticky = W)
        self.tags_pixiv_lbl.grid(column = 0, row = 11, sticky = W)
        
        t=0
        for lbl in self.tags_lbl_array:
            lbl[0].grid(column = 0, row = 12 + t, sticky = W)
            lbl[1].grid(column = 1, row = 12 + t, sticky = W)
            t += 1

    def process_info_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if self.process_info_imgs_init:
            return

        if path.isfile(self.path_pixiv):
            self.downloaded_image_pixiv_preview = deepcopy(self.downloaded_image_pixiv)
        elif path.isdir(self.path_pixiv):
            self.downloaded_image_pixiv_preview = Image.open(self.path_pixiv + '/' + listdir(self.path_pixiv)[0])
        self.downloaded_image_pixiv_preview.thumbnail(self.preview_size, resample=Image.ANTIALIAS)
        self.downloaded_photoImage_pixiv_preview = ImageTk.PhotoImage(self.downloaded_image_pixiv_preview)
        self.downloaded_image_pixiv_preview.close()

        self.process_info_imgs_init = True

    def hyperlink(self, event):
        open_new(event.widget.cget("text"))

    def display_big_selector(self):
        self.process_big_imgs()
        self.modify_big_widgets()
        self.forget_all_widgets()
        gv.big_selector_frame.place(x = round(gv.width*0.515), y = 20)
        gv.big_selector_canvas.yview_moveto(0)
        self.back_btn.place(x = round(gv.width*0.43), y = 100)
        self.prev_btn.place(x = round(gv.width*0.43), y = 123)
        self.next_btn.place(x = round(gv.width*0.43), y = 146)

        self.original_SubImgData.display_place()

        if path.isfile(self.path_pixiv):
            self.downloaded_SubImgData_pixiv.display_grid(0)
            gv.frame2.grid_rowconfigure(3, weight = 1)
        elif path.isdir(self.path_pixiv):
            t = 0
            for elem in self.sub_dir_img_array_pixiv:
                elem.display_grid(t)
                gv.frame2.grid_rowconfigure(t + 3, weight = 1)
                t += 4

    def process_big_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if self.process_big_imgs_init:
            return

        self.original_SubImgData = SubImageData(self.name_original, self.path_original, 'original', gv.window, self.original_image, self.original_var)#ImageTk.PhotoImage(resize(self.original_image))
        self.original_SubImgData.load()

        if path.isfile(self.path_pixiv):
            self.downloaded_SubImgData_pixiv = SubImageData(self.name_pixiv, self.path_pixiv, 'pixiv', gv.frame2, self.downloaded_image_pixiv, self.downloaded_pixiv_var)#ImageTk.PhotoImage(self.downloaded_image_pixiv)
            self.downloaded_SubImgData_pixiv.load()
        elif path.isdir(self.path_pixiv):
            for elem in self.sub_dir_img_array_pixiv:
                elem.load()

        self.process_big_imgs_init = True

    def modify_big_widgets(self):
        """
        Fills widgets with information\n
        IMPORTANT:\n
        Call load and process_big_imgs in that order before
        """
        if self.modify_big_widgets_init:
            return

        if self.index < len(gv.img_data_array)-1:
            self.next_btn.configure(state='enabled', command = gv.img_data_array[self.index+1].display_big_selector)
        else:
            self.next_btn.configure(state='disabled', command=None)
        if self.index > 0:
            self.prev_btn.configure(state='enabled', command = gv.img_data_array[self.index-1].display_big_selector)
        else:
            self.prev_btn.configure(state='disabled', command=None)

        self.modify_big_widgets_init = True
       
    def save(self):
        downloaded_name_new = None
        original_name_new = None

        if self.original_var.get() == 1:
            if self.downloaded_pixiv_var.get() == 1:
                downloaded_name_new = 'new_' + self.name_pixiv#TODO geht das mit renaming option?
                original_name_new = 'old_' + self.name_original
            else:
                # Move original image to Sourced and delete downloaded image/directory
                downloaded_name_new = None
                original_name_new = self.name_original
                if self.path_pixiv not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.path_pixiv)
        elif self.downloaded_pixiv_var.get() == 1:
            # Move downloaded image to Sourced and delete original image
            downloaded_name_new = self.name_pixiv
            original_name_new = None
            if self.path_original not in gv.delete_dirs_array:
                gv.delete_dirs_array.append(self.path_original)

        if self.downloaded_pixiv_var.get() == 0:#TODO Prompt: "Are you sure you want to delete both versions of [image]"
            for elem in self.sub_dir_img_array_pixiv:
                elem.save()
            if self.path_pixiv not in gv.delete_dirs_array:
                gv.delete_dirs_array.append(self.path_pixiv)
            if self.original_var.get() == 0:
                if self.path_original not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.path_original)

        if downloaded_name_new != None:
            try:
                move(self.path_pixiv, gv.cwd + '/Sourced/' + downloaded_name_new)
            except Exception as e:
                print("ERROR [0012] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0012] " + str(e))
                #mb.showerror("ERROR [0012]", "ERROR CODE [0012]\nSomething went wrong while moving the image " + self.path_pixiv)

        if original_name_new != None:
            try:
                move(self.path_original, gv.cwd + '/Sourced/' + original_name_new)
            except Exception as e:
                print("ERROR [0013] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0013] " + str(e))
                #mb.showerror("ERROR [0013]", "ERROR CODE [0013]\nSomething went wrong while moving the image " + self.path_original)
        try:
            remove(gv.cwd + '/Input/' + self.name_original)
        except Exception as e:
            print("ERROR [0014] " + str(e))
            gv.Files.Log.write_to_log("ERROR [0014] " + str(e))
            #mb.showerror("ERROR [0014]", "ERROR CODE [0014]\nSomething went wrong while removing the image " + gv.cwd + '/Input/' + self.name_original)

    def self_destruct(self):
        if self.original_SubImgData != None:
            self.original_SubImgData.self_destruct()
        if self.downloaded_SubImgData_pixiv != None:
            self.downloaded_SubImgData_pixiv.self_destruct()
        self.original_image.close()
        if self.downloaded_image_pixiv != None:
            self.downloaded_image_pixiv.close()
        for img in self.sub_dir_img_array_pixiv:
            img.self_destruct()
        del self.original_photoImage_thumb
        del self.downloaded_photoImage_pixiv_thumb
        del self.downloaded_photoImage_pixiv_preview

class SubImageData():
    def __init__(self, name, path, service, parent, img=None, var=None, master_folder=''):
        self.name = name
        self.path = path + '/' + name
        self.service = service
        self.par = parent
        self.img_obj = img
        self.photoImg = None
        self.size = None
        if var == None:
            self.var = IntVar(value=0)
        else:
            self.var = var
        self.chkbtn = None
        self.lbl = None
        self.wxh_lbl = None
        self.type_lbl = None
        self.folder = master_folder

        self.load_init = False

    def load(self):
        if self.load_init:
            return
        flag = False
        if self.img_obj == None:
            flag = True
            self.img_obj = Image.open(self.path)
        self.size = self.img_obj.size
        self.photoImg = ImageTk.PhotoImage(resize(self.img_obj))
        if flag:
            self.img_obj.close()
        if self.var == None:
            self.var = IntVar()
        self.chkbtn = Checkbutton(self.par, image=self.photoImg, var=self.var, style="chkbtn.TCheckbutton")
        self.chkbtn.image = self.photoImg
        self.lbl = Label(self.par, text=self.service, style='label.TLabel')
        self.wxh_lbl = Label(self.par, text=self.size, style='label.TLabel')
        self.type_lbl = Label(self.par, text=self.name[self.name.rfind(".")+1:], style='label.TLabel')

        self.load_init = True
    
    def display_grid(self, t):
        self.chkbtn.grid(row=t, column=1, rowspan=4)
        self.lbl.grid(row=t+0, column=0)
        self.wxh_lbl.grid(row=t+1, column=0)
        self.type_lbl.grid(row=t+2, column=0)
    
    def display_place(self):
        self.chkbtn.place(x = 15, y = 20)
        self.lbl.place(x = round(gv.width*0.43), y = 35)
        self.wxh_lbl.place(x = round(gv.width*0.43), y = 55)
        self.type_lbl.place(x = round(gv.width*0.43), y = 75)

    def save(self):
        if self.var.get() == 1:
            try:
                move(self.path, gv.cwd + '/Sourced/' + folder + '/' + self.name)
            except Exception as e:
                print("ERROR [0032] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0032] " + str(e))
                #mb.showerror("ERROR [0032]", "ERROR CODE [0032]\nSomething went wrong while moving the image " + self.path_original)

    def self_destruct(self):
        del self.photoImg

def resize(image):
    """
    Resizes given image to a third of the screen width and to the screen height-120 and returns it as a new object.
    """

    oldwidth = image.width
    oldheight = image.height

    new_image = deepcopy(image)

    if oldwidth > gv.width/3:
        newwidth = round(gv.width*0.4)
        newheight = round(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        new_image = image.resize(newsize, Image.ANTIALIAS)
    if new_image.height > gv.height-120:
        newheight = gv.height - 120
        newwidth = round(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        new_image = new_image.resize(newsize, Image.ANTIALIAS)
    return new_image