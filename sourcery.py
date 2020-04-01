# from tkinter import messagebox as mb
from time import sleep
from shutil import copy
from saucenao_caller import get_response, decode_response
from pixiv_handler import pixiv_download, pixiv_fetch_illustration
from danbooru_handler import danbooru_download, danbooru_fetch_illustration
from DIllustration import DIllustration
import global_variables as gv

def die(message, comm_error_q, comm_img_q, terminate_c_pipe):
    comm_error_q.put('[Sourcery] ' + message)
    comm_img_q.put('Stopped')
    #mb.showerror('ERROR', message)
    terminate_c_pipe.send(True)
    while not terminate_c_pipe.recv():
        terminate_c_pipe.send(True)
    #exit()

def do_sourcery(cwd, input_images_array, saucenao_key, minsim, input_dir, comm_q, comm_img_q, comm_stop_q, comm_error_q, img_data_q, duplicate_c_pipe, terminate_c_pipe):
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
            die(str(e), comm_error_q, comm_img_q, terminate_c_pipe)
        
        res = get_response(img, cwd, saucenao_key, minsim, comm_error_q)
        if res[0] == 401:
            # Exception while opening image!
            comm_error_q.put('[Sourcery] ' + res[1])
            continue
        elif res[0] == 403:
            # Incorrect or Invalid API Key!
            die(res[1], comm_error_q, comm_img_q, terminate_c_pipe)
        elif res[0] == 666:
            # Request failed!
            die(res[1], comm_error_q, comm_img_q, terminate_c_pipe)
        elif res[0] == 2:
            # generally non 200 statuses are due to either overloaded servers or the user is out of searches
            die(res[1] + '\nSauceNao servers are overloaded\nor you are out of searches.\nTry again tomorrow.', comm_error_q, comm_img_q, terminate_c_pipe)
        elif res[0] == 600:
            # One or more indexes are having an issue.
            # This search is considered partially successful, even if all indexes failed, so is still counted against your limit.
            # The error may be transient, but because we don't want to waste searches, allow time for recovery.
            comm_q.put((res[3], res[4]))
            die(res[1] + '\nSauceNao gave a response but there was a problem on their end.\nStopped further processing of images to give the server time to recover.\nTry again in a few minutes.', comm_error_q, comm_img_q, terminate_c_pipe)
        elif res[0] == 41:
            # Problem with search as submitted, bad image, or impossible request.
            # Issue is unclear, so don't flood requests.
            comm_q.put((res[3], res[4]))
            if res[3] < 1:
                die(res[1] + ' + Out of searches for today', comm_error_q, comm_img_q, terminate_c_pipe)
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
            processed_data = process_img_data_new(img, cwd + '/Sourcery/sourced_original/' + img, input_dir, res, minsim, comm_error_q)
            if processed_data != False:
                img_data_q.put(create_DIllustration(img, image, cwd + '/Sourcery/sourced_original/' + img, processed_data, minsim, comm_error_q))
            #process_img_data(img, image, res, minsim, img_data_q, comm_error_q)   
            if res[3] < 1:
                die('Out of searches for today', comm_error_q, comm_img_q, terminate_c_pipe)
            if res[2] < 1:
                comm_error_q.put('[Sourcery] Sleeping 30 seconds because of SauceNao restrictions')
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
    terminate_c_pipe.send(True)
            
def create_DIllustration(img_name_original, input_path, work_path, img_data, minsim, comm_error_q):
    """
    Creates a DIllustration object
    """
    d_illust = DIllustration(input_path, 
        [{"service":'Original', "name":img_name_original, "work_path":work_path}, 
        img_data[0], img_data[1], img_data[2], img_data[3]], minsim)
    return d_illust

def process_img_data_new(img_name_original, img_path, input_path, res, minsim, comm_error_q):
    """
    Downloads the image from pixiv and Danbooru
    Returns information on the downloads
    """
    # dict_list is list of dicts of this format: {"service_name": service_name, "illust_id": illust_id, "source": source}
    dict_list = decode_response(res[1])

    pixiv_visited = list()
    pixiv_illustration_list = list()

    danbooru_visited = list()
    danbooru_illustration_list = list()

    yandere_visited = list()
    yandere_illustration_list = list()

    konachan_visited = list()
    konachan_illustration_list = list()

    new_name = img_name_original

    for source in dict_list:
        if source['illust_id'] != 0:
            comm_error_q.put('[Sourcery] Attempting to fetch ' + source['service_name'] + ' illustration...')
            pixiv_illustration_list.extend(pixiv_fetcher(img_name_original, source, pixiv_visited, comm_error_q))
            danbooru_illustration_list.extend(danbooru_fetcher(img_name_original, source, 'Danbooru', danbooru_visited, True, False, False, comm_error_q))
            yandere_illustration_list.extend(danbooru_fetcher(img_name_original, source, 'Yandere', yandere_visited, False, True, False, comm_error_q))
            konachan_illustration_list.extend(danbooru_fetcher(img_name_original, source, 'Konachan', konachan_visited, False, False, True, comm_error_q))

        comm_error_q.put('[Sourcery] Downloaded ' + source['service_name'] + ' illustration successfully')

    if len(danbooru_illustration_list) == 0 and len(pixiv_illustration_list) == 0 and len(yandere_illustration_list) == 0 and len(konachan_illustration_list) == 0:
        comm_error_q.put('None of the requested images were available!')
        comm_error_q.put('DELETE' + img_path)
        gv.Files.Ref.new_reference(img_name_original, [], [], [], [], gv.Files.Conf.rename_pixiv, gv.Files.Conf.rename_danbooru, gv.Files.Conf.rename_yandere, gv.Files.Conf.rename_konachan, minsim, dict_list, input_path)
        return False
    
    pixiv_ref_list = list()
    for elem in pixiv_illustration_list:
        pixiv_ref_list.append((elem[1], elem[0].id))

    danbooru_ref_list = list()
    for elem in danbooru_illustration_list:
        danbooru_ref_list.append((elem[1], elem[0]['id']))

    yandere_ref_list = list()
    for elem in yandere_illustration_list:
        yandere_ref_list.append((elem[1], elem[0]['id']))

    konachan_ref_list = list()
    for elem in konachan_illustration_list:
        konachan_ref_list.append((elem[1], elem[0]['id']))

    gv.Files.Ref.new_reference(img_name_original, pixiv_ref_list, danbooru_ref_list, yandere_ref_list, konachan_ref_list, gv.Files.Conf.rename_pixiv, gv.Files.Conf.rename_danbooru, gv.Files.Conf.rename_yandere, gv.Files.Conf.rename_konachan, minsim, dict_list, input_path)

    return (pixiv_illustration_list, danbooru_illustration_list, yandere_illustration_list, konachan_illustration_list)


