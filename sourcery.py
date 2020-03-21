# from tkinter import messagebox as mb
from time import sleep
from shutil import copy
from saucenao_caller import get_response, decode_response
from pixiv_handler import pixiv_download, pixiv_fetch_illustration
from danbooru_handler import danbooru_download, danbooru_fetch_illustration
import global_variables as gv

def die(message, comm_error_q, comm_img_q):
    comm_error_q.put('[Sourcery] ' + message)
    comm_img_q.put('Stopped')
    #mb.showerror('ERROR', message)
    exit()

def do_sourcery(cwd, input_images_array, saucenao_key, minsim, input_dir, comm_q, comm_img_q, comm_stop_q, comm_error_q, img_data_q, duplicate_c_pipe):
    """
    1. for all images in input folder:
    2. get SauceNao information
    3. If success download image else next/die
    """
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
    pixiv_name = False
    pixiv_visited = list()
    pixiv_illustration = False
    pixiv_illustration_list = list()

    danbooru_name = False
    danbooru_parent_name = False
    danbooru_visited = list()
    danbooru_illustration = False
    danbooru_illustration_list = list()

    yandere_name = False
    yandere_parent_name = False
    yandere_visited = list()
    yandere_illustration = False
    yandere_illustration_list = list()

    konachan_name = False
    konachan_parent_name = False
    konachan_visited = list()
    konachan_illustration = False
    konachan_illustration_list = list()

    new_name = img_name_original

    for source in dict_list:
        if source['illust_id'] != 0:
            comm_error_q.put('[Sourcery] Attempting to fetch illustration...')
            if source['service_name'] == 'Pixiv':
                if source['illust_id'] not in pixiv_visited:
                    pixiv_illustration = pixiv_fetch_illustration(img_name_original, source['illust_id'], comm_error_q)
                    if pixiv_illustration != False:
                        pixiv_name = pixiv_download(img_name_original, pixiv_illustration, comm_error_q)
                    if pixiv_name != False:
                        pixiv_illustration_list.append((pixiv_illustration, pixiv_name))
                        pixiv_visited.append(source['illust_id'])
            if source['service_name'] == 'Danbooru':
                if source['illust_id'] not in danbooru_visited:
                    danbooru_illustration = danbooru_fetch_illustration(source['illust_id'], comm_error_q, danbooru=True)
                    if danbooru_illustration != False:
                        if 'parent_id' in danbooru_illustration:
                            if danbooru_illustration['parent_id'] != None and danbooru_illustration['parent_id'] not in danbooru_visited:
                                danbooru_parent_illustration = danbooru_fetch_illustration(danbooru_illustration['parent_id'], comm_error_q, danbooru=True)
                                if danbooru_parent_illustration != False:
                                    danbooru_parent_name = danbooru_download(img_name_original, danbooru_illustration['parent_id'], danbooru_parent_illustration, comm_error_q, danbooru=True)
                                if danbooru_parent_name != False:
                                    danbooru_illustration_list.append((danbooru_parent_illustration, danbooru_parent_name))
                                    danbooru_visited.append(danbooru_illustration['parent_id'])
                                    dict_list.append({"service_name": 'Danbooru', "member_id": -1, "illust_id": danbooru_illustration['parent_id'], "source": danbooru_parent_illustration['source'], "similarity": source['similarity']})#TODO similarity
                        danbooru_name = danbooru_download(img_name_original, source['illust_id'], danbooru_illustration, comm_error_q, danbooru=True)
                    if danbooru_name != False:
                        danbooru_illustration_list.append((danbooru_illustration, danbooru_name))
                        danbooru_visited.append(source['illust_id'])
            if source['service_name'] == 'Yandere':
                if source['illust_id'] not in yandere_visited:
                    yandere_illustration = danbooru_fetch_illustration(source['illust_id'], comm_error_q, yandere=True)
                    if yandere_illustration != False:
                        if 'parent_id' in yandere_illustration:
                            if yandere_illustration['parent_id'] != None and yandere_illustration['parent_id'] not in yandere_visited:
                                yandere_parent_illustration = danbooru_fetch_illustration(yandere_illustration['parent_id'], comm_error_q, yandere=True)
                                if yandere_parent_illustration != False:
                                    yandere_parent_name = danbooru_download(img_name_original, yandere_illustration['parent_id'], yandere_parent_illustration, comm_error_q, yandere=True)
                                if yandere_parent_name != False:
                                    yandere_illustration_list.append((yandere_parent_illustration, yandere_parent_name))
                                    yandere_visited.append(yandere_illustration['parent_id'])
                                    dict_list.append({"service_name": 'Yandere', "member_id": -1, "illust_id": yandere_illustration['parent_id'], "source": yandere_parent_illustration['source'], "similarity": source['similarity']})#TODO similarity
                        yandere_name = danbooru_download(img_name_original, source['illust_id'], yandere_illustration, comm_error_q, yandere=True)
                    if yandere_name != False:
                        yandere_illustration_list.append((yandere_illustration, yandere_name))
                        yandere_visited.append(source['illust_id'])
            if source['service_name'] == 'Konachan':
                if source['illust_id'] not in konachan_visited:
                    konachan_illustration = danbooru_fetch_illustration(source['illust_id'], comm_error_q, konachan=True)
                    if konachan_illustration != False:
                        if 'parent_id' in konachan_illustration:
                            if konachan_illustration['parent_id'] != None and konachan_illustration['parent_id'] not in konachan_visited:
                                konachan_parent_illustration = danbooru_fetch_illustration(konachan_illustration['parent_id'], comm_error_q, konachan=True)
                                if konachan_parent_illustration != False:
                                    konachan_parent_name = danbooru_download(img_name_original, konachan_illustration['parent_id'], konachan_parent_illustration, comm_error_q, konachan=True)
                                if konachan_parent_name != False:
                                    konachan_illustration_list.append((konachan_parent_illustration, konachan_parent_name))
                                    konachan_visited.append(konachan_illustration['parent_id'])
                                    dict_list.append({"service_name": 'Konachan', "member_id": -1, "illust_id": konachan_illustration['parent_id'], "source": konachan_parent_illustration['source'], "similarity": source['similarity']})#TODO similarity
                        konachan_name = danbooru_download(img_name_original, source['illust_id'], konachan_illustration, comm_error_q, konachan=True)
                    if konachan_name != False:
                        konachan_illustration_list.append((konachan_illustration, konachan_name))
                        konachan_visited.append(source['illust_id'])
        comm_error_q.put('[Sourcery] Downloaded illustration successfully')

    if len(danbooru_illustration_list) == 0 and len(pixiv_illustration_list) == 0 and len(yandere_illustration_list) == 0 and len(konachan_illustration_list) == 0:
        #gv.Files.Log.write_to_log('None of the requested images were available!')
        return # TODO message
    img_data_q.put((img_name_original, input_path, gv.Files.Conf.rename_pixiv, gv.Files.Conf.rename_danbooru, dict_list, pixiv_illustration_list, danbooru_illustration_list, yandere_illustration_list, konachan_illustration_list))
    
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

    gv.Files.Ref.new_reference(img_name_original, pixiv_name, pixiv_illustration_id, danbooru_name, danbooru_illustration_id, gv.Files.Conf.rename_pixiv, gv.Files.Conf.rename_danbooru, minsim)# TODO reference

