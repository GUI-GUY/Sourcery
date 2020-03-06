#!/usr/bin/python
#coding:utf-8

import os # path manipulation
import urllib
import requests
from webbrowser import open_new
import global_variables as gv

status = 'not done yet'

# https://github.com/uncountablecat/danbooru-grabber
# change this to your danbooru folder
# it might look something like this: '/users/YourUserName/DanbooruPics'
# make sure the folder already exists!
danbooru_folder = 'D:\All_Files\python\GitHub\Sourcery\Sourcery\dan'

# generate tag argument to be used in url and folder creation


# request json, get urls of pictures and download them
def grabber(tag_argv,page_num):
    r = requests.get('https://danbooru.donmai.us/posts.json?tags='+tag_argv+'&page='+str(page_num))
    streams = r.json()
    #print(streams)
    # check if all pages have been visited
    print(streams)
    tag_argv = 'explicits'
    # check if directory already exists
    if (os.path.exists(danbooru_folder + '/' + tag_argv) == False):
        os.mkdir(danbooru_folder + '/' + tag_argv)

    url = []
    for post in streams:
        if 'file_url' in post:
            url.append(post['file_url'])

    print(url)
    # download
    for address in url:
        #open_new(address)
        urllib.request.urlretrieve(address, danbooru_folder + '/' + tag_argv + '/' + address.split('/')[-1])


def main():
    # page_num = input('Enter the number of pages you want to download. To download all, simply enter a super large number:')
    # taginput = input('Enter tags,separated by space:') 

    page_num = 3
    taginput = 'uncensored flat_chest'
    n = 1
    while n <= int(page_num) and status == 'not done yet':
        tagList = taginput.split(' ')
        tag_argv = generate_tag_argv(tagList)
        grabber(tag_argv,n)
        n = n + 1

    print('Download successful!')
    u2 = u'どうぞ、召し上がってください！'
    print(u2)


if __name__ == '__main__':
    main()


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

