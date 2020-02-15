from os import listdir, path
from PIL import ImageTk, Image
from tkinter import IntVar, W
from tkinter import messagebox as mb
from tkinter.ttk import Label, Checkbutton, Button
from functools import partial
import global_variables as gv

# 5.2 Resize images to fit on screen
def resize(image):
    """
    Resizes given image to a third of the screen width and to the screen height-320 and returns it.
    """

    oldwidth = image.width
    oldheight = image.height

    if oldwidth > gv.width/3:
        newwidth = round(gv.width*0.4)
        newheight = round(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    if image.height > gv.height-120:
        newheight = gv.height - 120
        newwidth = round(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    return image

def display_big_selector2(index, window, frame2, display_view_results):
    """
    Draws all widgets for given image:
    - Name of image
    - Image (with checkbutton)
    - Image data
    - Downloaded images in scrollable canvas (with checkbutton)
    - Downloaded image data
    - Back button to results
    """
    forget = frame2.winfo_children()
    for widget in range(len(forget)):
        forget[0].grid_forget()
        del forget[0]

    for x in range(len(gv.big_ref_array)):
        del gv.big_ref_array[0]

    back_btn = Button(window, text = 'Back', command = display_view_results, style = 'button.TLabel')
    back_btn.place(x = round(gv.width*0.43), y = 100)

    try:
        original_image = Image.open(gv.cwd + '/Sourcery/sourced_original/' + gv.pixiv_images_array[index][2] + '.' + gv.pixiv_images_array[index][3])
    except Exception as e:
        print("ERROR [0001] " + str(e))
        mb.showerror("ERROR [0001]", "ERROR CODE [0001]\nSomething went wrong while loading an image, please go back and try again.")
        gv.Files.Log.write_to_log("ERROR [0001] " + str(e))
        return

    original_size = original_image.size
    original_image = resize(original_image)
    original_photoImage = ImageTk.PhotoImage(original_image)
    original_image.close()

    original_chkbtn = Checkbutton(window, image=original_photoImage, var=gv.chkbtn_vars_array[index][0], style="chkbtn.TCheckbutton")
    original_chkbtn.image = original_photoImage
    original_chkbtn.place(x = 15, y = 20)

    cropped_name_lbl = Label(window, text = gv.pixiv_images_array[index][2], style='label.TLabel')
    original_lbl = Label(window, text = 'original', style='label.TLabel')
    original_wxh_lbl = Label(window, text = original_size, style='label.TLabel')
    original_type_lbl = Label(window, text = gv.pixiv_images_array[index][3], style='label.TLabel')
    #cropped_name_lbl.place(x = round(gv.width*0.43), y = 15)
    original_lbl.place(x = round(gv.width*0.43), y = 35)
    original_wxh_lbl.place(x = round(gv.width*0.43), y = 55)
    original_type_lbl.place(x = round(gv.width*0.43), y = 75)

    gv.big_ref_array.extend([original_photoImage, original_image, original_chkbtn, cropped_name_lbl, original_wxh_lbl, original_type_lbl, back_btn])

    skip = False
    
    for target_list in gv.chkbtn_vars_big_array:
        if target_list[0] == gv.pixiv_images_array[index][2]:
            skip = True
            btn_index = gv.chkbtn_vars_big_array.index(target_list)
            break
    if not skip:
        gv.chkbtn_vars_big_array.append([gv.pixiv_images_array[index][2]]) #Append original img name w/o suffix
        btn_index = len(gv.chkbtn_vars_big_array)-1
    if gv.pixiv_images_array[index][9-4]: # if image has a corresponding folder
        t = 0
        
        for img in gv.pixiv_images_array[index][10-4]:
            if not skip:
                gv.chkbtn_vars_big_array[btn_index].append((img, IntVar())) # Append tuple with sub img name with suffix and corresponding IntVar
            try:
                downloaded_image = Image.open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + gv.pixiv_images_array[index][0] + '/' + img)
            except Exception as e:
                print("ERROR [0002] " + str(e))
                mb.showerror("ERROR [0002]", "ERROR CODE [0002]\nSomething went wrong while loading an image, please go back and try again.")
                gv.Files.Log.write_to_log("ERROR [0002] " + str(e))
                return
            
            downloaded_size = downloaded_image.size
            downloaded_image = resize(downloaded_image)
            downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)
            downloaded_image.close()

            downloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=gv.chkbtn_vars_big_array[btn_index][int(t/4)+1][1], style="chkbtn.TCheckbutton")
            downloaded_chkbtn.image = downloaded_photoImage
            downloaded_chkbtn.grid(column = 1, row = t, rowspan = 4)
            downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
            downloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
            downloaded_type_lbl = Label(frame2, text = img[img.rfind(".")+1:], style='label.TLabel')
            downloaded_lbl.grid(column = 0, row = t + 0, sticky = W)
            downloaded_wxh_lbl.grid(column = 0, row = t + 1, sticky = W)
            downloaded_type_lbl.grid(column = 0, row = t + 2, sticky = W)

            frame2.grid_rowconfigure(t + 3, weight = 1)

            gv.big_ref_array.extend([downloaded_photoImage, downloaded_image, downloaded_chkbtn])
            t += 4
    else:
        try:
            downloaded_image = Image.open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + gv.pixiv_images_array[index][0])
        except Exception as e:
            print("ERROR [0003] " + str(e))
            mb.showerror("ERROR [0003]", "ERROR CODE [0003]\nSomething went wrong while loading an image, please go back and try again.")
            gv.Files.Log.write_to_log("ERROR [0003] " + str(e))
            return
        downloaded_size = downloaded_image.size
        downloaded_image = resize(downloaded_image)
        downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)
        downloaded_image.close()
        

        downloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=gv.chkbtn_vars_array[index][1], style="chkbtn.TCheckbutton")
        downloaded_chkbtn.image = downloaded_photoImage
        downloaded_chkbtn.grid(column = 1, row = 0, rowspan = 4)
        downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
        downloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
        downloaded_type_lbl = Label(frame2, text = gv.pixiv_images_array[index][0][gv.pixiv_images_array[index][0].rfind(".")+1:], style='label.TLabel')
        downloaded_lbl.grid(column = 0, row = 0)
        downloaded_wxh_lbl.grid(column = 0, row = 1)
        downloaded_type_lbl.grid(column = 0, row = 2)

        gv.big_ref_array.extend([downloaded_photoImage, downloaded_image, downloaded_chkbtn])

