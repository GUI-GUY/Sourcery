from tkinter import IntVar, E, W, colorchooser, Text, END
#from tkinter import messagebox as mb
from tkinter.ttk import Label, Checkbutton, Button, Style, Entry, Frame
from functools import partial
from webbrowser import open_new
from pixiv_handler import pixiv_login
from file_operations import change_input, change_output
from ScrollFrame import ScrollFrame
import global_variables as gv


class Options():
    """Hosts all Options classes and methods to switch between the options views"""
    def __init__(self, parent, display_startpage, enforce_style):
        self.par = parent
        self.NAOO = SauceNaoOptions(parent)
        self.SouO = SourceryOptions(parent, enforce_style)
        self.ProO = ProviderOptions(parent)
        self.options_lbl = Label(parent, text="Options", font=("Arial Bold", 20), style="label.TLabel")

        self.provider_options_btn = Button(parent, text="Provider", command=self.display_provider_options, style="button.TLabel")
        self.saucenao_options_btn = Button(parent, text="SauceNao", command=self.display_saucenao_options, style="button.TLabel")
        self.sourcery_options_btn = Button(parent, text="Sourcery", command=self.display_sourcery_options, style="button.TLabel")

        self.options_back_btn = Button(parent, text="Back", command=display_startpage, style="button.TLabel")

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

        self.options_back_btn.place(x = int(gv.width/160*5), y = int(gv.height/90*50))

    def forget_all_widgets(self):
        for widget in self.par.winfo_children():
            widget.place_forget()

