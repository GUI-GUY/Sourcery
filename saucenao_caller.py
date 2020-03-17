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

def get_response(image_name, cwd, api_key, minsim, comm_error_q=None):#minsim='80!'
    """
    Request information from SauceNao on the given image
    Returns a List with a status code indicated success or which failure, a message for the user and information on the search limit
    """
    if api_key == None or api_key == '':
        return [403, 'Incorrect or Invalid API Key!\nGo to Options->SauceNao->SauceNao API-Key and insert a Key']
    try:
        image = Image.open(cwd + '/Sourcery/sourced_original/' + image_name)
    except Exception as e:
        print('ERROR [0019] ' + str(e))
        if comm_error_q != None:
            comm_error_q.put('[Sourcery] ERROR [0019] ' + str(e))
        else:
            gv.Files.Log.write_to_log('ERROR [0019] ' + str(e))
        #mb.showerror("ERROR CODE [0015]\nSomething went wrong while opening the image " + image_name)
        return [401, 'Something went wrong while opening the image ' + image_name]
    image = image.convert('RGB')
    image.thumbnail(thumbSize, resample=Image.ANTIALIAS)
    imageData = BytesIO()
    image.save(imageData,format='PNG')
    
    if True:
        #enable or disable indexes
        index_hmags='0'
        index_reserved='0'
        index_hcg='0'
        index_ddbobjects='0'
        index_ddbsamples='0'
        index_pixiv=gv.Files.Conf.use_pixiv
        index_pixivhistorical='0'
        index_reserved='0'
        index_seigaillust='0'
        index_danbooru=gv.Files.Conf.use_danbooru
        index_drawr='0'
        index_nijie='0'
        index_yandere='0'#TODO danbooru
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
        index_konachan='0'#TODO danbooru
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
        #db_count = 10# int(index_mangadex)+int(index_madokami)+int(index_pawoo)+int(index_da)+int(index_portalgraphics)+int(index_bcycosplay)+int(index_bcyillust)+int(index_idolcomplex)+int(index_e621)+int(index_animepictures)+int(index_sankaku)+int(index_konachan)+int(index_gelbooru)+int(index_shows)+int(index_movies)+int(index_hanime)+int(index_anime)+int(index_medibang)+int(index_2dmarket)+int(index_hmisc)+int(index_fakku)+int(index_shutterstock)+int(index_reserved)+int(index_animeop)+int(index_yandere)+int(index_nijie)+int(index_drawr)+int(index_danbooru)+int(index_seigaillust)+int(index_anime)+int(index_pixivhistorical)+int(index_pixiv)+int(index_ddbsamples)+int(index_ddbobjects)+int(index_hcg)+int(index_hanime)+int(index_hmags)

    url = 'http://saucenao.com/search.php?output_type=2&minsim='+minsim+'!&dbmask='+str(db_bitmask)+'&api_key='+api_key+'&numres='+gv.Files.Conf.saucenao_returns+'&depth='+gv.Files.Conf.saucenao_depth+'&bias='+gv.Files.Conf.saucenao_bias+'&biasmin='+gv.Files.Conf.saucenao_biasmin
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
    #print(results)
    return [200, results, results['header']['short_remaining'], results['header']['long_remaining'], results['header']['long_limit']]

def decode_response(results, EnableRename=False):
    """
    Returns a list of dictionaries with:\n
    service - pixiv/danbooru or '' if failure\n
    illust_id - 0 if failure\n
    member_id - negative if failure\n
    source_url - '' if failure\n
    """
    # print(results)
    
    if int(results['header']['results_returned']) > 0:
        #one or more results were returned
        #get vars to use
        service_name = ''
        illust_id = 0
        member_id = -1
        
        # index_id = results['results'][0]['header']['index_id']
        # page_string = ''
        # page_match = search('(_p[\d]+)\.', results['results'][0]['header']['thumbnail'])
        # if page_match:
        #     page_string = page_match.group(1)
        source = ''
        ret_dict = list()

        # print('results')
        # print(results)
        for elem in results['results']:
            if float(elem['header']['similarity']) >= float(results['header']['minimum_similarity']):
                # print('hit! '+str(elem['header']['similarity']))
                # print('minsim! '+str(results['header']['minimum_similarity']))
                if elem['header']['index_id'] == 5 or elem['header']['index_id'] == 6:
                    #5->pixiv 6->pixiv historical
                    service_name='Pixiv'
                    member_id = elem['data']['member_id']
                    illust_id = elem['data']['pixiv_id']
                    source = elem['data']['ext_urls']
                    ret_dict.append({"service_name": service_name, "member_id": member_id, "illust_id": illust_id, "source": source, "similarity": float(elem['header']['similarity'])})
                    # print(source)
                elif elem['header']['index_id'] == 9:
                    #9->danbooru
                    service_name='Danbooru'
                    illust_id = elem['data']['danbooru_id']
                    source = elem['data']['ext_urls']
                    ret_dict.append({"service_name": service_name, "illust_id": illust_id, "source": source, "similarity": float(elem['header']['similarity'])})
                else:
                    ret_dict.append({"service_name": service_name, "member_id": member_id, "illust_id": illust_id, "source": source, "similarity": float(elem['header']['similarity'])})
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
                #         newfname = os.path.join(cwd + '/Output/', service_name+'_'+str(member_id)+'_'+str(illust_id)+page_string+'.'+fname.split(".")[-1].lower())
                #     else:
                #         newfname = os.path.join(cwd + '/Output/', service_name+'_'+str(illust_id)+page_string+'.'+fname.split(".")[-1].lower())
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
    
        return ret_dict# [service_name, illust_id, member_id, source, results['header']['minimum_similarity']]
    return[{"service_name": '', "member_id": 0, "illust_id": -1, "source": '', "similarity": 0.0}]
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

