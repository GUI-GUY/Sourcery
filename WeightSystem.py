from tkinter import IntVar, StringVar, E, W
from tkinter.ttk import Label, Checkbutton, Button, Style, Entry, Frame, OptionMenu
from ScrollFrame import ScrollFrame
import global_variables as gv


class WeightSystem():
    """Includes all widgets for the weight system and methods to display and modify them"""
    def __init__(self, parent):
        self.par = parent
        self.scrollpar = ScrollFrame(self.par, gv.width/4, gv.height*0.6)
        self.scrollpar_frame = self.scrollpar.frame

        self.weight_system_lbl = Label(self.par, text="Weight System", font=("Arial Bold", 12), style="label.TLabel")
        width = 10
        self.filetype_weight_lbl = Label(self.scrollpar_frame, text="Filetype weight", font=("Arial Bold", 12), style="label.TLabel")
        self.png_weight_lbl = Label(self.scrollpar_frame, text="png", font=("Arial Bold", 10), style="label.TLabel")
        self.png_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.png_weight_entry.insert(0, gv.Files.Conf.png_weight)
        self.jpg_weight_lbl = Label(self.scrollpar_frame, text="jpg/jpeg", font=("Arial Bold", 10), style="label.TLabel")
        self.jpg_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.jpg_weight_entry.insert(0, gv.Files.Conf.jpg_weight)
        self.jfif_weight_lbl = Label(self.scrollpar_frame, text="jfif", font=("Arial Bold", 10), style="label.TLabel")
        self.jfif_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.jfif_weight_entry.insert(0, gv.Files.Conf.jfif_weight)
        self.gif_weight_lbl = Label(self.scrollpar_frame, text="gif", font=("Arial Bold", 10), style="label.TLabel")
        self.gif_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.gif_weight_entry.insert(0, gv.Files.Conf.gif_weight)
        self.bmp_weight_lbl = Label(self.scrollpar_frame, text="bmp", font=("Arial Bold", 10), style="label.TLabel")
        self.bmp_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.bmp_weight_entry.insert(0, gv.Files.Conf.bmp_weight)
        self.other_weight_lbl = Label(self.scrollpar_frame, text="other", font=("Arial Bold", 10), style="label.TLabel")
        self.other_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.other_weight_entry.insert(0, gv.Files.Conf.other_weight)

        
        self.higher_resolution_weight_lbl = Label(self.scrollpar_frame, text="Higher resolution", font=("Arial Bold", 10), style="label.TLabel")
        self.higher_resolution_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.higher_resolution_weight_entry.insert(0, gv.Files.Conf.higher_resolution_weight)

        self.service_weight_lbl = Label(self.scrollpar_frame, text="Service weight", font=("Arial Bold", 12), style="label.TLabel")
        self.original_weight_lbl = Label(self.scrollpar_frame, text="Original", font=("Arial Bold", 10), style="label.TLabel")
        self.original_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.original_weight_entry.insert(0, gv.Files.Conf.original_weight)
        self.pixiv_weight_lbl = Label(self.scrollpar_frame, text="Pixiv", font=("Arial Bold", 10), style="label.TLabel")
        self.pixiv_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.pixiv_weight_entry.insert(0, gv.Files.Conf.pixiv_weight)
        self.danbooru_weight_lbl = Label(self.scrollpar_frame, text="Danbooru", font=("Arial Bold", 10), style="label.TLabel")
        self.danbooru_weight_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.danbooru_weight_entry.insert(0, gv.Files.Conf.danbooru_weight)
        

        self.image_0_lbl = Label(self.scrollpar_frame, text="Image 1", font=("Arial Bold", 10), style="label.TLabel")
        self.image_1_lbl = Label(self.scrollpar_frame, text="Image 2", font=("Arial Bold", 10), style="label.TLabel")
        self.width_lbl = Label(self.scrollpar_frame, text="Width", font=("Arial Bold", 10), style="label.TLabel")
        self.height_lbl = Label(self.scrollpar_frame, text="Height", font=("Arial Bold", 10), style="label.TLabel")
        self.weight_lbl = Label(self.scrollpar_frame, text="Weight", font=("Arial Bold", 10), style="label.TLabel")
        self.image_0_weight_lbl = Label(self.scrollpar_frame, text="", font=("Arial Bold", 10), style="label.TLabel")
        self.image_1_weight_lbl = Label(self.scrollpar_frame, text="", font=("Arial Bold", 10), style="label.TLabel")
        
        self.service_0_var = StringVar(parent)
        self.service_choices = ['Original', 'Danbooru', 'Pixiv']
        self.service_0_optmen = OptionMenu(self.scrollpar_frame, self.service_0_var, 'Choose Service', *self.service_choices)

        self.filetype_0_var = StringVar(parent)
        self.filetype_choices = ['png', 'jpg', 'jfif', 'gif', 'bmp', 'other']
        self.filetype_0_optmen = OptionMenu(self.scrollpar_frame, self.filetype_0_var, 'Choose Filetype', *self.filetype_choices)

        self.service_1_var = StringVar(parent)
        self.service_1_optmen = OptionMenu(self.scrollpar_frame, self.service_1_var, 'Choose Service', *self.service_choices)

        self.filetype_1_var = StringVar(parent) # TODO OptionMenu Style
        self.filetype_1_optmen = OptionMenu(self.scrollpar_frame, self.filetype_1_var, 'Choose Filetype', *self.filetype_choices)

        self.width_0_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.width_0_entry.insert(0, '1600')
        self.height_0_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.height_0_entry.insert(0, '900')
        self.width_1_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.width_1_entry.insert(0, '1920')
        self.height_1_entry = Entry(self.scrollpar_frame, width=width, style="button.TLabel")
        self.height_1_entry.insert(0, '1080')

        self.test_weights_btn = Button(self.scrollpar_frame, text='Test', command=self.test_weights, style ="button.TLabel")

        self.save_btn = Button(parent, text='Save', command=self.danbooru_save, style ="button.TLabel")

    
    # on change dropdown value
    def test_weights(self):
        img_0_weight = 0
        s0_var = self.filetype_0_var.get()
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
        if s0_var == 'Pixiv':
            img_0_weight = img_0_weight + int(self.original_weight_entry.get())
        if int(self.width_0_entry.get()) > int(self.width_1_entry.get()):
            img_0_weight = img_0_weight + int(self.higher_resolution_weight_entry.get())

        img_1_weight = 0
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
        if s1_var == 'Original':
            img_1_weight = img_1_weight + int(self.original_weight_entry.get())
        if int(self.width_0_entry.get()) < int(self.width_1_entry.get()):
            img_1_weight = img_1_weight + int(self.higher_resolution_weight_entry.get())
        
        self.image_0_weight_lbl.configure(text=str(img_0_weight))
        self.image_1_weight_lbl.configure(text=str(img_1_weight))

    def weight_display(self):
        """
        Displays the danbooru options widgets
        """
        self.weight_system_lbl.place(x = int(gv.width/160*100), y = int(gv.height/90*8))
        self.scrollpar.display(x = int(gv.width/160*100), y= int(gv.height/90*10))

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
        self.original_weight_lbl.grid(row=38, column=0, sticky=W, padx=2, pady=1)
        self.original_weight_entry.grid(row=38, column=1, sticky=W, padx=2, pady=1)


        self.image_0_lbl.grid(row=39, column=0, sticky=W, padx=2, pady=1)
        self.service_0_optmen.grid(row=40, column=0, sticky=E+W, padx=2, pady=1)
        self.filetype_0_optmen.grid(row=41, column=0, sticky=E+W, padx=2, pady=1)
        self.width_0_entry.grid(row=42, column=0, sticky=W, padx=2, pady=1)
        self.height_0_entry.grid(row=43, column=0, sticky=W, padx=2, pady=1)
        self.image_1_lbl.grid(row=39, column=1, sticky=W, padx=2, pady=1)
        self.service_1_optmen.grid(row=40, column=1, sticky=E+W, padx=2, pady=1)
        self.filetype_1_optmen.grid(row=41, column=1, sticky=E+W, padx=2, pady=1)
        self.width_1_entry.grid(row=42, column=1, sticky=W, padx=2, pady=1)
        self.height_1_entry.grid(row=43, column=1, sticky=W, padx=2, pady=1)
        self.width_lbl.grid(row=42, column=2, sticky=W, padx=2, pady=1)
        self.height_lbl.grid(row=43, column=2, sticky=W, padx=2, pady=1)
        self.image_0_weight_lbl.grid(row=44, column=0, sticky=W, padx=2, pady=1)
        self.image_1_weight_lbl.grid(row=44, column=1, sticky=W, padx=2, pady=1)
        self.weight_lbl.grid(row=44, column=2, sticky=W, padx=2, pady=1)

        self.test_weights_btn.grid(row=45, column=2, sticky=W, padx=2, pady=1)

        self.save_btn.place(x = int(gv.width/160*100), y = gv.height-220)

    def danbooru_save(self):
        gv.Files.Log.write_to_log('Attempting to save Weight options...')
        gv.Files.Conf.png_weight = self.png_weight_entry.get()
        gv.Files.Conf.jpg_weight = self.jpg_weight_entry.get()
        gv.Files.Conf.jfif_weight = self.jfif_weight_entry.get()
        gv.Files.Conf.gif_weight = self.gif_weight_entry.get()
        gv.Files.Conf.bmp_weight = self.bmp_weight_entry.get()
        gv.Files.Conf.other_weight = self.other_weight_entry.get()
        gv.Files.Conf.pixiv_weight = self.pixiv_weight_entry.get()
        gv.Files.Conf.danbooru_weight = self.danbooru_weight_entry.get()
        gv.Files.Conf.original_weight = self.original_weight_entry.get()
        gv.Files.Conf.higher_resolution_weight = self.higher_resolution_weight_entry.get()
        gv.Files.Conf.write_config()
        gv.Files.Log.write_to_log('Saved Weight options')