def pixiv_fetcher(img_name_original, source, visited, comm_error_q):
    illustration_list = list()
    pixiv_name = False
    if source['service_name'] == 'Pixiv':
        if source['illust_id'] not in visited:
            pixiv_illustration = pixiv_fetch_illustration(img_name_original, source['illust_id'], comm_error_q)
            if pixiv_illustration != False:
                pixiv_name = pixiv_download(img_name_original, pixiv_illustration, comm_error_q)
            if pixiv_name != False:
                illustration_list.append((pixiv_illustration, pixiv_name, source))
                visited.append(source['illust_id'])
    return illustration_list

def danbooru_fetcher(img_name_original, source, service, visited, danbooru, yandere, konachan, comm_error_q):
    illustration_list = list()
    illustration = None
    parent_name = False
    name = False
    if source['service_name'] == service:
        if source['illust_id'] not in visited:
            illustration = danbooru_fetch_illustration(source['illust_id'], comm_error_q, danbooru=danbooru, yandere=yandere, konachan=konachan)
            if illustration != False:
                if 'parent_id' in illustration:
                    if illustration['parent_id'] != None and illustration['parent_id'] not in visited:
                        parent_illustration = danbooru_fetch_illustration(illustration['parent_id'], comm_error_q, danbooru=danbooru, yandere=yandere, konachan=konachan)
                        if parent_illustration != False:
                            parent_name = danbooru_download(img_name_original, illustration['parent_id'], parent_illustration, comm_error_q, danbooru=danbooru, yandere=yandere, konachan=konachan)
                        if parent_name != False:
                            illustration_list.append((parent_illustration, parent_name, {"service_name": 'Konachan', "member_id": -1, "illust_id": illustration['parent_id'], "source": parent_illustration['source'], "similarity": source['similarity']}))
                            visited.append(illustration['parent_id'])
                name = danbooru_download(img_name_original, source['illust_id'], illustration, comm_error_q, danbooru=danbooru, yandere=yandere, konachan=konachan)
            if name != False:
                illustration_list.append((illustration, name, source))
                visited.append(source['illust_id'])
    return illustration_list

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
                                    dict_list.append({"service_name": 'Danbooru', "member_id": -1, "illust_id": danbooru_illustration['parent_id'], "source": danbooru_parent_illustration['source'], "similarity": source['similarity']})
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
                                    dict_list.append({"service_name": 'Yandere', "member_id": -1, "illust_id": yandere_illustration['parent_id'], "source": yandere_parent_illustration['source'], "similarity": source['similarity']})
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
                                    dict_list.append({"service_name": 'Konachan', "member_id": -1, "illust_id": konachan_illustration['parent_id'], "source": konachan_parent_illustration['source'], "similarity": source['similarity']})
                        konachan_name = danbooru_download(img_name_original, source['illust_id'], konachan_illustration, comm_error_q, konachan=True)
                    if konachan_name != False:
                        konachan_illustration_list.append((konachan_illustration, konachan_name))
                        konachan_visited.append(source['illust_id'])
        comm_error_q.put('[Sourcery] Downloaded illustration successfully')

    if len(danbooru_illustration_list) == 0 and len(pixiv_illustration_list) == 0 and len(yandere_illustration_list) == 0 and len(konachan_illustration_list) == 0:
        comm_error_q.put('None of the requested images were available!')
        return
    img_data_q.put((img_name_original, input_path, dict_list, pixiv_illustration_list, danbooru_illustration_list, yandere_illustration_list, konachan_illustration_list))
    
    pixiv_ref_list = list()
    for elem in pixiv_illustration_list:
        pixiv_ref_list.append((elem[1], elem[0].id))

    danbooru_ref_list = list()
    for elem in danbooru_illustration_list:
        danbooru_ref_list.append((elem[1], elem[0]['id']))

    yandere_ref_list = list()
    for elem in yandere_illustration_list:
        yandere_ref_list.append((elem[1], elem[0]['id']))

    konachan_ref_list = list()
    for elem in konachan_illustration_list:
        konachan_ref_list.append((elem[1], elem[0]['id']))


    gv.Files.Ref.new_reference(img_name_original, pixiv_ref_list, danbooru_ref_list, yandere_ref_list, konachan_ref_list, gv.Files.Conf.rename_pixiv, gv.Files.Conf.rename_danbooru, gv.Files.Conf.rename_yandere, gv.Files.Conf.rename_konachan, minsim, dict_list, input_path)

