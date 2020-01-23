from os import makedirs, remove, path, startfile, getcwd
from shutil import move, rmtree
from tkinter import messagebox as mb

cwd = getcwd()

def init_directories():
    global cwd
    try:
        makedirs(cwd + "/Input", 0o777, True)
        makedirs(cwd + "/Sourced", 0o777, True)
        makedirs(cwd + "/Sourcery/sourced_original", 0o777, True)
        makedirs(cwd + "/Sourcery/sourced_progress/pixiv", 0o777, True)
        # makedirs(cwd + "/Sourcery/sourced_progress/danbooru", 0o777, True)
        # makedirs(cwd + "/Sourcery/sourced_progress/gelbooru", 0o777, True)
    except Exception as e:
        print(e)
        mb.showerror("Something went wrong while creating directories, please restart Sourcery [0007]")
        return

def init_configs():
    global cwd
    if not path.exists(cwd + '/Sourcery/theme'):
        write_theme('Dark Theme', ['blue', 'red', '#12345', 'orange', 'grey', 'purple', 'magenta'])
    if not path.exists(cwd + '/Sourcery/credentials'):
        write_credentials(['', '', '', ''])

def read_theme():
    """
    Returns a list with colour values as strings for the currently chosen style and a list with colour values for the custom style.\n
    Order:\n
    [0]background, [1]foreground, [2]button_background, [3]button_background_active, 
    [4]button_foreground_active, [5]button_background_pressed, [6]button_foreground_pressed
    """
    global cwd
    try:
        f = open(cwd + '/Sourcery/theme')
    except Exception as e:
        print(e)
        mb.showerror("Something went wrong while accessing a configuration file(theme), please restart Sourcery [0008]")
        f.close()
        return
    theme = f.readline()
    theme = theme[theme.find('=')+1:]
    ct = False
    if theme == 'Custom Theme\n':
        ct = True
    assign = f.readline()
    while theme != assign:
        assign = f.readline()
    
    colour_array = []
    custom_array = []
    while assign != '\n':
        assign = f.readline()
        colour_array.append(assign[assign.find('=')+1:-1])
        if ct:
            custom_array.append(assign[assign.find('=')+1:-1])
    if not ct:
        while assign != 'Custom Theme\n':
            assign = f.readline()
        while assign != '\n':
            assign = f.readline()
            custom_array.append(assign[assign.find('=')+1:-1])
    f.close()
    return colour_array, custom_array

def write_theme(chosen_theme, custom_theme):
    global cwd
    theme = """Current theme=""" + chosen_theme + """

Dark Theme
background=#252525
foreground=#ddd
button_background=#444
button_background_active=white
button_foreground_active=black
button_background_pressed=#111
button_foreground_pressed=white

Light Theme
background=#eee
foreground=black
button_background=#aaa
button_background_active=black
button_foreground_active=white
button_background_pressed=#ddd
button_foreground_pressed=black

Custom Theme
background=""" + custom_theme[0] + """
foreground=""" + custom_theme[1] + """
button_background=""" + custom_theme[2]+  """
button_background_active=""" + custom_theme[3] + """
button_foreground_active=""" + custom_theme[4] + """
button_background_pressed=""" + custom_theme[5] + """
button_foreground_pressed=""" + custom_theme[6] + """

END"""

    try:
        f = open(cwd + '/Sourcery/theme', 'w')
        f.write(theme)
    except Exception as e:
        print(e)
        mb.showerror("Something went wrong while accessing a configuration file(theme), please try again [0009]")
        f.close()
        return
    
    f.close()

def is_image(img):
    """
    Returns True if the given images ends with one of the following image suffixes:\n
    .png, .jpg, .jpeg, .jfif, .gif, .bmp\n
    otherwise False
    """
    if img.endswith(".png"):
        return True
    if img.endswith(".jpg"):
        return True
    if img.endswith(".jpeg"):
        return True
    if img.endswith(".jfif"):
        return True
    if img.endswith(".gif"):
        return True
    if img.endswith(".bmp"):
        return True
    return False

