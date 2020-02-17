#from sys import stdout, stderr
#from os import path, rename
from io import BytesIO
#import unicodedata
from requests import post
from PIL import Image
from json import JSONDecoder
#from codecs import getwriter
from re import search
#import time
from collections import OrderedDict
import global_variables as gv
#from pixiv_handler import pixiv_download
#from file_operations import write_to_log
# stdout = getwriter('utf8')(stdout.detach())
# stderr = getwriter('utf8')(stderr.detach())

thumbSize = (250,250)

if True:
    #enable or disable indexes
    index_hmags='0'
    index_reserved='0'
    index_hcg='0'
    index_ddbobjects='0'
    index_ddbsamples='0'
    index_pixiv='1'
    index_pixivhistorical='0'
    index_reserved='0'
    index_seigaillust='0'
    index_danbooru='0'
    index_drawr='0'
    index_nijie='0'
    index_yandere='0'
    index_animeop='0'
    index_reserved='0'
    index_shutterstock='0'
    index_fakku='0'
    index_hmisc='0'
    index_2dmarket='0'
    index_medibang='0'
    index_anime='0'
    index_hanime='0'
    index_movies='0'
    index_shows='0'
    index_gelbooru='0'
    index_konachan='0'
    index_sankaku='0'
    index_animepictures='0'
    index_e621='0'
    index_idolcomplex='0'
    index_bcyillust='0'
    index_bcycosplay='0'
    index_portalgraphics='0'
    index_da='0'
    index_pawoo='0'
    index_madokami='0'
    index_mangadex='0'

#generate appropriate bitmask
db_bitmask = int(index_mangadex+index_madokami+index_pawoo+index_da+index_portalgraphics+index_bcycosplay+index_bcyillust+index_idolcomplex+index_e621+index_animepictures+index_sankaku+index_konachan+index_gelbooru+index_shows+index_movies+index_hanime+index_anime+index_medibang+index_2dmarket+index_hmisc+index_fakku+index_shutterstock+index_reserved+index_animeop+index_yandere+index_nijie+index_drawr+index_danbooru+index_seigaillust+index_anime+index_pixivhistorical+index_pixiv+index_ddbsamples+index_ddbobjects+index_hcg+index_hanime+index_hmags,2)

def get_response(image, cwd, api_key, minsim):#minsim='80!'
    if api_key == None or api_key == '':
        return [403, 'Incorrect or Invalid API Key!\nGo to Options->SauceNao->SauceNao API-Key and insert a Key']
    try:
        image = Image.open(cwd + '/Sourcery/sourced_original/' + image)
    except Exception as e:
        print('ERROR [0019] ' + str(e))
        gv.Files.Log.write_to_log('ERROR [0019] ' + str(e))
        #mb.showerror("ERROR CODE [0015]\nSomething went wrong while opening the image " + image)
        return [401, 'Something went wrong while opening the image ' + image]
    image = image.convert('RGB')
    image.thumbnail(thumbSize, resample=Image.ANTIALIAS)
    imageData = BytesIO()
    image.save(imageData,format='PNG')
    
    url = 'http://saucenao.com/search.php?output_type=2&numres=1&minsim='+minsim+'&dbmask='+str(db_bitmask)+'&api_key='+api_key
    files = {'file': ("image.png", imageData.getvalue())}
    imageData.close()
    
    
    r = post(url, files=files)
    if r.status_code != 200:
        if r.status_code == 403:
            return [403, 'Incorrect or Invalid API Key!\nGo to Options->SauceNao->SauceNao API-Key and insert a Key']
        else:
            #generally non 200 statuses are due to either overloaded servers or the user is out of searches
            return [2, "status code: "+str(r.status_code)]
    else:
        results = JSONDecoder(object_pairs_hook=OrderedDict).decode(r.text)
        if int(results['header']['user_id'])>0:
            #api responded
            #print('Remaining Searches 30s|24h: '+str(results['header']['short_remaining'])+'|'+str(results['header']['long_remaining']))
            if int(results['header']['status'])>0:
                #One or more indexes are having an issue.
                #This search is considered partially successful, even if all indexes failed, so is still counted against your limit.
                #The error may be transient, but because we don't want to waste searches, allow time for recovery.
                return [600, 'API Error.', results['header']['short_remaining'], results['header']['long_remaining']]
            elif int(results['header']['status'])<0:
                #Problem with search as submitted, bad image, or impossible request.
                #Issue is unclear, so don't flood requests.
                return [41, 'Bad image or other request error.', results['header']['short_remaining'], results['header']['long_remaining']]
        else:
            #General issue, api did not respond. Normal site took over for this error state.
            #Issue is unclear, so don't flood requests.
            return [402, 'Bad image, or API failure.']

    return [200, results, results['header']['short_remaining'], results['header']['long_remaining']]

