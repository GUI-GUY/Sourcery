from os import listdir
from tkinter import IntVar, StringVar, E, W, colorchooser, Text, END
from tkinter import messagebox as mb
from tkinter.ttk import Label, Checkbutton, Button, Style, Entry, Frame, OptionMenu
from functools import partial
from webbrowser import open_new
#from pixiv_handler import pixiv_login
from file_operations import change_input, change_output, is_input_int_digit
from WeightSystem import WeightSystem
from ScrollFrame import ScrollFrame
import global_variables as gv

class Options():
    """Hosts all Options classes and methods to switch between the options views"""
    def __init__(self, parent, enforce_style, leftovers):
        self.par = parent
        self.NAOO = SauceNaoOptions(parent)
        self.SouO = SourceryOptions(parent, enforce_style, leftovers)
        self.ProO = ProviderOptions(parent)
        self.Debug = Debugging(parent, self)
        self.options_lbl = Label(parent, text="Options", font=("Arial Bold", 20), style="label.TLabel")

        self.provider_options_btn = Button(parent, text="Provider", command=self.display_provider_options, style="button.TLabel")
        self.saucenao_options_btn = Button(parent, text="SauceNao", command=self.display_saucenao_options, style="button.TLabel")
        self.sourcery_options_btn = Button(parent, text="Sourcery", command=self.display_sourcery_options, style="button.TLabel")
        self.debug_btn = Button(parent, text="Debug", command=self.display_debug, style="button.TLabel")

        self.options_back_btn = Button(parent, text="Back", command=gv.display_startpage, style="button.TLabel")

        if gv.config['Debug']['show'] == '1':
            self.debug_counter = 10
        else:
            self.debug_counter = 0

    def display_saucenao_options(self):
        """
        Draw 
        """
        if self.debug_counter < 10:
            self.debug_counter += 1
        else:
            gv.config['Debug']['show'] = '1'
            gv.write_config()
            self.saucenao_options_btn.place(x = int(gv.width/160*35), y = int(gv.height/90*5))
        self.forget_all_widgets()
        self.display_basic_options()
        self.NAOO.display()

    def display_sourcery_options(self):
        """
        Draw
        """
        self.forget_all_widgets()
        self.display_basic_options()
        self.SouO.display()

    def display_provider_options(self):
        """
        Draw 
        """
        self.forget_all_widgets()
        self.display_basic_options()
        self.ProO.display()

    def display_basic_options(self):
        """
        Draws options widgets that are shown on all options pages.
        """
        gv.esc_op = False
        self.options_lbl.place(x = int(gv.width/160*5), y = int(gv.height/90))

        self.sourcery_options_btn.place(x = int(gv.width/160*5), y = int(gv.height/90*5))
        self.provider_options_btn.place(x = int(gv.width/160*15), y = int(gv.height/90*5))
        self.saucenao_options_btn.place(x = int(gv.width/160*25), y = int(gv.height/90*5))
        if self.debug_counter == 10:
            self.debug_btn.place(x = int(gv.width/160*35), y = int(gv.height/90*5))

        self.options_back_btn.place(x = int(gv.width/160*5), y = gv.height-170)

    def display_debug(self):
        """
        Draw 
        """
        self.forget_all_widgets()
        self.display_basic_options()
        self.Debug.display()

    def forget_all_widgets(self):
        for widget in self.par.winfo_children():
            widget.place_forget()

