from os import makedirs, remove, path
from shutil import move, rmtree
from tkinter import messagebox as mb

def init_directories(cwd):
    try:
        makedirs(cwd + "/Input", 0o777, True)
        makedirs(cwd + "/Sourced", 0o777, True)
        makedirs(cwd + "/Sourcery/sourced_original", 0o777, True)
        makedirs(cwd + "/Sourcery/sourced_progress/pixiv", 0o777, True)
        makedirs(cwd + "/Sourcery/sourced_progress/danbooru", 0o777, True)
        makedirs(cwd + "/Sourcery/sourced_progress/gelbooru", 0o777, True)
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

def read_theme(cwd):
    """
    Returns a list with colour values as strings for the currently chosen style and a list with colour values for the custom style.\n
    Order:\n
    [0]background, [1]foreground, [2]button_background, [3]button_background_active, 
    [4]button_foreground_active, [5]button_background_pressed, [6]button_foreground_pressed
    """
    try:
        f = open(cwd + '/Sourcery/theme')
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)
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

def write_theme(cwd, chosen_theme, custom_theme):
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
        mb.showerror("ERROR", e)
    
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

def read_credentials(cwd):
    """
    Returns a list with saved credentials.\n
    Order:\n
    [0]SauceNao API-Key, [1]Pixiv Username, [2]Pixiv Password, [3]Pixiv refreshtoken
    """
    
    try:
        f = open(cwd + '/Sourcery/credentials')
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

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

def write_credentials(cwd, credentials_array):
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
        mb.showerror("ERROR", e)
    f.close()

def save(cwd, chkbtn_vars_array, chkbtn_vars_big_array, pixiv_images_array, delete_dirs_array, safe_to_show_array, frame):
    for element in delete_dirs_array:
        if path.isdir(element):
            rmtree(element)
        else:
            remove(element)
    delete_dirs_array.clear()

    for elem in chkbtn_vars_big_array:
        for img in elem:
            if img[1].get() == 1:
                move(cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0] + '/' + img[0], 
                    cwd + '/Sourced/' + elem[0] + '/' + img[0])
        rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0])
    chkbtn_vars_big_array.clear()

    for tup in chkbtn_vars_array:
        original_var = tup[0].get()
        downloaded_var = tup [1].get()

        if len(pixiv_images_array) > 0:
            if original_var == 1:
                if downloaded_var == 1:
                    # if pixiv_images_array[0][9]:
                    #     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2] + '/' + pixiv_images_array[0][1], 
                    #         cwd + '/Sourced/new_' + pixiv_images_array[0][1])
                    #     rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
                    # else:
                    move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0], # war im else
                            cwd + '/Sourced/new_' + pixiv_images_array[0][0])
                    move(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3], 
                        cwd + '/Sourced/old_' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
                else:
                    move(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3], 
                        cwd + '/Sourced/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
                    if pixiv_images_array[0][9-4]:
                        rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
                    else:
                        remove(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0])
            elif downloaded_var == 1:
                    # if pixiv_images_array[0][9]:
                    #     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2] + '/' + pixiv_images_array[0][1], 
                    #         cwd + '/Sourced/' + pixiv_images_array[0][1])
                    #     rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
                    # else:
                    move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0], # war im else
                            cwd + '/Sourced/' + pixiv_images_array[0][0])
                    remove(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
            remove(cwd + '/Input/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
            safe_to_show_array.remove(pixiv_images_array[0][2])
            for widget in frame.winfo_children():
                widget.grid_forget()
            for a in pixiv_images_array[0]:
                del a
            pixiv_images_array.pop(0)

if __name__ == '__main__':
    pass
    #write_credentials(getcwd(), read_credentials(getcwd()))