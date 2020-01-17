from tkinter import messagebox as mb
from time import sleep
from shutil import copy
from saucenao_caller import get_response, decode_response
from pixiv_handler import pixiv_authenticate, pixiv_login, pixiv_download

def do_sourcery(cwd, input_images_array, saucenao_key, comm_q, comm_img_q, pixiv_username, pixiv_password, credentials_array, comm_stop_q):
    pixiv_authenticate(pixiv_username, pixiv_password, credentials_array)
    # For every input image a request goes out to saucenao and gets decoded
    for img in input_images_array:
        comm_img_q.put(img)
        copy(cwd + '/Input/' + img, cwd + '/Sourcery/sourced_original')
        res = get_response(img, cwd, saucenao_key)
        if res[0] == 403:
            # stop()
            mb.showerror('ERROR', res[1])
        elif res[0] == 2:
            # stop()
            mb.showerror('ERROR', res[1] + '\nSauceNao servers are overloaded\nor you are out of searches.\nTry again tomorrow.')
        elif res[0] == 600:
            comm_q.put(res[3])
            # stop()
            mb.showerror('ERROR', res[1] + '\nSauceNao gave a response but there was a problem on their end.\nStopped further processing of images to give the server time to recover.\nTry again in a few minutes.')
        elif res[0] == 41:
            comm_q.put(res[3])
            #if res[3] < 1:
                #stop()
            if res[2] < 1:
                sleep(30)
            mb.showerror('ERROR', res[1])
        elif res[0] == 402:
            mb.showerror('ERROR', res[1])
        elif res[0] == 200:
            comm_q.put(res[3])
            img_data_array = decode_response(res[1])
            process_img_data(img_data_array, img)
            #if res[3] < 1:
                #stop()
            if res[2] < 1:
                sleep(30)
        if not comm_stop_q.empty():
            try:
                stop_signal = comm_stop_q.get()
                if stop_signal != None:
                    comm_img_q.put(stop_signal)
                    break
            except:
                pass
            

def process_img_data(img_data_array, img_name_original):
    if img_data_array[1] != 0:
        pixiv_download(img_data_array[1], img_name_original)
