from pathlib import Path
from pixivapi import Client, Size
from tkinter import messagebox as mb
#import os

client = Client()

#username = user_xhcz2358
#password = GoaldIsland
#refreshtoken = 'R8nav4UBcoRwYueYvfKFJgyoWhJDeYVr9hnBgmjSVm0'

def pixiv_login(username, password, credentials_array):
    try:
        client.login(username, password)
        credentials_array[3] = client.refresh_token
    except Exception as e:
        print(e)
        mb.showerror("ERROR", 'Login failed')

def pixiv_authenticate(username, password, credentials_array):
    try:
        client.authenticate(credentials_array[3])
    except Exception as e:
        print('auth with refreshtoken failed')
        pixiv_login(username, password, credentials_array)

def pixiv_download(imgid, img_name_original):
    try:
        illustration = client.fetch_illustration(imgid) # 75523989
        newname = img_name_original[:img_name_original.rfind('.')]
        illustration.download(directory=Path.cwd() / 'Sourcery/sourced_progress/pixiv', size=Size.ORIGINAL, filename=newname)
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

#pixiv_authenticate(username, password, credentials_array)