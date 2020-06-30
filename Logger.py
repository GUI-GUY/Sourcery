from os import getcwd
import logging as log
from tkinter import END, Text
from time import strftime

class Logger():
    """Includes the log text frame on the startpage and also methods to write these to the log file"""
    def __init__(self):
        self.log_text = None

    def init_log(self):
        self.log_text.configure(state='normal')
        self.log_text.insert(END, '\nSourcery started. Date: ' + strftime("20%y|%m|%d") + ' Time: ' + strftime("%H:%M:%S") + '\n')
        self.log_text.configure(state='disabled')

        f = open(getcwd() + '/Sourcery/sourcery.log', 'a')
        f.write('\nSourcery started. Date: ' + strftime("20%y-%m-%d") + ' Time: ' + strftime("%H:%M:%S") + '\n') #TODO
        f.close()
        log.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S', filename= getcwd() + '/Sourcery/sourcery.log', level=log.DEBUG)#TODO

    def write_to_log(self, message = '', mode = 0, in_log_text = True):
        if in_log_text:
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