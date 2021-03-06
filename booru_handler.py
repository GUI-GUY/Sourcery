from os import getcwd, path # path manipulation
from urllib.request import urlretrieve
from requests import get
#from webbrowser import open_new
from fake_useragent import UserAgent
import global_variables as gv

# https://github.com/uncountablecat/danbooru-grabber
# make sure the folder already exists!
# danbooru_folder = 'D:\All_Files\python\GitHub\Sourcery\Sourcery\dan'

try:
    header = UserAgent().random
except:
    header = "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"

# request json, get urls of pictures and download them
def booru_fetch_illustration(imgid, service, login_dict, comm_error_q=None):
    """
    Request info from danbooru API to given imgid\n
    Return illustration dictionary on success, False otherwise
    """
    try:
        if service == 'Danbooru':
            r = get('https://danbooru.donmai.us/posts/' + str(imgid) + '.json', headers = {"user_agent": header})
        elif service == 'Yandere':
            r = get('https://yande.re/post.json?tags=id:' + str(imgid), headers = {"user_agent": header})
        elif service == 'Konachan':
            r = get('https://konachan.com/post.json?tags=id:' + str(imgid), headers = {"user_agent": header})
        elif service == 'Gelbooru':
            if login_dict["gelbooru_api_key"] != '' or login_dict["gelbooru_user_id"] != '':
                r = get('https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&api_key=' + login_dict["gelbooru_api_key"] + '&user_id=' + login_dict["gelbooru_user_id"] + '&id=' + str(imgid), headers = {"user_agent": header})
            else:
                comm_error_q.put('[Sourcery] Gelbooru requires login')
                return False
        else:
            return False
        illustration = r.json()
        if service == 'Yandere' or service == 'Konachan' or service == 'Gelbooru':
            if 'id' in illustration[0]:
                return illustration[0]
        if 'id' in illustration:
            return illustration
        else:
            comm_error_q.put('[Sourcery] Work not found: ' + str(illustration))
            return False
    except Exception as e:
        print("ERROR [0056] " + str(e))
        if comm_error_q != None:
            comm_error_q.put("[Sourcery] ERROR [0056] " + str(e))
        else:
            print("ERROR [0056] " + str(e))
            #gv.Logger.write_to_log("ERROR [0056] " + str(e))
        #mb.showerror("ERROR [0056]", "ERROR CODE [0056]\nImage data could not be retrieved")
        return False
    
def booru_download(img_name_original, imgid, illustration, service='', comm_error_q=None):
    """
    Downloads given image from Danbooru and renames it properly\n
    Return the new name on success, False otherwise
    """
    if service == '':
        return False
    else:
        if 'file_url' in illustration:
            if 'file_ext' not in illustration:
                illustration['file_ext'] = illustration['file_url'].split('.')[-1]
            try:
                if gv.config[service]['rename'] == '1':
                    new_name = rename(illustration['file_url'].split('/')[-1], service.lower())
                else:
                    dot = img_name_original.rfind('.')
                    if dot != -1:
                        new_name = img_name_original[:dot] + '.' + illustration['file_ext']
                    else:
                        new_name = img_name_original + '.' + illustration['file_ext']
                    new_name = rename(new_name, service.lower())
                #urlretrieve(illustration['file_url'], getcwd() + '/Sourcery/sourced_progress/' + service.lower() + '/' + new_name)
                
                try:
                    r = get(illustration['file_url'], headers = {"user_agent": header})
                except Exception as e:
                    #print("ERROR [0074] " + str(e))
                    if comm_error_q != None:
                        comm_error_q.put("[Sourcery] ERROR [0074] " + str(e))
                    else:
                        print("ERROR [0074] " + str(e))
                
                with open(getcwd() + '/Sourcery/sourced_progress/' + service.lower() + '/' + new_name, 'wb') as outfile:
                    outfile.write(r.content)
                
                return new_name
            except Exception as e:
                #print("ERROR [0057] " + str(e))
                if comm_error_q != None:
                    comm_error_q.put("[Sourcery] ERROR [0057] " + str(e))
                else:
                    print("ERROR [0057] " + str(e))
                    #gv.Logger.write_to_log("ERROR [0057] " + str(e))
                #mb.showerror("ERROR [0057]", "ERROR CODE [0057]\nImage could not be downloaded")
                return False
        return False

