from os import path, listdir, remove, makedirs
from shutil import move, rmtree
from tkinter import IntVar, W, N
from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from webbrowser import open_new
from copy import deepcopy
from file_operations import is_image, gen_tagfile
import global_variables as gv

class ImageData():
    """Includes all information on the sourced images"""
    def __init__(self, old_name, pixiv_rename, danb_rename, dict_list, pixiv_illust_list, danbooru_illust_list, index):
        self.name_original = old_name
        self.thumb_size = (70,70)
        self.preview_size = (200, 200)
        self.siblings_array = list()
        self.pixiv_list = list()
        # dict_list is list of {"service_name": service_name, "illust_id": illust_id, "source": source}
        for elem in pixiv_illust_list:
            print('pixiv')
            print(elem[1])
            name = self.correct_name('pixiv', elem[1]) # TODO if name == False
            path_pixiv = gv.cwd + '/Sourcery/sourced_progress/pixiv/' + name
            self.pixiv_dict = self.pixiv_clean_dict(elem[0], dict_list) 
            self.pixiv_list.append(ProviderImageData('Pixiv', name, path_pixiv, self.thumb_size, self.preview_size, self.pixiv_dict, self.siblings_array))
        
        self.danb_list = list()
        for elem in danbooru_illust_list:
            print('dan')
            print(elem[1])
            name = self.correct_name('danbooru', elem[1]) # TODO if name == False
            path_danb = gv.cwd + '/Sourcery/sourced_progress/danbooru/' + name
            self.danb_dict = self.danbooru_clean_dict(elem[0], dict_list)
            self.danb_list.append(ProviderImageData('Danbooru', name, path_danb, self.thumb_size, self.preview_size, self.danb_dict, self.siblings_array))
        #self.name_pixiv = pixiv_name
        #self.set_name_pixiv()
        #self.name_danb = danb_name
        #self.set_name_danb()
        
        self.minsim = 80
        self.rename_pixiv = pixiv_rename
        self.rename_danbooru = danb_rename
        self.path_original = gv.cwd + '/Sourcery/sourced_original/' + self.name_original
        
        self.original_image = None
        self.downloaded_image_pixiv = None
        
        self.original_image_thumb = None
        self.original_photoImage_thumb = None

        self.original_var = IntVar(value=0)
        self.original_chkbtn = Checkbutton(master=gv.res_frame, var=self.original_var, style="chkbtn.TCheckbutton")
        self.original_lbl = Label(master=gv.res_frame, text = "Input", style='label.TLabel')
        self.original_wxh_lbl = Label(master=gv.res_frame, style='label.TLabel')
        self.original_type_lbl = Label(master=gv.res_frame, style='label.TLabel')
        self.original_cropped_lbl = Label(master=gv.res_frame, style='label.TLabel')

        self.big_selector_btn = Button(master=gv.res_frame, command=self.display_big_selector, text='Big Selector', style='button.TLabel')
        self.info_btn = Button(master=gv.res_frame, command=self.display_info, text='More Info', style='button.TLabel')        
        self.back_btn = Button(gv.window, text = 'Back', command = self.display_view_results, style = 'button.TLabel')
        self.next_btn = Button(gv.window, text = 'Next', style = 'button.TLabel')
        self.prev_btn = Button(gv.window, text = 'Previous', style = 'button.TLabel')
        self.index = index
        self.placed = False

        self.original_SubImgData = None

        self.load_init = False
        self.process_results_imgs_init = False
        self.process_big_imgs_init = False
        self.modify_results_widgets_init = False
        self.process_info_imgs_init = False
        self.locked = False

    def correct_name(self, folder, name):
        """
        Returns corrected given name on success, False otherwise
        """
        try:
            directory = listdir(gv.cwd + '/Sourcery/sourced_progress/' + folder + '/')
        except Exception as e:
            print("ERROR [0041] " + str(e))
            gv.Files.Log.write_to_log("ERROR [0041] " + str(e))
            mb.showerror("ERROR [0041]", "ERROR CODE [0041]\nSomething went wrong while accessing the 'Sourcery/sourced_progress/'" + folder + "folder, please restart Sourcery.")
            return False 
        for elem in directory:
            test = elem.rsplit('.', 1)
            if name == test[0]:
                return elem
        return False

    def pixiv_clean_dict(self, illust, dict_list):
        """
        Cleans up the dictionary to only include needed information and returns them as a formatted dictionary
        """
        x = None
        for t in dict_list:
            if t['service_name'] == 'Pixiv':
                x = t
                break
        if x == None:
            return None
        tags = list()
        for tag in illust.tags:
            tags.append(tag['name'] + ' | ' + str(tag['translated_name']))
        return {"artist": illust.user.name, "title": illust.title, "caption": illust.caption, "create_date": illust.create_date, "width": illust.width, "height": illust.height, "service": x['service_name'], "illust_id": x['illust_id'], "source": x['source'], "tags": str(tags)}

    def danbooru_clean_dict(self, illust, dict_list):
        """
        Cleans up the dictionary to only include needed information and returns them as a formatted dictionary
        """
        x = None
        for t in dict_list:
            if t['service_name'] == 'Danbooru':
                x = t
                break
        if x == None:
            return None

        tags = illust['tag_string_general']
        tags = tags.split() #TODO tags with ' in it
        return {"artist": illust['tag_string_artist'], "title": 'None', "caption": 'None', "create_date": illust['created_at'], "width": illust['image_width'], "height": illust['image_height'], "service": x['service_name'], "illust_id": x['illust_id'], "source": x['source'], "tags": str(tags)}

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
            self.original_image = Image.open(self.path_original)
        except Exception as e:
                print("ERROR [0039] " + str(e))
                #mb.showerror("ERROR [0039]", "ERROR CODE [0039]\nSomething went wrong while loading an image.")
                gv.Files.Log.write_to_log("ERROR [0039] " + str(e))
                return False

        for elem in self.pixiv_list:
            elem.load()

        for elem in self.danb_list:
            if elem.load() == False:
                pass # TODO
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
        self.original_image_thumb = deepcopy(self.original_image)
        self.original_image_thumb.thumbnail(self.thumb_size, resample=Image.ANTIALIAS)
        self.original_photoImage_thumb = ImageTk.PhotoImage(self.original_image_thumb)
        self.original_image_thumb.close()

        for elem in self.pixiv_list:
            elem.process_results_imgs()
    
        for elem in self.danb_list:
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
        self.original_wxh_lbl.configure(text = str(self.original_image.size))
        self.original_type_lbl.configure(text = self.name_original[self.name_original.rfind('.')+1:])
        self.original_cropped_lbl.configure(text = self.name_original)

        for elem in self.pixiv_list:
            elem.modify_results_widgets()

        for elem in self.danb_list:
            elem.modify_results_widgets()

        gv.res_frame.columnconfigure(0, weight=1)
        gv.res_frame.columnconfigure(1, weight=1)
        gv.res_frame.columnconfigure(2, weight=1)
        gv.res_frame.columnconfigure(3, weight=1)
        gv.res_frame.columnconfigure(4, weight=1)
        gv.res_frame.columnconfigure(5, weight=2)
        #self.modify_big_widgets_init = False
        self.modify_results_widgets_init = True

    def display_view_results(self):
        self.forget_all_widgets()
        gv.display_startpage()

    def display_results(self, t):
        """
        Displays all widgets corresponding to this image on the results frame\n
        IMPORTANT:\n
        Call load, process_results_imgs and modify_results_widgets in that order before
        """
        #self.index = int(t/4)
        self.original_chkbtn.grid(column = 0, row = t+1, sticky = W)
        self.original_lbl.grid(column = 2, row = t+1, sticky = W, padx = 10)
        self.original_wxh_lbl.grid(column = 3, row = t+1, sticky = W, padx = 10)
        self.original_type_lbl.grid(column = 4, row = t+1, sticky = W, padx = 10)
        self.info_btn.grid(column = 6, row = t+1, sticky = W, padx = 10)
        self.original_cropped_lbl.grid(column = 1, row = t, columnspan=6, sticky = W, padx = 10)
        self.big_selector_btn.grid(column = 5, row = t+1, sticky = W, padx = 10)

        t += 1
        for elem in self.pixiv_list:
            t = elem.display_results(t+1)
        for elem in self.danb_list:
            t = elem.display_results(t+1)

        return t

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
        
        gv.Files.Log.log_text.place_forget()
        gv.info_ScrollFrame.display(x = (gv.width/3)*1.85, y = 100)

        t = 0
        for elem in self.pixiv_list:
            elem.display_info(t)#TODO t = elem...
            t += 26
        for elem in self.danb_list:
            elem.display_info(t) #TODO t = elem...

    def display_big_selector(self):
        """
        Displays all widgets corresponding to this image on the big selector page\n
        IMPORTANT:\n
        Call load before
        """
        self.process_big_imgs()
        self.modify_big_widgets()
        self.forget_all_widgets()
        gv.big_selector_frame.place(x = round(gv.width*0.86), y = int(gv.height/90*9))
        gv.big_selector_canvas.yview_moveto(0)
        self.back_btn.place(x = round(gv.width*0.86), y = int(gv.height/90*4))
        self.prev_btn.place(x = round(gv.width*0.90), y = int(gv.height/90*4))
        self.next_btn.place(x = round(gv.width*0.94), y = int(gv.height/90*4))

        t = 0
        for elem in self.pixiv_list:
            t = elem.display_big_selector(t)
        for elem in self.danb_list:
            elem.display_big_selector(t) #TODO t = elem...

        self.original_SubImgData.display_place()

    def process_big_imgs(self):
        """
        Turns images into usable photoimages for tkinter\n
        IMPORTANT:\n
        Call load before
        """
        if self.process_big_imgs_init:
            return

        self.original_SubImgData = SubImageData(self.name_original, self.path_original, 'Input', gv.window, None, self.original_image, self.original_var)#ImageTk.PhotoImage(resize(self.original_image))
        self.original_SubImgData.load()

        for elem in self.pixiv_list:
            elem.process_big_imgs()


        for elem in self.danb_list:
            elem.process_big_imgs()

        self.process_big_imgs_init = True

    def modify_big_widgets(self):
        """
        Sets up next and previous buttons for the big selector screen\n
        """
        flag_next = False
        flag_prev = False
        for data in gv.img_data_array:
            if data.index-1 == self.index:
                self.next_btn.configure(state='enabled', command = data.display_big_selector)
                flag_next = True
            if data.index+1 == self.index:
                self.prev_btn.configure(state='enabled', command = data.display_big_selector)
                flag_prev = True
        if not flag_next:
            self.next_btn.configure(state='disabled', command=None)
        if not flag_prev:
            self.prev_btn.configure(state='disabled', command=None)
       
    def delete_both(self):
        """
        Returns True if user wants to delete both images (input and downloaded) or if at least one image is checked to save, otherwise False
        """
        if self.original_var.get() == 0 and self.pixiv.delete_both() and self.danb.delete_both():#TODO pixiv_list, danb_list
            return mb.askyesno('Delete both?', 'Do you really want to delete both images:\n' + self.name_original + '\n')#self.name_pixiv
        return True

    def save(self):
        """
        "Saves" own checked images and schedules the unchecked images to be deleted 
        """

        save_counter = 0
        for elem in self.pixiv_list:
            if save_counter > 2:
                break
            if elem.get_save_status():
                save_counter += 1
        for elem in self.danb_list:
            if save_counter > 2:
                break
            if elem.get_save_status():
                save_counter += 1
        if self.original_var.get() == 1:
            save_counter += 1

        if save_counter > 2:
            new_dir = gv.output_dir + '/' + self.name_original
            makedirs(new_dir, 0o777, True)
            t = 0
            if self.original_var.get() == 1:
                self.gen_tagfile()
                try:
                    move(self.path_original, gv.output_dir + '/' + self.name_original + '/' + self.name_original[:self.name_original.rfind('.')] + '_' + str(t) + self.name_original[self.name_original.rfind('.')+1:])
                except Exception as e:
                    print("ERROR [0013] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0013] " + str(e))
                    #mb.showerror("ERROR [0013]", "ERROR CODE [0013]\nSomething went wrong while moving the image " + self.path_original)
                t += 1
                
                pass
            else:
                if self.path_original not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.path_original)
            for elem in self.pixiv_list:
                elem.save(t, new_dir)
                t += 1
            for elem in self.danb_list:
                elem.save(t, new_dir)
                t += 1
            # make folder and save images in it with different names TODO try except
        else: #TODO delete_both here
            t = -1
            if self.original_var.get() == 1:
                self.gen_tagfile()
                try:
                    move(self.path_original, gv.output_dir + '/' + self.name_original)
                except Exception as e:
                    print("ERROR [0048] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0048] " + str(e))
                    #mb.showerror("ERROR [0048]", "ERROR CODE [0048]\nSomething went wrong while moving the image " + self.path_original)
            else:
                if self.path_original not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.path_original)
            for elem in self.pixiv_list:
                elem.save(t)
            for elem in self.danb_list:
                elem.save(t)
            # save the one stuff
        # TODO

        for widget in gv.info_frame.winfo_children():
            widget.grid_forget()

        if gv.Files.Conf.delete_input == '1':
            try:
                remove(gv.input_dir + self.name_original)
            except Exception as e:
                print("ERROR [0014] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0014] " + str(e))
                #mb.showerror("ERROR [0014]", "ERROR CODE [0014]\nSomething went wrong while removing the image " + gv.input_dir + self.name_original)
        
    def gen_tagfile(self):
        if gv.Files.Conf.gen_tagfile_original == '1':
            gen_tagfile(None, gv.output_dir, self.name_original)
        pass

    def forget_results(self):
        self.original_chkbtn.grid_forget()
        self.original_lbl.grid_forget()
        self.original_wxh_lbl.grid_forget()
        self.original_type_lbl.grid_forget()
        self.info_btn.grid_forget()
        self.original_cropped_lbl.grid_forget()
        self.big_selector_btn.grid_forget()

        for elem in self.pixiv_list:
            elem.forget_results()
        for elem in self.danb_list:
            elem.forget_results()

    def self_destruct(self):
        if self.original_SubImgData != None:
            self.original_SubImgData.self_destruct()
        if self.original_image != None:
            self.original_image.close()
        del self.original_photoImage_thumb

        self.original_chkbtn.image = None

        for elem in self.pixiv_list:
            elem.self_destruct()
        for elem in self.danb_list:
            elem.self_destruct()