def read_credentials():
    """
    Returns a list with saved credentials.\n
    Order:\n
    [0]SauceNao API-Key, [1]Pixiv Username, [2]Pixiv Password, [3]Pixiv refreshtoken
    """
    global cwd
    try:
        f = open(cwd + '/Sourcery/credentials')
    except Exception as e:
        print(e)
        mb.showerror("Something went wrong while accessing a configuration file(credentials), please try again [0010]")
        return

    credentials_array = ['','','',''] 
    creds = f.readline()
    while creds != 'END':
        if creds == 'SauceNao\n':
            creds = f.readline()
            credentials_array[0] = creds[creds.find('=')+1:-1]
        if creds == 'Pixiv\n':
            creds = f.readline()
            credentials_array[1] = creds[creds.find('=')+1:-1]
            creds = f.readline()
            credentials_array[2] = creds[creds.find('=')+1:-1]
            creds = f.readline()
            credentials_array[3] = creds[creds.find('=')+1:-1]
        creds = f.readline()
    f.close()
    return credentials_array

def write_credentials(credentials_array):
    global cwd
    creds = """SauceNao
API-Key=""" + credentials_array[0] + """

Pixiv
Username=""" + credentials_array[1] + """
Password=""" + credentials_array[2] + """
refreshtoken=""" + credentials_array[3] + """

END"""

    try:
        f = open(cwd + '/Sourcery/credentials', 'w')
        f.write(creds)
    except Exception as e:
        print(e)
        mb.showerror("Something went wrong while accessing a configuration file(credentials), please try again [0011]")
        f.close()
        return
    f.close()

def save(chkbtn_vars_array, chkbtn_vars_big_array, pixiv_images_array, delete_dirs_array, safe_to_show_array, frame):
    global cwd
    downloaded_name_new = None
    original_name_new = None
    pixiv_dir = cwd + '/Sourcery/sourced_progress/pixiv/'

    for i in range(len(pixiv_images_array)):
        original_var = chkbtn_vars_array[i][0].get()
        downloaded_var = chkbtn_vars_array[i][1].get()
        if original_var == 1:
            if downloaded_var == 1:
                downloaded_name_new = 'new_' + pixiv_images_array[i][0]
                original_name_new = 'old_' + pixiv_images_array[i][0]
            else:
                # Move original image to Sourced and delete downloaded image/directory
                downloaded_name_new = None
                original_name_new = pixiv_images_array[i][0]
                delete_dirs_array.append(pixiv_dir + pixiv_images_array[i][0])
        elif downloaded_var == 1:
            # Move downloaded image to Sourced and delete original image
            downloaded_name_new = pixiv_images_array[i][0]
            original_name_new = None
            delete_dirs_array.append(pixiv_dir + pixiv_images_array[i][0])
        
        if downloaded_var == 1:
            index = -1
            for elem in chkbtn_vars_big_array:
                if pixiv_images_array[i][2] == elem[0]:
                    index = chkbtn_vars_big_array.index(elem)
                    downloaded_name_new = None
                    break
            if index != -1:
                for img in chkbtn_vars_big_array[index]:
                    if img[1].get() == 1:
                        try:
                            move(pixiv_dir + pixiv_images_array[i][0] + '/' + img[0], cwd + '/Sourced/' + pixiv_images_array[i][0] + '/' + img[0])
                            delete_dirs_array.append(pixiv_dir + pixiv_images_array[i][0])
                        except Exception as e:
                            print(e)
                            mb.showerror("Something went wrong while moving the image " + img[0] + " from the folder " + pixiv_dir + pixiv_images_array[i][0])

        if downloaded_name_new != None:
            try:
                move(pixiv_dir + pixiv_images_array[i][0], cwd + '/Sourced/' + downloaded_name_new)
            except Exception as e:
                print(e)
                mb.showerror("Something went wrong while moving the image " + pixiv_images_array[i][0] + " from the folder " + pixiv_dir + '[0012]')
        if original_name_new != None:
            try:
                move(pixiv_dir + pixiv_images_array[i][0], cwd + '/Sourced/' + original_name_new)
            except Exception as e:
                print(e)
                mb.showerror("Something went wrong while moving the image " + pixiv_images_array[i][0] + " from the folder " + pixiv_dir + '[0013]')
        try:
            remove(cwd + '/Input/' + pixiv_images_array[i][0])
        except Exception as e:
            print(e)
            mb.showerror("Something went wrong while removing the image " + pixiv_images_array[i][0] + " from the folder " + cwd + '/Input/' + '[0014]')

        safe_to_show_array.remove(pixiv_images_array[i][2])

    for a in range(len(pixiv_images_array)):
        for b in range(len(pixiv_images_array[a])):
            del pixiv_images_array[a][0]
    pixiv_images_array.clear()

    for element in delete_dirs_array:
        if path.isdir(element):
            rmtree(element)
        else:
            remove(element)
    delete_dirs_array.clear()
    	
    for widget in frame.winfo_children():
        widget.grid_forget()