class Debugging():
    """Includes all widgets for Debugging and methods to display and modify them"""
    def __init__(self, parent, lord):
        self.par = parent
        self.lord = lord

        self.code_txt = Text(parent, width=int(gv.width/20), height=int(gv.height/30), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
        self.code_txt.insert(END, gv.config['Debug']['code'])
        self.execute_btn = Button(parent, text="Execute", command=self.execute, style="button.TLabel")
        self.debug_btn = Button(parent, text="Disable Debug mode", command=self.disable_debug, style="button.TLabel")
    
    def display(self):
        self.debug_btn.place(x = int(gv.width/160*5), y = int(gv.height/90*8))
        self.execute_btn.place(x = int(gv.width/160*5), y = int(gv.height/90*12))
        self.code_txt.place(x = int(gv.width/160*5), y = int(gv.height/90*15))
        

    def disable_debug(self):
        self.lord.debug_counter = 0
        gv.config['Debug']['show'] = '0'
        gv.write_config()
        self.lord.forget_all_widgets()
        self.lord.display_basic_options()
        self.lord.NAOO.display()
    
    def execute(self):
        txt = self.code_txt.get('1.0', END)
        gv.config['Debug']['code'] = txt
        gv.write_config()
        try:
            exec(txt)
        except Exception as e:
            print(e)

class SauceNaoOptions():
    """Includes all widgets for SauceNao and methods to display and modify them"""
    def __init__(self, parent):
        self.par = parent
        vcmd = (parent.register(is_input_int_digit))
        self.saucenao_key_lbl = Label(parent, text="SauceNao API-Key", style="label.TLabel")
        self.saucenao_key_number_lbl = Label(parent, width=50, text=gv.config['SauceNAO']['api_key'], style="button.TLabel")
        self.saucenao_key_entry = Entry(parent, width=52, style="button.TLabel")
        self.saucenao_key_change_btn = Button(parent, text="Change", command=self.saucenao_change_key, style="button.TLabel")
        self.saucenao_key_confirm_btn = Button(parent, text="Confirm", command=self.saucenao_set_key, style="button.TLabel")
        self.saucenao_minsim_lbl = Label(parent, text="Minimum similarity:", style="label.TLabel")
        self.saucenao_minsim_note_lbl = Label(parent, text="[default: 80]", style="label.TLabel")
        self.saucenao_minsim_entry = Entry(parent, width=10, validate='all', validatecommand=(vcmd, '%P', False, 0, 100), style="button.TLabel")
        self.saucenao_minsim_entry.insert(0, gv.config['SauceNAO']['minsim'])
        self.saucenao_save_btn = Button(parent, text="Save", command=self.saucenao_save, style="button.TLabel")

        self.saucenao_address_1_lbl = Label(parent, text="Your API-Key can be found here:", style="label.TLabel")
        self.saucenao_address_2_lbl = Label(parent, text="https://saucenao.com/user.php?page=search-api", style="label.TLabel")
        self.saucenao_address_2_lbl.configure(foreground='#2626ff', cursor='hand2', font=('Arial', 10))
        self.saucenao_address_2_lbl.bind("<Button-1>", self.hyperlink)

        self.saucenao_returns_lbl = Label(parent, text="Results:", font=("Arial Bold", 10), style="label.TLabel")
        self.saucenao_returns_note_lbl = Label(parent, text="[default: 10] Number of results to return. More results is slower. Should be at least 2 times the services you use.", font=("Arial Bold", 10), style="label.TLabel")
        self.saucenao_returns_entry = Entry(parent, width=10, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.saucenao_returns_entry.insert(0, gv.config['SauceNAO']['returns'])

        self.saucenao_depth_lbl = Label(parent, text="Depth:", style="label.TLabel")
        self.saucenao_bias_lbl = Label(parent, text="Bias:", style="label.TLabel")
        self.saucenao_biasmin_lbl = Label(parent, text="Biasmin:", style="label.TLabel")
        self.saucenao_depth_note_lbl = Label(parent, text="[default: 128] Search depth, deeper searches are slower but can pull out additional matches.", style="label.TLabel")
        self.saucenao_bias_note_lbl = Label(parent, text="[default: 15] Max similarity yield modifier.", style="label.TLabel")
        self.saucenao_biasmin_note_lbl = Label(parent, text="[default: 70] Min similarity to activate priority yield mode.", style="label.TLabel")
        self.saucenao_depth_entry = Entry(parent, width=10, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.saucenao_depth_entry.insert(0, gv.config['SauceNAO']['depth'])
        self.saucenao_bias_entry = Entry(parent, width=10, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.saucenao_bias_entry.insert(0, gv.config['SauceNAO']['bias'])
        self.saucenao_biasmin_entry = Entry(parent, width=10, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.saucenao_biasmin_entry.insert(0, gv.config['SauceNAO']['biasmin'])
    
    def display(self):
        """
        Draw options (API-Key, minsim) for SauceNao:
        """
        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*20)
        x3 = int(gv.width/160*27)
        x4 = int(gv.width/160*58)

        self.saucenao_key_lbl.place(x = x1, y = y + c * 1)
        self.saucenao_key_number_lbl.place(x = x2, y = y + c * 1)
        self.saucenao_key_change_btn.place(x = x4, y = y + c * 1)
        
        
        self.saucenao_address_1_lbl.place(x = x1, y = y + c * 2)
        self.saucenao_address_2_lbl.place(x = x3, y = y + c * 2)

        self.saucenao_minsim_lbl.place(x = x1, y = y + c * 4)
        self.saucenao_minsim_entry.place(x = x2, y = y + c * 4)
        self.saucenao_minsim_note_lbl.place(x = x3, y = y + c * 4)

        self.saucenao_returns_lbl.place(x = x1, y = y + c * 5)
        self.saucenao_returns_entry.place(x = x2, y = y + c * 5)
        self.saucenao_returns_note_lbl.place(x = x3, y = y + c * 5)

        self.saucenao_depth_lbl.place(x = x1, y = y + c * 6)
        self.saucenao_depth_entry.place(x = x2, y = y + c * 6)
        self.saucenao_depth_note_lbl.place(x = x3, y = y + c * 6)

        self.saucenao_bias_lbl.place(x = x1, y = y + c * 7)
        self.saucenao_bias_entry.place(x = x2, y = y + c * 7)
        self.saucenao_bias_note_lbl.place(x = x3, y = y + c * 7)

        self.saucenao_biasmin_lbl.place(x = x1, y = y + c * 8)
        self.saucenao_biasmin_entry.place(x = x2, y = y + c * 8)
        self.saucenao_biasmin_note_lbl.place(x = x3, y = y + c * 8)

        self.saucenao_save_btn.place(x = x1, y = y + c * 10)
    
    def saucenao_change_key(self):
        """
        Unlock API-Key widget for SauceNao, so that you can change your API-Key. 
        """
        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*20)
        x3 = int(gv.width/160*27)
        x4 = int(gv.width/160*58)
        self.saucenao_key_change_btn.place_forget()
        self.saucenao_key_number_lbl.place_forget()
        self.saucenao_key_confirm_btn.place(x = x4, y = y + c * 1)
        self.saucenao_key_entry.place(x = x2, y = y + c * 1)
        self.saucenao_key_entry.delete(0, len(gv.config['SauceNAO']['api_key']))
        self.saucenao_key_entry.insert(0, gv.config['SauceNAO']['api_key'])
        
    def saucenao_set_key(self):
        """
        Save SauceNao API-Key and revert the widget to being uneditable.
        """
        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*20)
        x3 = int(gv.width/160*27)
        x4 = int(gv.width/160*58)
        gv.Files.Log.write_to_log('Saving SauceNao API-Key')
        gv.config['SauceNAO']['api_key'] = self.saucenao_key_entry.get()
        e = gv.write_config()
        if e == None:
            gv.Files.Log.write_to_log('Saved SauceNao API-Key successfully')
        else:
            gv.Files.Log.write_to_log('Failed to save SauceNao API-Key')
        self.saucenao_key_confirm_btn.place_forget()
        self.saucenao_key_entry.place_forget()
        self.saucenao_key_change_btn.place(x = x4, y = y + c * 1)
        self.saucenao_key_number_lbl.configure(text=gv.config['SauceNAO']['api_key'])
        self.saucenao_key_number_lbl.place(x = x2, y = y + c * 1)

    def saucenao_save(self):
        gv.Files.Log.write_to_log('Saving SauceNAO options...')
        gv.config['SauceNAO']['minsim'] = self.saucenao_minsim_entry.get()
        gv.config['SauceNAO']['returns'] = self.saucenao_returns_entry.get()
        gv.config['SauceNAO']['depth'] = self.saucenao_depth_entry.get()
        gv.config['SauceNAO']['bias'] = self.saucenao_bias_entry.get()
        gv.config['SauceNAO']['biasmin'] = self.saucenao_biasmin_entry.get()
        gv.write_config()
        gv.Files.Log.write_to_log('Saved SauceNao Options')

    def hyperlink(self, event):
        """
        Opens a webbrowser with a URL on click of a widget that is bound to this method
        """
        open_new(event.widget.cget("text"))

class SourceryOptions():
    """Includes all widgets for Sourcery and methods to display and modify them"""
    def __init__(self, parent, enforce_style, leftovers):
        self.par = parent
        self.en_s = enforce_style
        self.leftovers = leftovers
        self.theme_lbl = Label(parent, text="Theme", font=("Arial Bold", 14), style="label.TLabel")
        self.dark_theme_btn = Button(parent, text="Dark Theme", command=self.change_to_dark_theme, style="button.TLabel")
        self.light_theme_btn = Button(parent, text="Light Theme", command=self.change_to_light_theme, style="button.TLabel")
        self.custom_theme_btn = Button(parent, text="Custom Theme", command=self.change_to_custom_theme, style="button.TLabel")
        self.custom_background_lbl = Label(parent, text="Background", style="label.TLabel")
        self.custom_foreground_lbl = Label(parent, text="Foreground", style="label.TLabel")
        self.custom_selected_background_lbl = Label(parent, text="Selected Background", style="label.TLabel")
        self.custom_button_background_lbl = Label(parent, text="Button Background", style="label.TLabel")
        self.custom_button_background_active_lbl = Label(parent, text="Button Background Active", style="label.TLabel")
        self.custom_button_foreground_active_lbl = Label(parent, text="Button Foreground Active", style="label.TLabel")
        self.custom_button_background_pressed_lbl = Label(parent, text="Button Background Pressed", style="label.TLabel")
        self.custom_button_foreground_pressed_lbl = Label(parent, text="Button Foreground Pressed", style="label.TLabel")
        self.custom_checkbutton_pressed_lbl = Label(parent, text="Checkbutton Pressed", style="label.TLabel")

        rel = 'raised'
        self.custom_background_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_foreground_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_selected_background_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_background_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_background_active_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_foreground_active_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_background_pressed_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_foreground_pressed_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_checkbutton_pressed_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.color_bind()

        self.save_custom_theme_btn = Button(parent, text="Save Custom Theme", command=self.save_custom_theme, style="button.TLabel")

        self.genereal_lbl = Label(parent, text="General", font=("Arial Bold", 14), style="label.TLabel")

        self.input_dir_0_lbl = Label(parent, text="Input Directory:", style="label.TLabel")
        self.input_dir_1_lbl = Label(parent, text=gv.input_dir, style="label.TLabel")
        self.input_dir_btn = Button(parent, text='Change', command=self.change_input, style="button.TLabel")
        self.output_dir_0_lbl = Label(parent, text="Output Directory:", style="label.TLabel")
        self.output_dir_1_lbl = Label(parent, text=gv.output_dir, style="label.TLabel")
        self.output_dir_btn = Button(parent, text='Change', command=self.change_output, style="button.TLabel")

        if gv.config['Sourcery']['delete_input'] == '':
            gv.config['Sourcery']['delete_input'] = '0'
            gv.write_config()
        self.delete_input_var = IntVar(value=gv.config.getint('Sourcery', 'delete_input'))
        self.delete_input_chkbtn = Checkbutton(parent, var=self.delete_input_var, text="Delete sourced images from the Input folder on save?", style="chkbtn.TCheckbutton")

        vcmd = (parent.register(is_input_int_digit))
        self.images_per_page_lbl = Label(parent, text="Images per page(Max:50, Restart required)", font=("Arial Bold", 10), style="label.TLabel")
        self.images_per_page_entry = Entry(parent, width=30, validate='all', validatecommand=(vcmd, '%P', False, 1, 50), style="button.TLabel")
        self.images_per_page_entry.insert(0, gv.config['Sourcery']['imgpp'])

        self.input_search_depth_lbl = Label(parent, text="Input search depth", font=("Arial Bold", 10), style="label.TLabel")
        self.input_search_depth_entry = Entry(parent, width=30, validate='all', validatecommand=(vcmd, '%P', True), style="button.TLabel")
        self.input_search_depth_entry.insert(0, gv.config['Sourcery']['input_search_depth'])

        self.direct_replace_lbl = Label(parent, text="Save images directly if similarity is over:", font=("Arial Bold", 10), style="label.TLabel")
        self.direct_replace_pixiv_var = IntVar(value = gv.config.getint('Pixiv', 'direct_replace'))
        self.direct_replace_pixiv_chkbtn = Checkbutton(parent, text="Save pixiv images directly", var=self.direct_replace_pixiv_var, style="chkbtn.TCheckbutton")
        self.direct_replace_danbooru_var = IntVar(value = gv.config.getint('Danbooru', 'direct_replace'))
        self.direct_replace_danbooru_chkbtn = Checkbutton(parent, text="Save danbooru images directly", var=self.direct_replace_danbooru_var, style="chkbtn.TCheckbutton")
        self.direct_replace_yandere_var = IntVar(value = gv.config.getint('Yandere', 'direct_replace'))
        self.direct_replace_yandere_chkbtn = Checkbutton(parent, text="Save yandere images directly", var=self.direct_replace_yandere_var, style="chkbtn.TCheckbutton")
        self.direct_replace_konachan_var = IntVar(value = gv.config.getint('Konachan', 'direct_replace'))
        self.direct_replace_konachan_chkbtn = Checkbutton(parent, text="Save konachan images directly", var=self.direct_replace_konachan_var, style="chkbtn.TCheckbutton")
        self.direct_replace_entry = Entry(parent, width=30, validate='all', validatecommand=(vcmd, '%P', False, 0, 100), style="button.TLabel")
        self.direct_replace_entry.insert(0, gv.config['Sourcery']['direct_replace'])

        self.restart_gui_lbl = Label(parent, text="Restart of Sourcery required(Images per page)!", font=("Arial Bold", 10), style="label.TLabel")

        self.cleanup_lbl = Label(parent, text="Cleanup", font=("Arial Bold", 14), style="label.TLabel")
        self.reference_entries_lbl = Label(parent, text="Reference entries", font=("Arial Bold", 10), style="label.TLabel")
        self.originals_lbl = Label(parent, text="Originals", font=("Arial Bold", 10), style="label.TLabel")
        self.downloaded_lbl = Label(parent, text="Downloaded", font=("Arial Bold", 10), style="label.TLabel")
        self.reference_entries_count_lbl = Label(parent, text="???", font=("Arial Bold", 10), style="label.TLabel")
        self.originals_count_lbl = Label(parent, text="???", font=("Arial Bold", 10), style="label.TLabel")
        self.downloaded_count_lbl = Label(parent, text="???", font=("Arial Bold", 10), style="label.TLabel")
        self.reference_clean_btn = Button(parent, text='Clean', command=self.clean_reference, style="button.TLabel")
        self.originals_clean_btn = Button(parent, text='Clean', command=self.clean_originals, style="button.TLabel")
        self.downloaded_clean_btn = Button(parent, text='Clean', command=self.clean_downloaded, style="button.TLabel")

        self.sourcery_confirm_btn = Button(parent, text="Save", command=self.sourcery_save, style="button.TLabel")

    def display(self):
        """
        Draw options for Sourcery Application:
        - Themes
        """
        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*24)
        self.color_insert()

        self.theme_lbl.place(x = x1, y = y-5)
        self.dark_theme_btn.place(x = x1, y = y + c * 1)
        self.light_theme_btn .place(x = x1, y = y + c * 2)
        self.custom_theme_btn.place(x = x1, y = y + c * 3)
        self.custom_background_lbl.place(x = x1, y = y + c * 4)
        self.custom_foreground_lbl.place(x = x1, y = y + c * 5)
        self.custom_selected_background_lbl.place(x = x1, y = y + c * 6)
        self.custom_button_background_lbl.place(x = x1, y = y + c * 7)
        self.custom_button_background_active_lbl.place(x = x1, y = y + c * 8)
        self.custom_button_foreground_active_lbl.place(x = x1, y = y + c * 9)
        self.custom_button_background_pressed_lbl.place(x = x1, y = y + c * 10)
        self.custom_button_foreground_pressed_lbl.place(x = x1, y = y + c * 11)
        self.custom_checkbutton_pressed_lbl.place(x = x1, y = y + c * 12)
        self.custom_background_color_lbl.place(x = x2, y = y + c * 4)
        self.custom_foreground_color_lbl.place(x = x2, y = y + c * 5)
        self.custom_selected_background_color_lbl.place(x = x2, y = y + c * 6)
        self.custom_button_background_color_lbl.place(x = x2, y = y + c * 7)
        self.custom_button_background_active_color_lbl.place(x = x2, y = y + c * 8)
        self.custom_button_foreground_active_color_lbl.place(x = x2, y = y + c * 9)
        self.custom_button_background_pressed_color_lbl.place(x = x2, y = y + c * 10)
        self.custom_button_foreground_pressed_color_lbl.place(x = x2, y = y + c * 11)
        self.custom_checkbutton_pressed_color_lbl.place(x = x2, y = y + c * 12)

        self.save_custom_theme_btn.place(x = x1, y = y + c * 13)

        y = int(gv.height/90*10)
        c = 23
        x3 = int(gv.width/160*40)
        x4 = int(gv.width/160*70)

        self.genereal_lbl.place(x = x3, y = y + c * 0)
        self.images_per_page_lbl.place(x = x3, y = y + c * 1)
        self.images_per_page_entry.place(x = x4, y = y + c * 1)

        self.delete_input_chkbtn.place(x = x3, y = y + c * 3)

        self.input_dir_0_lbl.place(x = x3+100, y = y + c * 5)
        self.input_dir_1_lbl.place(x = x4, y = y + c * 5)
        self.input_dir_btn.place(x = x3, y = y + c * 5)
        self.output_dir_0_lbl.place(x = x3+100, y = y + c * 6)
        self.output_dir_1_lbl.place(x = x4, y = y + c * 6)
        self.output_dir_btn.place(x = x3, y = y + c * 6)

        self.direct_replace_lbl.place(x = x3, y = y + c * 8)
        self.direct_replace_entry.place(x = x4, y = y + c * 8)
        self.direct_replace_pixiv_chkbtn.place(x = x3, y = y + c * 9)
        self.direct_replace_danbooru_chkbtn.place(x = x3, y = y + c * 10)
        self.direct_replace_yandere_chkbtn.place(x = x3, y = y + c * 11)
        self.direct_replace_konachan_chkbtn.place(x = x3, y = y + c * 12)

        self.input_search_depth_lbl.place(x = x3, y = y + c * 14)
        self.input_search_depth_entry.place(x = x4, y = y + c * 14)

        self.sourcery_confirm_btn.place(x = x3, y = y + c * 16)

        def count_downloaded():
            z = 0
            x = listdir(gv.cwd + '/Sourcery/sourced_progress')
            for elem in x:
                z += len(listdir(gv.cwd + '/Sourcery/sourced_progress/' + elem))
            return z

        self.reference_entries_count_lbl.configure(text=str(len(gv.Files.Ref.refs)))
        try:
            self.originals_count_lbl.configure(text=str(len(listdir(gv.cwd + '/Sourcery/sourced_original'))))
            self.downloaded_count_lbl.configure(text=str(count_downloaded()))
        except:
            pass

        self.cleanup_lbl.place(x = x3, y = y + c * 18)
        self.reference_entries_lbl.place(x = x3, y = y + c * 19)
        self.originals_lbl.place(x = x3, y = y + c * 20)
        self.downloaded_lbl.place(x = x3, y = y + c * 21)
        self.reference_entries_count_lbl.place(x = x3+150, y = y + c * 19)
        self.originals_count_lbl.place(x = x3+150, y = y + c * 20)
        self.downloaded_count_lbl.place(x = x3+150, y = y + c * 21)
        self.reference_clean_btn.place(x = x4, y = y + c * 19)
        self.originals_clean_btn.place(x = x4, y = y + c * 20)
        self.downloaded_clean_btn.place(x = x4, y = y + c * 21)

    def change_to_dark_theme(self):
        gv.Files.Theme.current_theme = "Dark Theme"
        gv.Files.Theme.write_theme(gv.Files.Theme.current_theme)
        self.en_s()

    def change_to_light_theme(self):
        gv.Files.Theme.current_theme = "Light Theme"
        gv.Files.Theme.write_theme(gv.Files.Theme.current_theme)
        self.en_s()

    def change_to_custom_theme(self):
        gv.Files.Theme.current_theme = "Custom Theme"
        gv.Files.Theme.write_theme(gv.Files.Theme.current_theme)
        self.en_s()

    def save_custom_theme(self):
        gv.Files.Log.write_to_log('Attempting to save Custom Theme...')
        gv.Files.Theme.custom_background = str(self.custom_background_color_lbl.cget('background'))
        gv.Files.Theme.custom_foreground = str(self.custom_foreground_color_lbl.cget('background'))
        gv.Files.Theme.custom_selected_background = str(self.custom_selected_background_color_lbl.cget('background'))
        gv.Files.Theme.custom_button_background = str(self.custom_button_background_color_lbl.cget('background'))
        gv.Files.Theme.custom_button_background_active = str(self.custom_button_background_active_color_lbl.cget('background'))
        gv.Files.Theme.custom_button_foreground_active = str(self.custom_button_foreground_active_color_lbl.cget('background'))
        gv.Files.Theme.custom_button_background_pressed = str(self.custom_button_background_pressed_color_lbl.cget('background'))
        gv.Files.Theme.custom_button_foreground_pressed = str(self.custom_button_foreground_pressed_color_lbl.cget('background'))
        gv.Files.Theme.custom_checkbutton_pressed = str(self.custom_checkbutton_pressed_color_lbl.cget('background'))
        e = gv.Files.Theme.write_theme(gv.Files.Theme.current_theme)
        if e == None:
            gv.Files.Log.write_to_log('Saved custom theme successfully')
            if gv.Files.Theme.current_theme == 'Custom Theme':
                self.change_to_custom_theme()
        else:
            gv.Files.Log.write_to_log('Failed to save Custom Theme')

    def color_insert(self):
        """
        Inserts the colors from the theme file into the custom theme preview
        """
        self.custom_background_color_lbl.configure(background = gv.Files.Theme.custom_background, cursor='hand2')
        self.custom_foreground_color_lbl.configure(background = gv.Files.Theme.custom_foreground, cursor='hand2')
        self.custom_selected_background_color_lbl.configure(background = gv.Files.Theme.custom_selected_background, cursor='hand2')
        self.custom_button_background_color_lbl.configure(background = gv.Files.Theme.custom_button_background, cursor='hand2')
        self.custom_button_background_active_color_lbl.configure(background = gv.Files.Theme.custom_button_background_active, cursor='hand2')
        self.custom_button_foreground_active_color_lbl.configure(background = gv.Files.Theme.custom_button_foreground_active, cursor='hand2')
        self.custom_button_background_pressed_color_lbl.configure(background = gv.Files.Theme.custom_button_background_pressed, cursor='hand2')
        self.custom_button_foreground_pressed_color_lbl.configure(background = gv.Files.Theme.custom_button_foreground_pressed, cursor='hand2')
        self.custom_checkbutton_pressed_color_lbl.configure(background = gv.Files.Theme.custom_checkbutton_pressed, cursor='hand2')
    
    def color_bind(self):
        """
        Binds the custom preview widgets to a color chooser
        """
        c_bg_c_par = partial(self.color_choose, self.custom_background_color_lbl)
        self.custom_background_color_lbl.bind("<Button-1>", c_bg_c_par)

        c_fg_c_par = partial(self.color_choose, self.custom_foreground_color_lbl)
        self.custom_foreground_color_lbl.bind("<Button-1>", c_fg_c_par)

        c_sb_c_par = partial(self.color_choose, self.custom_selected_background_color_lbl)
        self.custom_selected_background_color_lbl.bind("<Button-1>", c_sb_c_par)

        c_bbg_c_par = partial(self.color_choose, self.custom_button_background_color_lbl)
        self.custom_button_background_color_lbl.bind("<Button-1>", c_bbg_c_par)

        c_bbg_a_c_par = partial(self.color_choose, self.custom_button_background_active_color_lbl)
        self.custom_button_background_active_color_lbl.bind("<Button-1>", c_bbg_a_c_par)

        c_bfg_a_c_par = partial(self.color_choose, self.custom_button_foreground_active_color_lbl)
        self.custom_button_foreground_active_color_lbl.bind("<Button-1>", c_bfg_a_c_par)

        c_bbg_p_c_par = partial(self.color_choose, self.custom_button_background_pressed_color_lbl)
        self.custom_button_background_pressed_color_lbl.bind("<Button-1>", c_bbg_p_c_par)

        c_bfg_p_c_par = partial(self.color_choose, self.custom_button_foreground_pressed_color_lbl)
        self.custom_button_foreground_pressed_color_lbl.bind("<Button-1>", c_bfg_p_c_par)

        c_cb_p_c_par = partial(self.color_choose, self.custom_checkbutton_pressed_color_lbl)
        self.custom_checkbutton_pressed_color_lbl.bind("<Button-1>", c_cb_p_c_par)

    def color_choose(self, lbl, event):
        """
        Opens the color chooser and colors the label with the received color
        """
        color = colorchooser.askcolor()
        lbl.configure(background = color[1])

    def change_input(self):
        change_input()
        self.input_dir_1_lbl.configure(text=gv.input_dir)

    def change_output(self):
        change_output()
        self.output_dir_1_lbl.configure(text=gv.output_dir)

    def sourcery_save(self):
        gv.Files.Log.write_to_log('Saving Sourcery options...')
        diff = 0
        try:
            diff = int(self.images_per_page_entry.get()) - gv.config.getint('Sourcery', 'imgpp')
        except Exception as e:
            mb.showerror('Invalid Value', 'Please insert a positive integer value into the Images per page option')
        # if diff > 0:
        #     for num in range(diff):
        #         gv.imgpp_sem.release()
        # if diff != 0:
            # for num in range(diff, 0):
            #     gv.imgpp_sem.acquire(False)#TODO problem when more images are being displayed than imgpp
            # y = int(gv.height/90*10)
            # c = 23
            # x3 = int(gv.width/160*50)
            # self.restart_gui_lbl.place(x = x3, y = y + c * 17)
        gv.config['Sourcery']['imgpp'] = self.images_per_page_entry.get()
        gv.config['Sourcery']['delete_input'] = str(self.delete_input_var.get())
        gv.config['Sourcery']['direct_replace'] = self.direct_replace_entry.get()
        gv.config['Pixiv']['direct_replace'] = str(self.direct_replace_pixiv_var.get())
        gv.config['Danbooru']['direct_replace'] = str(self.direct_replace_danbooru_var.get())
        gv.config['Yandere']['direct_replace'] = str(self.direct_replace_yandere_var.get())
        gv.config['Konachan']['direct_replace'] = str(self.direct_replace_konachan_var.get())
        gv.config['Sourcery']['input_search_depth'] = str(self.input_search_depth_entry.get())
        gv.write_config()
        gv.Files.Log.write_to_log('Saved Sourcery Options')

    def clean_reference(self):
        if mb.askyesno('Delete?', 'Delete all Reference file entries?'):
            gv.Files.Ref.clean_reference(clear_list=True)
            self.reference_entries_count_lbl.configure(text=str(len(gv.Files.Ref.refs)))
    
    def clean_originals(self):
        if mb.askyesno('Delete?', 'Delete all Original files in the working directory (not in the Input folder)?'):
            try:
                delete_list = list()
                for elem in listdir(gv.cwd + '/Sourcery/sourced_original'):
                    if gv.cwd + '/Sourcery/sourced_original/' + elem not in delete_list:
                        delete_list.append(gv.cwd + '/Sourcery/sourced_original/' + elem)
                self.leftovers(delete_list)
                self.originals_count_lbl.configure(text=str(len(listdir(gv.cwd + '/Sourcery/sourced_original'))))
            except:
                self.originals_count_lbl.configure(text='ERROR')
        
    def clean_downloaded(self):
        def count_downloaded():
            z = 0
            x = listdir(gv.cwd + '/Sourcery/sourced_progress')
            for elem in x:
                z += len(listdir(gv.cwd + '/Sourcery/sourced_progress/' + elem))
            return z
        if mb.askyesno('Delete?', 'Delete all Downloaded files in the working directory (not in the Input folder)?'):
            try:
                delete_list = list()
                for elem in listdir(gv.cwd + '/Sourcery/sourced_progress'):
                    for el in listdir(gv.cwd + '/Sourcery/sourced_progress/' + elem):
                        if gv.cwd + '/Sourcery/sourced_progress/' + elem + '/' + el not in delete_list:
                            delete_list.append(gv.cwd + '/Sourcery/sourced_progress/' + elem + '/' + el)
                self.leftovers(delete_list)
                self.downloaded_count_lbl.configure(text=str(count_downloaded()))
            except:
                self.originals_count_lbl.configure(text='ERROR')

class ProviderOptions():
    """Hosts all image provider options Classes"""
    def __init__(self, parent):
        self.par = parent
        self.PixO = Provider('Pixiv', parent, self)
        self.DanO = Provider('Danbooru' , parent, self)
        self.YanO = Provider('Yandere' , parent, self)
        self.KonO = Provider('Konachan' , parent, self)
        self.Weight = WeightSystem(parent, self)

        self.original_lbl = Label(self.par, text='Original', font=('Arial Bold', 13), style="label.TLabel")
        self.all_services_lbl = Label(self.par, text='All Services', font=('Arial Bold', 13), style="label.TLabel")
        self.gen_tagfile_var = IntVar(value=gv.config.getint('Original', 'gen_tagfile'))
        self.tagfile_pixiv_var = IntVar(value=gv.config.getint('Original', 'tagfile_pixiv'))
        self.tagfile_danbooru_var = IntVar(value=gv.config.getint('Original', 'tagfile_danbooru'))
        self.tagfile_yandere_var = IntVar(value=gv.config.getint('Original', 'tagfile_yandere'))
        self.tagfile_konachan_var = IntVar(value=gv.config.getint('Original', 'tagfile_konachan'))
        self.gen_tagfile_chkbtn = Checkbutton(self.par, text='Generate tagfiles for original images', var=self.gen_tagfile_var, style="chkbtn.TCheckbutton")
        self.tagfile_pixiv_chkbtn = Checkbutton(self.par, text='Include pixiv tags', var=self.tagfile_pixiv_var, style="chkbtn.TCheckbutton")
        self.tagfile_danbooru_chkbtn = Checkbutton(self.par, text='Include danbooru tags', var=self.tagfile_danbooru_var, style="chkbtn.TCheckbutton")
        self.tagfile_yandere_chkbtn = Checkbutton(self.par, text='Include yandere tags', var=self.tagfile_yandere_var, style="chkbtn.TCheckbutton")
        self.tagfile_konachan_chkbtn = Checkbutton(self.par, text='Include konachan tags', var=self.tagfile_konachan_var, style="chkbtn.TCheckbutton")

        self.single_source_in_tagfile_var = IntVar(value=gv.config.getint('Original', 'single_source_in_tagfile'))
        self.single_source_in_tagfile_chkbtn = Checkbutton(self.par, text='If only one source is available, include its tags', var=self.single_source_in_tagfile_var, style="chkbtn.TCheckbutton")

        self.original_btn = Button(self.par, text='Original', command=self.original_display, style ="button.TLabel")
        self.pixiv_btn = Button(self.par, text='Pixiv', command=self.PixO.display, style ="button.TLabel")
        self.danbooru_btn = Button(self.par, text='Danbooru', command=self.DanO.display, style ="button.TLabel")
        self.yandere_btn = Button(self.par, text='Yandere', command=self.YanO.display, style ="button.TLabel")
        self.konachan_btn = Button(self.par, text='Konachan', command=self.KonO.display, style ="button.TLabel")
        self.weight_btn = Button(self.par, text='Weight System', command=self.Weight.weight_display, style ="button.TLabel")

        self.save_btn = Button(self.par, text='Save', command=self.save_all, style ="button.TLabel")
    
    def display(self):
        """
        Draw options (login) for all image providers:\n
        - Pixiv\n
        - Danbooru\n
        - Yande.re\n
        - Konachan\n
        """
        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*27)

        self.original_btn.place(x = x1, y = y + c * 1)
        self.pixiv_btn.place(x = x1, y = y + c * 2)
        self.danbooru_btn.place(x = x1, y = y + c * 3)
        self.yandere_btn.place(x = x1, y = y + c * 4)
        self.konachan_btn.place(x = x1, y = y + c * 5)
        self.weight_btn.place(x = x1, y = y + c * 7)
        
        self.save_btn.place(x = x2, y = y + c * 26)

        self.original_display()

    def forget(self):
        self.original_lbl.place_forget()
        self.all_services_lbl.place_forget()
        self.gen_tagfile_chkbtn.place_forget()
        self.tagfile_pixiv_chkbtn.place_forget()
        self.tagfile_danbooru_chkbtn.place_forget()
        self.tagfile_yandere_chkbtn.place_forget()
        self.tagfile_konachan_chkbtn.place_forget()
        self.single_source_in_tagfile_chkbtn.place_forget()

        #self.save_btn.place_forget()

    def original_display(self):
        self.PixO.forget()
        self.DanO.forget()
        self.YanO.forget()
        self.KonO.forget()
        self.Weight.forget()

        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*27)
        x2 = int(gv.width/160*28)

        self.original_lbl.place(x = x1, y = y + c * 1)
        self.gen_tagfile_chkbtn.place(x = x1, y = y + c * 2)
        self.tagfile_pixiv_chkbtn.place(x = x2, y = y + c * 3)
        self.tagfile_danbooru_chkbtn.place(x = x2, y = y + c * 4)
        self.tagfile_yandere_chkbtn.place(x = x2, y = y + c * 5)
        self.tagfile_konachan_chkbtn.place(x = x2, y = y + c * 6)

        self.all_services_lbl.place(x = x2, y = y + c * 8)
        self.single_source_in_tagfile_chkbtn.place(x = x2, y = y + c * 9)

    def save_all(self):
        self.PixO.save()
        self.DanO.save()
        self.YanO.save()
        self.KonO.save()
        self.Weight.weight_save()
        self.original_save()

    def original_save(self):
        gv.Files.Log.write_to_log('Saving Original options...')
        gv.config['Original']['gen_tagfile'] = str(self.gen_tagfile_var.get())
        gv.config['Original']['tagfile_pixiv'] = str(self.tagfile_pixiv_var.get())
        gv.config['Original']['tagfile_danbooru'] = str(self.tagfile_danbooru_var.get())
        gv.config['Original']['tagfile_yandere'] = str(self.tagfile_yandere_var.get())
        gv.config['Original']['tagfile_konachan'] = str(self.tagfile_konachan_var.get())
        gv.config['Original']['single_source_in_tagfile'] = str(self.single_source_in_tagfile_var.get())
        gv.write_config()
        gv.Files.Log.write_to_log('Saved Original options')

