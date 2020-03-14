from os import makedirs, path, getcwd
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
        self.custom_background = '#101010'
        self.custom_foreground = 'white'
        self.custom_button_background = 'purple'
        self.custom_button_background_active = 'yellow'
        self.custom_button_foreground_active = 'black'
        self.custom_button_background_pressed = '#fff'
        self.custom_button_foreground_pressed = 'green'
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
            "\n\nLight Theme"
            "\nbackground=#eee"
            "\nforeground=black"
            "\nbutton_background=#aaa"
            "\nbutton_background_active=black"
            "\nbutton_foreground_active=white"
            "\nbutton_background_pressed=#ddd"
            "\nbutton_foreground_pressed=black"
            "\n\nCustom Theme"
            "\nbackground=" + self.custom_background +
            "\nforeground=" + self.custom_foreground +
            "\nbutton_background=" + self.custom_button_background +
            "\nbutton_background_active=" + self.custom_button_background_active +
            "\nbutton_foreground_active=" + self.custom_button_foreground_active +
            "\nbutton_background_pressed=" + self.custom_button_background_pressed +
            "\nbutton_foreground_pressed=" + self.custom_button_foreground_pressed +
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
        self.pixiv_username = ''
        self.pixiv_password = ''
        self.pixiv_refreshtoken = ''
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
            if creds == 'Pixiv\n':
                creds = f.readline()
                self.pixiv_username = creds[creds.find('=')+1:-1]
                creds = f.readline()
                self.pixiv_password = creds[creds.find('=')+1:-1]
                creds = f.readline()
                self.pixiv_refreshtoken = creds[creds.find('=')+1:-1]
            creds = f.readline()
        f.close()
        return False

    def write_credentials(self):
        """
        Writes credentials to the credentials file
        """
        creds = ("SauceNao"
                "\nAPI-Key=" + self.saucenao_api_key +
                "\n\nPixiv"
                "\nUsername=" + self.pixiv_username +
                "\nPassword=" + self.pixiv_password +
                "\nrefreshtoken=" + self.pixiv_refreshtoken +
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
        #self.init_log()

    def init_log(self):
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
    
    def write_to_log(self, message = ''):
        if message != '':
            try:
                self.log.write('[' + strftime("%H:%M:%S") + '] ' + message + '\n')
                self.log.flush()
                self.log_text.configure(state='normal')
                self.log_text.insert(END,'[' + strftime("%H:%M:%S") + '] ' + message + '\n')
                self.log_text.configure(state='disabled')
            except Exception as e:
                print("ERROR [0036] " + str(e))
                #self.Log.write_to_log("ERROR [0033] " + str(e))
                mb.showerror("ERROR [0036]", "ERROR CODE [0036]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery as soon as possible.")

class ConfigFile():
    """Includes the options and also methods to write/read these to/from the config file"""
    def __init__(self, log):
        self.Log = log
        self.rename_pixiv = 'False'
        self.rename_danbooru = 'False'
        self.minsim = '80'
        self.imgpp = '12'
        self.tags_danbooru = ''
        self.tags_pixiv = ''
        self.input_dir = cwd + '/Input'
        self.output_dir = cwd + '/Output'
        self.delete_input = '0'
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
            if temp.startswith('rename_danbooru='):
                self.rename_danbooru = temp[temp.find('=')+1:-1]
            if temp.startswith('minsim='):
                self.minsim = temp[temp.find('=')+1:-1]
            if temp.startswith('imagesperpage='):
                self.imgpp = temp[temp.find('=')+1:-1]
            if temp.startswith('tags_danbooru='):
                self.tags_danbooru = temp[temp.find('=')+1:-1]
                self.tags_danbooru = self.tags_danbooru.replace(' /n ', '\n').replace(' /t ', '\t')
            if temp.startswith('tags_pixiv='):
                self.tags_pixiv = temp[temp.find('=')+1:-1]
                self.tags_pixiv = self.tags_pixiv.replace(' /n ', '\n').replace(' /t ', '\t')
            if temp.startswith('input_dir='):
                self.input_dir = temp[temp.find('=')+1:-1]
            if temp.startswith('output_dir='):
                self.output_dir = temp[temp.find('=')+1:-1]
            if temp.startswith('delete_input='):
                self.delete_input = temp[temp.find('=')+1:-1]  
            temp = f.readline()
        f.close()
        return False

    def write_config(self):
        """
        Writes the current options to the config file
        """
        try:
            temp_num = int(self.minsim)
            if temp_num < 0 or temp_num > 100:
                mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the Minimum similarity option')
                self.minsim = '80'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 0 and 100 into the Minimum similarity option')
            self.minsim = '80'
        try:
            temp_num = int(self.imgpp)
            if temp_num < 0 or temp_num > 1000:
                mb.showerror('Invalid Value', 'Please insert a value between 0 and 1000 into the Images per page option')
                self.imgpp = '12'
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a value between 0 and 1000 into the Images per page option')
            self.imgpp = '12'

        self.tags_danbooru = self.tags_danbooru.replace('\n', ' /n ').replace('\t', ' /t ')
        self.tags_pixiv = self.tags_pixiv.replace('\n', ' /n ').replace('\t', ' /t ')

        conf = ("rename_pixiv=" + self.rename_pixiv +
                "\nrename_danbooru=" + self.rename_danbooru +
                "\nminsim=" + self.minsim +
                "\nimagesperpage=" + self.imgpp +
                "\ntags_danbooru=" + self.tags_danbooru +
                "\ntags_pixiv=" + self.tags_pixiv +
                "\ninput_dir=" + self.input_dir +
                "\noutput_dir=" + self.output_dir +
                "\ndelete_input=" + self.delete_input +
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

class ReferenceFile():
    """Includes methods to add a new reference, read these from the reference file or delete its contents"""
    def __init__(self, log):
        self.Log = log

    def new_reference(self, old_name, new_name_pixiv, id_pixiv, new_name_danb, id_danb, rename_pixiv, rename_danbooru, minsim):
        """
        Appends a new image reference to the reference file
        """
        ref = ("{\"old_name\" : \"" + old_name +
                "\", \"new_name_pixiv\" : \"" + new_name_pixiv +
                "\", \"id_pixiv\" : " + str(id_pixiv) +
                ", \"new_name_danb\" : \"" + new_name_danb +
                "\", \"id_danb\" : " + str(id_danb) +
                ", \"rename_pixiv\" : \"" + rename_pixiv +
                "\", \"rename_danbooru\" : \"" + rename_danbooru +
                "\", \"minsim\" : " + str(minsim) +
                "}\n")
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