from tkinter import IntVar
#from tkinter import messagebox as mb
from tkinter.ttk import Label, Checkbutton, Button, Style, Entry, Frame
from functools import partial
from pixiv_handler import pixiv_login
import global_variables as gv

class Options():
    """Options"""
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
        self.options_lbl.place(x = 50, y = 10)

        self.sourcery_options_btn.place(x = 50, y = 50)
        self.provider_options_btn.place(x = 150, y = 50)
        self.saucenao_options_btn.place(x = 250, y = 50)

        self.options_back_btn.place(x = 50, y = 500)

    def forget_all_widgets(self):
        for widget in self.par.winfo_children():
            widget.place_forget()

class SauceNaoOptions():
    """SauceNaoOptions"""
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
    
    def display(self):
        """
        Draw options (API-Key, minsim) for SauceNao:
        """
        self.saucenao_key_lbl.place(x = 50, y = 100)
        self.saucenao_key_number_lbl.place(x = 180, y = 100)
        self.saucenao_key_change_btn.place(x = 550, y = 100)
        self.saucenao_minsim_lbl.place(x = 50, y = 123)
        self.saucenao_minsim_entry.place(x = 180, y = 123)
        self.saucenao_minsim_confirm_btn.place(x = 550, y = 123)
    
    def saucenao_change_key(self):
        """
        Unlock API-Key widget for SauceNao, so that you can change your API-Key. 
        """
        self.saucenao_key_change_btn.place_forget()
        self.saucenao_key_number_lbl.place_forget()
        self.saucenao_key_confirm_btn.place(x = 550, y = 100)
        self.saucenao_key_entry.place(x = 180, y = 100)
        self.saucenao_key_entry.delete(0, len(gv.Files.Cred.saucenao_api_key))
        self.saucenao_key_entry.insert(0, gv.Files.Cred.saucenao_api_key)
        
    def saucenao_set_key(self):
        """
        Save SauceNao API-Key and revert the widget to being uneditable.
        """
        gv.Files.Log.write_to_log('Attempting to save SauceNao API-Key')
        gv.Files.Cred.saucenao_api_key = self.saucenao_key_entry.get()
        e = gv.Files.Cred.write_credentials(gv.Files.Cred.saucenao_api_key)
        if e == None:
            gv.Files.Log.write_to_log('Saved SauceNao API-Key successfully')
        else:
            gv.Files.Log.write_to_log('Failed to save SauceNao API-Key')
        self.saucenao_key_confirm_btn.place_forget()
        self.saucenao_key_entry.place_forget()
        self.saucenao_key_change_btn.place(x = 550, y = 100)
        self.saucenao_key_number_lbl.configure(text=gv.Files.Cred.saucenao_api_key)
        self.saucenao_key_number_lbl.place(x = 180, y = 100)

    def saucenao_save(self):
        gv.Files.Log.write_to_log('Attempting to save SauceNAO options...')
        gv.Files.Conf.minsim = self.saucenao_minsim_entry.get()
        gv.Files.Conf.write_config()
        gv.Files.Log.write_to_log('Saved SauceNao Options')

