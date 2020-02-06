from pathlib import Path
from pixivapi import Client, Size
from global_variables import credentials_array
from file_operations import write_credentials, write_to_log
#from tkinter import messagebox as #mb

client = Client()

def pixiv_login():
    try:
        client.login(credentials_array[1], credentials_array[2])
        credentials_array[3] = client.refresh_token
    except Exception as e:
        print('ERROR [0021] Pixiv login failed' + str(e))
        write_to_log('ERROR [0021] Pixiv login failed' + str(e))
        #mb.showerror("ERROR", 'Login failed')
        return False
    return True


def pixiv_authenticate():
    try:
        client.authenticate(credentials_array[3])
    except Exception as e:
        print('ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        write_to_log('ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        login = pixiv_login()
        if login:
            write_credentials(credentials_array)
        return login 
    return True

def pixiv_download(imgid, img_name_original):
    try:
        illustration = client.fetch_illustration(imgid) # 75523989
        dot = img_name_original.rfind('.')
        if dot != -1:
            newname = img_name_original[:dot]
        else:
            newname = img_name_original
        illustration.download(directory=Path.cwd() / 'Sourcery/sourced_progress/pixiv', size=Size.ORIGINAL, filename=newname)
    except Exception as e:
        print('ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        write_to_log('ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        #mb.showerror("ERROR", e)


if __name__ == '__main__':
    pixiv_authenticate('', '', ['', '', '', ''])
    pixiv_download(0, '')
