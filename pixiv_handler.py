from pathlib import Path
from pixivapi import Client, Size
#from tkinter import messagebox as #mb
#import os

client = Client()

def pixiv_login(username, password, credentials_array):
    try:
        client.login(username, password)
        credentials_array[3] = client.refresh_token
    except Exception as e:
        print('ERROR [0021] Pixiv login failed' + str(e))
        #mb.showerror("ERROR", 'Login failed')
        return False
    return True


def pixiv_authenticate(username, password, credentials_array):
    try:
        client.authenticate(credentials_array[3])
    except Exception as e:
        print('ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        return pixiv_login(username, password, credentials_array)
    return True

def pixiv_download(imgid, img_name_original):
    try:
        illustration = client.fetch_illustration(imgid) # 75523989
        newname = img_name_original[:img_name_original.rfind('.')]
        illustration.download(directory=Path.cwd() / 'Sourcery/sourced_progress/pixiv', size=Size.ORIGINAL, filename=newname)
    except Exception as e:
        print('ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        #mb.showerror("ERROR", e)

#pixiv_authenticate(username, password, credentials_array)