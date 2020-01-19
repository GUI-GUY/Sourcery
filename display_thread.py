from os import listdir, path
from PIL import ImageTk, Image
from tkinter import IntVar
from tkinter import messagebox as mb
from tkinter.ttk import Label, Checkbutton, Button
from functools import partial
#from create_GUI import display_big_selector

width = 0
height = 0

# 5.2 Resize images to fit on screen
def resize(image):
    """
    Resizes given image to a third of the screen width and to the screen height-320 and returns it.
    """
    global width
    global height

    oldwidth = image.width
    oldheight = image.height

    if oldwidth > width/3:
        newwidth = round(width*0.4)
        newheight = round(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    if image.height > height-120:
        newheight = height - 120
        newwidth = round(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    return image

def display_big_selector2(index, cwd, window, frame2, pixiv_images_array, chkbtn_vars_array, display_view_results, chkbtn_vars_big_array, big_ref_array):
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

    for x in range(len(big_ref_array)):
        del big_ref_array[0]

    back_btn = Button(window, text = 'Back', command = display_view_results, style = 'button.TLabel')
    back_btn.place(x = round(width*0.43), y = 100)

    try:
        original_image = Image.open(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[index][2] + '.' + pixiv_images_array[index][3])
    except Exception as e:
        print(e)
        mb.showerror("Something went wrong while loading an image, please go back and try again [0001]")
        return

    original_size = original_image.size
    original_image = resize(original_image)
    original_photoImage = ImageTk.PhotoImage(original_image)
    original_image.close()

    original_chkbtn = Checkbutton(window, image=original_photoImage, var=chkbtn_vars_array[index][0], style="chkbtn.TCheckbutton")
    original_chkbtn.image = original_photoImage
    original_chkbtn.place(x = 15, y = 20)

    cropped_name_lbl = Label(window, text = pixiv_images_array[index][2], style='label.TLabel')
    original_lbl = Label(window, text = 'original', style='label.TLabel')
    original_wxh_lbl = Label(window, text = original_size, style='label.TLabel')
    original_type_lbl = Label(window, text = pixiv_images_array[index][3], style='label.TLabel')
    cropped_name_lbl.place(x = round(width*0.43), y = 15)
    original_lbl.place(x = round(width*0.43), y = 35)
    original_wxh_lbl.place(x = round(width*0.43), y = 55)
    original_type_lbl.place(x = round(width*0.43), y = 75)

    big_ref_array.extend([original_photoImage, original_image, original_chkbtn, cropped_name_lbl, original_wxh_lbl, original_type_lbl, back_btn])

    skip = False
    
    for target_list in chkbtn_vars_big_array:
        if target_list[0] == pixiv_images_array[index][2]:
            skip = True
            btn_index = chkbtn_vars_big_array.index(target_list)
            break
    if not skip:
        chkbtn_vars_big_array.append([pixiv_images_array[index][2]]) #Append original img name w/o suffix
        btn_index = len(chkbtn_vars_big_array)-1
    if pixiv_images_array[index][9-4]: # if image has a corresponding folder
        t = 0
        
        for img in pixiv_images_array[index][10-4]:
            if not skip:
                chkbtn_vars_big_array[btn_index].append((img, IntVar())) # Append tuple with sub img name with suffix and corresponding IntVar
            try:
                downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[index][0] + '/' + img)
            except Exception as e:
                print(e)
                mb.showerror("Something went wrong while loading an image, please go back and try again [0002]")
                return
            
            downloaded_size = downloaded_image.size
            downloaded_image = resize(downloaded_image)
            downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)
            downloaded_image.close()

            downloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=chkbtn_vars_big_array[btn_index][int(t/4)+1][1], style="chkbtn.TCheckbutton")
            downloaded_chkbtn.image = downloaded_photoImage
            downloaded_chkbtn.grid(column = 1, row = t, rowspan = 4)
            downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
            downloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
            downloaded_type_lbl = Label(frame2, text = img[img.rfind(".")+1:], style='label.TLabel')
            downloaded_lbl.grid(column = 0, row = t + 0)
            downloaded_wxh_lbl.grid(column = 0, row = t + 1)
            downloaded_type_lbl.grid(column = 0, row = t + 2)

            big_ref_array.extend([downloaded_photoImage, downloaded_image, downloaded_chkbtn])
            t += 4
    else:
        try:
            downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[index][0])
        except Exception as e:
            print(e)
            mb.showerror("Something went wrong while loading an image, please go back and try again [0003]")
            return
        downloaded_size = downloaded_image.size
        downloaded_image = resize(downloaded_image)
        downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)
        downloaded_image.close()
        

        downloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=chkbtn_vars_array[index][1], style="chkbtn.TCheckbutton")
        downloaded_chkbtn.image = downloaded_photoImage
        downloaded_chkbtn.grid(column = 1, row = 0, rowspan = 4)
        downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
        downloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
        downloaded_type_lbl = Label(frame2, text = pixiv_images_array[index][0][pixiv_images_array[index][0].rfind(".")+1:], style='label.TLabel')
        downloaded_lbl.grid(column = 0, row = 0)
        downloaded_wxh_lbl.grid(column = 0, row = 1)
        downloaded_type_lbl.grid(column = 0, row = 2)

        big_ref_array.extend([downloaded_photoImage, downloaded_image, downloaded_chkbtn])

