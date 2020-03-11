from os import getcwd # path manipulation
from urllib.request import urlretrieve
from requests import get
#from webbrowser import open_new
import global_variables as gv

# https://github.com/uncountablecat/danbooru-grabber
# make sure the folder already exists!
danbooru_folder = 'D:\All_Files\python\GitHub\Sourcery\Sourcery\dan'


# request json, get urls of pictures and download them
def danbooru_fetch_illustration(imgid, comm_error_q=None):
    r = get('https://danbooru.donmai.us/posts/' + str(imgid) + '.json')
    illustration = r.json()
    return illustration # TODO

def danbooru_download(img_name_original, imgid, illustration, comm_error_q=None):
    if 'file_url' in illustration:
        if gv.Files.Conf.rename_pixiv == 'True':
            urlretrieve(illustration['file_url'], getcwd() + '/Sourcery/sourced_progress/danbooru/' + illustration['file_url'].split('/')[-1])
            new_name = illustration['file_url'].split('/')[-1]
        else:
            dot = img_name_original.rfind('.')
            if dot != -1:
                new_name = img_name_original[:dot]
            else:
                new_name = img_name_original
            urlretrieve(illustration['file_url'], getcwd() + '/Sourcery/sourced_progress/danbooru/' + new_name + '.' + illustration['file_ext'])
    return new_name# TODO
    #urlretrieve('https://i.pximg.net/img-original/img/2018/11/16/00/00/01/71671760_p0.png', danbooru_folder + '/' + folder + '/' + stream['file_url'].split('/')[-1])


if __name__ == '__main__':
    danbooru_fetch_illustration(1)
    print('Download successful!')

# [{'id': 3810771, 
# 'created_at': '2020-03-06T04:51:23.187-05:00', 
# 'uploader_id': 546373, 
# 'score': 5, 
# 'source': 'https://twitter.com/RireNe_rn/status/1224175196031971329', 
# 'md5': '939593fb21e89156e0b44dfcc08207df', 
# 'last_comment_bumped_at': None, 
# 'rating': 's', 
# 'image_width': 1370, 
# 'image_height': 1202, 
# 'tag_string': '2girls akizone animal_ears bangs bare_shoulders black_jacket black_legwear blue_hair breasts character_name cleavage commentary dog_ears dog_tail eyebrows_visible_through_hair highres jacket long_hair multiple_girls multiple_views one_eye_closed open_mouth original purple_eyes red_eyes rene_(rirene) rirene_rn shirt shoes tail teeth thighhighs tongue tongue_out white_footwear white_hair white_shirt', 
# 'is_note_locked': False, 
# 'fav_count': 9, 
# 'file_ext': 'jpg', 
# 'last_noted_at': None, 
# 'is_rating_locked': False, 
# 'parent_id': None, 
# 'has_children': False, 
# 'approver_id': None, 
# 'tag_count_general': 31, 
# 'tag_count_artist': 2, 
# 'tag_count_character': 1, 
# 'tag_count_copyright': 1, 
# 'file_size': 322078, 
# 'is_status_locked': False, 
# 'pool_string': '', 
# 'up_score': 5, 
# 'down_score': 0, 
# 'is_pending': False, 
# 'is_flagged': False, 
# 'is_deleted': False, 
# 'tag_count': 37, 
# 'updated_at': '2020-03-06T04:52:15.214-05:00', 
# 'is_banned': False, 
# 'pixiv_id': None, 
# 'last_commented_at': None, 
# 'has_active_children': False, 
# 'bit_flags': 2, 
# 'tag_count_meta': 2, 
# 'has_large': True, 
# 'has_visible_children': False, 
# 'is_favorited': False, 
# 'tag_string_general': '2girls animal_ears bangs bare_shoulders black_jacket black_legwear blue_hair breasts character_name cleavage dog_ears dog_tail eyebrows_visible_through_hair jacket long_hair multiple_girls multiple_views one_eye_closed open_mouth purple_eyes red_eyes shirt shoes tail teeth thighhighs tongue tongue_out white_footwear white_hair white_shirt', 
# 'tag_string_character': 'rene_(rirene)', 
# 'tag_string_copyright': 'original', 
# 'tag_string_artist': 'akizone rirene_rn', 
# 'tag_string_meta': 'commentary highres', 
# 'file_url': 'https://danbooru.donmai.us/data/939593fb21e89156e0b44dfcc08207df.jpg', 
# 'large_file_url': 'https://danbooru.donmai.us/data/sample/sample-939593fb21e89156e0b44dfcc08207df.jpg', 
# 'preview_file_url': 'https://cdn.donmai.us/preview/93/95/939593fb21e89156e0b44dfcc08207df.jpg'}]

