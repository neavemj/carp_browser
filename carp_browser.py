# -*- coding: utf-8 -*-
"""
Genome browser for carp

"""

import Tkinter
import ttk


class carp_browser:

    def __init__(self, root):
        
        self.root = root
        root.configure(background="#333")
        root.title(" Carp Genome Browser ")
        # self.root.iconbitmap('newicon') # change little TK icon     
        
        ## initialize GUI ##
        
        # add a menu bar, then items within it   
        self.menu_bar = Tkinter.Menu(root)
        
        self.file_menu = Tkinter.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open")       
        self.edit_menu = Tkinter.Menu(self.menu_bar, tearoff=0)        
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl + Z", 
                              compound="left")        
        
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        root.config(menu=self.menu_bar)        
        
        # add left option pane
        ttk.Style().configure("TButton", background="#333")
        
        self.b1 = ttk.Button(root, text="b1", style="TButton", 
                        command=self.but_test)
        self.b1.grid(row=0, column=0)
        self.b2 = ttk.Button(root, text="b2")
        self.b2.grid(row=1, column=0)
        self.b3 = ttk.Button(root, text="b3")
        self.b3.grid(row=2, column=0)
        self.b4 = ttk.Button(root, text="b4")
        self.b4.grid(row=4, column=1)
        
    def but_test(self):
        print "button pressed"


if __name__ == "__main__":
    root = Tkinter.Tk()
    root.geometry("+100+100")
    app = carp_browser(root)
    root.mainloop()

