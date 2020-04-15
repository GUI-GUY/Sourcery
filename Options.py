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
    def __init__(self, parent, enforce_style):
        self.par = parent
        self.NAOO = SauceNaoOptions(parent)
        self.SouO = SourceryOptions(parent, enforce_style)
        self.ProO = ProviderOptions(parent)
        self.options_lbl = Label(parent, text="Options", font=("Arial Bold", 20), style="label.TLabel")

        self.provider_options_btn = Button(parent, text="Provider", command=self.display_provider_options, style="button.TLabel")
        self.saucenao_options_btn = Button(parent, text="SauceNao", command=self.display_saucenao_options, style="button.TLabel")
        self.sourcery_options_btn = Button(parent, text="Sourcery", command=self.display_sourcery_options, style="button.TLabel")

        self.options_back_btn = Button(parent, text="Back", command=gv.display_startpage, style="button.TLabel")

    def display_saucenao_options(self):
        """
        Draw 
        """
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

        self.options_back_btn.place(x = int(gv.width/160*5), y = gv.height-170)

    def forget_all_widgets(self):
        for widget in self.par.winfo_children():
            widget.place_forget()

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
    def __init__(self, parent, enforce_style):
        self.par = parent
        self.en_s = enforce_style
        self.theme_lbl = Label(parent, text="Theme", font=("Arial Bold", 14), style="label.TLabel")
        self.dark_theme_btn = Button(parent, text="Dark Theme", command=self.change_to_dark_theme, style="button.TLabel")
        self.light_theme_btn = Button(parent, text="Light Theme", command=self.change_to_light_theme, style="button.TLabel")
        self.custom_theme_btn = Button(parent, text="Custom Theme", command=self.change_to_custom_theme, style="button.TLabel")
        self.custom_background_lbl = Label(parent, text="Background", style="label.TLabel")
        self.custom_foreground_lbl = Label(parent, text="Foreground", style="label.TLabel")
        self.custom_button_background_lbl = Label(parent, text="Button Background", style="label.TLabel")
        self.custom_button_background_active_lbl = Label(parent, text="Button Background Active", style="label.TLabel")
        self.custom_button_foreground_active_lbl = Label(parent, text="Button Foreground Active", style="label.TLabel")
        self.custom_button_background_pressed_lbl = Label(parent, text="Button Background Pressed", style="label.TLabel")
        self.custom_button_foreground_pressed_lbl = Label(parent, text="Button Foreground Pressed", style="label.TLabel")
        self.custom_checkbutton_pressed_lbl = Label(parent, text="Checkbutton Pressed", style="label.TLabel")

        rel = 'raised'
        self.custom_background_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_foreground_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
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
        self.custom_button_background_lbl.place(x = x1, y = y + c * 6)
        self.custom_button_background_active_lbl.place(x = x1, y = y + c * 7)
        self.custom_button_foreground_active_lbl.place(x = x1, y = y + c * 8)
        self.custom_button_background_pressed_lbl.place(x = x1, y = y + c * 9)
        self.custom_button_foreground_pressed_lbl.place(x = x1, y = y + c * 10)
        self.custom_checkbutton_pressed_lbl.place(x = x1, y = y + c * 11)
        self.custom_background_color_lbl.place(x = x2, y = y + c * 4)
        self.custom_foreground_color_lbl.place(x = x2, y = y + c * 5)
        self.custom_button_background_color_lbl.place(x = x2, y = y + c * 6)
        self.custom_button_background_active_color_lbl.place(x = x2, y = y + c * 7)
        self.custom_button_foreground_active_color_lbl.place(x = x2, y = y + c * 8)
        self.custom_button_background_pressed_color_lbl.place(x = x2, y = y + c * 9)
        self.custom_button_foreground_pressed_color_lbl.place(x = x2, y = y + c * 10)
        self.custom_checkbutton_pressed_color_lbl.place(x = x2, y = y + c * 11)

        self.save_custom_theme_btn.place(x = x1, y = y + c * 12)

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