def display_view_results2(cwd, delete_dirs_array, frame, chkbtn_vars_array, pixiv_images_array, width1, height1, display_big_selector, safe_to_show_array, results_12_tuple_widgets_array):
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
    global width
    global height
    width = width1
    height = height1
    
    for b in range(len(pixiv_images_array)):
        for a in range(len(pixiv_images_array[0])):
            del pixiv_images_array[0][0]
        del pixiv_images_array[0]

    thumb_size = (70,70)
    try:
        pixiv_dir_array = listdir(cwd + '/Sourcery/sourced_progress/pixiv')
        sourced_original_array = listdir(cwd + '/Sourcery/sourced_original')
    except Exception as e:
        print(e)
        mb.showerror("Something went wrong while accessing a folder, please go back and try again [0004]")
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
            if cwd + '/Sourcery/sourced_progress/pixiv/' + img not in delete_dirs_array:
                delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                safe_to_show_array.remove(cropped)
            continue
        
        if cropped not in safe_to_show_array:
            continue

        original_image, downloaded_image, suffix, sub, dir_flag, continue_flag = image_opener(cwd, img, cropped, t, sourced_original_array, delete_dirs_array, safe_to_show_array, pixiv_sub_dir_array, chkbtn_vars_array)
        if continue_flag:
            continue

        original_size = original_image.size
        original_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)
        original_photoImage = ImageTk.PhotoImage(original_image)
        original_image.close()

        downloaded_size = downloaded_image.size
        downloaded_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)
        downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)
        downloaded_image.close()

        cropped_name_lbl = display_view_results_helper(frame, original_photoImage, downloaded_photoImage, chkbtn_vars_array, t, img, cropped, suffix, original_size, downloaded_size, dir_flag, display_big_selector, results_12_tuple_widgets_array)

        pixiv_images_array.append([img, sub, cropped, suffix, cropped_name_lbl, dir_flag, pixiv_sub_dir_array]) # , original_image, original_photoImage, downloaded_image, downloaded_photoImage
        if t > 32:
            break
        t += 3

