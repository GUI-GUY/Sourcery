from os import makedirs, path, getcwd
from sys import stderr
from configparser import ConfigParser
import logging as log
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
        self.Log = LogText()
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
            makedirs(cwd + "/Sourcery/sourced_progress/gelbooru", 0o777, True)
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
        self.theme = ConfigParser()

        self.theme.add_section('General')
        self.theme.add_section('Dark Theme')
        self.theme.add_section('Light Theme')
        self.theme.add_section('Custom Theme')
    
        self.theme['Dark Theme'] = {
            "background" : '#252525',
            "foreground" : '#ddd',
            "selected_background" : 'grey',
            "button_background" : '#444',
            "button_background_active" : 'white',
            "button_foreground_active" : 'black',
            "button_background_pressed" : '#111',
            "button_foreground_pressed" : 'white',
            "checkbutton_pressed" : 'green'
        }

        self.theme['Light Theme'] = {
            "background" : '#eee',
            "foreground" : 'black',
            "selected_background" : 'grey',
            "button_background" : '#aaa',
            "button_background_active" : 'black',
            "button_foreground_active" : 'white',
            "button_background_pressed" : '#ddd',
            "button_foreground_pressed" : 'black',
            "checkbutton_pressed" : 'green'
        }

        self.theme['Custom Theme'] = {
            "background" : '#1f1f1f',
            "foreground" : 'white',
            "selected_background" : 'grey',
            "button_background" : 'purple',
            "button_background_active" : '#dd64d3',
            "button_foreground_active" : 'black',
            "button_background_pressed" : '#fff',
            "button_foreground_pressed" : 'blue',
            "checkbutton_pressed" : 'green'
        }

        self.theme['General'] = {
            "current" : 'Dark Theme'
        }

        if path.isfile(cwd + '/Sourcery/theme.cfg'):
            self.theme.read_file(open(cwd + '/Sourcery/theme.cfg'))#TODO

        self.write_theme()

    def write_theme(self):
        self.theme.write(open(cwd + '/Sourcery/theme.cfg', 'w'))#TODO

class LogText():
    """Includes the log text frame on the startpage and also methods to write these to the log file"""
    def __init__(self):
        self.log_text = None

    def init_log(self):
        self.log_text.configure(state='normal')
        self.log_text.insert(END, '\nSourcery started. Date: ' + strftime("20%y|%m|%d") + ' Time: ' + strftime("%H:%M:%S") + '\n')
        self.log_text.configure(state='disabled')

    def write_to_log(self, message = '', mode = 0):
        self.log_text.configure(state='normal')
        self.log_text.insert(END,'[' + strftime("%H:%M:%S") + '] ' + message + '\n')
        self.log_text.configure(state='disabled')

        if mode == log.DEBUG:
            log.debug(message)
        elif mode == log.INFO:
            log.info(message)
        elif mode == log.WARNING:
            log.warning(message)
        elif mode == log.ERROR:
            log.error(message)
        elif mode == log.CRITICAL:
            log.critical(message)

class ReferenceFile():
    """Includes methods to add a new reference, read these from the reference file or delete its contents"""
    def __init__(self, log):
        self.Log = log
        self.refs = list()
        if self.read_reference():
            self.write_reference()

    def new_reference(self, old_name, pixiv_list, danbooru_list, yandere_list, konachan_list, gelbooru_list, rename_pixiv, rename_danbooru, rename_yandere, rename_konachan, rename_gelbooru, minsim, dict_list, input_path):
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
        gelbooru_ref = "["
        if len(gelbooru_list) == 0:
            gelbooru_ref = "[]"
        else:
            for elem in gelbooru_list:
                gelbooru_ref = (gelbooru_ref + 
                            "{\"new_name\" : \"" + elem[0] +
                            "\", \"id\" : \"" + str(elem[1]) +
                            "\"}, ")
            gelbooru_ref = gelbooru_ref[:-2] + "]"
        ref = ("{\"old_name\" : \"" + old_name +
                "\", \"pixiv\" : " + pixiv_ref +
                ", \"danbooru\" : " + danbooru_ref +
                ", \"yandere\" : " + yandere_ref +
                ", \"konachan\" : " + konachan_ref +
                ", \"gelbooru\" : " + gelbooru_ref +
                ", \"rename_pixiv\" : \"" + rename_pixiv +
                "\", \"rename_danbooru\" : \"" + rename_danbooru +
                "\", \"rename_yandere\" : \"" + rename_yandere +
                "\", \"rename_konachan\" : \"" + rename_konachan +
                "\", \"rename_gelbooru\" : \"" + rename_gelbooru +
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

    def clean_reference(self, clear_list=False):
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
        if clear_list:
            self.refs.clear()


if __name__ == "__main__":
    Ref = ReferenceFile(None)
    Ref.new_reference('a', 'b', 1)
    Ref.new_reference('x', 'y', 2)
    Ref.read_reference()
    Ref.clean_reference()