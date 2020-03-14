from os import startfile
#from tkinter import messagebox as mb
from tkinter import filedialog as fd
import global_variables as gv

def is_image(img):
    """
    Returns True if the given images ends with one of the following image suffixes:\n
    .png, .jpg, .jpeg, .jfif, .gif, .bmp\n
    otherwise False
    """
    if img.endswith(".png"):
        return True
    if img.endswith(".jpg"):
        return True
    if img.endswith(".jpeg"):
        return True
    if img.endswith(".jfif"):
        return True
    if img.endswith(".gif"):
        return True
    if img.endswith(".bmp"):
        return True
    # if img.endswith(".webp"):
    #     return True
    return False

def save():
    """
    Saves all locked in and checked (by the user) images(ImageData) and removes them from the img_data_array
    """

    if len(gv.img_data_array) == 0:
        return False
    
    remove_later_list = list()
    for data in gv.img_data_array:
        if gv.img_data_array.index(data) > int(gv.Files.Conf.imgpp):
            break
        if data.locked:
            if not data.delete_both():
                continue
            gv.Files.Log.write_to_log('Attempting to save image:' + data.name_original + '/' + data.name_pixiv + '...' )
            if not data.save():
                continue
            gv.Files.Log.write_to_log('Successfully saved image')
            data.forget_results()
            data.self_destruct()
            remove_later_list.append(data)
    for data in remove_later_list:
        gv.img_data_array.remove(data)
    # gv.last_occupied_result = 0
    # for data in gv.img_data_array:
    #     data.index = gv.last_occupied_result
    #     gv.last_occupied_result += 1
    remove_later_list.clear()
    gv.Files.Ref.clean_reference()
    return True

def change_input():
    gv.input_dir = fd.askdirectory()
    gv.Files.Conf.input_dir = gv.input_dir
    gv.Files.Conf.write_config()

def open_input():
    try:
        startfile(gv.input_dir)
    except Exception as e:
        print('ERROR [0022] ' + str(e))
        gv.Files.Log.write_to_log('ERROR [0022] ' + str(e))
        #mb.showerror("ERROR", e)

def change_output():
    gv.output_dir = fd.askdirectory()
    gv.Files.Conf.output_dir = gv.output_dir
    gv.Files.Conf.write_config()

def open_output():
    try:
        startfile(gv.output_dir)
    except Exception as e:
        print('ERROR [0023] ' + str(e))
        gv.Files.Log.write_to_log('ERROR [0023] ' + str(e))
        #mb.showerror("ERROR", e)

def display_statistics():
    pass

if __name__ == '__main__':
    #gv.Files.Log.write_to_log()
    #gv.Files.Log.write_to_log("hallo")
    pass