class ProviderImageData():
    """Includes all information on the sourced images for the given image provider"""
    def __init__(self, service, name, path, thumb_size, preview_size, dictionary, siblings_array):
        self.service = service
        self.name = name
        self.path = path
        self.thumb_size = thumb_size
        self.preview_size = preview_size
        self.dict = dictionary
        self.tags = dictionary['tags'].strip('[]\'').split('\', \'')
        self.siblings_array = siblings_array
        self.downloaded_image = None
        self.downloaded_image_thumb = None
        self.downloaded_photoImage_thumb = None
        self.downloaded_photoImage_preview = None
        self.downloaded_image_preview = None
        self.sub_dir_array = list()
        self.sub_dir_img_array = list()
        self.downloaded_var = IntVar(value=0)
        self.downloaded_chkbtn = Checkbutton(master = gv.res_frame, var=self.downloaded_var, style="chkbtn.TCheckbutton")
        self.downloaded_lbl = Label(master=gv.res_frame, text = service, style='label.TLabel')
        try:
            self.downloaded_wxh_lbl = Label(master=gv.res_frame, text = str(len(listdir(self.path))) + " images", style='label.TLabel')
        except:
            self.downloaded_wxh_lbl = Label(master=gv.res_frame, text = "More images", style='label.TLabel')
        self.downloaded_type_lbl = Label(master=gv.res_frame, style='label.TLabel')
        self.results_tags_lbl = Label(gv.res_frame, style='label.TLabel')

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

        if self.service == 'Pixiv':
            self.tags_lbl_array.append((Label(master=gv.info_frame, text = 'Original:', style='label.TLabel', font = ('Arial Bold', 11)), Label(master=gv.info_frame, text = 'Translated:', style='label.TLabel', font = ('Arial Bold', 11))))
            for tag in self.tags:
                self.tags_lbl_array.append((Label(master=gv.info_frame, text = tag[:tag.find(' | ')], style='label.TLabel'), Label(master=gv.info_frame, text = tag[tag.find(' | ')+2:], style='label.TLabel')))
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
            return

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
            self.downloaded_var.set(1)
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

    def save(self, t, new_dir=None):
        if t == -1:
            if self.downloaded_var.get() == 1:
                self.gen_tagfile(gv.output_dir)
                move(self.path, gv.output_dir + '/' + self.name)
            else:
                if gv.output_dir + '/' + self.name not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.gv.output_dir + '/' + self.name)
                for elem in self.sub_dir_img_array:
                    elem.save()
            pass# save your inmage in the outputdir+name
        else:
            if self.downloaded_var.get() == 1:
                self.gen_tagfile(gv.output_dir + '/' + new_dir)
                move(self.path, gv.output_dir + '/' + new_dir + '/' + self.name[:self.name.rfind('.')] + '_' + str(t) + self.name[self.name.rfind('.')+1:])
            else:
                if gv.output_dir + '/' + self.name not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.gv.output_dir + '/' + self.name)
                for elem in self.sub_dir_img_array:
                    elem.save(t)
            pass# save your image in the outputdir+new_dir+name+t
        #TODO try except

    def gen_tagfile(self, gen_dir):
        if self.service == 'Pixiv' and gv.Files.Conf.gen_tagfile_pixiv == '1':
            if path.isfile(self.path):
                gen_tagfile(None, gen_dir, self.name)
            elif path.isdir(self.path):
                for elem in self.sub_dir_img_array:
                    elem.gen_tagfile(gen_dir + '/' + self.name)
        elif self.service == 'Danbooru' and gv.Files.Conf.gen_tagfile_danbooru == '1':
            if path.isfile(self.path):
                gen_tagfile(None, gen_dir, self.name)
            elif path.isdir(self.path):
                for elem in self.sub_dir_img_array:
                    elem.gen_tagfile(gen_dir + '/' + self.name)
        
        pass

    def forget_results(self):
        self.downloaded_chkbtn.grid_forget()
        self.downloaded_lbl.grid_forget()
        self.downloaded_wxh_lbl.grid_forget()
        self.downloaded_type_lbl.grid_forget()

    def self_destruct(self):
        if self.downloaded_SubImgData != None:
            self.downloaded_SubImgData.self_destruct()
        if self.downloaded_image != None:
            self.downloaded_image.close()
        for img in self.sub_dir_img_array:
            img.self_destruct()
        del self.downloaded_photoImage_thumb
        del self.downloaded_photoImage_preview

        self.downloaded_chkbtn.image = None

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

    def save(self, t = -1):
        if t == -1:
            makedirs(gv.output_dir + '/' + self.folder, 0o777, True)#TODO try except
            if self.var.get() == 1:
                self.gen_tagfile(gv.output_dir + '/' + self.folder)
                try:
                    move(self.path, gv.output_dir + '/' + self.folder + '/' + self.name)
                except Exception as e:
                    print("ERROR [0037] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0037] " + str(e))
                    #mb.showerror("ERROR [0037]", "ERROR CODE [0037]\nSomething went wrong while moving the image " + self.path_original)
            # save your images in outputdir+self.folder
        else:
            if self.var.get() == 1:
                self.gen_tagfile(gv.output_dir + '/' + self.folder)
                try:
                    move(self.path, gv.output_dir + '/' + self.folder + '/' + self.name[:self.name.rfind('.')] + '_' + str(t) + self.name[self.name.rfind('.')+1:])
                except Exception as e:
                    print("ERROR [0049] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0049] " + str(e))
                    #mb.showerror("ERROR [0049]", "ERROR CODE [0049]\nSomething went wrong while moving the image " + self.path_original)
            # save your images in outputdir+self.folder+t
        
    def gen_tagfile(self, gen_dir):
        if self.service == 'Pixiv' and gv.Files.Conf.gen_tagfile_pixiv == '1':
            gen_tagfile(None, gen_dir, self.name)
        elif self.service == 'Danbooru' and gv.Files.Conf.gen_tagfile_danbooru == '1':
            gen_tagfile(None, gen_dir, self.name)
        pass

    def self_destruct(self):
        del self.photoImg
        del self.photoImg_thumb
        if self.chkbtn != None:
            self.chkbtn.image = None
        if self.thumb_chkbtn != None:
            self.thumb_chkbtn.image = None

def resize(image):
    """
    Resizes given image to a third of the screen width and to the screen height*0.87 and returns it as a new object.
    """

    oldwidth = image.width
    oldheight = image.height

    new_image = deepcopy(image)

    if oldwidth > gv.width/3:
        newwidth = int(gv.width*0.4)
        newheight = int(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        new_image = image.resize(newsize, Image.ANTIALIAS)
    if new_image.height > gv.height*0.87:
        newheight = int(gv.height*0.87)
        newwidth = int(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        new_image = new_image.resize(newsize, Image.ANTIALIAS)
    return new_image