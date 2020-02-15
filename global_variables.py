from os import getcwd
from Files import Files
# Every variable that can be "outmoduled" and appears in at least two modules

cwd = getcwd()
Files = Files()

frame = None

esc_op = False
#current_theme = 'Dark Theme'
width = 0
height = 0

# global arrays
input_images_array = [] # For all images in Input folder
#pixiv_images_array = [] # For all images in sourced_progress/pixiv folder
safe_to_show_array = [] # For all images that are fully downloaded
delete_dirs_array = [] # For empty directories or dirs where no original is present
chkbtn_vars_big_array = [] # [[imgname, (img, IntVar), (img, IntVar) ...]...]
chkbtn_vars_array = [] # 12x2 Checkbutton variables for the results screen
big_ref_array = [] # reference for all big selector widgets
results_12_tuple_widgets_array = [] # [([original_chkbtn, original_lbl, original_wxh_lbl, original_type_lbl, cropped_name_lbl], [downloaded_chkbtn, downloaded_lbl, downloaded_wxh_lbl, downloaded_type_lbl, big_selector_btn]), ([], []), ...]

img_data_array = []