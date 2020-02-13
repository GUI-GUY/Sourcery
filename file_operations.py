from os import makedirs, remove, path, startfile, getcwd, listdir
from shutil import move, rmtree
from tkinter import messagebox as mb
from time import strftime

cwd = getcwd()
# log = -1

class Files():
    """PixivOptions"""
    def __init__(self):
        self.Log = LogFile()
        self.Theme = ThemeFile(self.Log)
        self.Cred = CredFile(self.Log)
        self.create_files()
    
    def create_files(self):
        self.init_directories()
        self.init_configs()

    def init_directories(self):
        try:
            makedirs(cwd + "/Input", 0o777, True)
            makedirs(cwd + "/Sourced", 0o777, True)
            makedirs(cwd + "/Sourcery/sourced_original", 0o777, True)
            makedirs(cwd + "/Sourcery/sourced_progress/pixiv", 0o777, True)
            # makedirs(cwd + "/Sourcery/sourced_progress/danbooru", 0o777, True)
            # makedirs(cwd + "/Sourcery/sourced_progress/gelbooru", 0o777, True)
        except Exception as e:
            print("ERROR [0007] " + str(e))
            self.Log.write_to_log("ERROR [0007] " + str(e))
            mb.showerror("ERROR [0007]", "ERROR CODE [0007]\nSomething went wrong while creating directories, please restart Sourcery.")
            return

    def init_configs(self):
        if not path.exists(cwd + '/Sourcery/theme'):
            self.Log.write_theme('Dark Theme', ['blue', 'red', '#123456', 'orange', 'grey', 'purple', 'magenta'])
        if not path.exists(cwd + '/Sourcery/credentials'):
            self.Log.write_credentials(['', '', '', ''])
        if not path.exists(cwd + '/Sourcery/log'):
            try:
                log = open(cwd + '/Sourcery/log', 'x')
                
            except Exception as e:
                print("ERROR [0024] " + str(e))
                self.Log.write_to_log("ERROR [0024] " + str(e))
                mb.showerror("ERROR [0024]", "ERROR CODE [0024]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery.")
            log.close()
        self.Log.write_to_log()

