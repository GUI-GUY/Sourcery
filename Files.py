from os import makedirs, path, getcwd
from sys import stderr
from tkinter import END, Text
from tkinter import messagebox as mb
from time import strftime
from json import loads
#import global_variables as gv

cwd = getcwd()

class Files():
    """Hosts all File classes and creates neccesary files and folders on startup"""
    def __init__(self):
        self.create_files()
        self.Log = LogFile()
        self.Theme = ThemeFile(self.Log)
        self.Cred = CredFile(self.Log)
        self.Conf = ConfigFile(self.Log)
        self.Ref = ReferenceFile(self.Log)
        
    def create_files(self):
        self.init_directories()
        self.init_configs()

    def init_directories(self):
        try:
            makedirs(cwd + "/Input", 0o777, True)
            makedirs(cwd + "/Output", 0o777, True)
            makedirs(cwd + "/Sourcery/sourced_original", 0o777, True)
            makedirs(cwd + "/Sourcery/sourced_progress/pixiv", 0o777, True)
            makedirs(cwd + "/Sourcery/sourced_progress/danbooru", 0o777, True)
            makedirs(cwd + "/Sourcery/sourced_progress/yandere", 0o777, True)
            makedirs(cwd + "/Sourcery/sourced_progress/konachan", 0o777, True)
            # makedirs(cwd + "/Sourcery/sourced_progress/gelbooru", 0o777, True)
        except Exception as e:
            print("ERROR [0007] " + str(e))
            #self.Log.write_to_log("ERROR [0007] " + str(e))
            mb.showerror("ERROR [0007]", "ERROR CODE [0007]\nSomething went wrong while creating directories, please restart Sourcery.")

    def init_configs(self):
        """
        Creates all configuration files if they are not yet existent
        """
        if not path.exists(cwd + '/Sourcery/theme'):
            try:
                theme = open(cwd + '/Sourcery/theme', 'x')
                theme.close()
            except Exception as e:
                print("ERROR [0028] " + str(e))
                #self.Log.write_to_log("ERROR [0028] " + str(e))
                mb.showerror("ERROR [0028]", "ERROR CODE [0028]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery.")
            #self.Theme.write_theme('Dark Theme')# ['blue', 'red', '#123456', 'orange', 'grey', 'purple', 'magenta']
        if not path.exists(cwd + '/Sourcery/credentials'):
            try:
                cred = open(cwd + '/Sourcery/credentials', 'x')
                cred.close()
            except Exception as e:
                print("ERROR [0029] " + str(e))
                #self.Log.write_to_log("ERROR [0029] " + str(e))
                mb.showerror("ERROR [0029]", "ERROR CODE [0029]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery.")
            #self.Theme.write_credentials()
        if not path.exists(cwd + '/Sourcery/log'):
            try:
                log = open(cwd + '/Sourcery/log', 'x')
                log.close()
            except Exception as e:
                print("ERROR [0024] " + str(e))
                #self.Log.write_to_log("ERROR [0024] " + str(e))
                mb.showerror("ERROR [0024]", "ERROR CODE [0024]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery.")
        if not path.exists(cwd + '/Sourcery/config'):
            try:
                config = open(cwd + '/Sourcery/config', 'x')
                config.close()
            except Exception as e:
                print("ERROR [0027] " + str(e))
                #self.Log.write_to_log("ERROR [0027] " + str(e))
                mb.showerror("ERROR [0027]", "ERROR CODE [0027]\nSomething went wrong while accessing a configuration file(config), please restart Sourcery.")
        if not path.exists(cwd + '/Sourcery/reference'):
            try:
                reference = open(cwd + '/Sourcery/reference', 'x')
                reference.close()
            except Exception as e:
                print("ERROR [0036] " + str(e))
                #self.Log.write_to_log("ERROR [0036] " + str(e))
                mb.showerror("ERROR [0036]", "ERROR CODE [0036]\nSomething went wrong while accessing a configuration file(reference), please restart Sourcery.")

