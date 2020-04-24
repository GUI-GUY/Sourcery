from os import getcwd, path, makedirs
from json import loads
from copy import deepcopy
from requests import request, get
#from fake_useragent import UserAgent
import global_variables as gv

#headers = {"user-agent": UserAgent().random, 'accept-language':'en'}
headers = {'accept-language':'en'}

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
    try:
        res = get(img_info_url, headers=headers)
    except Exception as e:
        print("ERROR [0073] " + str(e))
        if comm_error_q != None:
            comm_error_q.put("[Sourcery] ERROR [0073] " + str(e))
        else:
            gv.Files.Log.write_to_log("ERROR [0073] " + str(e))
        return False
        #mb.showerror("ERROR [0073]", "ERROR CODE [0073]\nImage data could not be retrieved")
    js = loads(res.text)# {'error': True, 'message': '該当作品は削除されたか、存在しない作品IDです。', 'body': []}
    if js['error'] == False:
        #print(js["body"])
        
        return Illustration(js, headers)
    else:
        if comm_error_q != None:
            comm_error_q.put('[Sourcery] ' + js['message'] + str(imgid))
        else:
            gv.Files.Log.write_to_log(js['message'])
        return False

def pixiv_download(img_name_original, illustration, comm_error_q=None):
    """
    Download given image and rename it properly\n
    Return the new name on success, False otherwise
    """
    img_url = illustration.response["body"]["urls"]["original"]
    replace_template = "_p{page}"
    if illustration.page_count > 1:
        if gv.config['Pixiv']['rename'] == '1':
            folder_name = rename(str(illustration.id)) + '/'
            new_name = str(illustration.id) + '_p{page}.{filetype}'
        else:
            dot = img_name_original.rfind('.')
            if dot != -1:
                new_name = img_name_original[:dot] + '_p{page}.{filetype}'
                folder_name = rename(img_name_original[:dot]) + '/'
            else:
                new_name = img_name_original + '_p{page}.{filetype}'
                folder_name = rename(img_name_original) + '/'
            
        makedirs(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name, 0o777, False)
        for count in range(illustration.page_count):
            illustration.headers["referer"] = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illustration.id)
            img_url = img_url.replace(replace_template.format(page=count-1), replace_template.format(page=count))
            try:
                img_res = get(img_url, headers=illustration.headers)
            except Exception as e:
                print("ERROR [0066] " + str(e))
                if comm_error_q != None:
                    comm_error_q.put("[Sourcery] ERROR [0066] " + str(e))
                    return False
                else:
                    gv.Files.Log.write_to_log("ERROR [0066] " + str(e))
                #mb.showerror("ERROR [0066]", "ERROR CODE [0066]\nImage could not be downloaded")
            filetype = img_url.split(".")[-1]
            try:
                with open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name + new_name.format(page=count,filetype=filetype),"wb+") as f:
                    f.write(img_res.content)
            except Exception as e:
                print("ERROR [0065] " + str(e))
                if comm_error_q != None:
                    comm_error_q.put("[Sourcery] ERROR [0065] " + str(e))
                    return False
                else:
                    gv.Files.Log.write_to_log("ERROR [0065] " + str(e))
                #mb.showerror("ERROR [0065]", "ERROR CODE [0065]\nImage could not be downloaded")
        return folder_name[:-1]
    else:
        if gv.config['Pixiv']['rename'] == '1':
            new_name = str(illustration.id) + '_p0.{filetype}'
        else:
            dot = img_name_original.rfind('.')
            if dot != -1:
                new_name = img_name_original[:dot] + '.{filetype}'
            else:
                new_name = img_name_original + '.{filetype}'
        filetype = img_url.split('.')[-1]
        new_name = rename(new_name.format(filetype=filetype))

        illustration.headers["referer"] = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illustration.id)
        img_res = get(img_url, headers=illustration.headers)
        try:
            with open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + new_name, "wb+") as f :
                f.write(img_res.content)
        except Exception as e:
            print("ERROR [0064] " + str(e))
            if comm_error_q != None:
                comm_error_q.put("[Sourcery] ERROR [0064] " + str(e))
                return False
            else:
                gv.Files.Log.write_to_log("ERROR [0064] " + str(e))
            #mb.showerror("ERROR [0064]", "ERROR CODE [0064]\nImage could not be downloaded")
        return new_name
    
#________________________________________
    # replace_template = "_p{page}"
    # img_url = illustration.response["body"]["urls"]["original"]
    # if gv.config['Pixiv']['rename'] == '1':
    #     folder_name = str(illustration.id) + '/'
    #     new_name = str(illustration.id) + '_p{page}.{format}'
    # else:
    #     dot = img_name_original.rfind('.')
    #     if dot != -1:
    #         new_name = img_name_original[:dot] + '{page}.{format}'
    #         folder_name = img_name_original[:dot] + '/'
    #     else:
    #         new_name = img_name_original + '{page}.{format}'
    #         folder_name = img_name_original + '/'

    # if illustration.page_count > 1:
    #     makedirs(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name, 0o777, True)
    # else:
    #     folder_name = ''

    # image_format = ''
    # for count in range(illustration.page_count):
    #     illustration.headers["referer"] = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illustration.id)
    #     img_url = img_url.replace(replace_template.format(page=count-1), replace_template.format(page=count))
    #     img_res = get(img_url, headers=illustration.headers)
    #     if img_res.status_code != 200 :
    #         break
    #     image_format = img_url.split(".")[-1]
    #     if illustration.page_count > 1:
    #         name = rename
    #         with open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name + new_name.format(page=count,format=image_format),"wb+") as fp :
    #             fp.write(img_res.content)
    #     else:
    #         with open(gv.cwd + '/Sourcery/sourced_progress/pixiv/' + folder_name + new_name.format(page='',format=image_format),"wb+") as fp :
    #             fp.write(img_res.content)
    
    # if illustration.page_count > 1:
    #     return folder_name[:-1]
    # else:
    #     return new_name.format(page='',format=image_format)

def rename(desired_name, index=-1, new_name=''):
    if new_name == '':
        if path.isfile(getcwd() + '/Sourcery/sourced_progress/pixiv/' + desired_name) or path.isdir(getcwd() + '/Sourcery/sourced_progress/pixiv/' + desired_name):
            index = index+1
            dot = desired_name.rfind('.')
            if dot == -1:
                desired_name = rename_length(desired_name)
                new_name = desired_name + '_' + str(index)
            else:
                pre_name = rename_length(desired_name[:dot])
                new_name = pre_name + '_' + str(index) + desired_name[dot:] 
            return rename(desired_name, index, new_name)
    else:
        if path.isfile(getcwd() + '/Sourcery/sourced_progress/pixiv/' + new_name) or path.isdir(getcwd() + '/Sourcery/sourced_progress/pixiv/' + new_name):
            index = index+1
            dot = desired_name.rfind('.')
            if dot == -1:
                desired_name = rename_length(desired_name)
                new_name = desired_name + '_' + str(index)
            else:
                pre_name = rename_length(desired_name[:dot])
                new_name = pre_name + '_' + str(index) + desired_name[dot:] 
            return rename(desired_name, index, new_name)
        return new_name
    return desired_name

def rename_length(name):
    if len(name) > 165:
        name = name[:165]
    return name

def download(pid) :
    referer_template = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={pid}"
    img_info_url = "https://www.pixiv.net/ajax/illust/{pid}"
    replace_template = "_p{page}"

    file_name = "{pid}_p{page}.{format}"
    #headers = {"user-agent": UserAgent().random}

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