from pathlib import Path
from pixivapi import Client, Size
import global_variables as gv
#from file_operations import write_credentials, write_to_log
#from tkinter import messagebox as #mb

client = Client()

def pixiv_login():
    try:
        client.login(gv.Files.Cred.pixiv_username, gv.Files.Cred.pixiv_password)
        gv.Files.Cred.pixiv_refreshtoken = client.refresh_token
    except Exception as e:
        print('ERROR [0021] Pixiv login failed' + str(e))
        gv.Files.Log.write_to_log('ERROR [0021] Pixiv login failed' + str(e))
        #mb.showerror("ERROR", 'Login failed')
        return False
    return True


def pixiv_authenticate():
    try:
        client.authenticate(gv.Files.Cred.pixiv_refreshtoken)
    except Exception as e:
        print('ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        gv.Files.Log.write_to_log('ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        login = pixiv_login()
        if login:
            gv.Files.Cred.write_credentials()
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
        gv.Files.Log.write_to_log('ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        #mb.showerror("ERROR", e)


if __name__ == '__main__':
    pixiv_authenticate('', '', ['', '', '', ''])
    pixiv_download(0, '')
