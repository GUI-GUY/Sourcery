from os import startfile, path
from copy import deepcopy
from PIL import Image
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
        if gv.img_data_array.index(data) > gv.config.getint('Sourcery', 'imgpp'):
            break
        if data.locked:
            # if not data.delete_both():
            #     continue
            gv.Files.Log.write_to_log('Attempting to save image:' + data.sub_dill.name + '...' )
            if not data.save():
                print('error while saving')
                gv.Files.Log.write_to_log('error while saving')
                continue
            gv.Files.Log.write_to_log('Successfully saved image')
            data.forget_results()
            gv.imgpp_sem.release()
            data.self_destruct()
            remove_later_list.append(data)
    for data in remove_later_list:
        gv.img_data_array.remove(data)
        gv.img_data_sem.release()
    remove_later_list.clear()
    return True

def gen_tagfile(tags, gen_dir, name):
    """
    Takes a list of strings, the directory in which to generate the file and the name of the file
    """
    for tag in tags:
        counter = -1
        for ta in tags:
            if tag == ta:
                counter = counter + 1
        for t in range(counter):
            tags.remove(tag)
    if len(tags) == 0:
        return True
    try:
        f = open(gen_dir + '/' + name + '.txt', 'a', encoding='utf8')
        for tag in tags:
            if type(tag) == type(dict()):
                try:
                    f.write(tag['name'] + '\n')
                except:
                    pass
                try:
                    f.write(tag['translated_name'] + '\n')
                except:
                    pass
            else:
                f.write(tag + '\n')
        f.close()
        return True
    except Exception as e:
        print("ERROR [0053] " + str(e))
        gv.Files.Log.write_to_log("ERROR [0053] " + str(e))
        #mb.showerror("ERROR [0053]", "ERROR CODE [0053]\nSomething went wrong while generating the tagfile" + gen_dir + '/' + name + '.txt')
        return False

def change_input():
    gv.input_dir = fd.askdirectory()
    gv.config['Sourcery']['input_dir'] = gv.input_dir
    gv.write_config()

def open_input():
    try:
        startfile(gv.input_dir)
    except Exception as e:
        print('ERROR [0022] ' + str(e))
        gv.Files.Log.write_to_log('ERROR [0022] ' + str(e))
        #mb.showerror("ERROR", e)

def change_output():
    gv.output_dir = fd.askdirectory()
    gv.config['Sourcery']['output_dir'] = gv.output_dir
    gv.write_config()

def open_output():
    try:
        startfile(gv.output_dir)
    except Exception as e:
        print('ERROR [0023] ' + str(e))
        gv.Files.Log.write_to_log('ERROR [0023] ' + str(e))
        #mb.showerror("ERROR", e)

def display_statistics():
    pass

def resize(new_image):
    """
    Resizes given image to a third of the screen width and to the screen height*0.87 and returns it as a new object.
    """

    oldwidth = new_image.width
    oldheight = new_image.height

    #new_image = deepcopy(image)

    if oldwidth > gv.width/3:
        newwidth = int(gv.width*0.4)
        newheight = int(newwidth/(oldwidth/oldheight))
        newsize = newwidth, newheight
        new_image = new_image.resize(newsize, Image.ANTIALIAS)
    if new_image.height > gv.height*0.87:
        newheight = int(gv.height*0.87)
        newwidth = int(newheight/(oldheight/oldwidth))
        newsize = newwidth, newheight
        new_image = new_image.resize(newsize, Image.ANTIALIAS)
    return new_image

def is_input_int_digit(P, negative=False, min=-1, max=10000000000):
    if str.isdigit(P) or P == "" or (negative and P[0] == '-' and (str.isdigit(P[1:]) or P[1:] == "")): # if P is '' or '-' or negative/positive number
        if P != '' and ((P[0] == '-' and len(P) > 1) or P[0] != '-') and (int(P) < int(min) or int(P) > int(max)): # if P is negative/positive number and within min/max
            return False
        return True
    else:
        return False


if __name__ == '__main__':
    #gv.Files.Log.write_to_log()
    #gv.Files.Log.write_to_log("hallo")
    pass