from pathlib import Path
from pixivapi import Client, Size
from tkinter import messagebox as mb
import os

# def pixiv_init():
#     global client
#     global refreshtoken
client = Client()
refreshtoken = 'R8nav4UBcoRwYueYvfKFJgyoWhJDeYVr9hnBgmjSVm0'

def pixiv_login():
    global refreshtoken
    try:
        client.login('user_xhcz2358', 'GoaldIsland')
        refreshtoken = client.refresh_token
    except Exception as e:
        print(e)
        mb.showerror("ERROR", 'Login failed')

def pixiv_authenticate():
    global refreshtoken
    try:
        client.authenticate(refreshtoken)
    except Exception as e:
        print('auth failed')
        pixiv_login()

def pixiv_download(imgid):
    try:
        illustration = client.fetch_illustration(imgid) # 75523989
        illustration.download(directory=Path.cwd() / 'Sourcery/sourced_progress/pixiv', size=Size.ORIGINAL)
    except Exception as e:
        print(e)
        mb.showerror("ERROR", e)

pixiv_authenticate()