class ThemeFile():
    """PixivOptions"""
    def __init__(self, log):
        self.Log = log
        self.current_theme = 'Dark Theme'
        self.background = '#252525'
        self.foreground = '#ddd'
        self.button_background = '#444'
        self.button_background_active = 'white'
        self.button_foreground_active = 'black'
        self.button_background_pressed = '#111'
        self.button_foreground_pressed = 'white'
        self.custom_background = '#101010'
        self.custom_foreground = '#434343'
        self.custom_button_background = '#purple'
        self.custom_button_background_active = 'yellow'
        self.custom_button_foreground_active = 'black'
        self.custom_button_background_pressed = '#111'
        self.custom_button_foreground_pressed = 'green'
        self.read_theme()
    
    def read_theme(self):
        """
        Sets colour values as strings for the currently chosen style and setx colour values for the custom style.
        """
        try:
            f = open(cwd + '/Sourcery/theme')
        except Exception as e:
            print("ERROR [0008] " + str(e))
            self.Log.write_to_log("ERROR [0008] " + str(e))
            mb.showerror("ERROR [0008]", "ERROR CODE [0008]\nSomething went wrong while accessing a configuration file(theme), please restart Sourcery.")
            try:
                f.close()
            except:
                pass
        self.current_theme = f.readline()
        self.current_theme = self.current_theme[self.current_theme.find('=')+1:]
        ct = False
        if self.current_theme == 'Custom Theme\n':
            ct = True
        assign = f.readline()
        while self.current_theme != assign: #Read until current_theme is reached
            assign = f.readline()
        
        while assign != '\n': #Read in values for current theme
            assign = f.readline()
            if assign.startswith('background='):
                self.background = assign[assign.find('=')+1:-1]
            if assign.startswith('foreground='):
                self.foreground = assign[assign.find('=')+1:-1]
            if assign.startswith('button_background='):
                self.button_background = assign[assign.find('=')+1:-1]
            if assign.startswith('button_background_active='):
                self.button_background_active = assign[assign.find('=')+1:-1]
            if assign.startswith('button_foreground_active='):
                self.button_foreground_active = assign[assign.find('=')+1:-1]
            if assign.startswith('button_background_pressed='):
                self.button_background_pressed = assign[assign.find('=')+1:-1]
            if assign.startswith('button_foreground_pressed='):
                self.button_foreground_pressed = assign[assign.find('=')+1:-1]

        if ct: #if current theme is custom theme
            self.custom_background = self.background
            self.custom_foreground = self.foreground
            self.custom_button_background = self.button_background
            self.custom_button_background_active = self.button_background_active
            self.custom_button_foreground_active = self.button_foreground_active
            self.custom_button_background_pressed = self.button_background_pressed
            self.custom_button_foreground_pressed = self.button_foreground_pressed
        else:
            while assign != 'Custom Theme\n':
                assign = f.readline()
            while assign != '\n': #Read in values for custom theme
                assign = f.readline()
                if assign.startswith('background='):
                    self.custom_background = assign[assign.find('=')+1:-1]
                if assign.startswith('foreground='):
                    self.custom_foreground = assign[assign.find('=')+1:-1]
                if assign.startswith('button_background='):
                    self.custom_button_background = assign[assign.find('=')+1:-1]
                if assign.startswith('button_background_active='):
                    self.custom_button_background_active = assign[assign.find('=')+1:-1]
                if assign.startswith('button_foreground_active='):
                    self.custom_button_foreground_active = assign[assign.find('=')+1:-1]
                if assign.startswith('button_background_pressed='):
                    self.custom_button_background_pressed = assign[assign.find('=')+1:-1]
                if assign.startswith('button_foreground_pressed='):
                    self.custom_button_foreground_pressed = assign[assign.find('=')+1:-1]
        self.current_theme = self.current_theme[0:-1]
        f.close()
        
    def write_theme(self, chosen_theme):
        theme = """Current theme=""" + chosen_theme + """

Dark Theme
background=#252525
foreground=#ddd
button_background=#444
button_background_active=white
button_foreground_active=black
button_background_pressed=#111
button_foreground_pressed=white

Light Theme
background=#eee
foreground=black
button_background=#aaa
button_background_active=black
button_foreground_active=white
button_background_pressed=#ddd
button_foreground_pressed=black

Custom Theme
background=""" + self.custom_background + """
foreground=""" + self.custom_foreground + """
button_background=""" + self.custom_button_background+  """
button_background_active=""" + self.custom_button_background_active + """
button_foreground_active=""" + self.custom_button_foreground_active + """
button_background_pressed=""" + self.custom_button_background_pressed + """
button_foreground_pressed=""" + self.custom_button_foreground_pressed + """

END"""

        try:
            f = open(cwd + '/Sourcery/theme', 'w')
            f.write(theme)
        except Exception as e:
            print("ERROR [0009] " + str(e))
            self.Log.write_to_log("ERROR [0009] " + str(e))
            mb.showerror("ERROR [0009]", "ERROR CODE [0009]\nSomething went wrong while accessing a configuration file(theme), please try again.")
            try:
                f.close()
            except:
                pass
            return e
        f.close()
        self.read_theme()
        return None

class CredFile():
    """PixivOptions"""
    def __init__(self, log):
        self.Log = log
        self.saucenao_api_key = ''
        self.pixiv_username = ''
        self.pixiv_password = ''
        self.pixiv_refreshtoken = ''
        self.read_credentials()

    def read_credentials(self):
        """
        Reads in saved credentials.
        """
        try:
            f = open(cwd + '/Sourcery/credentials')
        except Exception as e:
            print("ERROR [0010] " + str(e))
            self.Log.write_to_log("ERROR [0010] " + str(e))
            mb.showerror("ERROR [0010]", "ERROR CODE [0010]\nSomething went wrong while accessing a configuration file(credentials), please try again.")

        creds = f.readline()
        while creds != 'END':
            if creds == 'SauceNao\n':
                creds = f.readline()
                self.saucenao_api_key = creds[creds.find('=')+1:-1]
            if creds == 'Pixiv\n':
                creds = f.readline()
                self.pixiv_username = creds[creds.find('=')+1:-1]
                creds = f.readline()
                self.pixiv_password = creds[creds.find('=')+1:-1]
                creds = f.readline()
                self.pixiv_refreshtoken = creds[creds.find('=')+1:-1]
            creds = f.readline()
        f.close()

    def write_credentials(self):
        creds = """SauceNao
API-Key=""" + self.saucenao_api_key + """

Pixiv
Username=""" + self.pixiv_username + """
Password=""" + self.pixiv_password + """
refreshtoken=""" + self.pixiv_refreshtoken + """

END"""

        try:
            f = open(cwd + '/Sourcery/credentials', 'w')
            f.write(creds)
        except Exception as e:
            print("ERROR [0011] " + str(e))
            self.Log.write_to_log("ERROR [0011] " + str(e))
            mb.showerror("ERROR [0011]", "ERROR CODE [0011]\nSomething went wrong while accessing a configuration file(credentials), please try again.")
            try:
                f.close()
            except:
                pass
            return e
        f.close()
        return None

