# -*- coding: utf-8 -*-
"""
Genome browser for carp

"""

import Tkinter
import ttk


class carp_browser:

    def __init__(self, master):
        
        #self.master = root
        #master.title(" Carp Genome Browser ")
        # self.root.iconbitmap('newicon') # change little TK icon
        
        # add a menu bar, then items within it
        menu_bar = Tkinter.Menu(master)
        
        file_menu = Tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open")
        
        edit_menu = Tkinter.Menu(menu_bar, tearoff=0)        
        edit_menu.add_command(label="Undo", accelerator="Ctrl + Z", 
                              compound="left")        
        
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        master.config(menu=menu_bar)        
        
        frame = Tkinter.Frame(master)
        frame.grid()
        master.configure(background="#333")  
        f2 = Tkinter.Frame(master, width=800, height=500)
        f2.grid(row=0, column=0, rowspan=4, columnspan=8)
        f2.configure(background="#334")
        
        #style = ttk.Style()
        #style.theme_use("clam")
        #print s.theme_use()
        
        ttk.Style().configure("TButton", background="#333")
        b1 = ttk.Button(master, text="b1", style="TButton", 
                        command=self.but_test)
        b1.grid(row=0, column=0)
        b2 = ttk.Button(root, text="b2")
        b2.grid(row=1, column=0)
        b3 = ttk.Button(root, text="b3")
        b3.grid(row=2, column=0)
        b4 = ttk.Button(root, text="b4")
        b4.grid(row=3, column=0)
        
    def but_test(self):
        print "button pressed"


if __name__ == "__main__":
    root = Tkinter.Tk()
    root.geometry("+100+100")
    app = carp_browser(root)
    root.mainloop()

