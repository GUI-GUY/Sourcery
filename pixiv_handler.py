from os import getcwd, path, makedirs
from json import loads
from copy import deepcopy
from requests import request, get
from fake_useragent import UserAgent
import global_variables as gv

headers = {"user-agent": UserAgent().random, 'accept-language':'en'}

class Illustration():
    """Includes all information on the pixiv image"""
    def __init__(self, response, headers):
        self.response = response
        self.headers = deepcopy(headers)
        self.id = response['body']['illustId']
        self.tags = list()
        #print(response['body']['tags']['tags'][1])
        for elem in response['body']['tags']['tags']:
            if 'translation' in elem:
                if 'en' in elem['translation']:
                    self.tags.append({'name': elem['tag'], 'translated_name': elem['translation']['en']})
                else:
                    self.tags.append({'name': elem['tag'], 'translated_name': None})
            else:
                self.tags.append({'name': elem['tag'], 'translated_name': None})
        self.tags.append("title:" + response['body']['title'])
        self.tags.append("pixiv work:" + str(response['body']['illustId']))
        self.tags.append("rating:" + str(response['body']['sl']))
        self.tags.append("creator:" + response['body']['userName'])
        self.user = Artist(response['body']['userName'], response['body']['userId'])
        self.title = response['body']['title']
        self.caption = response['body']['illustComment']
        self.description = response['body']['description']
        self.create_date = response['body']['createDate']
        self.width = response['body']['width']
        self.height = response['body']['height']
        self.page_count = response['body']['pageCount']
        # self.sanity_level = response['body']['sl']
        
class Artist():
    """Includes all information on the artist"""
    def __init__(self, name, userid):
        self.name = name
        self.id = userid
        
def pixiv_fetch_illustration(img_name_original, imgid, comm_error_q=None):
    """
    Request information from pixiv for the given imgid\n
    Return illustration object on success, False otherwise
    """
    global headers
    img_info_url = "https://www.pixiv.net/ajax/illust/" + str(imgid)
    res = get(img_info_url, headers=headers)
    js = loads(res.text)# {'error': True, 'message': '該当作品は削除されたか、存在しない作品IDです。', 'body': []}
    
    if js['error'] == False:
        #print(js["body"])
        
        return Illustration(js, headers)
    return False

def pixiv_download(img_name_original, illustration, comm_error_q=None):
    """
    Download given image and rename it properly\n
    Return the new name on success, False otherwise
    """
    replace_template = "_p{page}"
    img_url = illustration.response["body"]["urls"]["original"]
    if gv.Files.Conf.rename_pixiv == '1':
        folder_name = str(illustration.id) + '/'
        new_name = str(illustration.id) + '_p{page}.{format}'
    else:
        dot = img_name_original.rfind('.')
        if dot != -1:
            new_name = img_name_original[:dot] + '{page}.{format}'
            folder_name = img_name_original[:dot] + '/'
        else:
            new_name = img_name_original + '{page}.{format}'
            folder_name = img_name_original + '/'

    if illustration.page_count > 1:
        makedirs(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name, 0o777, True)
    else:
        folder_name = ''

    image_format = ''
    for count in range(illustration.page_count):
        illustration.headers["referer"] = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illustration.id)
        img_url = img_url.replace(replace_template.format(page=count-1), replace_template.format(page=count))
        img_res = get(img_url, headers=illustration.headers)
        if img_res.status_code != 200 :
            break
        image_format = img_url.split(".")[-1]
        if illustration.page_count > 1:
            with open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name + new_name.format(page=count,format=image_format),"wb+") as fp :
                fp.write(img_res.content)
        else:
            with open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name + new_name.format(page='',format=image_format),"wb+") as fp :
                fp.write(img_res.content)
    
    if illustration.page_count > 1:
        return folder_name[:-1]
    else:
        return new_name.format(page='',format=image_format)


def download(pid) :
    referer_template = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={pid}"
    img_info_url = "https://www.pixiv.net/ajax/illust/{pid}"
    replace_template = "_p{page}"

    file_name = "{pid}_p{page}.{format}"
    headers = {"user-agent": UserAgent().random}

    if pid == '':
        #pid = 80147954
        pid = 77908149
    print(pid)
    dir_path = getcwd() + '/Image/' + str(pid)
    if not path.exists(dir_path):
        makedirs(dir_path)
    file_name = path.join(dir_path,file_name)

    # if self.gif_down.isGIF(pid) :
    #     self.gif_down.download(pid)
    if False:
        pass
    else :
        headers = headers.copy()
        info_url = img_info_url.format(pid=pid)
        res = get(info_url, headers=headers)
        js = loads(res.text)# {'error': True, 'message': '該当作品は削除されたか、存在しない作品IDです。', 'body': []}
        
        if js['error'] == False:
            #print(js["body"])
            img_url = js["body"]["urls"]["original"]

            count = -1
            while True :
                headers["referer"] = referer_template.format(pid=pid)
                img_url = img_url.replace(replace_template.format(page=count), replace_template.format(page=count + 1))
                img_res = get(img_url, headers=headers)
                if img_res.status_code != 200 :
                    break
                image_format = img_url.split(".")[-1]
                with open(file_name.format(pid=pid,page=count+1,format=image_format),"wb+") as fp :
                    fp.write(img_res.content)
                count += 1
    print(pid,"The download is complete.")

if __name__ == "__main__" :
    #download(input('id:'))
    x = pixiv_fetch_illustration('name', 77079631)#79580140
    pixiv_download('name', x)#79580140
    pass