class ThemeFile():
    """Includes the color hex codes for the current and the custom theme and also methods to write/read these to/from the theme file"""
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
        self.checkbutton_pressed = 'green'
        self.custom_background = '#101010'
        self.custom_foreground = 'white'
        self.custom_button_background = 'purple'
        self.custom_button_background_active = 'yellow'
        self.custom_button_foreground_active = 'black'
        self.custom_button_background_pressed = '#fff'
        self.custom_button_foreground_pressed = 'green'
        self.custom_checkbutton_pressed = 'green'
        if self.read_theme():
            self.write_theme('Dark Theme')
    
    def read_theme(self):
        """
        Sets colour values as strings for the currently chosen style and sets colour values for the custom style.
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
            return False
        temp = f.readline()
        if not temp.startswith('Current theme='):
            f.close()
            return True
        self.current_theme = temp
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
            if assign.startswith('checkbutton_pressed='):
                self.checkbutton_pressed = assign[assign.find('=')+1:-1]

        if ct: #if current theme is custom theme
            self.custom_background = self.background
            self.custom_foreground = self.foreground
            self.custom_button_background = self.button_background
            self.custom_button_background_active = self.button_background_active
            self.custom_button_foreground_active = self.button_foreground_active
            self.custom_button_background_pressed = self.button_background_pressed
            self.custom_button_foreground_pressed = self.button_foreground_pressed
            self.custom_checkbutton_foreground_pressed = self.checkbutton_pressed
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
                if assign.startswith('checkbutton_pressed='):
                    self.custom_checkbutton_pressed = assign[assign.find('=')+1:-1]
        self.current_theme = self.current_theme[0:-1]
        f.close()
        return False
        
    def write_theme(self, chosen_theme):
        """
        Writes information for the chosen theme and the custom theme to the theme file
        """
        theme = ("Current theme=" + chosen_theme +
            "\n\nDark Theme"
            "\nbackground=#252525"
            "\nforeground=#ddd"
            "\nbutton_background=#444"
            "\nbutton_background_active=white"
            "\nbutton_foreground_active=black"
            "\nbutton_background_pressed=#111"
            "\nbutton_foreground_pressed=white"
            "\ncheckbutton_pressed=green"
            "\n\nLight Theme"
            "\nbackground=#eee"
            "\nforeground=black"
            "\nbutton_background=#aaa"
            "\nbutton_background_active=black"
            "\nbutton_foreground_active=white"
            "\nbutton_background_pressed=#ddd"
            "\nbutton_foreground_pressed=black"
            "\ncheckbutton_pressed=green"
            "\n\nCustom Theme"
            "\nbackground=" + self.custom_background +
            "\nforeground=" + self.custom_foreground +
            "\nbutton_background=" + self.custom_button_background +
            "\nbutton_background_active=" + self.custom_button_background_active +
            "\nbutton_foreground_active=" + self.custom_button_foreground_active +
            "\nbutton_background_pressed=" + self.custom_button_background_pressed +
            "\nbutton_foreground_pressed=" + self.custom_button_foreground_pressed +
            "\ncheckbutton_pressed=" + self.custom_checkbutton_pressed +
            "\n\nEND")

        try:
            f = open(cwd + '/Sourcery/theme', 'w')
            f.write(theme)
        except Exception as e:
            print("ERROR [0009] " + str(e))
            self.Log.write_to_log("ERROR [0009] " + str(e))
            mb.showerror("ERROR [0009]", "ERROR CODE [0009]\nSomething went wrong while accessing a configuration file(theme), please try again or restart Sourcery.")
            try:
                f.close()
            except:
                pass
            return e
        f.close()
        self.read_theme()
        return None

class CredFile():
    """Includes the credentials of the user and also methods to write/read these to/from the credentials file"""
    def __init__(self, log):
        self.Log = log
        self.saucenao_api_key = ''
        if self.read_credentials():
            self.write_credentials()

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
            return False
        creds = f.readline()
        if creds != 'SauceNao\n':
            f.close()
            return True
        while not creds.startswith('END'):
            if creds == 'SauceNao\n':
                creds = f.readline()
                self.saucenao_api_key = creds[creds.find('=')+1:-1]
            creds = f.readline()
        f.close()
        return False

    def write_credentials(self):
        """
        Writes credentials to the credentials file
        """
        creds = ("SauceNao"
                "\nAPI-Key=" + self.saucenao_api_key +
                "\n\nEND")
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
        self.read_credentials()
        return None

class LogFile():
    """Includes the opened log and the log text frame on the startpage and also methods to write these to the log file"""
    def __init__(self):
        self.log = -1
        self.log_text = None
        self.init_log_init = False
        #self.init_log()

    def init_log(self):
        if self.init_log_init:
            return
        try:
            self.log = open(cwd + '/Sourcery/log', 'a')
            self.log.write('\nSourcery started. Date:' + strftime("20%y|%m|%d") + ' Time:' + strftime("%H:%M:%S") + '\n')
            self.log_text.configure(state='normal')
            self.log_text.insert(END, '\nSourcery started. Date:' + strftime("20%y|%m|%d") + ' Time:' + strftime("%H:%M:%S") + '\n')
            self.log_text.configure(state='disabled')
        except Exception as e:
            print("ERROR [0038] " + str(e))
            #self.Log.write_to_log("ERROR [0038] " + str(e))
            mb.showerror("ERROR [0038]", "ERROR CODE [0038]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery.")
        self.init_log_init = True

    def write_to_log(self, message = ''):
        if self.log == -1:
            self.init_log()
        if message != '':
            try:
                self.log.write('[' + strftime("%H:%M:%S") + '] ' + message + '\n')
                self.log.flush()
                self.log_text.configure(state='normal')
                self.log_text.insert(END,'[' + strftime("%H:%M:%S") + '] ' + message + '\n')
                self.log_text.configure(state='disabled')
            except Exception as e:
                print("ERROR [0050] " + str(e))
                #self.Log.write_to_log("ERROR [0050] " + str(e))
                mb.showerror("ERROR [0050]", "ERROR CODE [0050]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery as soon as possible.")

    def write(self, message):
        self.write_to_log(message)
        #self.log.write('[' + strftime("%H:%M:%S") + '] ' + message + '\n')
        stderr.flush()
        #self.log.flush()

class ConfigFile():
    """Includes the options and also methods to write/read these to/from the config file"""
    def __init__(self, log):
        self.Log = log
        self.rename_pixiv = '0'
        self.tags_pixiv = ''
        self.gen_tagfile_pixiv = '0'
        self.tagfile_pixiv_pixiv = '0'
        self.tagfile_danbooru_pixiv = '0'
        self.tagfile_yandere_pixiv = '0'
        self.tagfile_konachan_pixiv = '0'
        self.direct_replace_pixiv = '0'
        self.use_pixiv = '1'

        self.rename_danbooru = '0'
        self.tags_danbooru = ''
        self.gen_tagfile_danbooru = '0'
        self.tagfile_pixiv_danbooru = '0'
        self.tagfile_danbooru_danbooru = '0'
        self.tagfile_yandere_danbooru = '0'
        self.tagfile_konachan_danbooru = '0'
        self.direct_replace_danbooru = '0'
        self.use_danbooru = '1'

        self.rename_yandere = '0'
        self.tags_yandere = ''
        self.gen_tagfile_yandere = '0'
        self.tagfile_pixiv_yandere = '0'
        self.tagfile_danbooru_yandere = '0'
        self.tagfile_yandere_yandere = '0'
        self.tagfile_konachan_yandere = '0'
        self.direct_replace_yandere = '0'
        self.use_yandere = '1'


        self.rename_konachan = '0'
        self.tags_konachan = ''
        self.gen_tagfile_konachan = '0'
        self.tagfile_pixiv_konachan = '0'
        self.tagfile_danbooru_konachan = '0'
        self.tagfile_yandere_konachan = '0'
        self.tagfile_konachan_konachan = '0'
        self.direct_replace_konachan = '0'
        self.use_konachan = '1'

        self.minsim = '80'
        self.imgpp = '12'
        self.input_dir = cwd + '/Input'
        self.output_dir = cwd + '/Output'
        self.delete_input = '0'
        self.gen_tagfile_original = '0'
        self.tagfile_pixiv_original = '0'
        self.tagfile_danbooru_original = '0'
        self.tagfile_yandere_original = '0'
        self.tagfile_konachan_original = '0'
        self.saucenao_returns = '10'
        self.direct_replace = '100'
        self.input_search_depth = '1'
        self.saucenao_depth = '128'
        self.saucenao_bias = '15'
        self.saucenao_biasmin = '70'
        self.png_weight = '0'
        self.jpg_weight = '0'
        self.jfif_weight = '0'
        self.gif_weight = '0'
        self.bmp_weight = '0'
        self.other_weight = '0'
        self.higher_resolution_weight = '0'
        self.pixiv_weight = '0'
        self.danbooru_weight = '0'
        self.yandere_weight = '0'
        self.konachan_weight = '0'
        self.original_weight = '0'
        if self.read_config():
            self.write_config()
    
    def read_config(self):
        """
        Reads in the options from the config file
        """
        try:
            f = open(cwd + '/Sourcery/config')
        except Exception as e:
            print("ERROR [0026] " + str(e))
            self.Log.write_to_log("ERROR [0026] " + str(e))
            mb.showerror("ERROR [0026]", "ERROR CODE [0026]\nSomething went wrong while accessing a configuration file(config), please try again or restart Sourcery.")
            return False
        temp = f.readline()
        if not temp.startswith('rename_pixiv='):
            f.close()
            return True
        while (not temp.startswith('END')):
            if temp.startswith('rename_pixiv='):
                self.rename_pixiv = temp[temp.find('=')+1:-1]
            elif temp.startswith('tags_pixiv='):
                self.tags_pixiv = temp[temp.find('=')+1:-1]
                self.tags_pixiv = self.tags_pixiv.replace(' /n ', '\n').replace(' /t ', '\t')
            elif temp.startswith('gen_tagfile_pixiv='):
                self.gen_tagfile_pixiv = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_pixiv_pixiv='):
                self.tagfile_pixiv_pixiv = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_danbooru_pixiv='):
                self.tagfile_danbooru_pixiv = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_yandere_pixiv='):
                self.tagfile_yandere_pixiv = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_konachan_pixiv='):
                self.tagfile_konachan_pixiv = temp[temp.find('=')+1:-1]
            elif temp.startswith('use_pixiv='):
                self.use_pixiv = temp[temp.find('=')+1:-1]
            elif temp.startswith('direct_replace_pixiv='):
                self.direct_replace_pixiv = temp[temp.find('=')+1:-1]

            elif temp.startswith('rename_danbooru='):
                self.rename_danbooru = temp[temp.find('=')+1:-1]
            elif temp.startswith('tags_danbooru='):
                self.tags_danbooru = temp[temp.find('=')+1:-1]
                self.tags_danbooru = self.tags_danbooru.replace(' /n ', '\n').replace(' /t ', '\t')
            elif temp.startswith('gen_tagfile_danbooru='):
                self.gen_tagfile_danbooru = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_pixiv_danbooru='):
                self.tagfile_pixiv_danbooru = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_danbooru_danbooru='):
                self.tagfile_danbooru_danbooru = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_yandere_danbooru='):
                self.tagfile_yandere_danbooru = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_konachan_danbooru='):
                self.tagfile_konachan_danbooru = temp[temp.find('=')+1:-1]
            elif temp.startswith('use_danbooru='):
                self.use_danbooru = temp[temp.find('=')+1:-1]
            elif temp.startswith('direct_replace_danbooru='):
                self.direct_replace_danbooru = temp[temp.find('=')+1:-1]
        
            elif temp.startswith('rename_yandere='):
                self.rename_yandere = temp[temp.find('=')+1:-1]
            elif temp.startswith('tags_yandere='):
                self.tags_yandere = temp[temp.find('=')+1:-1]
                self.tags_yandere = self.tags_yandere.replace(' /n ', '\n').replace(' /t ', '\t')
            elif temp.startswith('gen_tagfile_yandere='):
                self.gen_tagfile_yandere = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_pixiv_yandere='):
                self.tagfile_pixiv_yandere = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_danbooru_yandere='):
                self.tagfile_danbooru_yandere = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_yandere_yandere='):
                self.tagfile_yandere_yandere = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_konachan_yandere='):
                self.tagfile_konachan_yandere = temp[temp.find('=')+1:-1]
            elif temp.startswith('use_yandere='):
                self.use_yandere = temp[temp.find('=')+1:-1]
            elif temp.startswith('direct_replace_yandere='):
                self.direct_replace_yandere = temp[temp.find('=')+1:-1]

            elif temp.startswith('rename_konachan='):
                self.rename_konachan = temp[temp.find('=')+1:-1]
            elif temp.startswith('tags_konachan='):
                self.tags_konachan = temp[temp.find('=')+1:-1]
                self.tags_konachan = self.tags_konachan.replace(' /n ', '\n').replace(' /t ', '\t')     
            elif temp.startswith('gen_tagfile_konachan='):
                self.gen_tagfile_konachan = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_pixiv_konachan='):
                self.tagfile_pixiv_konachan = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_danbooru_konachan='):
                self.tagfile_danbooru_konachan = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_yandere_konachan='):
                self.tagfile_yandere_konachan = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_konachan_konachan='):
                self.tagfile_konachan_konachan = temp[temp.find('=')+1:-1]
            elif temp.startswith('use_konachan='):
                self.use_konachan = temp[temp.find('=')+1:-1]
            elif temp.startswith('direct_replace_konachan='):
                self.direct_replace_konachan = temp[temp.find('=')+1:-1]

            elif temp.startswith('minsim='):
                self.minsim = temp[temp.find('=')+1:-1]
            elif temp.startswith('imagesperpage='):
                self.imgpp = temp[temp.find('=')+1:-1]
            elif temp.startswith('input_dir='):
                self.input_dir = temp[temp.find('=')+1:-1]
            elif temp.startswith('output_dir='):
                self.output_dir = temp[temp.find('=')+1:-1]
            elif temp.startswith('delete_input='):
                self.delete_input = temp[temp.find('=')+1:-1]
            elif temp.startswith('gen_tagfile_original='):
                self.gen_tagfile_original = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_pixiv_original='):
                self.tagfile_pixiv_original = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_danbooru_original='):
                self.tagfile_danbooru_original = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_yandere_original='):
                self.tagfile_yandere_original = temp[temp.find('=')+1:-1]
            elif temp.startswith('tagfile_konachan_original='):
                self.tagfile_konachan_original = temp[temp.find('=')+1:-1]
            elif temp.startswith('saucenao_returns='):
                self.saucenao_returns = temp[temp.find('=')+1:-1]
            elif temp.startswith('direct_replace='):
                self.direct_replace = temp[temp.find('=')+1:-1]
            if temp.startswith('input_search_depth='):
                self.input_search_depth = temp[temp.find('=')+1:-1]
            elif temp.startswith('saucenao_depth='):
                self.saucenao_depth = temp[temp.find('=')+1:-1]
            elif temp.startswith('saucenao_bias='):
                self.saucenao_bias = temp[temp.find('=')+1:-1]
            elif temp.startswith('saucenao_biasmin='):
                self.saucenao_biasmin = temp[temp.find('=')+1:-1]
            elif temp.startswith('png_weight='):
                self.png_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('jpg_weight='):
                self.jpg_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('jfif_weight='):
                self.jfif_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('gif_weight='):
                self.gif_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('bmp_weight='):
                self.bmp_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('other_weight='):
                self.other_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('higher_resolution_weight='):
                self.higher_resolution_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('pixiv_weight='):
                self.pixiv_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('danbooru_weight='):
                self.danbooru_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('yandere_weight='):
                self.yandere_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('konachan_weight='):
                self.konachan_weight = temp[temp.find('=')+1:-1]
            elif temp.startswith('original_weight='):
                self.original_weight = temp[temp.find('=')+1:-1]

            temp = f.readline()
        f.close()
        return False

    def write_config(self):
        """
        Writes the current options to the config file
        """
        self.numbers_cruncher()

        self.tags_pixiv = self.tags_pixiv.replace('\n', ' /n ').replace('\t', ' /t ')
        self.tags_danbooru = self.tags_danbooru.replace('\n', ' /n ').replace('\t', ' /t ')
        self.tags_yandere = self.tags_yandere.replace('\n', ' /n ').replace('\t', ' /t ')
        self.tags_konachan = self.tags_konachan.replace('\n', ' /n ').replace('\t', ' /t ')

        conf = ("rename_pixiv=" + self.rename_pixiv +
                "\ntags_pixiv=" + self.tags_pixiv +
                "\ngen_tagfile_pixiv=" + self.gen_tagfile_pixiv +
                "\ntagfile_pixiv_pixiv=" + self.tagfile_pixiv_pixiv +
                "\ntagfile_danbooru_pixiv=" + self.tagfile_danbooru_pixiv +
                "\ntagfile_yandere_pixiv=" + self.tagfile_yandere_pixiv +
                "\ntagfile_konachan_pixiv=" + self.tagfile_konachan_pixiv +
                "\ndirect_replace_pixiv=" + self.direct_replace_pixiv +
                "\nuse_pixiv=" + self.use_pixiv +
                "\nrename_danbooru=" + self.rename_danbooru +
                "\ntags_danbooru=" + self.tags_danbooru +
                "\ngen_tagfile_danbooru=" + self.gen_tagfile_danbooru +
                "\ntagfile_pixiv_danbooru=" + self.tagfile_pixiv_danbooru +
                "\ntagfile_danbooru_danbooru=" + self.tagfile_danbooru_danbooru +
                "\ntagfile_yandere_danbooru=" + self.tagfile_yandere_danbooru +
                "\ntagfile_konachan_danbooru=" + self.tagfile_konachan_danbooru +
                "\ndirect_replace_danbooru=" + self.direct_replace_danbooru +
                "\nuse_danbooru=" + self.use_danbooru +
                "\nrename_yandere=" + self.rename_yandere +
                "\ntags_yandere=" + self.tags_yandere +
                "\ngen_tagfile_yandere=" + self.gen_tagfile_yandere +
                "\ntagfile_pixiv_yandere=" + self.tagfile_pixiv_yandere +
                "\ntagfile_danbooru_yandere=" + self.tagfile_danbooru_yandere +
                "\ntagfile_yandere_yandere=" + self.tagfile_yandere_yandere +
                "\ntagfile_konachan_yandere=" + self.tagfile_konachan_yandere +
                "\ndirect_replace_yandere=" + self.direct_replace_yandere +
                "\nuse_yandere=" + self.use_yandere +
                "\nrename_konachan=" + self.rename_konachan +
                "\ntags_konachan=" + self.tags_konachan +
                "\ngen_tagfile_konachan=" + self.gen_tagfile_konachan +
                "\ntagfile_pixiv_konachan=" + self.tagfile_pixiv_konachan +
                "\ntagfile_danbooru_konachan=" + self.tagfile_danbooru_konachan +
                "\ntagfile_yandere_konachan=" + self.tagfile_yandere_konachan +
                "\ntagfile_konachan_konachan=" + self.tagfile_konachan_konachan +
                "\ndirect_replace_konachan=" + self.direct_replace_konachan +
                "\nuse_konachan=" + self.use_konachan +
                "\nminsim=" + self.minsim +
                "\nimagesperpage=" + self.imgpp +
                "\ntags_yandere=" + self.tags_yandere +
                "\ntags_konachan=" + self.tags_konachan +
                "\ninput_dir=" + self.input_dir +
                "\noutput_dir=" + self.output_dir +
                "\ndelete_input=" + self.delete_input +
                "\ngen_tagfile_original=" + self.gen_tagfile_original +
                "\ntagfile_pixiv_original=" + self.tagfile_pixiv_original +
                "\ntagfile_danbooru_original=" + self.tagfile_danbooru_original +
                "\ntagfile_yandere_original=" + self.tagfile_yandere_original +
                "\ntagfile_konachan_original=" + self.tagfile_konachan_original +
                "\nsaucenao_returns=" + self.saucenao_returns +
                "\ndirect_replace=" + self.direct_replace +
                "\ninput_search_depth=" + self.input_search_depth +
                "\nsaucenao_depth=" + self.saucenao_depth +
                "\nsaucenao_bias=" + self.saucenao_bias +
                "\nsaucenao_biasmin=" + self.saucenao_biasmin +
                "\npng_weight=" + self.png_weight +
                "\njpg_weight=" + self.jpg_weight +
                "\njfif_weight=" + self.jfif_weight +
                "\ngif_weight=" + self.gif_weight +
                "\nbmp_weight=" + self.bmp_weight +
                "\nother_weight=" + self.other_weight +
                "\nhigher_resolution_weight=" + self.higher_resolution_weight +
                "\npixiv_weight=" + self.pixiv_weight +
                "\ndanbooru_weight=" + self.danbooru_weight +
                "\nyandere_weight=" + self.yandere_weight +
                "\nkonachan_weight=" + self.konachan_weight +
                "\noriginal_weight=" + self.original_weight +
                "\n\nEND")
        try:
            f = open(cwd + '/Sourcery/config', 'w')
            f.write(conf)
        except Exception as e:
            print("ERROR [0025] " + str(e))
            self.Log.write_to_log("ERROR [0025] " + str(e))
            mb.showerror("ERROR [0025]", "ERROR CODE [0025]\nSomething went wrong while accessing a configuration file(config), please try again or restart Sourcery.")
            return
        f.close()
        self.read_config()

    def numbers_cruncher(self):
        try:
            temp_num = int(self.minsim)
            if temp_num < 0 or temp_num > 100:
                mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the Minimum similarity option')
                self.minsim = '80'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the Minimum similarity option')
            self.minsim = '80'
        try:
            temp_num = int(self.direct_replace)
            if temp_num < 0 or temp_num > 100:
                mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the Direct Replace option')
                self.direct_replace = '100'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the Direct Replace option')
            self.direct_replace = '100'
        try:
            temp_num = int(self.imgpp)
            if temp_num < 1 or temp_num > 1000:
                mb.showerror('Invalid Value', 'Please insert a value between 1 and 1000 into the Images per page option')
                self.imgpp = '12'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 1 and 1000 into the Images per page option')
            self.imgpp = '12'
        try:
            temp_num = int(self.saucenao_returns)
            if temp_num < 1:
                mb.showerror('Invalid Value', 'Please insert a value between 1 and 100 into the SauceNao Returns option')
                self.saucenao_returns = '10'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 1 and infinite into the SauceNao Returns option')
            self.saucenao_returns = '10'
        try:
            temp_num = int(self.input_search_depth)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between -1 and infinite into the SauceNao Returns option')
            self.input_search_depth = '1'
        try:
            temp_num = int(self.saucenao_depth)
            if temp_num < 0:
                mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the SauceNao depth option')
                self.saucenao_depth = '128'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 0 and infinite into the SauceNao depth option')
            self.saucenao_depth = '128'
        try:
            temp_num = int(self.saucenao_bias)
            if temp_num < 0 or temp_num > 100:
                mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the SauceNao bias option')
                self.saucenao_bias = '15'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the SauceNao bias option')
            self.saucenao_bias = '15'
        try:
            temp_num = int(self.saucenao_biasmin)
            if temp_num < 0 or temp_num > 100:
                mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the SauceNao biasmin option')
                self.saucenao_biasmin = '70'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the SauceNao biasmin option')
            self.saucenao_biasmin = '70'
        try:
            temp_num = int(self.png_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the png weight option')
            self.png_weight = '0'
        try:
            temp_num = int(self.jpg_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the jpg weight option')
            self.jpg_weight = '0'
        try:
            temp_num = int(self.jfif_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the jfif weight option')
            self.jfif_weight = '0'
        try:
            temp_num = int(self.gif_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the gif weight option')
            self.gif_weight = '0'
        try:
            temp_num = int(self.bmp_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the bmp weight option')
            self.bmp_weight = '0'
        try:
            temp_num = int(self.other_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the other weight option')
            self.other_weight = '0'
        try:
            temp_num = int(self.higher_resolution_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the Higher resolution weight option')
            self.higher_resolution_weight = '0'
        try:
            temp_num = int(self.pixiv_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the Pixiv weight option')
            self.pixiv_weight = '0'
        try:
            temp_num = int(self.danbooru_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the Danbooru weight option')
            self.danbooru_weight = '0'
        try:
            temp_num = int(self.yandere_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the Yandere weight option')
            self.yandere_weight = '0'
        try:
            temp_num = int(self.konachan_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the Konachan weight option')
            self.konachan_weight = '0'
        try:
            temp_num = int(self.original_weight)
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert an integer value into the Original weight option')
            self.original_weight = '0'

class ReferenceFile():
    """Includes methods to add a new reference, read these from the reference file or delete its contents"""
    def __init__(self, log):
        self.Log = log # TODO self.refs to delete duplicate refs

    def new_reference(self, old_name, pixiv_list, danbooru_list, yandere_list, konachan_list, rename_pixiv, rename_danbooru, rename_yandere, rename_konachan, minsim, dict_list, input_path):
        """
        Appends a new image reference to the reference file
        """
        pixiv_ref = "["
        if len(pixiv_list) == 0:
            pixiv_ref = "[]"
        else:
            for elem in pixiv_list:
                pixiv_ref = (pixiv_ref + 
                            "{\"new_name\" : \"" + elem[0] +
                            "\", \"id\" : \"" + str(elem[1]) +
                            "\"}, ")
            pixiv_ref = pixiv_ref[:-2] + "]"
        danbooru_ref = "["
        if len(danbooru_list) == 0:
            danbooru_ref = "[]"
        else:
            for elem in danbooru_list:
                danbooru_ref = (danbooru_ref + 
                            "{\"new_name\" : \"" + elem[0] +
                            "\", \"id\" : \"" + str(elem[1]) +
                            "\"}, ")
            danbooru_ref = danbooru_ref[:-2] + "]"
        yandere_ref = "["
        if len(yandere_list) == 0:
            yandere_ref = "[]"
        else:
            for elem in yandere_list:
                yandere_ref = (yandere_ref + 
                            "{\"new_name\" : \"" + elem[0] +
                            "\", \"id\" : \"" + str(elem[1]) +
                            "\"}, ")
            yandere_ref = yandere_ref[:-2] + "]"
        konachan_ref = "["
        if len(konachan_list) == 0:
            konachan_ref = "[]"
        else:
            for elem in konachan_list:
                konachan_ref = (konachan_ref + 
                            "{\"new_name\" : \"" + elem[0] +
                            "\", \"id\" : \"" + str(elem[1]) +
                            "\"}, ")
            konachan_ref = konachan_ref[:-2] + "]"
        ref = ("{\"old_name\" : \"" + old_name +
                "\", \"pixiv\" : " + pixiv_ref +
                ", \"danbooru\" : " + danbooru_ref +
                ", \"yandere\" : " + yandere_ref +
                ", \"konachan\" : " + konachan_ref +
                ", \"rename_pixiv\" : \"" + rename_pixiv +
                "\", \"rename_danbooru\" : \"" + rename_danbooru +
                "\", \"rename_yandere\" : \"" + rename_yandere +
                "\", \"rename_konachan\" : \"" + rename_konachan +
                "\", \"minsim\" : " + str(minsim) +
                ", \"dict_list\" : " + str(dict_list).replace("'", "\"").replace("\\", "/") +
                ", \"input_path\" : \"" + input_path.replace("\\", "/") +
                "\"}\n")
        try:
            f = open(cwd + '/Sourcery/reference', 'a')
            f.write(ref)
        except Exception as e:
            print("ERROR [0033] " + str(e))
            #self.Log.write_to_log("ERROR [0033] " + str(e))
            #mb.showerror("ERROR [0033]", "ERROR CODE [0033]\nSomething went wrong while accessing a configuration file(reference).")
            return
        f.close()

    def read_reference(self):
        """
        Reads in all references from the reference file
        Returns a list of reference dicionaries.
        """
        try:
            f = open(cwd + '/Sourcery/reference')
        except Exception as e:
            print("ERROR [0034] " + str(e))
            #self.Log.write_to_log("ERROR [0034] " + str(e))
            #mb.showerror("ERROR [0034]", "ERROR CODE [0034]\nSomething went wrong while accessing a configuration file(reference), please try again.")
            return False
        return_array = list()

        temp = f.readline()
        if not temp.startswith('{'):
            f.close()
            return False
        while (temp.startswith('{')):
            return_array.append(loads(temp[:-1]))
            temp = f.readline()
        f.close()
        #print(str(return_array))
        return return_array

    def clean_reference(self):
        """
        Deletes the content of the reference file
        """
        try:
            f = open(cwd + '/Sourcery/reference', 'w')
        except Exception as e:
            print("ERROR [0035] " + str(e))
            #self.Log.write_to_log("ERROR [0035] " + str(e))
            #mb.showerror("ERROR [0035]", "ERROR CODE [0035]\nSomething went wrong while accessing a configuration file(reference), please try again.")
            return
        f.close()

if __name__ == "__main__":
    Ref = ReferenceFile(None)
    Ref.new_reference('a', 'b', 1)
    Ref.new_reference('x', 'y', 2)
    Ref.read_reference()
    Ref.clean_reference()