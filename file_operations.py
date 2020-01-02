import os
from tkinter import messagebox as mb

def init_directories(cwd):
    try:
        os.makedirs(cwd + "/Input", 0o777, True)
        os.makedirs(cwd + "/Sourced", 0o777, True)
        os.makedirs(cwd + "/Sourcery/sourced_original", 0o777, True)
        os.makedirs(cwd + "/Sourcery/sourced_progress/pixiv", 0o777, True)
        os.makedirs(cwd + "/Sourcery/sourced_progress/danbooru", 0o777, True)
        os.makedirs(cwd + "/Sourcery/sourced_progress/gelbooru", 0o777, True)
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
button_foreground_active=blue
button_background_pressed=#111
button_foreground_pressed=red

Light Theme
background=#fff
foreground=#ddd
button_background=#444
button_background_active=white
button_foreground_active=blue
button_background_pressed=#111
button_foreground_pressed=red

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

if __name__ == '__main__':
    write_credentials(os.getcwd(), read_credentials(os.getcwd()))