def rename(desired_name, service, index=-1, new_name=''):
    if new_name == '':
        if path.isfile(getcwd() + '/Sourcery/sourced_progress/' + service + '/' + desired_name) or path.isdir(getcwd() + '/Sourcery/sourced_progress/' + service + '/' + desired_name):
            index = index+1
            dot = desired_name.rfind('.')
            if dot == -1:
                desired_name = rename_length(desired_name)
                new_name = desired_name + '_' + str(index)
            else:
                pre_name = rename_length(desired_name[:dot])
                new_name = pre_name + '_' + str(index) + desired_name[dot:] 
            return rename(desired_name, service, index, new_name)
    else:
        if path.isfile(getcwd() + '/Sourcery/sourced_progress/' + service + '/' + new_name) or path.isdir(getcwd() + '/Sourcery/sourced_progress/' + service + '/' + new_name):
            index = index+1
            dot = desired_name.rfind('.')
            if dot == -1:
                desired_name = rename_length(desired_name)
                new_name = desired_name + '_' + str(index)
            else:
                pre_name = rename_length(desired_name[:dot])
                new_name = pre_name + '_' + str(index) + desired_name[dot:] 
            return rename(desired_name, service, index, new_name)
        return new_name
    return desired_name

def rename_length(name):
    if len(name) > 170:
        name = name[:165]
    return name

if __name__ == '__main__':
    liste = [5261777, 5265046 , 5261812]
    idx = liste[2]
    a = booru_fetch_illustration(idx, 'Gelbooru')
    #print(a)
    b = booru_download('name', idx, a, 'Gelbooru')
    if b != False:
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

#     a={'id': 3829692, 
# 'created_at': '2020-03-21T07:45:40.020-04:00', 
# 'uploader_id': 131474, 
# 'score': 2, 
# 'source': 'https://www.pixiv.net/fanbox/creator/3211072/post/907906', 
# 'md5': '0054859d8fc89c886926ed24aba7bf0b', 
# 'last_comment_bumped_at': None, 
# 'rating': 'q', 
# 'image_width': 2145, 
# 'image_height': 3000, 
# 'tag_string': '1girl absurdres arms_at_sides bangs bare_shoulders black_camisole black_jacket black_legwear black_shirt black_skirt blurry blush breasts brown_legwear buttons camisole closed_mouth collarbone commentary_request eyebrows_visible_through_hair eyelashes fanbox_reward hair_between_eyes halter_top halterneck haori_iori high-waist_skirt highres invisible_chair jacket large_breasts leather leather_jacket long_hair long_sleeves looking_at_viewer medium_breasts miniskirt nipples off_shoulder one_breast_out one_side_up open_clothes open_jacket original paid_reward pantyhose parted_lips pencil_skirt red_eyes ribbed_shirt shirt shirt_tucked_in sidelocks signature silver_hair simple_background sitting skirt sleeveless sleeveless_shirt solo spaghetti_strap two_side_up very_long_hair wavy_hair white_background white_hair', 
# 'is_note_locked': False, 
# 'fav_count': 5, 
# 'file_ext': 'jpg', 
# 'last_noted_at': None, 
# 'is_rating_locked': False, 
# 'parent_id': 3829691, 
# 'has_children': False, 
# 'approver_id': None, 
# 'tag_count_general': 61, 
# 'tag_count_artist': 1, 
# 'tag_count_character': 0, 
# 'tag_count_copyright': 1, 
# 'file_size': 9362476, 
# 'is_status_locked': False, 
# 'pool_string': '', 
# 'up_score': 2, 
# 'down_score': 0, 
# 'is_pending': False, 
# 'is_flagged': False, 
# 'is_deleted': False, 
# 'tag_count': 68, 
# 'updated_at': '2020-03-21T07:46:14.694-04:00', 
# 'is_banned': False, 
# 'pixiv_id': None, 
# 'last_commented_at': None, 
# 'has_active_children': False, 
# 'bit_flags': 2, 
# 'tag_count_meta': 5, 
# 'has_large': True, 
# 'has_visible_children': False, 
# 'is_favorited': False, 
# 'tag_string_general': '1girl arms_at_sides bangs bare_shoulders black_camisole black_jacket black_legwear black_shirt black_skirt blurry blush breasts brown_legwear buttons camisole closed_mouth collarbone eyebrows_visible_through_hair eyelashes hair_between_eyes halter_top halterneck high-waist_skirt invisible_chair jacket large_breasts leather leather_jacket long_hair long_sleeves looking_at_viewer medium_breasts miniskirt nipples off_shoulder one_breast_out one_side_up open_clothes open_jacket pantyhose parted_lips pencil_skirt red_eyes ribbed_shirt shirt shirt_tucked_in sidelocks signature silver_hair simple_background sitting skirt sleeveless sleeveless_shirt solo spaghetti_strap two_side_up very_long_hair wavy_hair white_background white_hair', 
# 'tag_string_character': '', 
# 'tag_string_copyright': 'original', 
# 'tag_string_artist': 'haori_iori', 
# 'tag_string_meta': 'absurdres commentary_request fanbox_reward highres paid_reward', 
# 'file_url': 'https://danbooru.donmai.us/data/0054859d8fc89c886926ed24aba7bf0b.jpg', 
# 'large_file_url': 'https://danbooru.donmai.us/data/sample/sample-0054859d8fc89c886926ed24aba7bf0b.jpg', 
# 'preview_file_url': 'https://cdn.donmai.us/preview/00/54/0054859d8fc89c886926ed24aba7bf0b.jpg'}

