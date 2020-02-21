from os import startfile
#from tkinter import messagebox as mb
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
    for i in range(12):
        if len(gv.img_data_array) == 0:
            break
        
        ImgData = gv.img_data_array.pop()
        gv.Files.Log.write_to_log('Attempting to save image:' + ImgData.name_original + '/' + ImgData.name_pixiv + '...' )
        ImgData.save()
        gv.Files.Log.write_to_log('Successfully saved image')
        #TODO
        ImgData.self_destruct()
        del ImgData

    for widget in gv.frame.winfo_children():
        widget.grid_forget()

def open_input():
    try:
        startfile(gv.cwd + "/Input")
    except Exception as e:
        print('ERROR [0022] ' + str(e))
        gv.Files.Log.write_to_log('ERROR [0022] ' + str(e))
        #mb.showerror("ERROR", e)
        
def open_sourced():
    try:
        startfile(gv.cwd + "/Sourced")
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