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
    global width
    global height

    oldwidth = image.width
    oldheight = image.height

    if oldwidth > width/3:
        newwidth = round(width/3)
        newheight = round(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    if image.height > height-320:
        newheight = height - 320
        newwidth = round(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        image = image.resize(newsize, Image.ANTIALIAS)
    return image

def display_big_selector2(index, cwd, window, frame2, pixiv_images_array, chkbtn_vars_array):

    original_image = Image.open(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[index][2] + '.' + pixiv_images_array[index][3])
    original_size = original_image.size
    original_image = resize(original_image)
    original_photoImage = ImageTk.PhotoImage(original_image)

    original_chkbtn = Checkbutton(window, image=original_photoImage, var=chkbtn_vars_array[index][0], style="chkbtn.TCheckbutton")
    original_chkbtn.image = original_photoImage
    original_chkbtn.place(x = 20, y = 73)

    cropped_name_lbl = Label(window, text = pixiv_images_array[index][2], style='label.TLabel')
    original_wxh_lbl = Label(window, text = original_size, style='label.TLabel')
    original_type_lbl = Label(window, text = pixiv_images_array[index][3], style='label.TLabel')
    cropped_name_lbl.place(x = 50, y = 50)
    original_wxh_lbl.place(x = 50, y = 500)
    original_type_lbl.place(x = 50, y = 523)

    if pixiv_images_array[index][9]:
        t = 0
        chkbtn_vars_big_array = []
        for img in pixiv_images_array[index][10]:
            chkbtn_vars_big_array.append(IntVar())
            downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[index][0] + '/' + img)
            downloaded_size = downloaded_image.size # TODO is this runtime or instant assigned in the label?
            downloaded_image = resize(downloaded_image)
            downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)

            dowloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=chkbtn_vars_big_array[int(t/4)], style="chkbtn.TCheckbutton")
            dowloaded_chkbtn.image = downloaded_photoImage
            dowloaded_chkbtn.grid(column = 0, row = t, rowspan = 4)
            downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
            dowloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
            downloaded_type_lbl = Label(frame2, text = img[img.rfind(".")+1:], style='label.TLabel')
            downloaded_lbl.grid(column = 1, row = t + 0)
            dowloaded_wxh_lbl.grid(column = 1, row = t + 1)
            downloaded_type_lbl.grid(column = 1, row = t + 2)
            t += 4
    else:
        downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[index][0])
        downloaded_size = downloaded_image.size
        downloaded_image = resize(downloaded_image)
        downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)

        dowloaded_chkbtn = Checkbutton(frame2, image=downloaded_photoImage, var=chkbtn_vars_array[index][1], style="chkbtn.TCheckbutton")
        dowloaded_chkbtn.image = downloaded_photoImage
        dowloaded_chkbtn.grid(column = 0, row = 0, rowspan = 4)
        downloaded_lbl = Label(frame2, text = "pixiv", style='label.TLabel')
        dowloaded_wxh_lbl = Label(frame2, text = downloaded_size, style='label.TLabel')
        downloaded_type_lbl = Label(frame2, text = pixiv_images_array[index][0][pixiv_images_array[index][0].rfind(".")+1:], style='label.TLabel')
        downloaded_lbl.grid(column = 1, row = 0)
        dowloaded_wxh_lbl.grid(column = 1, row = 1)
        downloaded_type_lbl.grid(column = 1, row = 2)


