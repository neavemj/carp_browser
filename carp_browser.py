# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

import Tkinter
import ttk


class App:

    def __init__(self, master):

        frame = Tkinter.Frame(master)
        frame.grid()
        master.configure(background="black")  
        f2 = Tkinter.Frame(master, width=800, height=500)
        f2.grid(row=0, column=0, rowspan=4, columnspan=8)
        f2.configure(background="#333")
        
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

root = Tkinter.Tk()
app = App(root)
root.mainloop()