#     b={'id': 3829556, 
# 'created_at': '2020-03-21T04:53:15.811-04:00', 
# 'uploader_id': 515384, 
# 'score': 2, 
# 'source': 'https://twitter.com/haori_crescendo/status/1241285803747102720', 
# 'md5': 'cc09a5986a8ae6b77eeb8c9b5c348ea3', 
# 'last_comment_bumped_at': None, 
# 'rating': 's', 
# 'image_width': 858, 
# 'image_height': 1200, 
# 'tag_string': '1girl bare_shoulders black_jacket black_shirt black_skirt blurry breasts brown_legwear camisole cleavage collarbone commentary_request haori_iori high-waist_skirt highres invisible_chair jacket large_breasts leather leather_jacket long_hair looking_at_viewer miniskirt off_shoulder one_side_up open_clothes open_jacket original pantyhose parted_lips pencil_skirt red_eyes ribbed_shirt shirt shirt_tucked_in signature silver_hair simple_background sitting skirt sleeveless sleeveless_shirt solo spaghetti_strap white_background', 
# 'is_note_locked': False, 
# 'fav_count': 9, 
# 'file_ext': 'jpg', 
# 'last_noted_at': None, 
# 'is_rating_locked': False, 
# 'parent_id': 3829691, 
# 'has_children': False, 
# 'approver_id': None, 
# 'tag_count_general': 41, 'tag_count_artist': 1, 'tag_count_character': 0, 'tag_count_copyright': 1, 'file_size': 181978, 'is_status_locked': False, 'pool_string': '', 'up_score': 2, 'down_score': 0, 'is_pending': False, 'is_flagged': False, 'is_deleted': False, 'tag_count': 45, 'updated_at': '2020-03-21T07:46:37.019-04:00', 'is_banned': False, 'pixiv_id': None, 'last_commented_at': None, 'has_active_children': False, 'bit_flags': 2, 'tag_count_meta': 2, 'has_large': True, 'has_visible_children': False, 'is_favorited': False, 'tag_string_general': '1girl bare_shoulders black_jacket black_shirt black_skirt blurry breasts brown_legwear camisole cleavage collarbone high-waist_skirt invisible_chair jacket large_breasts leather leather_jacket long_hair looking_at_viewer miniskirt off_shoulder one_side_up open_clothes open_jacket pantyhose parted_lips pencil_skirt red_eyes ribbed_shirt shirt shirt_tucked_in signature silver_hair simple_background sitting skirt sleeveless sleeveless_shirt solo spaghetti_strap white_background', 'tag_string_character': '', 'tag_string_copyright': 'original', 'tag_string_artist': 'haori_iori', 'tag_string_meta': 'commentary_request highres', 'file_url': 'https://danbooru.donmai.us/data/cc09a5986a8ae6b77eeb8c9b5c348ea3.jpg', 'large_file_url': 'https://danbooru.donmai.us/data/sample/sample-cc09a5986a8ae6b77eeb8c9b5c348ea3.jpg', 
# 'preview_file_url': 'https://cdn.donmai.us/preview/cc/09/cc09a5986a8ae6b77eeb8c9b5c348ea3.jpg'}

