# from tkinter import messagebox as mb
from time import sleep
from shutil import copy
from saucenao_caller import get_response, decode_response
from pixiv_handler import pixiv_authenticate, pixiv_download, pixiv_fetch_illustration
from danbooru_handler import danbooru_download, danbooru_fetch_illustration
import global_variables as gv

def die(message, comm_error_q, comm_img_q):
    comm_error_q.put('[Sourcery] ' + message)
    comm_img_q.put('Stopped')
    #mb.showerror('ERROR', message)
    exit()

def do_sourcery(cwd, input_images_array, saucenao_key, minsim, input_dir, comm_q, comm_img_q, comm_stop_q, comm_error_q, img_data_q, duplicate_c_pipe):
    """
    1. Pixiv Login
    2. for all images in input folder:
    3. get SauceNao information
    4. If success download image else next/die
    """
    comm_error_q.put('[Sourcery] Attempting Pixiv login...')
    if not pixiv_authenticate(comm_error_q):
        die('Pixiv Authentication Failed.\nPlease check your login data.', comm_error_q, comm_img_q)
    comm_error_q.put('[Sourcery] Pixiv login successful')

    # For every input image a request goes out to saucenao and gets decoded
    for image in input_images_array:
        img = image.split('/')[-1]
        comm_img_q.put(img)
        comm_error_q.put('[Sourcery] Sourcing: ' + img)
        # if an ImageData instance with the same original name, minsim and rename options already exists, skip
        duplicate_c_pipe.send({'img_name': img, 'minsim': minsim, 'rename_pixiv': gv.Files.Conf.rename_pixiv, 'rename_danbooru': gv.Files.Conf.rename_danbooru})
        next_img = duplicate_c_pipe.recv()
        if next_img:
            comm_error_q.put('[Sourcery] Image has already been sourced')
            continue
        try:
            comm_error_q.put('[Sourcery] Moving image to working directory')
            copy(image, cwd + '/Sourcery/sourced_original')
        except Exception as e:
            die(str(e), comm_error_q, comm_img_q)
        
        res = get_response(img, cwd, saucenao_key, minsim, comm_error_q)
        if res[0] == 401:
            # Exception while opening image!
            comm_error_q.put('[Sourcery] ' + res[1])
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
            comm_q.put((res[3], res[4]))
            die(res[1] + '\nSauceNao gave a response but there was a problem on their end.\nStopped further processing of images to give the server time to recover.\nTry again in a few minutes.', comm_error_q, comm_img_q)
        elif res[0] == 41:
            # Problem with search as submitted, bad image, or impossible request.
            # Issue is unclear, so don't flood requests.
            comm_q.put((res[3], res[4]))
            if res[3] < 1:
                die(res[1] + ' + Out of searches for today', comm_error_q, comm_img_q)
            else:
                comm_error_q.put('[Sourcery] ' + res[1])
            if res[2] < 1:
                sleep(30)
        elif res[0] == 402:
            # General issue, api did not respond. Normal site took over for this error state.
            # Issue is unclear, so don't flood requests.
            comm_error_q.put('[Sourcery] ' + res[1])
            sleep(10)
        elif res[0] == 200:
            comm_q.put((res[3], res[4]))
            process_img_data(img, image, res, minsim, img_data_q, comm_error_q)   
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
            
def process_img_data(img_name_original, input_path, res, minsim, img_data_q, comm_error_q):
    """
    Downloads the image from pixiv and Danbooru
    Returns information on the downloads
    """
    # dict_list is list of dicts of this format: {"service_name": service_name, "illust_id": illust_id, "source": source}
    dict_list = decode_response(res[1])
    # print('hier dict list:')
    # print(dict_list)
    pixiv_illustration = False
    pixiv_illustration_list = list()
    danbooru_illustration = False
    danbooru_illustration_list = list()
    new_name = img_name_original
    danb_name = False
    pixiv_name = False
    pixiv_visited = list()
    danbooru_visited = list()

    for source in dict_list: # TODO same id filter
        if source['illust_id'] != 0:
            comm_error_q.put('[Sourcery] Attempting to fetch illustration...')
            if source['service_name'] == 'Pixiv':
                if source['illust_id'] not in pixiv_visited:
                    pixiv_illustration = pixiv_fetch_illustration(img_name_original, source['illust_id'], comm_error_q)
                    if pixiv_illustration != False:
                        pixiv_name = pixiv_download(img_name_original, source['illust_id'], pixiv_illustration, comm_error_q)
                    if pixiv_name != False:
                        pixiv_illustration_list.append((pixiv_illustration, pixiv_name))
                        pixiv_visited.append(source['illust_id'])
            if source['service_name'] == 'Danbooru':
                if source['illust_id'] not in danbooru_visited:
                    danbooru_illustration = danbooru_fetch_illustration(source['illust_id'], comm_error_q)
                    if danbooru_illustration != False:
                        danb_name = danbooru_download(img_name_original, source['illust_id'], danbooru_illustration, comm_error_q)
                    if danb_name != False:
                        danbooru_illustration_list.append((danbooru_illustration, danb_name))
                        danbooru_visited.append(source['illust_id'])
        comm_error_q.put('[Sourcery] Downloaded illustration successfully')
    
    if len(danbooru_illustration_list) == 0 and len(pixiv_illustration_list) == 0:
        return #TODO Message
    img_data_q.put((img_name_original, input_path, gv.Files.Conf.rename_pixiv, gv.Files.Conf.rename_danbooru, dict_list, pixiv_illustration_list, danbooru_illustration_list))
    
    pixiv_name = ''
    pixiv_illustration_id = ''
    for elem in pixiv_illustration_list:
        pixiv_name = pixiv_name + ' | ' + elem[1]
        pixiv_illustration_id = pixiv_illustration_id + str(elem[0].id) + ' | '
    
    danbooru_name = ''
    danbooru_illustration_id = ''
    for elem in danbooru_illustration_list:
        danbooru_name = danbooru_name + ' | ' + elem[1]
        danbooru_illustration_id = danbooru_illustration_id + str(elem[0]['id']) + ' | '

    gv.Files.Ref.new_reference(img_name_original, pixiv_name, pixiv_illustration_id, danb_name, danbooru_illustration_id, gv.Files.Conf.rename_pixiv, gv.Files.Conf.rename_danbooru, minsim)# TODO
    
    #return img_name_original, pixiv_name, danb_name, dict_list, pixiv_illustration, danbooru_illustration
    #return False, None, None, None, None # TODO