class Provider():
    """Includes all widgets for Pixiv and methods to display and modify them"""
    def __init__(self, name, parent, lord):
        self.name = name
        self.par = parent
        self.lord = lord
        self.scrollpar = ScrollFrame(self.par, gv.width/3, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame
        self.use_var = IntVar(value=gv.config.getint(self.name, 'use'))
        self.use_chkbtn = Checkbutton(self.scrollpar_frame, text='Use ' + self.name.lower(), var=self.use_var, style="chkbtn.TCheckbutton")
        self.lbl = Label(parent, text=self.name, font=('Arial Bold', 13), style="label.TLabel")
        self.rename_var = IntVar(value=gv.config.getint(self.name, 'rename'))
        self.rename_chkbtn = Checkbutton(self.scrollpar_frame, text='Rename images from ' + self.name.lower() + ' to ' + self.name.lower() + ' name', var=self.rename_var, style="chkbtn.TCheckbutton")

        self.show_tags_lbl = Label(self.scrollpar_frame, text="Put tags seperated by spaces or newlines here\nto make them show up in the results screen:", style="label.TLabel")
        self.show_tags_txt = Text(self.scrollpar_frame, width=int(gv.width/30), height=int(gv.height*0.01), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))

        self.show_tags_txt.insert(END, gv.config[self.name]['tags'])
        self.tags = None

        self.gen_tagfile_var = IntVar(value=gv.config.getint(self.name, 'gen_tagfile'))
        self.tagfile_pixiv_var = IntVar(value=gv.config.getint(self.name, 'tagfile_pixiv'))
        self.tagfile_danbooru_var = IntVar(value=gv.config.getint(self.name, 'tagfile_danbooru'))
        self.tagfile_yandere_var = IntVar(value=gv.config.getint(self.name, 'tagfile_yandere'))
        self.tagfile_konachan_var = IntVar(value=gv.config.getint(self.name, 'tagfile_konachan'))
        self.gen_tagfile_chkbtn = Checkbutton(self.scrollpar_frame, text='Generate tagfiles for ' + self.name.lower() + ' images', var=self.gen_tagfile_var, style="chkbtn.TCheckbutton")
        self.tagfile_pixiv_chkbtn = Checkbutton(self.scrollpar_frame, text='Include pixiv tags', var=self.tagfile_pixiv_var, style="chkbtn.TCheckbutton")
        self.tagfile_danbooru_chkbtn = Checkbutton(self.scrollpar_frame, text='Include danbooru tags', var=self.tagfile_danbooru_var, style="chkbtn.TCheckbutton")
        self.tagfile_yandere_chkbtn = Checkbutton(self.scrollpar_frame, text='Include yandere tags', var=self.tagfile_yandere_var, style="chkbtn.TCheckbutton")
        self.tagfile_konachan_chkbtn = Checkbutton(self.scrollpar_frame, text='Include konachan tags', var=self.tagfile_konachan_var, style="chkbtn.TCheckbutton")
        
        #self.save_btn = Button(parent, text='Save', command=self.save, style ="button.TLabel")

    def display(self):
        """
        Displays the options widgets
        """
        self.lord.forget()
        self.lord.DanO.forget()
        self.lord.YanO.forget()
        self.lord.KonO.forget()
        self.lord.Weight.forget()

        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*27)

        self.use_chkbtn.grid(row= 0, column= 0, sticky=W, padx=2, pady=1)

        self.show_tags_lbl.grid(row= 8, column= 0, sticky=W, padx=2, pady=1, columnspan=3)
        self.show_tags_txt.grid(row= 9, column= 0, sticky=W, padx=2, pady=1, columnspan=3)
        self.scrollpar_frame.columnconfigure(2, weight=1)

        self.gen_tagfile_chkbtn.grid(row= 13, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.tagfile_pixiv_chkbtn.grid(row= 14, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_danbooru_chkbtn.grid(row= 15, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_yandere_chkbtn.grid(row= 16, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_konachan_chkbtn.grid(row= 17, column= 0, sticky=W, padx=15, pady=1, columnspan=2)

        self.rename_chkbtn.grid(row= 18, column= 0, sticky=W, padx=2, pady=1, columnspan=2)

        self.lbl.place(x = x2, y = y + c * 1)
        self.scrollpar.display(x = x2, y= y + c * 2)

        #self.save_btn.place(x = int(gv.width/160*40), y = gv.height-220)    

    def forget(self):
        self.lbl.place_forget()
        self.scrollpar.sub_frame.place_forget()

        self.use_chkbtn.grid_forget()
        self.show_tags_lbl.grid_forget()
        self.show_tags_txt.grid_forget()

        self.gen_tagfile_chkbtn.grid_forget()
        self.tagfile_pixiv_chkbtn.grid_forget()
        self.tagfile_danbooru_chkbtn.grid_forget()

        self.rename_chkbtn.grid_forget()

        #self.save_btn.place_forget()

    def save(self):
        gv.Files.Log.write_to_log('Saving ' + self.name + ' options...')
        gv.config[self.name]['rename'] = str(self.rename_var.get())
        self.tags = self.show_tags_txt.get('1.0', END)
        gv.config[self.name]['tags'] = self.tags
        gv.config[self.name]['gen_tagfile'] = str(self.gen_tagfile_var.get())
        gv.config[self.name]['tagfile_pixiv'] = str(self.tagfile_pixiv_var.get())
        gv.config[self.name]['tagfile_danbooru'] = str(self.tagfile_danbooru_var.get())
        gv.config[self.name]['tagfile_yandere'] = str(self.tagfile_yandere_var.get())
        gv.config[self.name]['tagfile_konachan'] = str(self.tagfile_konachan_var.get())
        gv.config[self.name]['use'] = str(self.use_var.get())
        gv.write_config()
        if self.name == 'Pixiv':
            gv.results_tags_pixiv = self.tags.split()
        elif self.name == 'Danbooru':
            gv.results_tags_danbooru = self.tags.split()
        elif self.name == 'Yandere':
            gv.results_tags_yandere = self.tags.split()
        elif self.name == 'Konachan':
            gv.results_tags_konachan = self.tags.split()
        # elif self.name == 'Gelbooru':
        #     gv.results_tags_gelbooru = self.tags.split()
        gv.Files.Log.write_to_log('Saved ' + self.name + ' options')