#     c={'id': 3829691, 
# 'created_at': '2020-03-21T07:45:12.336-04:00', 
# 'uploader_id': 131474, 
# 'score': 3, 
# 'source': 'https://www.pixiv.net/fanbox/creator/3211072/post/907915', 
# 'md5': '3fd3c3d3a19fecb726d3a6ec92325532', 
# 'last_comment_bumped_at': None, 
# 'rating': 's', 
# 'image_width': 2145, 
# 'image_height': 3000, 
# 'tag_string': '1girl absurdres arms_at_sides bangs bare_shoulders black_camisole black_jacket black_legwear black_shirt black_skirt blurry blush breasts brown_legwear buttons camisole cleavage collarbone commentary_request eyebrows_visible_through_hair eyelashes fanbox_reward hair_between_eyes halter_top halterneck haori_iori high-waist_skirt highres huge_filesize invisible_chair jacket large_breasts leather leather_jacket long_hair long_sleeves looking_at_viewer medium_breasts miniskirt off_shoulder one_side_up open_clothes open_jacket original paid_reward pantyhose parted_lips pencil_skirt red_eyes ribbed_shirt shirt shirt_tucked_in sidelocks signature silver_hair simple_background sitting skirt sleeveless sleeveless_shirt solo spaghetti_strap two_side_up very_long_hair wavy_hair white_background white_hair', 
# 'is_note_locked': False, 
# 'fav_count': 3, 
# 'file_ext': 'png', 
# 'last_noted_at': None, 
# 'is_rating_locked': False, 
# 'parent_id': None, 
# 'has_children': True, 
# 'approver_id': None, 
# 'tag_count_general': 59, 
# 'tag_count_artist': 1, 
# 'tag_count_character': 0, 
# 'tag_count_copyright': 1, 
# 'file_size': 11816684, 
# 'is_status_locked': False, 
# 'pool_string': '', 
# 'up_score': 3, 
# 'down_score': 0, 
# 'is_pending': False, 
# 'is_flagged': False, 
# 'is_deleted': False, 
# 'tag_count': 67, 
# 'updated_at': '2020-03-21T07:46:01.433-04:00', 
# 'is_banned': False, 
# 'pixiv_id': None, 
# 'last_commented_at': None, 
# 'has_active_children': True, 
# 'bit_flags': 2, 
# 'tag_count_meta': 6, 
# 'has_large': True, 
# 'has_visible_children': True, 
# 'is_favorited': False, 
# 'tag_string_general': '1girl arms_at_sides bangs bare_shoulders black_camisole black_jacket black_legwear black_shirt black_skirt blurry blush breasts brown_legwear buttons camisole cleavage collarbone eyebrows_visible_through_hair eyelashes hair_between_eyes halter_top halterneck high-waist_skirt invisible_chair jacket large_breasts leather leather_jacket long_hair long_sleeves looking_at_viewer medium_breasts miniskirt off_shoulder one_side_up open_clothes open_jacket pantyhose parted_lips pencil_skirt red_eyes ribbed_shirt shirt shirt_tucked_in sidelocks signature silver_hair simple_background sitting skirt sleeveless sleeveless_shirt solo spaghetti_strap two_side_up very_long_hair wavy_hair white_background white_hair', 
# 'tag_string_character': '', 
# 'tag_string_copyright': 'original', 
# 'tag_string_artist': 'haori_iori', 
# 'tag_string_meta': 'absurdres commentary_request fanbox_reward highres huge_filesize paid_reward', 
# 'file_url': 'https://danbooru.donmai.us/data/3fd3c3d3a19fecb726d3a6ec92325532.png', 
# 'large_file_url': 'https://danbooru.donmai.us/data/sample/sample-3fd3c3d3a19fecb726d3a6ec92325532.jpg', 
# 'preview_file_url': 'https://cdn.donmai.us/preview/3f/d3/3fd3c3d3a19fecb726d3a6ec92325532.jpg'}