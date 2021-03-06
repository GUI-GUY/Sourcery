from os import getcwd, path
from multiprocessing import Semaphore
from configparser import ConfigParser
from copy import copy
from time import strftime
import logging as log
from Files import Files
from Logger import Logger
# Every variable that can be "outmoduled" and appears in at least two modules

def init_config():

    config.add_section('Original')
    config.add_section('Pixiv')
    config.add_section('Danbooru')
    config.add_section('Yandere')
    config.add_section('Konachan')
    config.add_section('Gelbooru')
    config.add_section('Weight')
    config.add_section('SauceNAO')
    config.add_section('Sourcery')
    config.add_section('Debug')
    
    config['Weight'] = {
        "png" : '10',
        "jpg" : '7',
        "jfif" : '1',
        "gif" : '10',
        "bmp" : '5',
        "other" : '0',
        "higher_resolution" : '10',
        "pixiv" : '8',
        "danbooru" : '10',
        "yandere" : '5',
        "konachan" : '5',
        "gelbooru" : '5',
        "original" : '5'
    }
    
    config['SauceNAO'] = {
        "api_key" : '',
        "minsim" : '80',
        "returns" : '10',
        "depth" : '128',
        "bias" : '15',
        "biasmin" : '70'
    }

    config['Sourcery'] = {
        "imgpp" : '12',
        "input_dir" : cwd + '/Input',
        "output_dir" : cwd + '/Output',
        "delete_input" : '0',
        "direct_replace" : '100',
        "input_search_depth" : '1'
    }

    config['Original'] = {
        "single_source_in_tagfile" : '0'
    }

    config['Debug'] = {
        "show" : '0',
        "code" : ''
    }

    if path.isfile(cwd + '/Sourcery/config.cfg'):
        config.read_file(open(cwd + '/Sourcery/config.cfg'))#TODO
    
    write_config()

def write_config():
    config.write(open(cwd + '/Sourcery/config.cfg', 'w'))#TODO

cwd = getcwd()
Files = Files()
Logger = Logger()
Startpage_Class = None
default_dict = {"rename":'0', "tags":'', "gen_tagfile":'0', "tagfile_pixiv":'0', "tagfile_danbooru":'0', "tagfile_yandere":'0', "tagfile_konachan":'0', "tagfile_gelbooru":'0', "direct_replace":'0', "use":'1', "jump_log":'1', "api_key":'', "user_id":''}
config = ConfigParser(defaults=default_dict)
init_config()
input_dir = config['Sourcery']['input_dir']
output_dir = config['Sourcery']['output_dir']


width = 0
height = 0
res_frame = None # ScrollFrame for results to put widgets in
big_frame = None # ScrollFrame for big selector to put widgets in
info_frame = None # ScrollFrame for info to put widgets in
res_frame_height = None
res_frame_width = None
big_frame_height = None
big_frame_width = None
info_frame_height = None
info_frame_width = None
window = None
big_selector_frame = None
big_selector_canvas = None
display_startpage = None
log_text = None
info_ScrollFrame = None

last_occupied_result = 0
imgpp_sem = Semaphore(config.getint('Sourcery', 'imgpp'))
img_data_sem = Semaphore(50)

# global lists
services = ["pixiv", "danbooru", "yandere", "konachan", "gelbooru"]
delete_dirs_array = list() # For empty directories or dirs where no original is present
img_data_array = list() # For all ImageData instances
results_tags_danbooru = config['Danbooru']['tags'].split()
results_tags_pixiv = config['Pixiv']['tags'].split()
results_tags_yandere = config['Yandere']['tags'].split()
results_tags_konachan = config['Konachan']['tags'].split()
results_tags_gelbooru = config['Gelbooru']['tags'].split()

def class_parallel_loader(method):
    method()

# COLORS = ['white', 'snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
#     'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
#     'navajo white', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'burlywood1', 'burlywood2', 
#     'burlywood3', 'burlywood4', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
#     'lavender blush', 'misty rose', 'snow2', 'snow3',
#     'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
#     'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
#     'PeachPuff3', 'PeachPuff4',
#     'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
#     'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
#     'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
#     'MistyRose4', 'wheat1', 
#     'wheat2', 'wheat3', 'wheat4','thistle', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 
#     'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
#     'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
#     'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
#     'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
#     'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'azure2', 'azure3', 
#     'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
#     'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
#     'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
#     'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
#     'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
#     'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
#     'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
#     'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
#     'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
#     'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
#     'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
#     'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
#     'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
#     'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
#     'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
#     'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
#     'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
#     'DarkOliveGreen3', 'DarkOliveGreen4', 'green', 'dark green', 'dark olive green',
#     'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
#     'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
#     'forest green', 'olive drab', 'dark khaki', 'khaki', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 
#     'pale goldenrod', 'light goldenrod yellow', 'light yellow',
#     'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow', 'yellow2', 'yellow3', 
#     'yellow4', 'gold', 'gold2', 'gold3', 'gold4', 'light goldenrod', 
#     'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 
#     'goldenrod', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'dark goldenrod',
#     'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'rosy brown',
#     'indian red', 'saddle brown', 'sandy brown',
#     'dark salmon', 'salmon', 'light salmon', 'orange', 'orange2',
#     'orange3', 'orange4', 'dark orange', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'OrangeRed2',
#     'OrangeRed3', 'OrangeRed4',
#     'coral', 'coral1', 'coral2', 'coral3', 'coral4', 'light coral', 'tomato', 'orange red', 'red', 'red2', 'red3', 'red4', 'hot pink',
#     'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'deep pink', 'DeepPink2', 'DeepPink3', 'DeepPink4', 
#     'pink', 'pink1', 'pink2', 'pink3', 'pink4', 'light pink',
#     'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4',
#     'pale violet red', 'PaleVioletRed1',
#     'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon', 'medium violet red', 'violet red', 
#     'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
#     'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple',
#     'purple1', 'purple2', 'purple3', 'purple4', 'medium purple', 'MediumPurple1', 'MediumPurple2',
#     'MediumPurple3', 'MediumPurple4',
#     'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
#     'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'tan1',
#     'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
#     'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
#     'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4',
#     'tomato2', 'tomato3', 'tomato4', 'maroon1', 'maroon2',
#     'maroon3', 'maroon4', 'magenta',  
#     'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
#     'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
#     'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'black',
#     'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
#     'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
#     'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
#     'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
#     'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
#     'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
#     'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
#     'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
#     'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
#     'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
#     'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99', 'dark slate gray', 'dim gray', 'slate gray',
#     'light slate gray', 'gray', 'light grey']

# MAX_ROWS = 36
# FONT_SIZE = 10 # (pixels)

# root = Tk()
# root.title("Named colour chart")
# row = 0
# col = 0
# for color in COLORS:
# e = Label(root, text=color, background=color, 
#         font=(None, -FONT_SIZE))
# e.grid(row=row, column=col, sticky=E+W)
# row += 1
# if (row > 36):
#     row = 0
#     col += 1

# root.mainloop()
