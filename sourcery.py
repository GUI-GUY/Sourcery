# from tkinter import messagebox as mb
from time import sleep
from shutil import copy
from saucenao_caller import get_response, decode_response
from pixiv_handler import pixiv_authenticate, pixiv_download

def die(message, comm_error_q, comm_img_q):
    comm_error_q.put(message)
    comm_img_q.put('Stopped')
    #mb.showerror('ERROR', message)
    exit()

def do_sourcery(cwd, input_images_array, saucenao_key, minsim, comm_q, comm_img_q, comm_stop_q, comm_error_q):
    if not pixiv_authenticate():
        die('Pixiv Authentication Failed.\nPlease check your login data.', comm_error_q, comm_img_q)
    # For every input image a request goes out to saucenao and gets decoded
    for img in input_images_array:
        comm_img_q.put(img)
        try:
            copy(cwd + '/Input/' + img, cwd + '/Sourcery/sourced_original')
        except Exception as e:
            die(str(e), comm_error_q, comm_img_q)
        res = get_response(img, cwd, saucenao_key, minsim)
        if res[0] == 401:
            # Exception while opening image!
            comm_error_q.put(res[1])
            continue
        elif res[0] == 403:
            # Incorrect or Invalid API Key!
            die(res[1], comm_error_q, comm_img_q)
        elif res[0] == 2:
            # generally non 200 statuses are due to either overloaded servers or the user is out of searches
            die(res[1] + '\nSauceNao servers are overloaded\nor you are out of searches.\nTry again tomorrow.', comm_error_q, comm_img_q)
        elif res[0] == 600:
            # One or more indexes are having an issue.
            # This search is considered partially successful, even if all indexes failed, so is still counted against your limit.
            # The error may be transient, but because we don't want to waste searches, allow time for recovery.
            comm_q.put(res[3])
            die(res[1] + '\nSauceNao gave a response but there was a problem on their end.\nStopped further processing of images to give the server time to recover.\nTry again in a few minutes.', comm_error_q, comm_img_q)
        elif res[0] == 41:
            # Problem with search as submitted, bad image, or impossible request.
            # Issue is unclear, so don't flood requests.
            comm_q.put(res[3])
            if res[3] < 1:
                die(res[1] + ' + Out of searches for today', comm_error_q, comm_img_q)
            else:
                comm_error_q.put(res[1])
            if res[2] < 1:
                sleep(30)
        elif res[0] == 402:
            # General issue, api did not respond. Normal site took over for this error state.
            # Issue is unclear, so don't flood requests.
            comm_error_q.put(res[1])
            sleep(10)
        elif res[0] == 200:
            comm_q.put(res[3])
            img_data_array = decode_response(res[1])
            process_img_data(img_data_array, img)
            if res[3] < 1:
                die('Out of searches for today', comm_error_q, comm_img_q)
            if res[2] < 1:
                sleep(30)
        if not comm_stop_q.empty():
            try:
                stop_signal = comm_stop_q.get()
                if stop_signal != None:
                    comm_img_q.put(stop_signal)
                    return
            except:
                pass
    comm_img_q.put("Finished")
    exit()
            
def process_img_data(img_data_array, img_name_original):
    if img_data_array[1] != 0:
        pixiv_download(img_data_array[1], img_name_original)
