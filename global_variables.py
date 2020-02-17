from os import getcwd
from Files import Files
# Every variable that can be "outmoduled" and appears in at least two modules

cwd = getcwd()
Files = Files()

frame = None
frame2 = None
frame3 = None
window = None
big_selector_frame = None
big_selector_canvas = None
display_view_results = None

esc_op = False
width = 0
height = 0

# global arrays
input_images_array = [] # For all images in Input folder
delete_dirs_array = [] # For empty directories or dirs where no original is present
img_data_array = [] # For all ImageData instances