def display_view_results2():
    t = 0
    #print("display")
    #print(gv.img_data_array)
    while t < 12*3:
        if t/3 > len(gv.img_data_array)-1:
            break
        gv.img_data_array[int(t/3)].load()
        gv.img_data_array[int(t/3)].process_results_imgs()
        gv.img_data_array[int(t/3)].modify_widgets()
        gv.img_data_array[int(t/3)].display_results(t)
        t += 3

def display_view_results3(frame, display_big_selector):
    """
    Draws all widgets for first dozen in pixiv images:
    - Name of image
    - Image (with checkbutton)
    - Image data
    - Downloaded images (with checkbutton)
    - Downloaded image data
    - All in scrollable canvas
    - Back button to startpage
    - Back and save button to startpage
    - Refresh and save button
    """
    
    # for b in range(len(gv.pixiv_images_array)):
    #     for a in range(len(gv.pixiv_images_array[0])):
    #         del gv.pixiv_images_array[0][0]
    #     del gv.pixiv_images_array[0]

    try:
        pixiv_dir_array = listdir(gv.cwd + '/Sourcery/sourced_progress/pixiv')
        sourced_original_array = listdir(gv.cwd + '/Sourcery/sourced_original')
    except Exception as e:
        print("ERROR [0004] " + str(e))
        mb.showerror("ERROR [0004]", "ERROR CODE [0004]\nSomething went wrong while accessing a folder, please go back and try again.")
        gv.Files.Log.write_to_log("ERROR [0004] " + str(e))
        return        
    
    pixiv_sub_dir_array = []
    
    # TODO delete non images
    for t in range(len(sourced_original_array)):
        sourced_original_array[t] = sourced_original_array[t].rpartition('.')
    
    t = 0
    for img in pixiv_dir_array:
        pointdex = img.rfind(".")
        if pointdex == -1:
            cropped = img
        else:
            cropped = img[:pointdex] # deletes the suffix
        # If input is empty, delete every element
        if len(sourced_original_array) == 0:
            if gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img not in gv.delete_dirs_array:
                gv.delete_dirs_array.append(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                try:
                    gv.safe_to_show_array.remove(cropped)
                except:
                    pass
            continue
        
        if cropped not in gv.safe_to_show_array:
            continue

        # original_image, downloaded_image, suffix, sub, dir_flag, continue_flag = image_opener(img, cropped, t, sourced_original_array, pixiv_sub_dir_array)
        # if continue_flag:
        #     continue

        # original_size = original_image.size
        # original_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)
        # original_photoImage = ImageTk.PhotoImage(original_image)
        # original_image.close()

        # downloaded_size = downloaded_image.size
        # downloaded_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)
        # downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)
        # downloaded_image.close()

        # cropped_name_lbl = display_view_results_helper(frame, original_photoImage, downloaded_photoImage, t, img, cropped, suffix, original_size, downloaded_size, dir_flag, display_big_selector)

        # gv.pixiv_images_array.append([img, sub, cropped, suffix, cropped_name_lbl, dir_flag, pixiv_sub_dir_array]) # , original_image, original_photoImage, downloaded_image, downloaded_photoImage
        if t > 32:
            break
        t += 3

def image_opener(img, cropped, t, sourced_original_array, pixiv_sub_dir_array):
    dir_flag = False
    suffix = ''
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
        
def display_view_results_helper(frame, original_photoImage, downloaded_photoImage, t, img, cropped, suffix, original_size, downloaded_size, dir_flag, display_big_selector):
    rst = gv.results_12_tuple_widgets_array
    # [([original_chkbtn, original_lbl, original_wxh_lbl, original_type_lbl, cropped_name_lbl], 
    # [downloaded_chkbtn, downloaded_lbl, downloaded_wxh_lbl, downloaded_type_lbl, big_selector_btn]), ([], []), ...]
    # original_chkbtn:
    rst[int(t/3)][0][0].configure(image=original_photoImage, var=gv.chkbtn_vars_array[int(t/3)][0])
    rst[int(t/3)][0][0].image = original_photoImage
    rst[int(t/3)][0][0].grid(column = 0, row = t+1)
    # original_lbl:
    rst[int(t/3)][0][1].grid(column = 2, row = t+1, sticky = W, padx = 10)
    # original_wxh_lbl:
    rst[int(t/3)][0][2].configure(text = str(original_size))
    rst[int(t/3)][0][2].grid(column = 3, row = t+1, sticky = W, padx = 10)
    # original_type_lbl:
    rst[int(t/3)][0][3].configure(text = suffix)
    rst[int(t/3)][0][3].grid(column = 4, row = t+1, sticky = W, padx = 10)
    # cropped_name_lbl:
    rst[int(t/3)][0][4].configure(text = cropped)
    rst[int(t/3)][0][4].grid(column = 1, row = t, columnspan=3, sticky = W, padx = 10)

    # downloaded_chkbtn:
    rst[int(t/3)][1][0].configure(image=downloaded_photoImage, var=gv.chkbtn_vars_array[int(t/3)][1])
    rst[int(t/3)][1][0].image = downloaded_photoImage
    rst[int(t/3)][1][0].grid(column = 0, row = t+2)
    # downloaded_lbl:
    rst[int(t/3)][1][1].grid(column = 2, row = t+2, sticky = W, padx = 10)
    # misc:
    if dir_flag:
        rst[int(t/3)][1][0].configure(state = 'disabled')
    else:
        rst[int(t/3)][1][2].configure(text = str(downloaded_size))# downloaded_wxh_lbl
        rst[int(t/3)][1][3].configure(text = img[img.rfind(".")+1:])# downloaded_type_lbl
        rst[int(t/3)][1][0].configure(state = 'enabled')
    # downloaded_wxh_lbl:
    rst[int(t/3)][1][2].grid(column = 3, row = t+2, sticky = W, padx = 10)
    # downloaded_type_lbl:
    rst[int(t/3)][1][3].grid(column = 4, row = t+2, sticky = W, padx = 10)
    # big_selector_btn:
    big_selector_partial = partial(display_big_selector, int(t/3))
    rst[int(t/3)][1][4].configure(command=big_selector_partial)
    rst[int(t/3)][1][4].grid(column = 5, row = t+2, sticky = W, padx = 10)

    return rst[int(t/3)][0][4]