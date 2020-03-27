from tkinter import Canvas, Scrollbar
from tkinter.ttk import Frame
import global_variables as gv

class ScrollFrame():
    """A frame with a scrollbar"""
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        self.sub_frame = Frame(parent, width=width, height=height, style="frame.TFrame")
        self.canvas = Canvas(self.sub_frame, width=width, height=height, background=gv.Files.Theme.background, highlightthickness=0)
        self.frame = Frame(self.canvas, width=width, height=height, style="frame.TFrame")
        self.scrollbar = Scrollbar(self.sub_frame, orient="vertical", command=self.canvas.yview)
            # activebackground=gv.Files.Theme.background,
            # activerelief='flat', 
            # background='yellow', 
            # borderwidth=50, 
            # elementborderwidth=20, 
            # highlightbackground='green', 
            # highlightcolor='orange', 
            # highlightthickness=30, 
            # relief='flat', 
            # # repeatdelay, 
            # # repeatinterval, 
            # # takefocus, 
            # troughcolor='blue', 
            # )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        #https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
        self.scrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>", self.myfunction)

        self.frame.bind('<Enter>', self.bound_to_mousewheel)
        self.frame.bind('<Leave>', self.unbound_to_mousewheel)

    def myfunction(self, event):
        """
        Setup scroll region for results screen.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=self.width, height=self.height)

    def bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        # # with Windows OS
        # root.bind("<MouseWheel>", mouse_wheel)
        # # with Linux OS
        # root.bind("<Button-4>", mouse_wheel)
        # root.bind("<Button-5>", mouse_wheel)  

    def unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>") 

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def display(self, x, y):
        self.sub_frame.place(x=x, y=y)
        self.canvas.yview_moveto(0)