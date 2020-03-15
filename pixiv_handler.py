from pathlib import Path
from pixivapi import Client, Size
import global_variables as gv
#from tkinter import messagebox as mb

client = Client()

def pixiv_login(comm_error_q=None):
    """
    Attempt to login to pixiv with the login data(username, password)
    """
    try:
        client.login(gv.Files.Cred.pixiv_username, gv.Files.Cred.pixiv_password)
        gv.Files.Cred.pixiv_refreshtoken = client.refresh_token
    except Exception as e:
        print('ERROR [0021] Pixiv login failed' + str(e))
        if comm_error_q != None:
            comm_error_q.put('[Sourcery] ERROR [0021] Pixiv login failed' + str(e))
        else:
            gv.Files.Log.write_to_log('ERROR [0021] Pixiv login failed' + str(e))
        #mb.showerror("ERROR", 'Login failed')
        return False
    return True


def pixiv_authenticate(comm_error_q=None):
    """
    Attempt to login to pixiv with the refreshtoken
    """
    try:
        client.authenticate(gv.Files.Cred.pixiv_refreshtoken)
    except Exception as e:
        print('ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        if comm_error_q != None:
            comm_error_q.put('[Sourcery] ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        else:
            gv.Files.Log.write_to_log('ERROR [0020] Pixiv authentication with refreshtoken failed - Attempting with login data')
        login = pixiv_login(comm_error_q)
        if login:
            gv.Files.Cred.write_credentials()
        return login 
    return True

def pixiv_fetch_illustration(img_name_original, imgid, comm_error_q=None):
    """
    Request information from pixiv for the given imgid\n
    Return illustration object on success, False otherwise
    """
    #print('id' + imgid)
    try:
        illustration = client.fetch_illustration(imgid) # 75523989
    except Exception as e:
        print('ERROR [0030]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e) + '\n')
        if comm_error_q != None:
            comm_error_q.put('[Sourcery] ERROR [0030]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e))
        else:
            gv.Files.Log.write_to_log('ERROR [0030]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e))
        #mb.showerror("ERROR", e)
        return False
    return illustration

def pixiv_download(img_name_original, imgid, illustration, comm_error_q=None):
    """
    Download given image and rename it properly\n
    Return the new name on success, False otherwise
    """
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
        if comm_error_q != None:
            comm_error_q.put('[Sourcery] ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e))
        else:
            gv.Files.Log.write_to_log('ERROR [0018]\nID: ' + str(imgid) + '\nName: ' + img_name_original + '\nError: ' + str(e))
        #mb.showerror("ERROR", e)
        return False
    return new_name


if __name__ == '__main__':
    pass
