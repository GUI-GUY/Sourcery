from pathlib import Path
from pixivapi import Client, Size
import global_variables as gv
#from tkinter import messagebox as mb

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

def pixiv_fetch_illustration(img_name_original, imgid):
    try:
        illustration = client.fetch_illustration(imgid) # 75523989
        #illustration.sanity_level
    except Exception as e:
        print('ERROR [0030]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        gv.Files.Log.write_to_log('ERROR [0030]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        #mb.showerror("ERROR", e)
        return False
    return illustration

def pixiv_download(img_name_original, imgid, illustration):
    try:
        if gv.Files.Conf.rename_pixiv == 'True':
            illustration.download(directory=Path.cwd() / 'Sourcery/sourced_progress/pixiv', size=Size.ORIGINAL)
            new_name = str(illustration.id)
        else:
            dot = img_name_original.rfind('.')
            if dot != -1:
                new_name = img_name_original[:dot]
            else:
                new_name = img_name_original
            illustration.download(directory=Path.cwd() / 'Sourcery/sourced_progress/pixiv', size=Size.ORIGINAL, filename=new_name)
    except Exception as e:
        print('ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        gv.Files.Log.write_to_log('ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        #mb.showerror("ERROR", e)
        return False, None
    return True, new_name


if __name__ == '__main__':
    pass
