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
        if not path.exists(cwd + '/Sourcery/log'):
            try:
                log = open(cwd + '/Sourcery/log', 'x')
                log.close()
            except Exception as e:
                print("ERROR [0024] " + str(e))
                #self.Log.write_to_log("ERROR [0024] " + str(e))
                mb.showerror("ERROR [0024]", "ERROR CODE [0024]\nSomething went wrong while accessing a configuration file(log), please restart Sourcery.")
        if not path.exists(cwd + '/Sourcery/config.cfg'):
            try:
                config = open(cwd + '/Sourcery/config.cfg', 'x')
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
        self.custom_background = '#1f1f1f'
        self.custom_foreground = 'white'
        self.custom_button_background = 'purple'
        self.custom_button_background_active = '#dd64d3'
        self.custom_button_foreground_active = 'black'
        self.custom_button_background_pressed = '#fff'
        self.custom_button_foreground_pressed = 'blue'
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

class ReferenceFile():
    """Includes methods to add a new reference, read these from the reference file or delete its contents"""
    def __init__(self, log):
        self.Log = log
        self.refs = list()
        if self.read_reference():
            self.write_reference()

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
        
        self.refs.append(loads(ref))
        self.append_reference(ref)
        return loads(ref)
    
    def append_reference(self, ref):
        try:
            f = open(cwd + '/Sourcery/reference', 'a')
            f.write(ref)
        except Exception as e:
            print("ERROR [0033] " + str(e))
            #self.Log.write_to_log("ERROR [0033] " + str(e))
            #mb.showerror("ERROR [0033]", "ERROR CODE [0033]\nSomething went wrong while accessing a configuration file(reference).")
            return
        f.close()

    def write_reference(self):
        self.clean_reference()
        try:
            f = open(cwd + '/Sourcery/reference', 'a')
            for ref in self.refs:
                f.write(str(ref).replace("'", "\"") + '\n')
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

        temp = f.readline()
        if not temp.startswith('{'):
            f.close()
            return False
        while (temp.startswith('{')):
            ref = loads(temp[:-1])
            if ref not in self.refs:
                self.refs.append(ref)
            temp = f.readline()
        f.close()
        return True
        #print(str(return_array))
        #return return_array

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
        self.refs.clear()

if __name__ == "__main__":
    Ref = ReferenceFile(None)
    Ref.new_reference('a', 'b', 1)
    Ref.new_reference('x', 'y', 2)
    Ref.read_reference()
    Ref.clean_reference()