from os import path, listdir, remove, makedirs
from shutil import move, rmtree
from tkinter import IntVar, W, N
from tkinter import messagebox as mb
from tkinter.ttk import Checkbutton, Label, Button
from PIL import ImageTk, Image
from webbrowser import open_new
from copy import deepcopy
from file_operations import is_image, gen_tagfile
from ProviderImageData import ProviderImageData
from SubImageData import SubImageData
import global_variables as gv

class ImageData():
    """Includes all information on the sourced images"""
    def __init__(self, old_name, input_path, pixiv_rename, danb_rename, dict_list, pixiv_illust_list, danbooru_illust_list, index):
        self.name_original = old_name
        self.thumb_size = (70,70)
        self.preview_size = (200, 200)
        self.siblings_array = list()
        self.pixiv_list = list()
        # dict_list is list of {"service_name": service_name, "illust_id": illust_id, "source": source}
        for elem in pixiv_illust_list:
            #print('pixiv')
            #print(elem[1])
            name = self.correct_name('pixiv', elem[1]) # TODO if name == False
            #print(name)
            path_pixiv = gv.cwd + '/Sourcery/sourced_progress/pixiv/' + name
            self.pixiv_dict = self.pixiv_clean_dict(elem[0], dict_list) 
            self.pixiv_list.append(ProviderImageData('Pixiv', name, path_pixiv, self.thumb_size, self.preview_size, self.pixiv_dict, elem[0], self.siblings_array))
        
        self.danb_list = list()
        for elem in danbooru_illust_list:
            #print('dan')
            #print(elem[1])
            name = self.correct_name('danbooru', elem[1]) # TODO if name == False
            path_danb = gv.cwd + '/Sourcery/sourced_progress/danbooru/' + name
            self.danb_dict = self.danbooru_clean_dict(elem[0], dict_list)
            self.danb_list.append(ProviderImageData('Danbooru', name, path_danb, self.thumb_size, self.preview_size, self.danb_dict, elem[0], self.siblings_array))
        #self.name_pixiv = pixiv_name
        #self.set_name_pixiv()
        #self.name_danb = danb_name
        #self.set_name_danb()
        
        self.minsim = 80
        self.rename_pixiv = pixiv_rename
        self.rename_danbooru = danb_rename
        self.path_original = gv.cwd + '/Sourcery/sourced_original/' + self.name_original
        self.input_path = input_path
        
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
        return {"artist": illust.user.name, "title": illust.title, "caption": illust.caption, "create_date": illust.create_date, "width": illust.width, "height": illust.height, "service": x['service_name'], "illust_id": x['illust_id'], "source": x['source'], "similarity": float(x['similarity']), "tags": str(tags)}

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
        return {"artist": illust['tag_string_artist'], "title": 'None', "caption": 'None', "create_date": illust['created_at'], "width": illust['image_width'], "height": illust['image_height'], "service": x['service_name'], "illust_id": x['illust_id'], "source": x['source'], "similarity": float(x['similarity']), "tags": str(tags)}

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
            elem.load() # TODO error

        for elem in self.danb_list:
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
        flag = False
        if gv.Files.Conf.direct_replace_pixiv == '1':
            for elem in self.pixiv_list:
                if elem.is_greater_than_direct_sim():
                    flag = True
        if gv.Files.Conf.direct_replace_danbooru == '1':
            for elem in self.danb_list:
                if elem.is_greater_than_direct_sim():
                    flag = True

        if flag:
            if gv.Files.Conf.direct_replace_pixiv == '1':
                for elem in self.pixiv_list:
                    if elem.is_greater_than_direct_sim():
                        elem.downloaded_var.set(1)
                    else:
                        elem.downloaded_var.set(0)
            if gv.Files.Conf.direct_replace_danbooru == '1':
                for elem in self.danb_list:
                    if elem.is_greater_than_direct_sim():
                        elem.downloaded_var.set(1)
                    else:
                        elem.downloaded_var.set(0)
            return -1
        
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
        # TODO gv.Files.Conf.direct_replace
        pixiv_tags = list()
        for elem in self.pixiv_list:
            pixiv_tags.extend(elem.get_tags_list())

        danbooru_tags = list()
        for elem in self.danb_list:
            danbooru_tags.extend(elem.get_tags_list())

        #--Does the user want to save more than one image?--#
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
        ##----##
        

        #--If yes, make a head directory(new_dir, full path) with the original name and save all checked images in it--#
        if save_counter > 1:
            new_dir = gv.output_dir + '/' + self.name_original[:self.name_original.rfind('.')]
            makedirs(new_dir, 0o777, True)
            t = 0
            if self.original_var.get() == 1:
                new_img_name = self.name_original[:self.name_original.rfind('.')] + '_' + str(t) + self.name_original[self.name_original.rfind('.'):]
                self.gen_tagfile(pixiv_tags, danbooru_tags, new_dir, self.name_original[:self.name_original.rfind('.')] + '_' + str(t))
                try:
                    move(self.path_original, new_dir + '/' + new_img_name)
                except Exception as e:
                    print("ERROR [0013] " + str(e))
                    gv.Files.Log.write_to_log("ERROR [0013] " + str(e))
                    #mb.showerror("ERROR [0013]", "ERROR CODE [0013]\nSomething went wrong while moving the image " + self.path_original)
                t += 1
            else:
                if self.path_original not in gv.delete_dirs_array:
                    gv.delete_dirs_array.append(self.path_original)
            for elem in self.pixiv_list:
                elem.save(pixiv_tags, danbooru_tags, t, new_dir)
                t += 1
            for elem in self.danb_list:
                elem.save(pixiv_tags, danbooru_tags, t, new_dir)
                t += 1
            # make folder and save images in it with different names TODO try except
        ##----##

        #--If no, go through all saves, the only one that is checked will be in there--#
        else: #TODO delete_both here
            if self.original_var.get() == 1:
                self.gen_tagfile(pixiv_tags, danbooru_tags, gv.output_dir, self.name_original[:self.name_original.rfind('.')])
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
                elem.save(pixiv_tags, danbooru_tags)
            for elem in self.danb_list:
                elem.save(pixiv_tags, danbooru_tags)
        ##----##
        # TODO

        self.forget_results()

        for widget in gv.info_frame.winfo_children():
            widget.grid_forget()

        if gv.Files.Conf.delete_input == '1':
            try:
                remove(self.input_path)
            except Exception as e:
                print("ERROR [0014] " + str(e))
                gv.Files.Log.write_to_log("ERROR [0014] " + str(e))
                #mb.showerror("ERROR [0014]", "ERROR CODE [0014]\nSomething went wrong while removing the image " + gv.input_dir + self.name_original)
        
    def gen_tagfile(self, pixiv_tags, danbooru_tags, gen_dir, name):
        if gv.Files.Conf.gen_tagfile_original == '1':
            all_tags = list()
            if gv.Files.Conf.tagfile_pixiv_original == '1':
                all_tags.extend(pixiv_tags)
            if gv.Files.Conf.tagfile_danbooru_original == '1':
                all_tags.extend(danbooru_tags)
            
            gen_tagfile(all_tags, gen_dir, name)
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
        self.original_photoImage_thumb = None

        self.original_chkbtn.image = None

        for elem in self.pixiv_list:
            elem.self_destruct()
        for elem in self.danb_list:
            elem.self_destruct()
