from tkinter import IntVar, StringVar, E, W
from tkinter import messagebox as mb
from tkinter.ttk import Label, Checkbutton, Button, Style, Entry, Frame, OptionMenu
from file_operations import is_input_int_digit
from ScrollFrame import ScrollFrame
import global_variables as gv


class WeightSystem():
    """Includes all widgets for the weight system and methods to display and modify them"""
    def __init__(self, parent, lord):
        self.par = parent
        self.lord = lord
        self.scrollpar = ScrollFrame(self.par, gv.width/3, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame

        self.weight_system_lbl = Label(self.par, text="Weight System", font=("Arial Bold", 12), style="label.TLabel")
        width = 10
        vcmd = (parent.register(is_input_int_digit))
        self.filetype_weight_lbl = Label(self.scrollpar_frame, text="Filetype weight", font=("Arial Bold", 12), style="label.TLabel")
        self.png_weight_lbl = Label(self.scrollpar_frame, text="png", font=("Arial Bold", 10), style="label.TLabel")
        self.png_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.png_weight_entry.insert(0, gv.config['Weight']['png'])
        self.jpg_weight_lbl = Label(self.scrollpar_frame, text="jpg/jpeg", font=("Arial Bold", 10), style="label.TLabel")
        self.jpg_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.jpg_weight_entry.insert(0, gv.config['Weight']['jpg'])
        self.jfif_weight_lbl = Label(self.scrollpar_frame, text="jfif", font=("Arial Bold", 10), style="label.TLabel")
        self.jfif_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.jfif_weight_entry.insert(0, gv.config['Weight']['jfif'])
        self.gif_weight_lbl = Label(self.scrollpar_frame, text="gif", font=("Arial Bold", 10), style="label.TLabel")
        self.gif_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.gif_weight_entry.insert(0, gv.config['Weight']['gif'])
        self.bmp_weight_lbl = Label(self.scrollpar_frame, text="bmp", font=("Arial Bold", 10), style="label.TLabel")
        self.bmp_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.bmp_weight_entry.insert(0, gv.config['Weight']['bmp'])
        self.other_weight_lbl = Label(self.scrollpar_frame, text="other", font=("Arial Bold", 10), style="label.TLabel")
        self.other_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.other_weight_entry.insert(0, gv.config['Weight']['other'])

        
        self.higher_resolution_weight_lbl = Label(self.scrollpar_frame, text="Higher resolution\n(Compared to input image)", font=("Arial Bold", 10), style="label.TLabel")
        self.higher_resolution_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.higher_resolution_weight_entry.insert(0, gv.config['Weight']['higher_resolution'])

        self.service_weight_lbl = Label(self.scrollpar_frame, text="Service weight", font=("Arial Bold", 12), style="label.TLabel")
        self.original_weight_lbl = Label(self.scrollpar_frame, text="Original", font=("Arial Bold", 10), style="label.TLabel")
        self.original_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.original_weight_entry.insert(0, gv.config['Weight']['original'])
        self.pixiv_weight_lbl = Label(self.scrollpar_frame, text="Pixiv", font=("Arial Bold", 10), style="label.TLabel")
        self.pixiv_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.pixiv_weight_entry.insert(0, gv.config['Weight']['pixiv'])
        self.danbooru_weight_lbl = Label(self.scrollpar_frame, text="Danbooru", font=("Arial Bold", 10), style="label.TLabel")
        self.danbooru_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.danbooru_weight_entry.insert(0, gv.config['Weight']['danbooru'])
        self.yandere_weight_lbl = Label(self.scrollpar_frame, text="Yandere", font=("Arial Bold", 10), style="label.TLabel")
        self.yandere_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.yandere_weight_entry.insert(0, gv.config['Weight']['yandere'])
        self.konachan_weight_lbl = Label(self.scrollpar_frame, text="Konachan", font=("Arial Bold", 10), style="label.TLabel")
        self.konachan_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.konachan_weight_entry.insert(0, gv.config['Weight']['konachan'])
        self.gelbooru_weight_lbl = Label(self.scrollpar_frame, text="Gelbooru", font=("Arial Bold", 10), style="label.TLabel")
        self.gelbooru_weight_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.gelbooru_weight_entry.insert(0, gv.config['Weight']['gelbooru'])
        

        self.image_0_lbl = Label(self.scrollpar_frame, text="Image 1", font=("Arial Bold", 10), style="label.TLabel")
        self.image_1_lbl = Label(self.scrollpar_frame, text="Image 2", font=("Arial Bold", 10), style="label.TLabel")
        self.width_lbl = Label(self.scrollpar_frame, text="Width", font=("Arial Bold", 10), style="label.TLabel")
        self.height_lbl = Label(self.scrollpar_frame, text="Height", font=("Arial Bold", 10), style="label.TLabel")
        self.weight_lbl = Label(self.scrollpar_frame, text="Weight", font=("Arial Bold", 10), style="label.TLabel")
        self.image_0_weight_lbl = Label(self.scrollpar_frame, text="", font=("Arial Bold", 10), style="label.TLabel")
        self.image_1_weight_lbl = Label(self.scrollpar_frame, text="", font=("Arial Bold", 10), style="label.TLabel")
        
        self.service_0_var = StringVar(parent)
        self.service_choices = ['Original', 'Danbooru', 'Pixiv', 'Yandere', 'Konachan']
        self.service_0_optmen = OptionMenu(self.scrollpar_frame, self.service_0_var, 'Choose Service', *self.service_choices, style='optmen.TMenubutton')

        self.filetype_0_var = StringVar(parent)
        self.filetype_choices = ['png', 'jpg', 'jfif', 'gif', 'bmp', 'other']
        self.filetype_0_optmen = OptionMenu(self.scrollpar_frame, self.filetype_0_var, 'Choose Filetype', *self.filetype_choices, style='optmen.TMenubutton')

        self.service_1_var = StringVar(parent)
        self.service_1_optmen = OptionMenu(self.scrollpar_frame, self.service_1_var, 'Choose Service', *self.service_choices, style='optmen.TMenubutton')

        self.filetype_1_var = StringVar(parent)
        self.filetype_1_optmen = OptionMenu(self.scrollpar_frame, self.filetype_1_var, 'Choose Filetype', *self.filetype_choices, style='optmen.TMenubutton')

        self.width_0_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.width_0_entry.insert(0, '1600')
        self.height_0_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.height_0_entry.insert(0, '900')
        self.width_1_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.width_1_entry.insert(0, '1920')
        self.height_1_entry = Entry(self.scrollpar_frame, width=width, validate='all', validatecommand=(vcmd, '%P'), style="button.TLabel")
        self.height_1_entry.insert(0, '1080')

        self.test_weights_btn = Button(self.scrollpar_frame, text='Test', command=self.test_weights, style ="button.TLabel")

        #self.save_btn = Button(parent, text='Save', command=self.weight_save, style ="button.TLabel")

    def test_weights(self):
        img_0_weight = 0
        img_1_weight = 0
        s0_var = self.filetype_0_var.get()
        try:
            if s0_var == 'png':
                img_0_weight = img_0_weight + int(self.png_weight_entry.get())
            if s0_var == 'jpg':
                img_0_weight = img_0_weight + int(self.jpg_weight_entry.get())
            if s0_var == 'jfif':
                img_0_weight = img_0_weight + int(self.jfif_weight_entry.get())
            if s0_var == 'gif':
                img_0_weight = img_0_weight + int(self.gif_weight_entry.get())
            if s0_var == 'bmp':
                img_0_weight = img_0_weight + int(self.bmp_weight_entry.get())
            if s0_var == 'other':
                img_0_weight = img_0_weight + int(self.other_weight_entry.get())
            s0_var = self.service_0_var.get()
            if s0_var == 'Danbooru':
                img_0_weight = img_0_weight + int(self.danbooru_weight_entry.get())
            if s0_var == 'Pixiv':
                img_0_weight = img_0_weight + int(self.pixiv_weight_entry.get())
            if s0_var == 'Yandere':
                img_0_weight = img_0_weight + int(self.yandere_weight_entry.get())
            if s0_var == 'Konachan':
                img_0_weight = img_0_weight + int(self.konachan_weight_entry.get())
            if s0_var == 'Gelbooru':
                img_0_weight = img_0_weight + int(self.gelbooru_weight_entry.get())
            if s0_var == 'Original':
                img_0_weight = img_0_weight + int(self.original_weight_entry.get())
            if int(self.width_0_entry.get())/int(self.height_0_entry.get()) == int(self.width_1_entry.get())/int(self.height_1_entry.get()):
                if int(self.width_0_entry.get()) > int(self.width_1_entry.get()):
                    img_0_weight = img_0_weight + int(self.higher_resolution_weight_entry.get())
                elif int(self.width_0_entry.get()) < int(self.width_1_entry.get()):
                    img_1_weight = img_1_weight + int(self.higher_resolution_weight_entry.get())
            
            s1_var = self.filetype_1_var.get()
            if s1_var == 'png':
                img_1_weight = img_1_weight + int(self.png_weight_entry.get())
            if s1_var == 'jpg':
                img_1_weight = img_1_weight + int(self.jpg_weight_entry.get())
            if s1_var == 'jfif':
                img_1_weight = img_1_weight + int(self.jfif_weight_entry.get())
            if s1_var == 'gif':
                img_1_weight = img_1_weight + int(self.gif_weight_entry.get())
            if s1_var == 'bmp':
                img_1_weight = img_1_weight + int(self.bmp_weight_entry.get())
            if s1_var == 'other':
                img_1_weight = img_1_weight + int(self.other_weight_entry.get())
            s1_var = self.service_1_var.get()
            if s1_var == 'Danbooru':
                img_1_weight = img_1_weight + int(self.danbooru_weight_entry.get())
            if s1_var == 'Pixiv':
                img_1_weight = img_1_weight + int(self.pixiv_weight_entry.get())
            if s1_var == 'Yandere':
                img_1_weight = img_1_weight + int(self.yandere_weight_entry.get())
            if s1_var == 'Konachan':
                img_1_weight = img_1_weight + int(self.konachan_weight_entry.get())
            if s1_var == 'Gelbooru':
                img_1_weight = img_1_weight + int(self.gelbooru_weight_entry.get())
            if s1_var == 'Original':
                img_1_weight = img_1_weight + int(self.original_weight_entry.get())
                    
            self.image_0_weight_lbl.configure(text=str(img_0_weight))
            self.image_1_weight_lbl.configure(text=str(img_1_weight))
        except:
            mb.showerror('Invalid Value', 'Please insert an integer value into the Weight options and the width and height')

    def weight_display(self):
        """
        Displays the danbooru options widgets
        """
        self.lord.forget()
        self.lord.PixO.forget()
        self.lord.DanO.forget()
        self.lord.YanO.forget()
        self.lord.KonO.forget()
        self.lord.GelO.forget()

        y = int(gv.height/90*10)
        c = 23
        x1 = int(gv.width/160*5)
        x2 = int(gv.width/160*27)
        
        self.weight_system_lbl.place(x = x2, y = y + c * 1)
        self.scrollpar.display(x = x2, y= y + c * 2)

        self.filetype_weight_lbl.grid(row=10, column=0, sticky=W, padx=2, pady=1)
        self.png_weight_lbl.grid(row=11, column=0, sticky=W, padx=2, pady=1)
        self.png_weight_entry.grid(row=11, column=1, sticky=W, padx=2, pady=1)
        self.jpg_weight_lbl.grid(row=14, column=0, sticky=W, padx=2, pady=1)
        self.jpg_weight_entry.grid(row=14, column=1, sticky=W, padx=2, pady=1)
        self.jfif_weight_lbl.grid(row=17, column=0, sticky=W, padx=2, pady=1)
        self.jfif_weight_entry.grid(row=17, column=1, sticky=W, padx=2, pady=1)
        self.gif_weight_lbl.grid(row=20, column=0, sticky=W, padx=2, pady=1)
        self.gif_weight_entry.grid(row=20, column=1, sticky=W, padx=2, pady=1)
        self.bmp_weight_lbl.grid(row=23, column=0, sticky=W, padx=2, pady=1)
        self.bmp_weight_entry.grid(row=23, column=1, sticky=W, padx=2, pady=1)
        self.other_weight_lbl.grid(row=26, column=0, sticky=W, padx=2, pady=1)
        self.other_weight_entry.grid(row=26, column=1, sticky=W, padx=2, pady=1)

        
        self.higher_resolution_weight_lbl.grid(row=30, column=0, sticky=W, padx=2, pady=1)
        self.higher_resolution_weight_entry.grid(row=30, column=1, sticky=W, padx=2, pady=1)

        self.service_weight_lbl.grid(row=34, column=0, sticky=W, padx=2, pady=1)
        self.pixiv_weight_lbl.grid(row=35, column=0, sticky=W, padx=2, pady=1)
        self.pixiv_weight_entry.grid(row=35, column=1, sticky=W, padx=2, pady=1)
        self.danbooru_weight_lbl.grid(row=37, column=0, sticky=W, padx=2, pady=1)
        self.danbooru_weight_entry.grid(row=37, column=1, sticky=W, padx=2, pady=1)
        self.yandere_weight_lbl.grid(row=39, column=0, sticky=W, padx=2, pady=1)
        self.yandere_weight_entry.grid(row=39, column=1, sticky=W, padx=2, pady=1)
        self.konachan_weight_lbl.grid(row=41, column=0, sticky=W, padx=2, pady=1)
        self.konachan_weight_entry.grid(row=41, column=1, sticky=W, padx=2, pady=1)
        self.gelbooru_weight_lbl.grid(row=43, column=0, sticky=W, padx=2, pady=1)
        self.gelbooru_weight_entry.grid(row=43, column=1, sticky=W, padx=2, pady=1)
        self.original_weight_lbl.grid(row=45, column=0, sticky=W, padx=2, pady=1)
        self.original_weight_entry.grid(row=45, column=1, sticky=W, padx=2, pady=1)


        self.image_0_lbl.grid(row=45, column=0, sticky=W, padx=2, pady=1)
        self.service_0_optmen.grid(row=46, column=0, sticky=E+W, padx=2, pady=1)
        self.filetype_0_optmen.grid(row=47, column=0, sticky=E+W, padx=2, pady=1)
        self.width_0_entry.grid(row=48, column=0, sticky=W, padx=2, pady=1)
        self.height_0_entry.grid(row=49, column=0, sticky=W, padx=2, pady=1)
        self.image_1_lbl.grid(row=45, column=1, sticky=W, padx=2, pady=1)
        self.service_1_optmen.grid(row=46, column=1, sticky=E+W, padx=2, pady=1)
        self.filetype_1_optmen.grid(row=47, column=1, sticky=E+W, padx=2, pady=1)
        self.width_1_entry.grid(row=48, column=1, sticky=W, padx=2, pady=1)
        self.height_1_entry.grid(row=49, column=1, sticky=W, padx=2, pady=1)
        self.width_lbl.grid(row=48, column=2, sticky=W, padx=2, pady=1)
        self.height_lbl.grid(row=49, column=2, sticky=W, padx=2, pady=1)
        self.image_0_weight_lbl.grid(row=50, column=0, sticky=W, padx=2, pady=1)
        self.image_1_weight_lbl.grid(row=50, column=1, sticky=W, padx=2, pady=1)
        self.weight_lbl.grid(row=50, column=2, sticky=W, padx=2, pady=1)

        self.test_weights_btn.grid(row=55, column=2, sticky=W, padx=2, pady=1)

        #self.save_btn.place(x = int(gv.width/160*40), y = gv.height-220)

    def forget(self):
        self.weight_system_lbl.place_forget()
        self.scrollpar.sub_frame.place_forget()

        self.filetype_weight_lbl.grid_forget()
        self.png_weight_lbl.grid_forget()
        self.png_weight_entry.grid_forget()
        self.jpg_weight_lbl.grid_forget()
        self.jpg_weight_entry.grid_forget()
        self.jfif_weight_lbl.grid_forget()
        self.jfif_weight_entry.grid_forget()
        self.gif_weight_lbl.grid_forget()
        self.gif_weight_entry.grid_forget()
        self.bmp_weight_lbl.grid_forget()
        self.bmp_weight_entry.grid_forget()
        self.other_weight_lbl.grid_forget()
        self.other_weight_entry.grid_forget()

        
        self.higher_resolution_weight_lbl.grid_forget()
        self.higher_resolution_weight_entry.grid_forget()

        self.service_weight_lbl.grid_forget()
        self.pixiv_weight_lbl.grid_forget()
        self.pixiv_weight_entry.grid_forget()
        self.danbooru_weight_lbl.grid_forget()
        self.danbooru_weight_entry.grid_forget()
        self.yandere_weight_lbl.grid_forget()
        self.yandere_weight_entry.grid_forget()
        self.konachan_weight_lbl.grid_forget()
        self.konachan_weight_entry.grid_forget()
        self.gelbooru_weight_lbl.grid_forget()
        self.gelbooru_weight_entry.grid_forget()
        self.original_weight_lbl.grid_forget()
        self.original_weight_entry.grid_forget()


        self.image_0_lbl.grid_forget()
        self.service_0_optmen.grid_forget()
        self.filetype_0_optmen.grid_forget()
        self.width_0_entry.grid_forget()
        self.height_0_entry.grid_forget()
        self.image_1_lbl.grid_forget()
        self.service_1_optmen.grid_forget()
        self.filetype_1_optmen.grid_forget()
        self.width_1_entry.grid_forget()
        self.height_1_entry.grid_forget()
        self.width_lbl.grid_forget()
        self.height_lbl.grid_forget()
        self.image_0_weight_lbl.grid_forget()
        self.image_1_weight_lbl.grid_forget()
        self.weight_lbl.grid_forget()

        self.test_weights_btn.grid_forget()

        #self.save_btn.place_forget()


    def weight_save(self):
        gv.Files.Log.write_to_log('Saving Weight options...')
        gv.config['Weight']['png'] = self.png_weight_entry.get()
        gv.config['Weight']['jpg'] = self.jpg_weight_entry.get()
        gv.config['Weight']['jfif'] = self.jfif_weight_entry.get()
        gv.config['Weight']['gif'] = self.gif_weight_entry.get()
        gv.config['Weight']['bmp'] = self.bmp_weight_entry.get()
        gv.config['Weight']['other'] = self.other_weight_entry.get()
        gv.config['Weight']['pixiv'] = self.pixiv_weight_entry.get()
        gv.config['Weight']['danbooru'] = self.danbooru_weight_entry.get()
        gv.config['Weight']['yandere'] = self.yandere_weight_entry.get()
        gv.config['Weight']['konachan'] = self.konachan_weight_entry.get()
        gv.config['Weight']['gelbooru'] = self.konachan_weight_entry.get()
        gv.config['Weight']['original'] = self.original_weight_entry.get()
        gv.config['Weight']['higher_resolution'] = self.higher_resolution_weight_entry.get()
        gv.write_config()
        gv.Files.Log.write_to_log('Saved Weight options')