# OrderedDict([('header', OrderedDict([('user_id', '32608'), ('account_type', '1'), ('short_limit', '6'), ('long_limit', '200'), ('long_remaining', 193), ('short_remaining', 5), ('status', 0), ('results_requested', 2), 
# ('index', 
# OrderedDict(
#     [('5', OrderedDict([('status', 0), ('parent_id', 5), ('id', 5), ('results', 2)])), 
#     ('51', OrderedDict([('status', 0), ('parent_id', 5), ('id', 51), ('results', 2)])), 
#     ('52', OrderedDict([('status', 0), ('parent_id', 5), ('id', 52), ('results', 2)])), 
#     ('53', OrderedDict([('status', 0), ('parent_id', 5), ('id', 53), ('results', 2)])), 
#     ('9', OrderedDict([('status', 0), ('parent_id', 9), ('id', 9), ('results', 2)]))])), 
#     ('search_depth', '128'), 
#     ('minimum_similarity', 35.33), 
#     ('query_image_display', 'userdata/Vgd1ZzlH4.png.png'), 
#     ('query_image', 'Vgd1ZzlH4.png'), ('results_returned', 2)])), 
    
#     ('results', 
#     [OrderedDict(
#         [('header', OrderedDict(
#             [('similarity', '95.50'), 
#             ('thumbnail', 'https://img1.saucenao.com/res/pixiv/7690/76900548_p0_master1200.jpg?auth=AKizfJXBfY--Hayju-eldw&exp=1583964983'), 
#             ('index_id', 5), 
#             ('index_name', 'Index #5: Pixiv Images - 76900548_p0_master1200.jpg')])), 
#             ('data', Or548_p0_master1200.jpg')])),
#             ('data', OrderedDict(
#                 [('ext_urls', ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=76900548']), 
#                 ('title', 'FGO-ド0548), 
#                 ('member_name', 'ミツ'), 
#                 ('membeアを開けないで！！'), 
#                 ('pixiv_id', 76900548), 
#                 ('member_name', 'ミツ'), 
#                 ('member_id', 3433634)]))]), 
#     OrderedDict(
#         [('header', OrderedDict(
#             [('similarity', '92.9e421c6ce77_0.jpg'), 
#             ('index_id', 9), ('7'), 
#             ('thumbnail', 'https://img3.saucenao.com/booru/7/c/7c74656676876eac14c979e421c6ce77_0.jpg'), 
#             ('index_id', 9), 
#             ('index_name', 'Index #9: Danbooru - 7c7464859']), 
#             ('danbooru_id', 3634859), 
#             ('cr56676876eac14c979e421c6ce77_0.jpg')])), 
#             ('data', OrderedDict([('ext_urls', ['https://danbooru.donmai.us/post/show/3634859']), 
#             ('danbooru_id', 3634859), 
#             ('cre (fate), bradamante (fate/grand order),ator', 'wei yu'), 
#             ('material', 'fate/grand order, fate (series), pixiv'), 
#             ('characters', 'artoria pendragon (all), bb (fate) (all), bb (swimsuit mooncancer) ri (fate/grand order), nitocris (fate/g(fate), bradamante (fate/grand order), caster, caster (fate/zero), fergus mac roich (fate/grand order), hildr (fate/grand order), jack the ripper (fate/apocrmo (fate) (all), tamamo no mae (fate), ypha), jekyll and hyde (fate), mata hari (fate/grand order), nitocris (fate/grand order), ortlinde (fate/grand order), osakabe-hime (fate/grand order), penthesilea (fate/grand order), santa alter, shuten douji (fate/grand order), tamamo (fate) (all), tamamo no mae (fate), thrud (fate/grand order), valkyrie (fate/grand order)'), 
#             ('source', 'https://i.pximg.net/img-original/img/2019/09/22/01/08/22/76900548')]))])])])