class SourceryOptions():
    """SourceryOptions"""
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
        self.custom_background_entry = Entry(parent, width=30, style="button.TLabel")
        self.custom_foreground_entry = Entry(parent, width=30, style="button.TLabel")
        self.custom_button_background_entry = Entry(parent, width=30, style="button.TLabel")
        self.custom_button_background_active_entry = Entry(parent, width=30, style="button.TLabel")
        self.custom_button_foreground_active_entry = Entry(parent, width=30, style="button.TLabel")
        self.custom_button_background_pressed_entry = Entry(parent, width=30, style="button.TLabel")
        self.custom_button_foreground_pressed_entry = Entry(parent, width=30, style="button.TLabel")
        self.save_custom_theme_btn = Button(parent, text="Save Custom Theme", command=self.save_custom_theme, style="button.TLabel")

        self.custom_background = gv.Files.Theme.custom_background
        self.custom_foreground = gv.Files.Theme.custom_foreground
        self.custom_button_background = gv.Files.Theme.custom_button_background
        self.custom_button_background_active = gv.Files.Theme.custom_button_background_active
        self.custom_button_foreground_active = gv.Files.Theme.custom_button_foreground_active
        self.custom_button_background_pressed = gv.Files.Theme.custom_button_background_pressed
        self.custom_button_foreground_pressed = gv.Files.Theme.custom_button_foreground_pressed

        self.style = Style()
        self.preview_btn = Button(parent, text="Preview Button", style="preview.TLabel")
        self.preview_lbl = Label(parent, text="Preview Label")

        self.invalid_lbl_array = list()
        self.old_one_invalid = False
        self.save_custom_theme_btn_state = 'enabled'
        for i in range(7):
            self.invalid_lbl_array.append(Label(master=parent, text = 'Invalid!', style="label.TLabel"))

        self.refresh_custom_preview_init = False

    def display(self):
        """
        Draw options for Sourcery Application:
        - Themes
        """
        y = 100
        c = 23
        x1 = 50
        x2 = 240
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
        self.custom_background_entry.place(x = x2, y = y + c * 4)
        self.custom_foreground_entry.place(x = x2, y = y + c * 5)
        self.custom_button_background_entry.place(x = x2, y = y + c * 6)
        self.custom_button_background_active_entry.place(x = x2, y = y + c * 7)
        self.custom_button_foreground_active_entry.place(x = x2, y = y + c * 8)
        self.custom_button_background_pressed_entry.place(x = x2, y = y + c * 9)
        self.custom_button_foreground_pressed_entry.place(x = x2, y = y + c * 10)
        self.save_custom_theme_btn.place(x = x1, y = y + c * 11)
        self.preview_lbl.place(x = x2, y = y + c * 2)
        self.preview_btn.place(x = x2, y = y + c * 3)

        if not self.refresh_custom_preview_init:
            self.refresh_custom_preview_init = True
            self.refresh_custom_preview()
    
    def refresh_custom_preview(self):
        one_invalid = False

        bg = self.custom_background_entry.get()
        if self.color_check(bg, 0, 4):
            one_invalid = True

        fg = self.custom_foreground_entry.get()
        if self.color_check(fg, 1, 5):
            one_invalid = True

        bbg = self.custom_button_background_entry.get()
        if self.color_check(bbg, 2, 6):
            one_invalid = True

        bba = self.custom_button_background_active_entry.get()
        if self.color_check(bba, 3, 7):
            one_invalid = True

        bfa = self.custom_button_foreground_active_entry.get()
        if self.color_check(bfa, 4, 8):
            one_invalid = True

        bbp = self.custom_button_background_pressed_entry.get()
        if self.color_check(bbp, 5, 9):
            one_invalid = True

        bfp = self.custom_button_foreground_pressed_entry.get()
        if self.color_check(bfp, 6, 10):
            one_invalid = True

        if one_invalid != self.old_one_invalid:
            self.old_one_invalid = one_invalid
            if self.save_custom_theme_btn_state == 'disabled':
                self.save_custom_theme_btn.configure(state='enabled')
                self.save_custom_theme_btn_state = 'enabled'
            else:
                self.save_custom_theme_btn.configure(state='disabled')
                self.save_custom_theme_btn_state = 'disabled'
        try:
            self.preview_lbl.configure(foreground=fg, background=bg, font=("Arial Bold", 10))
            self.style.configure("preview.TLabel", foreground=fg, background=bbg, font=("Arial Bold", 10))
            self.style.map("preview.TLabel", 
                foreground=[('pressed', bfp), ('active', bfa)],
                background=[('pressed', '!disabled', bbp), ('active', bba)])
        except:
            pass
        #TODO'Please insert a value between #000000 and #ffffff or a valid color name into the Background option'
        self.par.after(100, self.refresh_custom_preview)

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
        self.custom_background = self.custom_background_entry.get()
        self.custom_foreground = self.custom_foreground_entry.get()
        self.custom_button_background = self.custom_button_background_entry.get()
        self.custom_button_background_active = self.custom_button_background_active_entry.get()
        self.custom_button_foreground_active = self.custom_button_foreground_active_entry.get()
        self.custom_button_background_pressed = self.custom_button_background_pressed_entry.get()
        self.custom_button_foreground_pressed = self.custom_button_foreground_pressed_entry.get()
        self.color_insert()
        gv.Files.Theme.custom_background = self.custom_background_entry.get()
        gv.Files.Theme.custom_foreground = self.custom_foreground_entry.get()
        gv.Files.Theme.custom_button_background = self.custom_button_background_entry.get()
        gv.Files.Theme.custom_button_background_active = self.custom_button_background_active_entry.get()
        gv.Files.Theme.custom_button_foreground_active = self.custom_button_foreground_active_entry.get()
        gv.Files.Theme.custom_button_background_pressed = self.custom_button_background_pressed_entry.get()
        gv.Files.Theme.custom_button_foreground_pressed = self.custom_button_foreground_pressed_entry.get()
        e = gv.Files.Theme.write_theme(gv.Files.Theme.current_theme)
        if e == None:
            gv.Files.Log.write_to_log('Saved custom theme successfully')
        else:
            gv.Files.Log.write_to_log('Failed to save Custom Theme')

    def color_check(self, color, index, offset):
        y = 100
        c = 23
        if color.startswith('#') and (len(color) == 7 or len(color) == 4):
            try:
                num = int(color[1:], 16)
                if num < 0 or num > 16777215:
                    self.invalid_lbl_array[index].place(x = 440, y = y + c * offset)
                    return True
                else:
                    self.invalid_lbl_array[index].place_forget()
            except:
                self.invalid_lbl_array[index].place(x = 440, y = y + c * offset)
                return True
        elif color not in gv.COLORS:
            self.invalid_lbl_array[index].place(x = 440, y = y + c * offset)
            return True
        else:
            self.invalid_lbl_array[index].place_forget()

    def color_insert(self):
        self.custom_background_entry.delete(0, len(self.custom_background_entry.get()))
        self.custom_background_entry.insert(0, self.custom_background)
        self.custom_foreground_entry.delete(0, len(self.custom_foreground_entry.get()))
        self.custom_foreground_entry.insert(0, self.custom_foreground)
        self.custom_button_background_entry.delete(0, len(self.custom_button_background_entry.get()))
        self.custom_button_background_entry.insert(0, self.custom_button_background)
        self.custom_button_background_active_entry.delete(0, len(self.custom_button_background_active_entry.get()))
        self.custom_button_background_active_entry.insert(0, self.custom_button_background_active)
        self.custom_button_foreground_active_entry.delete(0, len(self.custom_button_foreground_active_entry.get()))
        self.custom_button_foreground_active_entry.insert(0, self.custom_button_foreground_active)
        self.custom_button_background_pressed_entry.delete(0, len(self.custom_button_background_pressed_entry.get()))
        self.custom_button_background_pressed_entry.insert(0, self.custom_button_background_pressed)
        self.custom_button_foreground_pressed_entry.delete(0, len(self.custom_button_foreground_pressed_entry.get()))
        self.custom_button_foreground_pressed_entry.insert(0, self.custom_button_foreground_pressed)
        pass