def image_opener(cwd, img, cropped, t, sourced_original_array, delete_dirs_array, safe_to_show_array, pixiv_sub_dir_array, chkbtn_vars_array):
    dir_flag = False
    suffix = ''
    sub = ''
    if path.isfile(cwd + '/Sourcery/sourced_progress/pixiv/' + img):
        for image in sourced_original_array:
            if image[0] == cropped:
                suffix = image[2]
                break
        if suffix == '':
            if cwd + '/Sourcery/sourced_progress/pixiv/' + img not in delete_dirs_array:
                delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                safe_to_show_array.remove(cropped)
            return None,None,None,None,None, True
        try:
            original_image = Image.open(cwd + '/Sourcery/sourced_original/' + cropped + '.' + suffix) 
            downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
        except Exception as e:
            print(e)
            mb.showerror("Something went wrong while loading an image, please go back and try again [0005]")
            return
    elif path.isdir(cwd + '/Sourcery/sourced_progress/pixiv/' + img):
        dir_flag = True
        try:
            pixiv_sub_dir_array.extend(listdir(cwd + '/Sourcery/sourced_progress/pixiv/' + img))
            if len(pixiv_sub_dir_array) == 0:
                if cwd + '/Sourcery/sourced_progress/pixiv/' + img not in delete_dirs_array:
                    delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                    safe_to_show_array.remove(cropped)
                return None,None,None,None,None, True
            pathname = ''
            for image in sourced_original_array:
                if image[0] == img:
                    pathname = cwd + '/Sourcery/sourced_original/' + image[0] + image[1] + image[2]
                    suffix = image[2]
                    break
            if suffix == '':
                if cwd + '/Sourcery/sourced_progress/pixiv/' + img not in delete_dirs_array:
                    delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                    safe_to_show_array.remove(cropped)
                return None,None,None,None,None, True
            chkbtn_vars_array[int(t/3)][0].set(1)
            chkbtn_vars_array[int(t/3)][1].set(0)
            sub = pixiv_sub_dir_array[0]
            original_image = Image.open(pathname)
            downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + img + '/' + pixiv_sub_dir_array[0])
        except Exception as e:
            print(e)
            mb.showerror("Something went wrong while loading an image, please go back and try again [0006]")
            return
    return original_image, downloaded_image, suffix, sub, dir_flag, False
        
def display_view_results_helper(frame, original_photoImage, downloaded_photoImage, chkbtn_vars_array, t, img, cropped, suffix, original_size, downloaded_size, dir_flag, display_big_selector, rst):
    # rst = results_12_tuple_widgets_array
    # [([original_chkbtn, original_lbl, original_wxh_lbl, original_type_lbl, cropped_name_lbl], 
    # [downloaded_chkbtn, downloaded_lbl, downloaded_wxh_lbl, downloaded_type_lbl, big_selector_btn]), ([], []), ...]
    # original_chkbtn:
    rst[int(t/3)][0][0].configure(image=original_photoImage, var=chkbtn_vars_array[int(t/3)][0])
    rst[int(t/3)][0][0].image = original_photoImage
    rst[int(t/3)][0][0].grid(column = 0, row = t+1)
    # original_lbl:
    rst[int(t/3)][0][1].grid(column = 2, row = t+1)
    # original_wxh_lbl:
    rst[int(t/3)][0][2].configure(text = str(original_size))
    rst[int(t/3)][0][2].grid(column = 3, row = t+1)
    # original_type_lbl:
    rst[int(t/3)][0][3].configure(text = suffix)
    rst[int(t/3)][0][3].grid(column = 4, row = t+1)
    # cropped_name_lbl:
    rst[int(t/3)][0][4].configure(text = cropped)
    rst[int(t/3)][0][4].grid(column = 1, row = t, columnspan=3)

    # downloaded_chkbtn:
    rst[int(t/3)][1][0].configure(image=downloaded_photoImage, var=chkbtn_vars_array[int(t/3)][1])
    rst[int(t/3)][1][0].image = downloaded_photoImage
    rst[int(t/3)][1][0].grid(column = 0, row = t+2)
    # downloaded_lbl:
    rst[int(t/3)][1][1].grid(column = 2, row = t+2)
    # misc:
    if dir_flag:
        rst[int(t/3)][1][0].configure(state = 'disabled')
    else:
        rst[int(t/3)][1][2].configure(text = str(downloaded_size))# downloaded_wxh_lbl
        rst[int(t/3)][1][3].configure(text = img[img.rfind(".")+1:])# downloaded_type_lbl
        rst[int(t/3)][1][0].configure(state = 'enabled')
    # downloaded_wxh_lbl:
    rst[int(t/3)][1][2].grid(column = 3, row = t+2)
    # downloaded_type_lbl:
    rst[int(t/3)][1][3].grid(column = 4, row = t+2)
    # big_selector_btn:
    big_selector_partial = partial(display_big_selector, int(t/3))
    rst[int(t/3)][1][4].configure(command=big_selector_partial)
    rst[int(t/3)][1][4].grid(column = 5, row = t+2)

    return rst[int(t/3)][0][4]