# def save_deprecated(chkbtn_vars_array, chkbtn_vars_big_array, pixiv_images_array, delete_dirs_array, safe_to_show_array, frame):
#     global cwd
#     for element in delete_dirs_array:
#         if path.isdir(element):
#             rmtree(element)
#         else:
#             remove(element)
#     delete_dirs_array.clear()

#     do_not_delete_tree = False
#     for elem in chkbtn_vars_big_array:
#         for img in elem:
#             if img[1].get() == 1:
#                 try:
#                     move(cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0] + '/' + img[0], 
#                     cwd + '/Sourced/' + elem[0] + '/' + img[0])
#                 except Exception as e:
#                     print(e)
#                     mb.showerror("Something went wrong while saving the image " + img[0] + " from the folder " + cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0] + ". You have to recover the image and delete the folder manually.")
#                     do_not_delete_tree = True
#         try:
#             if do_not_delete_tree:
#                 rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0])
#                 do_not_delete_tree = False
#         except Exception as e:
#             print(e)
        
#     chkbtn_vars_big_array.clear()

#     for tup in chkbtn_vars_array:
#         original_var = tup[0].get()
#         downloaded_var = tup [1].get()

#         if len(pixiv_images_array) > 0:
#             if original_var == 1:
#                 if downloaded_var == 1:
#                     # if pixiv_images_array[0][5]:
#                     #     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2] + '/' + pixiv_images_array[0][1], 
#                     #         cwd + '/Sourced/new_' + pixiv_images_array[0][1])
#                     #     rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
#                     # else:

#                     # Move original and downloaded image from their respective folders to Sourced and rename them 
#                     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0], # war im else
#                             cwd + '/Sourced/new_' + pixiv_images_array[0][0])
#                     move(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3], 
#                         cwd + '/Sourced/old_' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
#                 else:
#                     # Move original image to Sourced and delete downloaded image/directory
#                     move(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3], 
#                         cwd + '/Sourced/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
#                     if pixiv_images_array[0][5]:
#                         rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
#                     else:
#                         remove(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0])
#             elif downloaded_var == 1:
#                     # if pixiv_images_array[0][5]:
#                     #     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2] + '/' + pixiv_images_array[0][1], 
#                     #         cwd + '/Sourced/' + pixiv_images_array[0][1])
#                     #     rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
#                     # else:

#                     # Move downloaded image to Sourced and delete original image
#                     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0], # war im else
#                             cwd + '/Sourced/' + pixiv_images_array[0][0])
#                     remove(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
#             # Delete image from input
#             remove(cwd + '/Input/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
#             safe_to_show_array.remove(pixiv_images_array[0][2])
            
#             for a in range(len(pixiv_images_array[0])):
#                 del pixiv_images_array[0][0]
#             #pixiv_images_array.pop(0)
#     for widget in frame.winfo_children():
#         widget.grid_forget()

def open_input():
    global cwd
    try:
        startfile(cwd + "/Input")
    except Exception as e:
        print(e)
        #mb.showerror("ERROR", e)

def open_sourced():
    global cwd
    try:
        startfile(cwd + "/Sourced")
    except Exception as e:
        print(e)
        #mb.showerror("ERROR", e)

def display_statistics():
    global cwd
    pass

if __name__ == '__main__':
    pass
    #write_credentials(getcwd(), read_credentials(getcwd()))