def display_view_results2(cwd, delete_dirs_array, frame, chkbtn_vars_array, pixiv_images_array, width1, height1, display_big_selector):
    global width
    global height
    width = width1
    height = height1
    thumb_size = (70,70)
    pixiv_dir_array = listdir(cwd + '/Sourcery/sourced_progress/pixiv')
    pixiv_sub_dir_array = []
    sourced_original_array = listdir(cwd + '/Sourcery/sourced_original')
    # TODO delete non images
    for t in range(len(sourced_original_array)):
        sourced_original_array[t] = sourced_original_array[t].rpartition('.')
    
    t = 0
    for img in pixiv_dir_array:
        # If input is empty, delete every element
        if len(sourced_original_array) == 0:
            delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
            continue
        flag = False # IsDirectory flag
        pointdex = img.rfind(".")
        if pointdex == -1:
            cropped = img
        else:
            cropped = img[:pointdex] # deletes the suffix
        suffix = ''
        sub = ''
        if path.isfile(cwd + '/Sourcery/sourced_progress/pixiv/' + img):
            for image in sourced_original_array:
                if image[0] == cropped:
                    suffix = image[2]
                    break
            if suffix == '':
                delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                continue
            try:
                original_image = Image.open(cwd + '/Sourcery/sourced_original/' + cropped + '.' + suffix) 
                downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)
        elif path.isdir(cwd + '/Sourcery/sourced_progress/pixiv/' + img):
            flag = True
            try:
                pixiv_sub_dir_array = listdir(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                if len(pixiv_sub_dir_array) == 0:
                    delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                    continue
                pathname = ''
                for image in sourced_original_array:
                    if image[0] == img:
                        pathname = cwd + '/Sourcery/sourced_original/' + image[0] + image[1] + image[2]
                        suffix = image[2]
                        break
                if suffix == '':
                    delete_dirs_array.append(cwd + '/Sourcery/sourced_progress/pixiv/' + img)
                    continue
                sub = pixiv_sub_dir_array[0]
                original_image = Image.open(pathname)
                downloaded_image = Image.open(cwd + '/Sourcery/sourced_progress/pixiv/' + img + '/' + pixiv_sub_dir_array[0])
            except Exception as e:
                print(e)
                mb.showerror("ERROR", e)

        original_size = original_image.size
        downloaded_size = downloaded_image.size

        original_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)
        downloaded_image.thumbnail(thumb_size, resample=Image.ANTIALIAS)

        original_photoImage = ImageTk.PhotoImage(original_image)
        downloaded_photoImage = ImageTk.PhotoImage(downloaded_image)

        original_chkbtn = Checkbutton(frame, image=original_photoImage, var=chkbtn_vars_array[int(t/3)][0], style="chkbtn.TCheckbutton")
        dowloaded_chkbtn = Checkbutton(frame, image=downloaded_photoImage, var=chkbtn_vars_array[int(t/3)][1], style="chkbtn.TCheckbutton")
        original_chkbtn.image = original_photoImage
        dowloaded_chkbtn.image = downloaded_photoImage
        original_chkbtn.grid(column = 0, row = t+1)
        dowloaded_chkbtn.grid(column = 0, row = t+2)
        cropped_name_lbl = Label(frame, text = cropped, style='label.TLabel')
        original_lbl = Label(frame, text = "original", style='label.TLabel')
        original_wxh_lbl = Label(frame, text = str(original_size), style='label.TLabel')
        original_type_lbl = Label(frame, text = suffix, style='label.TLabel')
        downloaded_lbl = Label(frame, text = "pixiv", style='label.TLabel')
        cropped_name_lbl.grid(column = 1, row = t, columnspan=3)
        original_lbl.grid(column = 2, row = t+1)
        original_wxh_lbl.grid(column = 3, row = t+1)
        original_type_lbl.grid(column = 4, row = t+1)
        downloaded_lbl.grid(column = 2, row = t+2)
        if flag:
            downloaded_wxh_lbl = Label(frame, text = "More images", style='label.TLabel')
            downloaded_type_lbl = Label(frame, text = "More images", style='label.TLabel')
        else:
            downloaded_wxh_lbl = Label(frame, text = str(downloaded_size), style='label.TLabel')
            downloaded_type_lbl = Label(frame, text = img[img.rfind(".")+1:], style='label.TLabel')
        downloaded_wxh_lbl.grid(column = 3, row = t+2)
        downloaded_type_lbl.grid(column = 4, row = t+2)
        big_selector_partial = partial(display_big_selector, int(t/3))
        big_selector_btn = Button(frame, text='View in Big Selector', command=big_selector_partial, style='button.TLabel')
        big_selector_btn.grid(column = 5, row = t+2)

        pixiv_images_array.append([img, sub, cropped, suffix, cropped_name_lbl, original_image, original_photoImage, downloaded_image, downloaded_photoImage, flag, pixiv_sub_dir_array])
        if t > 32:
            break
        t += 3