class SauceNaoOptions():
    """Includes all widgets for SauceNao and methods to display and modify them"""
    def __init__(self, parent):
        self.par = parent
        self.saucenao_key_lbl = Label(parent, text="SauceNao API-Key", style="label.TLabel")
        self.saucenao_key_number_lbl = Label(parent, width=50, text=gv.Files.Cred.saucenao_api_key, style="button.TLabel")
        self.saucenao_key_entry = Entry(parent, width=52, style="button.TLabel")
        self.saucenao_key_change_btn = Button(parent, text="Change", command=self.saucenao_change_key, style="button.TLabel")
        self.saucenao_key_confirm_btn = Button(parent, text="Confirm", command=self.saucenao_set_key, style="button.TLabel")
        self.saucenao_minsim_lbl = Label(parent, text="Minimum similarity", style="label.TLabel")
        self.saucenao_minsim_entry = Entry(parent, width=20, style="button.TLabel")
        self.saucenao_minsim_entry.insert(0, gv.Files.Conf.minsim)
        self.saucenao_minsim_confirm_btn = Button(parent, text="Save", command=self.saucenao_save, style="button.TLabel")

        self.saucenao_address_1 = Label(parent, text="Your API-Key can be found here:", style="label.TLabel")
        self.saucenao_address_2 = Label(parent, text="https://saucenao.com/user.php?page=search-api", style="label.TLabel")
        self.saucenao_address_2.configure(foreground='#2626ff', cursor='hand2', font=('Arial', 10))
        self.saucenao_address_2.bind("<Button-1>", self.hyperlink)
    
    def display(self):
        """
        Draw options (API-Key, minsim) for SauceNao:
        """
        self.saucenao_key_lbl.place(x = int(gv.width/160*5), y = int(gv.height/90*10))
        self.saucenao_key_number_lbl.place(x = int(gv.width/160*18), y = int(gv.height/90*10))
        self.saucenao_key_change_btn.place(x = int(gv.width/160*55), y = int(gv.height/90*10))
        self.saucenao_minsim_lbl.place(x = int(gv.width/160*5), y = int(gv.height/90*12.3))
        self.saucenao_minsim_entry.place(x = int(gv.width/160*18), y = int(gv.height/90*12.3))
        self.saucenao_minsim_confirm_btn.place(x = int(gv.width/160*55), y = int(gv.height/90*12.3))
        self.saucenao_address_1.place(x = int(gv.width/160*5), y = int(gv.height/90*15.6))
        self.saucenao_address_2.place(x = int(gv.width/160*5), y = int(gv.height/90*17.9))
    
    def saucenao_change_key(self):
        """
        Unlock API-Key widget for SauceNao, so that you can change your API-Key. 
        """
        self.saucenao_key_change_btn.place_forget()
        self.saucenao_key_number_lbl.place_forget()
        self.saucenao_key_confirm_btn.place(x = int(gv.width/160*55), y = int(gv.height/90*10))
        self.saucenao_key_entry.place(x = int(gv.width/160*18), y = int(gv.height/90*10))
        self.saucenao_key_entry.delete(0, len(gv.Files.Cred.saucenao_api_key))
        self.saucenao_key_entry.insert(0, gv.Files.Cred.saucenao_api_key)
        
    def saucenao_set_key(self):
        """
        Save SauceNao API-Key and revert the widget to being uneditable.
        """
        gv.Files.Log.write_to_log('Attempting to save SauceNao API-Key')
        gv.Files.Cred.saucenao_api_key = self.saucenao_key_entry.get()
        e = gv.Files.Cred.write_credentials()
        if e == None:
            gv.Files.Log.write_to_log('Saved SauceNao API-Key successfully')
        else:
            gv.Files.Log.write_to_log('Failed to save SauceNao API-Key')
        self.saucenao_key_confirm_btn.place_forget()
        self.saucenao_key_entry.place_forget()
        self.saucenao_key_change_btn.place(x = int(gv.width/160*55), y = int(gv.height/90*10))
        self.saucenao_key_number_lbl.configure(text=gv.Files.Cred.saucenao_api_key)
        self.saucenao_key_number_lbl.place(x = int(gv.width/160*18), y = int(gv.height/90*10))

    def saucenao_save(self):
        gv.Files.Log.write_to_log('Attempting to save SauceNAO options...')
        gv.Files.Conf.minsim = self.saucenao_minsim_entry.get()
        gv.Files.Conf.write_config()
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

        rel = 'raised'
        self.custom_background_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_foreground_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_background_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_background_active_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_foreground_active_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_background_pressed_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.custom_button_foreground_pressed_color_lbl = Label(parent, width=10, relief=rel, style="label.TLabel")
        self.color_bind()

        self.save_custom_theme_btn = Button(parent, text="Save Custom Theme", command=self.save_custom_theme, style="button.TLabel")

        self.input_dir_0_lbl = Label(parent, text="Input Directory:", style="label.TLabel")
        self.input_dir_1_lbl = Label(parent, text=gv.input_dir, style="label.TLabel")
        self.input_dir_btn = Button(parent, text='Change', command=self.change_input, style="button.TLabel")
        self.output_dir_0_lbl = Label(parent, text="Output Directory:", style="label.TLabel")
        self.output_dir_1_lbl = Label(parent, text=gv.output_dir, style="label.TLabel")
        self.output_dir_btn = Button(parent, text='Change', command=self.change_output, style="button.TLabel")

        if gv.Files.Conf.delete_input == '':
            gv.Files.Conf.delete_input = '0'
            gv.Files.Conf.write_config()
        self.delete_input_var = IntVar(value=int(gv.Files.Conf.delete_input))
        self.delete_input_chkbtn = Checkbutton(parent, var=self.delete_input_var, text="Delete sourced images from the Input folder?", style="chkbtn.TCheckbutton")

        self.images_per_page_lbl = Label(parent, text="Images per page", font=("Arial Bold", 10), style="label.TLabel")
        self.images_per_page_entry = Entry(parent, width=30, style="button.TLabel")
        self.images_per_page_entry.insert(0, gv.Files.Conf.imgpp)
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
        self.custom_background_color_lbl.place(x = x2, y = y + c * 4)
        self.custom_foreground_color_lbl.place(x = x2, y = y + c * 5)
        self.custom_button_background_color_lbl.place(x = x2, y = y + c * 6)
        self.custom_button_background_active_color_lbl.place(x = x2, y = y + c * 7)
        self.custom_button_foreground_active_color_lbl.place(x = x2, y = y + c * 8)
        self.custom_button_background_pressed_color_lbl.place(x = x2, y = y + c * 9)
        self.custom_button_foreground_pressed_color_lbl.place(x = x2, y = y + c * 10)

        self.save_custom_theme_btn.place(x = x1, y = y + c * 12)

        self.images_per_page_lbl.place(x = x1, y = y + c * 15)
        self.images_per_page_entry.place(x = x2, y = y + c * 15)

        self.delete_input_chkbtn.place(x = x1, y = y + c * 16)

        self.input_dir_0_lbl.place(x = x1, y = y + c * 17)
        self.input_dir_1_lbl.place(x = x2, y = y + c * 17)
        self.input_dir_btn.place(x = x1+100, y = y + c * 17)
        self.output_dir_0_lbl.place(x = x1, y = y + c * 18)
        self.output_dir_1_lbl.place(x = x2, y = y + c * 18)
        self.output_dir_btn.place(x = x1+100, y = y + c * 18)

        self.sourcery_confirm_btn.place(x = x1, y = y + c * 23)

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
        gv.Files.Log.write_to_log('Attempting to save Sourcery options...')
        gv.Files.Conf.imgpp = self.images_per_page_entry.get()
        gv.Files.Conf.delete_input = str(self.delete_input_var.get())
        gv.Files.Conf.write_config()
        gv.Files.Log.write_to_log('Saved Sourcery Options')