class LogFile():
    """PixivOptions"""
    def __init__(self):
        self.log = -1
        self.init_log()

    def init_log(self):
        try:
            self.log = open(cwd + '/Sourcery/log', 'a')
            self.log.write('\nSourcery started. Date:' + strftime("20%y|%m|%d") + ' Time:' + strftime("%H:%M:%S") + '\n')
        except Exception as e:
            pass#TODO
    
    def write_to_log(self, message = ''):
        if message != '':
            try:
                self.log.write('[' + strftime("%H:%M:%S") + '] ' + message + '\n')
                self.log.flush()
            except Exception as e:
                print(str(e))
                pass#TODO
            self.log.flush()
    

# def init_directories():
#     try:
#         makedirs(cwd + "/Input", 0o777, True)
#         makedirs(cwd + "/Sourced", 0o777, True)
#         makedirs(cwd + "/Sourcery/sourced_original", 0o777, True)
#         makedirs(cwd + "/Sourcery/sourced_progress/pixiv", 0o777, True)
#         # makedirs(cwd + "/Sourcery/sourced_progress/danbooru", 0o777, True)
#         # makedirs(cwd + "/Sourcery/sourced_progress/gelbooru", 0o777, True)
#     except Exception as e:
#         print("ERROR [0007] " + str(e))
#         write_to_log("ERROR [0007] " + str(e))
#         mb.showerror("ERROR [0007]", "ERROR CODE [0007]\nSomething went wrong while creating directories, please restart Sourcery.")
#         return

# def init_configs():
#     if not path.exists(cwd + '/Sourcery/theme'):
#         write_theme('Dark Theme', ['blue', 'red', '#123456', 'orange', 'grey', 'purple', 'magenta'])
#     if not path.exists(cwd + '/Sourcery/credentials'):
#         write_credentials(['', '', '', ''])
#     if not path.exists(cwd + '/Sourcery/log'):
#         try:
#             log = open(cwd + '/Sourcery/log', 'x')
            
#         except Exception as e:
#             print("ERROR [0024] " + str(e))
#             write_to_log("ERROR [0024] " + str(e))
#             mb.showerror("ERROR [0024]", "ERROR CODE [0024]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery.")
#         log.close()
#     write_to_log()
# 
# def read_theme():
#     """
#     Returns a list with colour values as strings for the currently chosen style and a list with colour values for the custom style.\n
#     Order:\n
#     [0]background, [1]foreground, [2]button_background, [3]button_background_active, 
#     [4]button_foreground_active, [5]button_background_pressed, [6]button_foreground_pressed
#     """
#     try:
#         f = open(cwd + '/Sourcery/theme')
#     except Exception as e:
#         print("ERROR [0008] " + str(e))
#         write_to_log("ERROR [0008] " + str(e))
#         mb.showerror("ERROR [0008]", "ERROR CODE [0008]\nSomething went wrong while accessing a configuration file(theme), please restart Sourcery.")
#         f.close()
#         return
#     theme = f.readline()
#     theme = theme[theme.find('=')+1:]
#     ct = False
#     if theme == 'Custom Theme\n':
#         ct = True
#     assign = f.readline()
#     while theme != assign:
#         assign = f.readline()
    
#     colour_array = []
#     custom_array = []
#     while assign != '\n':
#         assign = f.readline()
#         colour_array.append(assign[assign.find('=')+1:-1])
#         if ct:
#             custom_array.append(assign[assign.find('=')+1:-1])
#     if not ct:
#         while assign != 'Custom Theme\n':
#             assign = f.readline()
#         while assign != '\n':
#             assign = f.readline()
#             custom_array.append(assign[assign.find('=')+1:-1])
#     f.close()
#     return colour_array, custom_array, theme[0:-1]

