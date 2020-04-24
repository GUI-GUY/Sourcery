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
    for image_path in input_images_array:
        image_name = image_path.split('/')[-1]
        comm_img_q.put(image_name)
        comm_error_q.put('[Sourcery] Sourcing: ' + image_name)
        # if an ImageData instance with the same original name, minsim and rename options already exists, skip
        duplicate_c_pipe.send(('DATA', {'img_name': image_name, 'minsim': minsim, 'rename_pixiv': gv.config['Pixiv']['rename'], 'rename_danbooru': gv.config['Danbooru']['rename']})) # TODO yandere konachan rename
        if duplicate_c_pipe.recv():
            comm_error_q.put('[Sourcery] Image has already been sourced')
            continue
        try:
            #comm_error_q.put('[Sourcery] Moving image to working directory')
            copy(image_path, cwd + '/Sourcery/sourced_original')
        except Exception as e:
            die(str(e), comm_error_q, comm_img_q, terminate_c_pipe)
        
        res = get_response(image_name, cwd, saucenao_key, minsim, comm_error_q)
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
            processed_data = process_img_data_new(image_name, cwd + '/Sourcery/sourced_original/' + image_name, image_path, res, minsim, comm_error_q, duplicate_c_pipe)
            if processed_data != False:
                img_data_q.put(create_DIllustration(image_name, image_path, cwd + '/Sourcery/sourced_original/' + image_name, processed_data, minsim, comm_error_q))
            #process_img_data(image_name, image, res, minsim, img_data_q, comm_error_q)   
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
        img_data[0], img_data[1], img_data[2], img_data[3]], img_data[4], minsim)
    return d_illust

def process_img_data_new(img_name_original, img_path, input_path, res, minsim, comm_error_q, duplicate_c_pipe):
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
            comm_error_q.put('[Sourcery] Fetching ' + source['service_name'] + ' illustration...')
            pixiv_illustration_list.extend(pixiv_fetcher(img_name_original, source, pixiv_visited, comm_error_q))
            danbooru_illustration_list.extend(danbooru_fetcher(img_name_original, source, 'Danbooru', danbooru_visited, True, False, False, comm_error_q))
            yandere_illustration_list.extend(danbooru_fetcher(img_name_original, source, 'Yandere', yandere_visited, False, True, False, comm_error_q))
            konachan_illustration_list.extend(danbooru_fetcher(img_name_original, source, 'Konachan', konachan_visited, False, False, True, comm_error_q))

    if len(danbooru_illustration_list) == 0 and len(pixiv_illustration_list) == 0 and len(yandere_illustration_list) == 0 and len(konachan_illustration_list) == 0:
        comm_error_q.put('[Sourcery] No sources were found!')
        comm_error_q.put('DELETE' + img_path)
        gv.Files.Ref.new_reference(img_name_original, [], [], [], [], gv.config['Pixiv']['rename'], gv.config['Danbooru']['rename'], gv.config['Yandere']['rename'], gv.config['Konachan']['rename'], minsim, dict_list, input_path)
        return False

    comm_error_q.put('[Sourcery] Downloaded illustrations successfully')

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

    duplicate_c_pipe.send(('REF', (img_name_original, pixiv_ref_list, danbooru_ref_list, yandere_ref_list, konachan_ref_list, gv.config['Pixiv']['rename'], gv.config['Danbooru']['rename'], gv.config['Yandere']['rename'], gv.config['Konachan']['rename'], minsim, dict_list, input_path)))
    ref = duplicate_c_pipe.recv()#gv.Files.Ref.new_reference()

    return (pixiv_illustration_list, danbooru_illustration_list, yandere_illustration_list, konachan_illustration_list, ref)


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
    illustration = False
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
