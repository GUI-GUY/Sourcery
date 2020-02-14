from os import makedirs, path, getcwd
from tkinter import messagebox as mb
from time import strftime

cwd = getcwd()

class Files():
    """PixivOptions"""
    def __init__(self):
        self.create_files()
        self.Log = LogFile()
        self.Theme = ThemeFile(self.Log)
        self.Cred = CredFile(self.Log)
        self.Conf = ConfigFile(self.Log)
        
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
            #self.Log.write_to_log("ERROR [0007] " + str(e))
            mb.showerror("ERROR [0007]", "ERROR CODE [0007]\nSomething went wrong while creating directories, please restart Sourcery.")

    def init_configs(self):#TODO
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
        self.custom_button_background = 'purple'
        self.custom_button_background_active = 'yellow'
        self.custom_button_foreground_active = 'black'
        self.custom_button_background_pressed = '#111'
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

        creds = f.readline()
        if creds != 'SauceNao\n':
            f.close()
            return True
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
        return False

    def write_credentials(self):
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

class ConfigFile():
    def __init__(self, log):
        self.Log = log
        self.rename_pixiv = ''
        self.minsim = ''
        if self.read_config():
            self.write_config()
    
    def read_config(self):
        try:
            f = open(cwd + '/Sourcery/credentials')
        except Exception as e:
            print("ERROR [0026] " + str(e))
            self.Log.write_to_log("ERROR [0026] " + str(e))
            mb.showerror("ERROR [0026]", "ERROR CODE [0026]\nSomething went wrong while accessing a configuration file(config), please try again.")
        
        temp = f.readline()
        if not temp.startswith('rename_pixiv='):
            f.close()
            return True
        while(temp != 'END\n'):
            if temp.startswith('rename_pixiv='):
                self.rename_pixiv = temp[temp.find('=')+1:-1]
            if temp.startswith('minsim='):
                self.minsim = temp[temp.find('=')+1:-1]
            temp = f.readline()
        f.close()
        return False

    def write_config(self):
        conf = ("rename_pixiv=" + self.rename_pixiv +
                "\nminsim=" + self.minsim +
                "\n\nEND")

        try:
            f = open(cwd + '/Sourcery/config', 'w')
            f.write(conf)
        except Exception as e:
            print("ERROR [0025] " + str(e))
            self.Log.write_to_log("ERROR [0025] " + str(e))
            mb.showerror("ERROR [0025]", "ERROR CODE [0025]\nSomething went wrong while accessing a configuration file(config), please try again.")

        f.close()
        self.read_config()