# def write_theme(chosen_theme, custom_theme):
#     theme = """Current theme=""" + chosen_theme + """

# Dark Theme
# background=#252525
# foreground=#ddd
# button_background=#444
# button_background_active=white
# button_foreground_active=black
# button_background_pressed=#111
# button_foreground_pressed=white

# Light Theme
# background=#eee
# foreground=black
# button_background=#aaa
# button_background_active=black
# button_foreground_active=white
# button_background_pressed=#ddd
# button_foreground_pressed=black

# Custom Theme
# background=""" + custom_theme[0] + """
# foreground=""" + custom_theme[1] + """
# button_background=""" + custom_theme[2]+  """
# button_background_active=""" + custom_theme[3] + """
# button_foreground_active=""" + custom_theme[4] + """
# button_background_pressed=""" + custom_theme[5] + """
# button_foreground_pressed=""" + custom_theme[6] + """

# END"""

#     try:
#         f = open(cwd + '/Sourcery/theme', 'w')
#         f.write(theme)
#     except Exception as e:
#         print("ERROR [0009] " + str(e))
#         write_to_log("ERROR [0009] " + str(e))
#         mb.showerror("ERROR [0009]", "ERROR CODE [0009]\nSomething went wrong while accessing a configuration file(theme), please try again.")
#         try:
#             f.close()
#         except:
#             pass
#         return e
#     f.close()
#     return None

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

# def read_credentials():
#     """
#     Returns a list with saved credentials.\n
#     Order:\n
#     [0]SauceNao API-Key, [1]Pixiv Username, [2]Pixiv Password, [3]Pixiv refreshtoken
#     """
#     try:
#         f = open(cwd + '/Sourcery/credentials')
#     except Exception as e:
#         print("ERROR [0010] " + str(e))
#         write_to_log("ERROR [0010] " + str(e))
#         mb.showerror("ERROR [0010]", "ERROR CODE [0010]\nSomething went wrong while accessing a configuration file(credentials), please try again.")
#         return

#     credentials_array = ['','','',''] 
#     creds = f.readline()
#     while creds != 'END':
#         if creds == 'SauceNao\n':
#             creds = f.readline()
#             credentials_array[0] = creds[creds.find('=')+1:-1]
#         if creds == 'Pixiv\n':
#             creds = f.readline()
#             credentials_array[1] = creds[creds.find('=')+1:-1]
#             creds = f.readline()
#             credentials_array[2] = creds[creds.find('=')+1:-1]
#             creds = f.readline()
#             credentials_array[3] = creds[creds.find('=')+1:-1]
#         creds = f.readline()
#     f.close()
#     return credentials_array

# def write_credentials(credentials_array):
#     creds = """SauceNao
# API-Key=""" + credentials_array[0] + """

# Pixiv
# Username=""" + credentials_array[1] + """
# Password=""" + credentials_array[2] + """
# refreshtoken=""" + credentials_array[3] + """

# END"""

#     try:
#         f = open(cwd + '/Sourcery/credentials', 'w')
#         f.write(creds)
#     except Exception as e:
#         print("ERROR [0011] " + str(e))
#         write_to_log("ERROR [0011] " + str(e))
#         mb.showerror("ERROR [0011]", "ERROR CODE [0011]\nSomething went wrong while accessing a configuration file(credentials), please try again.")
#         try:
#             f.close()
#         except:
#             pass
#         return e
#     f.close()
#     return None