class ProviderOptions():
    """ProviderOptions"""
    def __init__(self, parent):
        self.par = parent
        self.PixO = PixivOptions(parent)
    
    def display(self):
        """
        Draw options (login) for all image providers:
        - Pixiv 
        """
        self.PixO.pixiv_display()

class PixivOptions():
    """PixivOptions"""
    def __init__(self, parent):
        self.par = parent
        self.pixiv_login_lbl = Label(parent, text="Pixiv Login", style="label.TLabel")
        self.pixiv_user_lbl = Label(parent, text="Username", style="label.TLabel")
        self.pixiv_user_filled_lbl = Label(parent, width=50, text=gv.Files.Cred.pixiv_username, style="button.TLabel")
        self.pixiv_user_entry = Entry(parent, width=52, style="button.TLabel")
        self.pixiv_password_lbl = Label(parent, text="Password", style="label.TLabel")
        self.pixiv_password_filled_lbl = Label(parent, width=50, text=gv.Files.Cred.pixiv_password, style="button.TLabel")
        self.pixiv_password_entry = Entry(parent, width=52, style="button.TLabel")
        self.pixiv_login_change_btn = Button(parent, text="Change", command=self.pixiv_change_login, style="button.TLabel")
        self.pixiv_login_confirm_btn = Button(parent, text="Confirm & Save", command=partial(self.pixiv_set_login, True), style="button.TLabel")
        self.pixiv_login_confirm_nosave_btn = Button(parent, text="Confirm & Don't Save", command=partial(self.pixiv_set_login, False), style="button.TLabel")
        self.pixiv_warning_lbl = Label(parent, width=50, text='THIS WILL BE SAVED IN PLAINTEXT!!!', style="label.TLabel")
        if gv.Files.Conf.rename_pixiv == 'True':
            self.rename_var = IntVar(value=1)
        else:
            self.rename_var = IntVar(value=0)
        self.rename_chkbtn = Checkbutton(parent, text='Rename images from pixiv to pixiv name', var=self.rename_var, style="chkbtn.TCheckbutton")
        self.save_btn = Button(parent, text='Save', command=self.pixiv_save, style ="button.TLabel")

    def pixiv_change_login(self):
        """
        Unlock login widget for pixiv, so that you can change your login data. 
        """
        y = 100
        c = 23
        self.pixiv_user_filled_lbl.place_forget()
        self.pixiv_password_filled_lbl.place_forget()
        self.pixiv_login_change_btn.place_forget()
        self.pixiv_user_entry.place(x = 120, y = y + c * 1)
        self.pixiv_password_entry.place(x = 120, y = y + c * 2)
        self.pixiv_login_confirm_btn.place(x = 50, y = y + c * 4)
        self.pixiv_login_confirm_nosave_btn.place(x = 180, y = y + c * 4)
        self.pixiv_user_entry.delete(0, len(gv.Files.Cred.pixiv_username))
        self.pixiv_password_entry.delete(0, len(gv.Files.Cred.pixiv_password))
        self.pixiv_user_entry.insert(0, gv.Files.Cred.pixiv_username)
        self.pixiv_password_entry.insert(0, gv.Files.Cred.pixiv_password)

    def pixiv_set_login(self, save):
        """
        Save pixiv login data and revert the widgets to being uneditable.
        """
        y = 100
        c = 23
        self.pixiv_user_entry.place_forget()
        self.pixiv_password_entry.place_forget()
        self.pixiv_login_confirm_btn.place_forget()
        self.pixiv_login_confirm_nosave_btn.place_forget()
        self.pixiv_user_filled_lbl.place(x = 120, y = y + c * 1)
        self.pixiv_password_filled_lbl.place(x = 120, y = y + c * 2)
        self.pixiv_login_change_btn.place(x = 50, y = y + c * 4)
        
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
        y = 100
        c = 23
        self.pixiv_login_lbl.place(x = 50, y = y)
        self.pixiv_user_lbl.place(x = 50, y = y + c * 1)
        self.pixiv_user_filled_lbl.place(x = 120, y = y + c * 1)
        self.pixiv_password_lbl.place(x = 50, y = y + c * 2)
        self.pixiv_password_filled_lbl.place(x = 120, y = y + c * 2)
        self.pixiv_login_change_btn.place(x = 50, y = y + c * 4)
        self.pixiv_warning_lbl.place(x = 50, y = y + c * 3)

        self.rename_chkbtn.place(x = 50, y = y + c * 6)
        self.save_btn.place(x = 50, y = y + c * 7)

    def pixiv_save(self):
        gv.Files.Log.write_to_log('Attempting to save Pixiv options...')
        if self.rename_var.get() == 1:
            gv.Files.Conf.rename_pixiv = 'True'
        else:
            gv.Files.Conf.rename_pixiv = 'False'
        gv.Files.Conf.write_config()
        gv.Files.Log.write_to_log('Saved Pixiv options')