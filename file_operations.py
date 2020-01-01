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
    Returns a list with colour values as strings for the currently chosen style.\n
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
    assign = f.readline()
    while theme != assign:
        assign = f.readline()
    
    colour_array = []
    while assign != '\n':
        assign = f.readline()
        colour_array.append(assign[assign.find('=')+1:-1])
        
    return colour_array


def is_image(img):
    """Returns True if the given images ends with a common image suffix such as .png or .jpg\n
    otherwise False"""
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
    [0]SauceNao API-Key, [1]Pixiv Username, [2]Pixiv Password, [3]Pixiv refreshtoken, 
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
    
    return credentials_array