def save(chkbtn_vars_array, chkbtn_vars_big_array, pixiv_images_array, delete_dirs_array, safe_to_show_array, frame, process):
    downloaded_name_new = None
    original_name_new = None
    pixiv_dir = cwd + '/Sourcery/sourced_progress/pixiv/'
    sourced_original_dir = cwd + '/Sourcery/sourced_original/'
    for i in range(len(pixiv_images_array)):
        original_var = chkbtn_vars_array[i][0].get()
        downloaded_var = chkbtn_vars_array[i][1].get()
        if original_var == 1:
            if downloaded_var == 1:
                downloaded_name_new = 'new_' + pixiv_images_array[i][0]
                original_name_new = 'old_' + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3]
            else:
                # Move original image to Sourced and delete downloaded image/directory
                downloaded_name_new = None
                original_name_new = pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3]
                if pixiv_dir + pixiv_images_array[i][0] not in delete_dirs_array:
                    delete_dirs_array.append(pixiv_dir + pixiv_images_array[i][0])
        elif downloaded_var == 1:
            # Move downloaded image to Sourced and delete original image
            downloaded_name_new = pixiv_images_array[i][0]
            original_name_new = None
            if sourced_original_dir + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3] not in delete_dirs_array:
                delete_dirs_array.append(sourced_original_dir + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3])
        
        index = -1
        for elem in chkbtn_vars_big_array:
            if pixiv_images_array[i][2] == elem[0]:
                index = chkbtn_vars_big_array.index(elem)
                downloaded_name_new = None
                break
        if index != -1:
            skip_first = True
            for img in chkbtn_vars_big_array[index]:
                if skip_first:
                    skip_first = False
                    continue
                if img[1].get() == 1:
                    try:
                        move(pixiv_dir + pixiv_images_array[i][0] + '/' + img[0], cwd + '/Sourced/' + pixiv_images_array[i][0] + '/' + img[0])
                    except Exception as e:
                        print("ERROR [0016] " + str(e))
                        write_to_log("ERROR [0016] " + str(e))
                        mb.showerror("ERROR [0016]", "ERROR CODE [0016]\nSomething went wrong while moving the image " + img[0] + " from the folder " + pixiv_dir + pixiv_images_array[i][0])
            if pixiv_dir + pixiv_images_array[i][0] not in delete_dirs_array:
                delete_dirs_array.append(pixiv_dir + pixiv_images_array[i][0])

        if downloaded_name_new != None:
            try:
                move(pixiv_dir + pixiv_images_array[i][0], cwd + '/Sourced/' + downloaded_name_new)
            except Exception as e:
                print("ERROR [0012] " + str(e))
                write_to_log("ERROR [0012] " + str(e))
                mb.showerror("ERROR [0012]", "ERROR CODE [0012]\nSomething went wrong while moving the image " + pixiv_images_array[i][0] + " from the folder " + pixiv_dir)
        if original_name_new != None:
            try:
                move(sourced_original_dir + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3], cwd + '/Sourced/' + original_name_new)
            except Exception as e:
                print("ERROR [0013] " + str(e))
                write_to_log("ERROR [0013] " + str(e))
                mb.showerror("ERROR [0013]", "ERROR CODE [0013]\nSomething went wrong while moving the image " + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3] + " from the folder " + pixiv_dir)
        try:
            remove(cwd + '/Input/' + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3])
        except Exception as e:
            print("ERROR [0014] " + str(e))
            write_to_log("ERROR [0014] " + str(e))
            mb.showerror("ERROR [0014]", "ERROR CODE [0014]\nSomething went wrong while removing the image " + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3] + " from the folder " + cwd + '/Input/')
        # try:
        #     remove(sourced_original_dir + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3])
        # except Exception as e:
        #     print("ERROR [0015] " + str(e))
        #     write_to_log("ERROR [0015] " + str(e))
        #     mb.showerror("ERROR [0015]", "ERROR CODE [0015]\nSomething went wrong while removing the image " + pixiv_images_array[i][2] + '.' + pixiv_images_array[i][3] + " from the folder " + cwd + '/Sourcery/sourced_original/')

        safe_to_show_array.remove(pixiv_images_array[i][2])

    for a in range(len(pixiv_images_array)):
        for b in range(len(pixiv_images_array[a])):
            del pixiv_images_array[a][0]
    pixiv_images_array.clear()

    if not process.is_alive():
        for img in listdir(sourced_original_dir):
            if sourced_original_dir + img not in delete_dirs_array:
                delete_dirs_array.append(sourced_original_dir + img)

    for element in delete_dirs_array:
        try:
            if path.isdir(element):
                rmtree(element)
            elif path.isfile(element):
                remove(element)
        except Exception as e:
            print('ERROR [0017] ' + str(e))
            write_to_log("ERROR [0017] " + str(e))
            #mb.showerror("ERROR", "ERROR CODE [0017]\nSomething went wrong while removing the image " + element)

    delete_dirs_array.clear()
    	
    for widget in frame.winfo_children():
        widget.grid_forget()