class ProviderOptions():
    """Hosts all image provider options Classes"""
    def __init__(self, parent):
        self.par = parent
        self.PixO = PixivOptions(parent, self)
        self.DanO = DanbooruOptions(parent, self)
        self.YanO = YandereOptions(parent, self)
        self.KonO = KonachanOptions(parent, self)
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
        self.pixiv_btn = Button(self.par, text='Pixiv', command=self.PixO.pixiv_display, style ="button.TLabel")
        self.danbooru_btn = Button(self.par, text='Danbooru', command=self.DanO.danbooru_display, style ="button.TLabel")
        self.yandere_btn = Button(self.par, text='Yandere', command=self.YanO.yandere_display, style ="button.TLabel")
        self.konachan_btn = Button(self.par, text='Konachan', command=self.KonO.konachan_display, style ="button.TLabel")
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
        self.PixO.pixiv_save()
        self.DanO.danbooru_save()
        self.YanO.yandere_save()
        self.KonO.konachan_save()
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

class PixivOptions():
    """Includes all widgets for Pixiv and methods to display and modify them"""
    def __init__(self, parent, lord):
        self.par = parent
        self.lord = lord
        self.scrollpar = ScrollFrame(self.par, gv.width/3, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame
        self.use_pixiv_var = IntVar(value=gv.config.getint('Pixiv', 'use'))
        self.use_pixiv_chkbtn = Checkbutton(self.scrollpar_frame, text='Use pixiv', var=self.use_pixiv_var, style="chkbtn.TCheckbutton")
        self.pixiv_lbl = Label(parent, text="Pixiv", font=('Arial Bold', 13), style="label.TLabel")
        self.rename_var = IntVar(value=gv.config.getint('Pixiv', 'rename'))
        self.rename_chkbtn = Checkbutton(self.scrollpar_frame, text='Rename images from pixiv to pixiv name', var=self.rename_var, style="chkbtn.TCheckbutton")

        self.show_tags_lbl = Label(self.scrollpar_frame, text="Put tags seperated by spaces or newlines here\nto make them show up in the results screen:", style="label.TLabel")
        self.show_tags_txt = Text(self.scrollpar_frame, width=int(gv.width/30), height=int(gv.height*0.01), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))

        self.show_tags_txt.insert(END, gv.config['Pixiv']['tags'])
        self.tags = None

        self.gen_tagfile_var = IntVar(value=gv.config.getint('Pixiv', 'gen_tagfile'))
        self.tagfile_pixiv_var = IntVar(value=gv.config.getint('Pixiv', 'tagfile_pixiv'))
        self.tagfile_danbooru_var = IntVar(value=gv.config.getint('Pixiv', 'tagfile_danbooru'))
        self.tagfile_yandere_var = IntVar(value=gv.config.getint('Pixiv', 'tagfile_yandere'))
        self.tagfile_konachan_var = IntVar(value=gv.config.getint('Pixiv', 'tagfile_konachan'))
        self.gen_tagfile_chkbtn = Checkbutton(self.scrollpar_frame, text='Generate tagfiles for pixiv images', var=self.gen_tagfile_var, style="chkbtn.TCheckbutton")
        self.tagfile_pixiv_chkbtn = Checkbutton(self.scrollpar_frame, text='Include pixiv tags', var=self.tagfile_pixiv_var, style="chkbtn.TCheckbutton")
        self.tagfile_danbooru_chkbtn = Checkbutton(self.scrollpar_frame, text='Include danbooru tags', var=self.tagfile_danbooru_var, style="chkbtn.TCheckbutton")
        self.tagfile_yandere_chkbtn = Checkbutton(self.scrollpar_frame, text='Include yandere tags', var=self.tagfile_yandere_var, style="chkbtn.TCheckbutton")
        self.tagfile_konachan_chkbtn = Checkbutton(self.scrollpar_frame, text='Include konachan tags', var=self.tagfile_konachan_var, style="chkbtn.TCheckbutton")
        
        #self.save_btn = Button(parent, text='Save', command=self.pixiv_save, style ="button.TLabel")

    def pixiv_display(self):
        """
        Displays the pixiv options widgets
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

        self.use_pixiv_chkbtn.grid(row= 0, column= 0, sticky=W, padx=2, pady=1)

        self.show_tags_lbl.grid(row= 8, column= 0, sticky=W, padx=2, pady=1, columnspan=3)
        self.show_tags_txt.grid(row= 9, column= 0, sticky=W, padx=2, pady=1, columnspan=3)
        self.scrollpar_frame.columnconfigure(2, weight=1)

        self.gen_tagfile_chkbtn.grid(row= 13, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.tagfile_pixiv_chkbtn.grid(row= 14, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_danbooru_chkbtn.grid(row= 15, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_yandere_chkbtn.grid(row= 16, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_konachan_chkbtn.grid(row= 17, column= 0, sticky=W, padx=15, pady=1, columnspan=2)

        self.rename_chkbtn.grid(row= 18, column= 0, sticky=W, padx=2, pady=1, columnspan=2)

        self.pixiv_lbl.place(x = x2, y = y + c * 1)
        self.scrollpar.display(x = x2, y= y + c * 2)

        #self.save_btn.place(x = int(gv.width/160*40), y = gv.height-220)    

    def forget(self):
        self.pixiv_lbl.place_forget()
        self.scrollpar.sub_frame.place_forget()

        self.use_pixiv_chkbtn.grid_forget()
        self.show_tags_lbl.grid_forget()
        self.show_tags_txt.grid_forget()

        self.gen_tagfile_chkbtn.grid_forget()
        self.tagfile_pixiv_chkbtn.grid_forget()
        self.tagfile_danbooru_chkbtn.grid_forget()

        self.rename_chkbtn.grid_forget()

        #self.save_btn.place_forget()

    def pixiv_save(self):
        gv.Files.Log.write_to_log('Saving Pixiv options...')
        gv.config['Pixiv']['rename'] = str(self.rename_var.get())
        self.tags = self.show_tags_txt.get('1.0', END)
        gv.config['Pixiv']['tags'] = self.tags
        gv.config['Pixiv']['gen_tagfile'] = str(self.gen_tagfile_var.get())
        gv.config['Pixiv']['tagfile_pixiv'] = str(self.tagfile_pixiv_var.get())
        gv.config['Pixiv']['tagfile_danbooru'] = str(self.tagfile_danbooru_var.get())
        gv.config['Pixiv']['tagfile_yandere'] = str(self.tagfile_yandere_var.get())
        gv.config['Pixiv']['tagfile_konachan'] = str(self.tagfile_konachan_var.get())
        gv.config['Pixiv']['use'] = str(self.use_pixiv_var.get())
        gv.write_config()
        gv.results_tags_pixiv = self.tags.split()
        gv.Files.Log.write_to_log('Saved Pixiv options')

class DanbooruOptions():
    """Includes all widgets for Danbooru and methods to display and modify them"""
    def __init__(self, parent, lord):
        self.par = parent
        self.lord = lord
        self.scrollpar = ScrollFrame(self.par, gv.width/3, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame
        self.use_danbooru_var = IntVar(value=gv.config.getint('Danbooru', 'use'))
        self.use_danbooru_chkbtn = Checkbutton(self.scrollpar_frame, text='Use danbooru', var=self.use_danbooru_var, style="chkbtn.TCheckbutton")
        self.danbooru_lbl = Label(parent, text="Danbooru", font=('Arial Bold', 13), style="label.TLabel")
        self.show_tags_lbl = Label(self.scrollpar_frame, text="Put tags seperated by spaces or newlines here\nto make them show up in the results screen:", style="label.TLabel")
        self.show_tags_txt = Text(self.scrollpar_frame, width=int(gv.width/30), height=int(gv.height*0.01), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
        
        self.rename_var = IntVar(value=gv.config.getint('Danbooru', 'rename'))
        self.rename_chkbtn = Checkbutton(self.scrollpar_frame, text='Rename images from danbooru to danbooru name', var=self.rename_var, style="chkbtn.TCheckbutton")

        self.show_tags_txt.insert(END, gv.config['Danbooru']['tags'])
        self.tags = None

        self.gen_tagfile_var = IntVar(value=gv.config.getint('Danbooru', 'gen_tagfile'))
        self.tagfile_pixiv_var = IntVar(value=gv.config.getint('Danbooru', 'tagfile_pixiv'))
        self.tagfile_danbooru_var = IntVar(value=gv.config.getint('Danbooru', 'tagfile_danbooru'))
        self.tagfile_yandere_var = IntVar(value=gv.config.getint('Danbooru', 'tagfile_yandere'))
        self.tagfile_konachan_var = IntVar(value=gv.config.getint('Danbooru', 'tagfile_konachan'))
        self.gen_tagfile_chkbtn = Checkbutton(self.scrollpar_frame, text='Generate tagfiles for danbooru images', var=self.gen_tagfile_var, style="chkbtn.TCheckbutton")
        self.tagfile_pixiv_chkbtn = Checkbutton(self.scrollpar_frame, text='Include pixiv tags', var=self.tagfile_pixiv_var, style="chkbtn.TCheckbutton")
        self.tagfile_danbooru_chkbtn = Checkbutton(self.scrollpar_frame, text='Include danbooru tags', var=self.tagfile_danbooru_var, style="chkbtn.TCheckbutton")
        self.tagfile_yandere_chkbtn = Checkbutton(self.scrollpar_frame, text='Include yandere tags', var=self.tagfile_yandere_var, style="chkbtn.TCheckbutton")
        self.tagfile_konachan_chkbtn = Checkbutton(self.scrollpar_frame, text='Include konachan tags', var=self.tagfile_konachan_var, style="chkbtn.TCheckbutton")

        #self.save_btn = Button(parent, text='Save', command=self.danbooru_save, style ="button.TLabel")

    def danbooru_display(self):
        """
        Displays the danbooru options widgets
        """
        self.lord.forget()
        self.lord.PixO.forget()
        self.lord.YanO.forget()
        self.lord.KonO.forget()
        self.lord.Weight.forget()

        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*27)

        self.danbooru_lbl.place(x = x2, y = y + c * 1)
        self.scrollpar.display(x = x2, y= y + c * 2)

        self.use_danbooru_chkbtn.grid(row= 1, column= 0, sticky=W, padx=2, pady=1)
        self.show_tags_lbl.grid(row= 3, column= 0, sticky=W, padx=2, pady=1)
        self.show_tags_txt.grid(row= 4, column= 0, sticky=W, padx=2, pady=1)

        self.gen_tagfile_chkbtn.grid(row= 9, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.tagfile_pixiv_chkbtn.grid(row= 10, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_danbooru_chkbtn.grid(row= 11, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_yandere_chkbtn.grid(row= 12, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_konachan_chkbtn.grid(row= 13, column= 0, sticky=W, padx=15, pady=1, columnspan=2)

        self.rename_chkbtn.grid(row= 15, column= 0, sticky=W, padx=2, pady=1)

        #self.save_btn.place(x = int(gv.width/160*40), y = gv.height-220)

    def forget(self):
        self.danbooru_lbl.place_forget()
        self.scrollpar.sub_frame.place_forget()

        self.use_danbooru_chkbtn.grid_forget()
        self.show_tags_lbl.grid_forget()
        self.show_tags_txt.grid_forget()

        self.gen_tagfile_chkbtn.grid_forget()
        self.tagfile_pixiv_chkbtn.grid_forget()
        self.tagfile_danbooru_chkbtn.grid_forget()

        self.rename_chkbtn.grid_forget()

        #self.save_btn.place_forget()

    def danbooru_save(self):
        gv.Files.Log.write_to_log('Saving Danbooru options...')
        self.tags = self.show_tags_txt.get('1.0', END)
        gv.config['Danbooru']['tags'] = self.tags
        gv.config['Danbooru']['gen_tagfile'] = str(self.gen_tagfile_var.get())
        gv.config['Danbooru']['tagfile_pixiv'] = str(self.tagfile_pixiv_var.get())
        gv.config['Danbooru']['tagfile_danbooru'] = str(self.tagfile_danbooru_var.get())
        gv.config['Danbooru']['tagfile_yandere'] = str(self.tagfile_yandere_var.get())
        gv.config['Danbooru']['tagfile_konachan'] = str(self.tagfile_konachan_var.get())
        gv.config['Danbooru']['use'] = str(self.use_danbooru_var.get())
        gv.write_config()
        gv.results_tags_danbooru = self.tags.split()
        gv.Files.Log.write_to_log('Saved Danbooru options')

class YandereOptions():
    """Includes all widgets for Yandere and methods to display and modify them"""
    def __init__(self, parent, lord):
        self.par = parent
        self.lord = lord
        self.scrollpar = ScrollFrame(self.par, gv.width/3, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame
        self.use_yandere_var = IntVar(value=gv.config.getint('Yandere', 'use'))
        self.use_yandere_chkbtn = Checkbutton(self.scrollpar_frame, text='Use yandere', var=self.use_yandere_var, style="chkbtn.TCheckbutton")
        self.yandere_lbl = Label(parent, text="Yande.re", font=('Arial Bold', 13), style="label.TLabel")
        self.show_tags_lbl = Label(self.scrollpar_frame, text="Put tags seperated by spaces or newlines here\nto make them show up in the results screen:", style="label.TLabel")
        self.show_tags_txt = Text(self.scrollpar_frame, width=int(gv.width/30), height=int(gv.height*0.01), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
        
        self.rename_var = IntVar(value=gv.config.getint('Yandere', 'rename'))
        self.rename_chkbtn = Checkbutton(self.scrollpar_frame, text='Rename images from yandere to yandere name', var=self.rename_var, style="chkbtn.TCheckbutton")

        self.show_tags_txt.insert(END, gv.config['Yandere']['tags'])
        self.tags = None

        self.gen_tagfile_var = IntVar(value=gv.config.getint('Yandere', 'gen_tagfile'))
        self.tagfile_pixiv_var = IntVar(value=gv.config.getint('Yandere', 'tagfile_pixiv'))
        self.tagfile_danbooru_var = IntVar(value=gv.config.getint('Yandere', 'tagfile_danbooru'))
        self.tagfile_yandere_var = IntVar(value=gv.config.getint('Yandere', 'tagfile_yandere'))
        self.tagfile_konachan_var = IntVar(value=gv.config.getint('Yandere', 'tagfile_konachan'))
        self.gen_tagfile_chkbtn = Checkbutton(self.scrollpar_frame, text='Generate tagfiles for yandere images', var=self.gen_tagfile_var, style="chkbtn.TCheckbutton")
        self.tagfile_pixiv_chkbtn = Checkbutton(self.scrollpar_frame, text='Include pixiv tags', var=self.tagfile_pixiv_var, style="chkbtn.TCheckbutton")
        self.tagfile_danbooru_chkbtn = Checkbutton(self.scrollpar_frame, text='Include danbooru tags', var=self.tagfile_danbooru_var, style="chkbtn.TCheckbutton")
        self.tagfile_yandere_chkbtn = Checkbutton(self.scrollpar_frame, text='Include yandere tags', var=self.tagfile_yandere_var, style="chkbtn.TCheckbutton")
        self.tagfile_konachan_chkbtn = Checkbutton(self.scrollpar_frame, text='Include konachan tags', var=self.tagfile_konachan_var, style="chkbtn.TCheckbutton")

        #self.save_btn = Button(parent, text='Save', command=self.yandere_save, style ="button.TLabel")

    def yandere_display(self):
        """
        Displays the yandere options widgets
        """
        self.lord.forget()
        self.lord.PixO.forget()
        self.lord.DanO.forget()
        self.lord.KonO.forget()
        self.lord.Weight.forget()

        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*27)

        self.yandere_lbl.place(x = x2, y = y + c * 1)
        self.scrollpar.display(x = x2, y= y + c * 2)

        self.use_yandere_chkbtn.grid(row= 1, column= 0, sticky=W, padx=2, pady=1)
        self.show_tags_lbl.grid(row= 3, column= 0, sticky=W, padx=2, pady=1)
        self.show_tags_txt.grid(row= 4, column= 0, sticky=W, padx=2, pady=1)

        self.gen_tagfile_chkbtn.grid(row= 9, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.tagfile_pixiv_chkbtn.grid(row= 10, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_danbooru_chkbtn.grid(row= 11, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_yandere_chkbtn.grid(row= 12, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_konachan_chkbtn.grid(row= 13, column= 0, sticky=W, padx=15, pady=1, columnspan=2)


        self.rename_chkbtn.grid(row= 15, column= 0, sticky=W, padx=2, pady=1)

        #self.save_btn.place(x = int(gv.width/160*40), y = gv.height-220)

    def forget(self):
        self.yandere_lbl.place_forget()
        self.scrollpar.sub_frame.place_forget()

        self.use_yandere_chkbtn.grid_forget()
        self.show_tags_lbl.grid_forget()
        self.show_tags_txt.grid_forget()

        self.gen_tagfile_chkbtn.grid_forget()
        self.tagfile_pixiv_chkbtn.grid_forget()
        self.tagfile_danbooru_chkbtn.grid_forget()

        self.rename_chkbtn.grid_forget()

        #self.save_btn.place_forget()

    def yandere_save(self):
        gv.Files.Log.write_to_log('Saving Yande.re options...')
        self.tags = self.show_tags_txt.get('1.0', END)
        gv.config['Yandere']['tags'] = self.tags
        gv.config['Yandere']['gen_tagfile'] = str(self.gen_tagfile_var.get())
        gv.config['Yandere']['tagfile_pixiv'] = str(self.tagfile_pixiv_var.get())
        gv.config['Yandere']['tagfile_danbooru'] = str(self.tagfile_danbooru_var.get())
        gv.config['Yandere']['tagfile_yandere'] = str(self.tagfile_yandere_var.get())
        gv.config['Yandere']['tagfile_konachan'] = str(self.tagfile_konachan_var.get())
        gv.config['Yandere']['use'] = str(self.use_yandere_var.get())
        gv.write_config()
        gv.results_tags_yandere = self.tags.split()
        gv.Files.Log.write_to_log('Saved Yande.re options')

class KonachanOptions():
    """Includes all widgets for Konachan and methods to display and modify them"""
    def __init__(self, parent, lord):
        self.par = parent
        self.lord = lord
        self.scrollpar = ScrollFrame(self.par, gv.width/3, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame
        self.use_konachan_var = IntVar(value=gv.config.getint('Konachan', 'use'))
        self.use_konachan_chkbtn = Checkbutton(self.scrollpar_frame, text='Use konachan', var=self.use_konachan_var, style="chkbtn.TCheckbutton")
        self.konachan_lbl = Label(parent, text="Konachan", font=('Arial Bold', 13), style="label.TLabel")
        self.show_tags_lbl = Label(self.scrollpar_frame, text="Put tags seperated by spaces or newlines here\nto make them show up in the results screen:", style="label.TLabel")
        self.show_tags_txt = Text(self.scrollpar_frame, width=int(gv.width/30), height=int(gv.height*0.01), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10))
        
        self.rename_var = IntVar(value=gv.config.getint('Konachan', 'rename'))
        self.rename_chkbtn = Checkbutton(self.scrollpar_frame, text='Rename images from konachan to konachan name', var=self.rename_var, style="chkbtn.TCheckbutton")

        self.show_tags_txt.insert(END, gv.config['Konachan']['tags'])
        self.tags = None

        self.gen_tagfile_var = IntVar(value=gv.config.getint('Konachan', 'gen_tagfile'))
        self.tagfile_pixiv_var = IntVar(value=gv.config.getint('Konachan', 'tagfile_pixiv'))
        self.tagfile_danbooru_var = IntVar(value=gv.config.getint('Konachan', 'tagfile_danbooru'))
        self.tagfile_yandere_var = IntVar(value=gv.config.getint('Konachan', 'tagfile_yandere'))
        self.tagfile_konachan_var = IntVar(value=gv.config.getint('Konachan', 'tagfile_konachan'))
        self.gen_tagfile_chkbtn = Checkbutton(self.scrollpar_frame, text='Generate tagfiles for konachan images', var=self.gen_tagfile_var, style="chkbtn.TCheckbutton")
        self.tagfile_pixiv_chkbtn = Checkbutton(self.scrollpar_frame, text='Include pixiv tags', var=self.tagfile_pixiv_var, style="chkbtn.TCheckbutton")
        self.tagfile_danbooru_chkbtn = Checkbutton(self.scrollpar_frame, text='Include danbooru tags', var=self.tagfile_danbooru_var, style="chkbtn.TCheckbutton")
        self.tagfile_yandere_chkbtn = Checkbutton(self.scrollpar_frame, text='Include yandere tags', var=self.tagfile_yandere_var, style="chkbtn.TCheckbutton")
        self.tagfile_konachan_chkbtn = Checkbutton(self.scrollpar_frame, text='Include konachan tags', var=self.tagfile_konachan_var, style="chkbtn.TCheckbutton")

        #self.save_btn = Button(parent, text='Save', command=self.konachan_save, style ="button.TLabel")

    def konachan_display(self):
        """
        Displays the konachan options widgets
        """
        self.lord.forget()
        self.lord.PixO.forget()
        self.lord.DanO.forget()
        self.lord.YanO.forget()
        self.lord.Weight.forget()

        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*27)

        self.konachan_lbl.place(x = x2, y = y + c * 1)
        self.scrollpar.display(x = x2, y= y + c * 2)

        self.use_konachan_chkbtn.grid(row= 1, column= 0, sticky=W, padx=2, pady=1)
        self.show_tags_lbl.grid(row= 3, column= 0, sticky=W, padx=2, pady=1)
        self.show_tags_txt.grid(row= 4, column= 0, sticky=W, padx=2, pady=1)

        self.gen_tagfile_chkbtn.grid(row= 9, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.tagfile_pixiv_chkbtn.grid(row= 10, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_danbooru_chkbtn.grid(row= 11, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_yandere_chkbtn.grid(row= 12, column= 0, sticky=W, padx=15, pady=1, columnspan=2)
        self.tagfile_konachan_chkbtn.grid(row= 13, column= 0, sticky=W, padx=15, pady=1, columnspan=2)

        self.rename_chkbtn.grid(row= 15, column= 0, sticky=W, padx=2, pady=1)

        #self.save_btn.place(x = int(gv.width/160*40), y = gv.height-220)

    def forget(self):
        self.konachan_lbl.place_forget()
        self.scrollpar.sub_frame.place_forget()

        self.use_konachan_chkbtn.grid_forget()
        self.show_tags_lbl.grid_forget()
        self.show_tags_txt.grid_forget()

        self.gen_tagfile_chkbtn.grid_forget()
        self.tagfile_pixiv_chkbtn.grid_forget()
        self.tagfile_danbooru_chkbtn.grid_forget()

        self.rename_chkbtn.grid_forget()

        #self.save_btn.place_forget()

    def konachan_save(self):
        gv.Files.Log.write_to_log('Saving Konachan options...')
        self.tags = self.show_tags_txt.get('1.0', END)
        gv.config['Konachan']['tags'] = self.tags
        gv.config['Konachan']['gen_tagfile'] = str(self.gen_tagfile_var.get())
        gv.config['Konachan']['tagfile_pixiv'] = str(self.tagfile_pixiv_var.get())
        gv.config['Konachan']['tagfile_danbooru'] = str(self.tagfile_danbooru_var.get())
        gv.config['Konachan']['tagfile_yandere'] = str(self.tagfile_yandere_var.get())
        gv.config['Konachan']['tagfile_konachan'] = str(self.tagfile_konachan_var.get())
        gv.config['Konachan']['use'] = str(self.use_konachan_var.get())
        gv.write_config()
        gv.results_tags_konachan = self.tags.split()
        gv.Files.Log.write_to_log('Saved Konachan options')