def decode_response(results, EnableRename=False):
    """
    Returns a list:\n
    [0]service - pixiv or '' if failure\n
    [1]illust_id - 0 if failure\n
    [2]member_id - negative if failure\n
    [3]source_url - '' if failure\n
    """
    # print(results)
    
    if int(results['header']['results_returned']) > 0:
        #one or more results were returned
        if float(results['results'][0]['header']['similarity']) > float(results['header']['minimum_similarity']):
            # print('hit! '+str(results['results'][0]['header']['similarity']))

            #get vars to use
            service_name = ''
            illust_id = 0
            member_id = -1
            index_id = results['results'][0]['header']['index_id']
            page_string = ''
            page_match = search('(_p[\d]+)\.', results['results'][0]['header']['thumbnail'])
            source = ''
            if page_match:
                page_string = page_match.group(1)
                
            if index_id == 5 or index_id == 6:
                #5->pixiv 6->pixiv historical
                service_name='pixiv'
                member_id = results['results'][0]['data']['member_id']
                illust_id = results['results'][0]['data']['pixiv_id']
                source = results['results'][0]['data']['ext_urls']
                # print(source)
            # elif index_id == 8:
            #     #8->nico nico seiga
            #     service_name='seiga'
            #     member_id = results['results'][0]['data']['member_id']
            #     illust_id = results['results'][0]['data']['seiga_id']
            # elif index_id == 10:
            #     #10->drawr
            #     service_name='drawr'
            #     member_id = results['results'][0]['data']['member_id']
            #     illust_id = results['results'][0]['data']['drawr_id']								
            # elif index_id == 11:
            #     #11->nijie
            #     service_name='nijie'
            #     member_id = results['results'][0]['data']['member_id']
            #     illust_id = results['results'][0]['data']['nijie_id']
            # elif index_id == 34:
            #     #34->da
            #     service_name='da'
            #     illust_id = results['results'][0]['data']['da_id']
            # else:
            #     #unknown
            #     #print('Unhandled Index! Exiting...')
            #     #sys.exit(2)
                
            # try:
            #     if member_id >= 0:
            #         newfname = os.path.join(cwd + '/Sourced/', service_name+'_'+str(member_id)+'_'+str(illust_id)+page_string+'.'+fname.split(".")[-1].lower())
            #     else:
            #         newfname = os.path.join(cwd + '/Sourced/', service_name+'_'+str(illust_id)+page_string+'.'+fname.split(".")[-1].lower())
            #     print('New Name: '+newfname)
            #     if EnableRename:
            #         os.rename(fname, newfname)
            # except Exception as e:
            #     print(str(e))
            #     sys.exit(3)
            
        # else:
        #     print('miss... '+str(results['results'][0]['header']['similarity']))

        # if int(results['header']['long_remaining'])<1: #could potentially be negative
        #     #print('Out of searches for today. Sleeping for 6 hours...')
        #     time.sleep(6*60*60)
        # if int(results['header']['short_remaining'])<1:
        #     #print('Out of searches for this 30 second period. Sleeping for 25 seconds...')
        #     time.sleep(25)
    
            return [service_name, illust_id, member_id, source]
    return['', 0, -1, '']
    #print('All Done!')

    # OrderedDict([('header', 
    #   OrderedDict([
    #       ('user_id', '32608'), 
    #       ('account_type', '1'), 
    #       ('short_limit', '6'), 
    #       ('long_limit', '200'), 
    #       ('long_remaining', 198), 
    #       ('short_remaining', 5), 
    #       ('status', 0), 
    #       ('results_requested', 1), 
    #       ('index', 
    #           OrderedDict([('5', 
    #               OrderedDict([
    #                   ('status', 0), 
    #                   ('parent_id', 5), 
    #                   ('id', 5), 
    #                   ('results', 1)])), 
    #       ('51', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 5), 
    #               ('id', 51), 
    #               ('results', 1)])), 
    #       ('52', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 5), 
    #               ('id', 52), 
    #               ('results', 1)])), 
    #       ('53', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 5), 
    #               ('id', 53), 
    #               ('results', 1)])), 
    #       ('6', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 6), 
    #               ('id', 6), 
    #               ('results', 1)])), 
    #       ('8', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 8), 
    #               ('id', 8), 
    #               ('results', 1)])), 
    #       ('10', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 10), 
    #               ('id', 10), 
    #               ('results', 1)])), 
    #       ('11', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 11), 
    #               ('id', 11), 
    #               ('results', 1)])), 
    #       ('34', 
    #           OrderedDict([
    #               ('status', 0), 
    #               ('parent_id', 34), 
    #               ('id', 34), 
    #               ('results', 1)]))])), 
    #   ('search_depth', '128'), 
    #   ('minimum_similarity', 80), 
    #   ('query_image_display', 'userdata/xaOlyeO2O.png.png'), 
    #   ('query_image', 'xaOlyeO2O.png'), 
    #   ('results_returned', 1)])), 
    # ('results', 
    # [OrderedDict([
    # ('header', OrderedDict([
    #   ('similarity', '94.29'), 
    #   ('thumbnail', 'https://img1.saucenao.com/res/pixiv/1945/19455311_s.jpg?auth=qq9sB6Bl50wH2DyH9NHJHw&exp=1577906473'), 
    #   ('index_id', 5), 
    #   ('index_name', 'Index #5: Pixiv Images - 19455311_s.jpg')])), 
    # ('data', OrderedDict([
    #   ('ext_urls', ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=19455311']), 
    #   ('title', '流氷'), 
    #   ('pixiv_id', 19455311), 
    #   ('member_name', 'ke-ta'), 
    #   ('member_id', 3104565)]))])])])