# def write_to_log(message = ''):
#     global log
#     if log == -1:
#         try:
#             log = open(cwd + '/Sourcery/log', 'a')
#             log.write('\nSourcery started. Date:' + strftime("20%y|%m|%d") + ' Time:' + strftime("%H:%M:%S") + '\n')
#         except Exception as e:
#             pass#TODO
#     if message != '':
#         try:
#             log.write('[' + strftime("%H:%M:%S") + '] ' + message + '\n')
#             log.flush()
#         except Exception as e:
#             print(str(e))
#             pass#TODO
#         log.flush()
    
def open_input():
    try:
        startfile(cwd + "/Input")
    except Exception as e:
        print('ERROR [0022] ' + str(e))
        write_to_log('ERROR [0022] ' + str(e))
        #mb.showerror("ERROR", e)
        
def open_sourced():
    try:
        startfile(cwd + "/Sourced")
    except Exception as e:
        print('ERROR [0023] ' + str(e))
        write_to_log('ERROR [0023] ' + str(e))
        #mb.showerror("ERROR", e)

def display_statistics():
    pass

if __name__ == '__main__':
    init_configs()
    #write_to_log()
    #write_to_log("hallo")
    pass
    #write_credentials(getcwd(), read_credentials(getcwd()))
    # def save_deprecated(chkbtn_vars_array, chkbtn_vars_big_array, pixiv_images_array, delete_dirs_array, safe_to_show_array, frame):
    #     global cwd
    #     for element in delete_dirs_array:
    #         if path.isdir(element):
    #             rmtree(element)
    #         else:
    #             remove(element)
    #     delete_dirs_array.clear()

    #     do_not_delete_tree = False
    #     for elem in chkbtn_vars_big_array:
    #         for img in elem:
    #             if img[1].get() == 1:
    #                 try:
    #                     move(cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0] + '/' + img[0], 
    #                     cwd + '/Sourced/' + elem[0] + '/' + img[0])
    #                 except Exception as e:
    #                     print(str(e))
    #                     mb.showerror("Something went wrong while saving the image " + img[0] + " from the folder " + cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0] + ". You have to recover the image and delete the folder manually.")
    #                     do_not_delete_tree = True
    #         try:
    #             if do_not_delete_tree:
    #                 rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + elem[0])
    #                 do_not_delete_tree = False
    #         except Exception as e:
    #             print(str(e))
            
    #     chkbtn_vars_big_array.clear()

    #     for tup in chkbtn_vars_array:
    #         original_var = tup[0].get()
    #         downloaded_var = tup [1].get()

    #         if len(pixiv_images_array) > 0:
    #             if original_var == 1:
    #                 if downloaded_var == 1:
    #                     # if pixiv_images_array[0][5]:
    #                     #     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2] + '/' + pixiv_images_array[0][1], 
    #                     #         cwd + '/Sourced/new_' + pixiv_images_array[0][1])
    #                     #     rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
    #                     # else:

    #                     # Move original and downloaded image from their respective folders to Sourced and rename them 
    #                     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0], # war im else
    #                             cwd + '/Sourced/new_' + pixiv_images_array[0][0])
    #                     move(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3], 
    #                         cwd + '/Sourced/old_' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
    #                 else:
    #                     # Move original image to Sourced and delete downloaded image/directory
    #                     move(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3], 
    #                         cwd + '/Sourced/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
    #                     if pixiv_images_array[0][5]:
    #                         rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
    #                     else:
    #                         remove(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0])
    #             elif downloaded_var == 1:
    #                     # if pixiv_images_array[0][5]:
    #                     #     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2] + '/' + pixiv_images_array[0][1], 
    #                     #         cwd + '/Sourced/' + pixiv_images_array[0][1])
    #                     #     rmtree(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][2])
    #                     # else:

    #                     # Move downloaded image to Sourced and delete original image
    #                     move(cwd + '/Sourcery/sourced_progress/pixiv/' + pixiv_images_array[0][0], # war im else
    #                             cwd + '/Sourced/' + pixiv_images_array[0][0])
    #                     remove(cwd + '/Sourcery/sourced_original/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
    #             # Delete image from input
    #             remove(cwd + '/Input/' + pixiv_images_array[0][2] + '.' + pixiv_images_array[0][3])
    #             safe_to_show_array.remove(pixiv_images_array[0][2])
                
    #             for a in range(len(pixiv_images_array[0])):
    #                 del pixiv_images_array[0][0]
    #             #pixiv_images_array.pop(0)
    #     for widget in frame.winfo_children():
    #         widget.grid_forget()