class ProviderOptions():
    """Hosts all image provider options Classes"""
    def __init__(self, parent):
        self.par = parent
        self.PixO = PixivOptions(parent)
        self.DanO = DanbooruOptions(parent)
    
    def display(self):
        """
        Draw options (login) for all image providers:
        - Pixiv 
        """
        self.PixO.pixiv_display()
        self.DanO.danb_display()

class PixivOptions():
    """Includes all widgets for Pixiv and methods to display and modify them"""
    def __init__(self, parent):
        self.par = parent
        self.scrollpar = ScrollFrame(self.par, gv.width/4, gv.height*0.6)
        self.scrollpar_frame =self.scrollpar.frame
        self.pixiv_lbl = Label(parent, text="Pixiv", font=('Arial Bold', 13), style="label.TLabel")
        self.pixiv_login_lbl = Label(self.scrollpar_frame, text="Pixiv Login", style="label.TLabel")
        self.pixiv_user_lbl = Label(self.scrollpar_frame, text="Username", style="label.TLabel")
        self.pixiv_user_filled_lbl = Label(self.scrollpar_frame, width=50, text=gv.Files.Cred.pixiv_username, style="button.TLabel")
        self.pixiv_user_entry = Entry(self.scrollpar_frame, width=52, style="button.TLabel")
        self.pixiv_password_lbl = Label(self.scrollpar_frame, text="Password", style="label.TLabel")
        self.pixiv_password_filled_lbl = Label(self.scrollpar_frame, width=50, text=gv.Files.Cred.pixiv_password, style="button.TLabel")
        self.pixiv_password_entry = Entry(self.scrollpar_frame, width=52, style="button.TLabel")
        self.pixiv_login_change_btn = Button(self.scrollpar_frame, text="Change", command=self.pixiv_change_login, style="button.TLabel")
        self.pixiv_login_confirm_btn = Button(self.scrollpar_frame, text="Confirm & Save", command=partial(self.pixiv_set_login, True), style="button.TLabel")
        self.pixiv_login_confirm_nosave_btn = Button(self.scrollpar_frame, text="Confirm & Don't Save", command=partial(self.pixiv_set_login, False), style="button.TLabel")
        self.pixiv_warning_lbl = Label(self.scrollpar_frame, width=50, text='THIS WILL BE SAVED IN PLAINTEXT!!!', style="label.TLabel")
        if gv.Files.Conf.rename_pixiv == 'True':
            self.rename_var = IntVar(value=1)
        else:
            self.rename_var = IntVar(value=0)
        self.rename_chkbtn = Checkbutton(self.scrollpar_frame, text='Rename images from pixiv to pixiv name', var=self.rename_var, style="chkbtn.TCheckbutton")
        self.save_btn = Button(parent, text='Save', command=self.pixiv_save, style ="button.TLabel")

        self.show_tags_lbl = Label(self.scrollpar_frame, text="Put tags seperated by spaces or newlines here\nto make them show up in the results screen:", style="label.TLabel")
        self.show_tags_txt = Text(self.scrollpar_frame, width=int(gv.width/30), height=int(gv.height*0.01), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10)) # TODO not upadated with theme

        self.show_tags_txt.insert(END, gv.Files.Conf.tags_pixiv)
        self.tags = None

        self.pixiv_address_1 = Label(self.scrollpar_frame, text="Your Login Data can be found here:", style="label.TLabel")
        self.pixiv_address_2 = Label(self.scrollpar_frame, text="https://www.pixiv.net/setting_user.php", style="label.TLabel")
        self.pixiv_address_2.configure(foreground='#2626ff', cursor='hand2', font=('Arial', 10))
        self.pixiv_address_2.bind("<Button-1>", self.hyperlink)

    def pixiv_change_login(self):
        """
        Unlock login widget for pixiv, so that you can change your login data. 
        """
        self.pixiv_user_filled_lbl.grid_forget()
        self.pixiv_password_filled_lbl.grid_forget()
        self.pixiv_login_change_btn.grid_forget()
        self.pixiv_user_entry.grid(row= 1, column= 1, sticky=W, padx=2, pady=1)
        self.pixiv_password_entry.grid(row= 2, column= 1, sticky=W, padx=2, pady=1)
        self.pixiv_login_confirm_btn.grid(row= 3, column= 0, sticky=W, padx=2, pady=1)
        self.pixiv_login_confirm_nosave_btn.grid(row= 3, column= 1, sticky=W, padx=2, pady=1)
        self.pixiv_user_entry.delete(0, len(gv.Files.Cred.pixiv_username))
        self.pixiv_password_entry.delete(0, len(gv.Files.Cred.pixiv_password))
        self.pixiv_user_entry.insert(0, gv.Files.Cred.pixiv_username)
        self.pixiv_password_entry.insert(0, gv.Files.Cred.pixiv_password)

    def pixiv_set_login(self, save):
        """
        Save pixiv login data and revert the widgets to being uneditable.
        """
        self.pixiv_user_entry.grid_forget()
        self.pixiv_password_entry.grid_forget()
        self.pixiv_login_confirm_btn.grid_forget()
        self.pixiv_login_confirm_nosave_btn.grid_forget()
        self.pixiv_user_filled_lbl.grid(row= 1, column= 1, sticky=W, padx=2, pady=1)
        self.pixiv_password_filled_lbl.grid(row= 2, column= 1, sticky=W, padx=2, pady=1)
        self.pixiv_login_change_btn.grid(row= 3, column= 0, sticky=W, padx=2, pady=1)
        
        gv.Files.Cred.pixiv_username = self.pixiv_user_entry.get()
        gv.Files.Cred.pixiv_password = self.pixiv_password_entry.get()
        if save:
            gv.Files.Log.write_to_log('Attempting to save Pixiv Login Data...')
            e = gv.Files.Cred.write_credentials()
        else:
            gv.Files.Log.write_to_log('Attempting to generate refreshtoken and save it...')
            pixiv_login()
            gv.Files.Cred.pixiv_username = ''
            gv.Files.Cred.pixiv_password = ''
            e = gv.Files.Cred.write_credentials()
        if e == None:
            gv.Files.Log.write_to_log('Saved pixiv login data successfully')
        self.pixiv_user_filled_lbl.configure(text=gv.Files.Cred.pixiv_username)
        self.pixiv_password_filled_lbl.configure(text=gv.Files.Cred.pixiv_password)

    def pixiv_display(self):
        """
        Displays the pixiv options widgets
        """
        self.pixiv_user_entry.grid_forget()
        self.pixiv_password_entry.grid_forget()
        self.pixiv_login_confirm_btn.grid_forget()
        self.pixiv_login_confirm_nosave_btn.grid_forget()
        
        self.pixiv_lbl.place(x = int(gv.width/160*5), y = int(gv.height/90*8))
        self.scrollpar.display(x = int(gv.width/160*5), y= int(gv.height/90*10))

        #TODO lager das aus damits nicht öfters aufgerufen wird
        self.pixiv_login_lbl.grid(row= 0, column= 0, sticky=W, padx=2, pady=1)
        self.pixiv_user_lbl.grid(row= 1, column= 0, sticky=W, padx=2, pady=1)
        self.pixiv_user_filled_lbl.grid(row= 1, column= 1, sticky=W, padx=2, pady=1)
        self.pixiv_password_lbl.grid(row= 2, column= 0, sticky=W, padx=2, pady=1)
        self.pixiv_password_filled_lbl.grid(row= 2, column= 1, sticky=W, padx=2, pady=1)
        self.pixiv_login_change_btn.grid(row= 3, column= 0, sticky=W, padx=2, pady=1)
        self.pixiv_warning_lbl.grid(row= 4, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.pixiv_address_1.grid(row= 5, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.pixiv_address_2.grid(row= 6, column= 0, sticky=W, padx=2, pady=1, columnspan=2)

        self.show_tags_lbl.grid(row= 7, column= 0, sticky=W, padx=2, pady=1, columnspan=3)
        self.show_tags_txt.grid(row= 8, column= 0, sticky=W, padx=2, pady=1, columnspan=3)
        self.scrollpar_frame.columnconfigure(2, weight=1)

        self.rename_chkbtn.grid(row= 9, column= 0, sticky=W, padx=2, pady=1, columnspan=2)
        self.save_btn.place(x = int(gv.width/160*5), y = gv.height-220)

    def pixiv_save(self):
        gv.Files.Log.write_to_log('Attempting to save Pixiv options...')
        if self.rename_var.get() == 1:
            gv.Files.Conf.rename_pixiv = 'True'
        else:
            gv.Files.Conf.rename_pixiv = 'False'
        self.tags = self.show_tags_txt.get('1.0', END)
        gv.Files.Conf.tags_pixiv = self.tags
        gv.Files.Conf.write_config()
        gv.results_tags_pixiv = self.tags.split()
        gv.Files.Log.write_to_log('Saved Pixiv options')
    
    def hyperlink(self, event):
        """
        Opens a webbrowser with a URL on click of a widget that is bound to this method
        """
        open_new(event.widget.cget("text"))

class DanbooruOptions():
    """Includes all widgets for Danbooru and methods to display and modify them"""
    def __init__(self, parent):
        self.par = parent
        self.scrollpar = ScrollFrame(self.par, gv.width/4, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame
        self.danbooru_lbl = Label(parent, text="Danbooru", font=('Arial Bold', 13), style="label.TLabel")
        self.show_tags_lbl = Label(self.scrollpar_frame, text="Put tags seperated by spaces or newlines here\nto make them show up in the results screen:", style="label.TLabel")
        self.show_tags_txt = Text(self.scrollpar_frame, width=int(gv.width/30), height=int(gv.height*0.01), foreground=gv.Files.Theme.foreground, background=gv.Files.Theme.background, font=("Arial Bold", 10)) # TODO not upadated with theme
        self.save_btn = Button(parent, text='Save', command=self.danbooru_save, style ="button.TLabel")

        self.show_tags_txt.insert(END, gv.Files.Conf.tags_danbooru)
        self.tags = None

    def danb_display(self):
        """
        Displays the danbooru options widgets
        """
        self.danbooru_lbl.place(x = int(gv.width/160*50), y = int(gv.height/90*8))
        self.scrollpar.display(x = int(gv.width/160*50), y= int(gv.height/90*10))

        self.show_tags_lbl.grid(row= 0, column= 0, sticky=W, padx=2, pady=1)
        self.show_tags_txt.grid(row= 1, column= 0, sticky=W, padx=2, pady=1)
        self.save_btn.place(x = int(gv.width/160*50), y = gv.height-220)

    def danbooru_save(self):
        gv.Files.Log.write_to_log('Attempting to save Danbooru options...')
        self.tags = self.show_tags_txt.get('1.0', END)
        gv.Files.Conf.tags_danbooru = self.tags
        gv.Files.Conf.write_config()
        gv.results_tags_danbooru = self.tags.split()
        gv.Files.Log.write_to_log('Saved Danbooru options')
