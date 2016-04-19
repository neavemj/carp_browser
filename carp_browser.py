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
        
        #### add left option pane ####

        self.left_pane = Tkinter.Frame(root, height=800, width=300, bg="#333",
                                       bd=1, relief=Tkinter.SUNKEN)
        self.left_pane.grid(row=0, column=0, padx=20, pady=20, sticky="n")        
                
        ttk.Style().configure("TCheckbutton", background="#333", foreground="gray",
                        takefocus=False)     
           
        self.chk1 = ttk.Checkbutton(self.left_pane, text="Cyprinus carpio")                               
        self.chk1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.chk2 = ttk.Checkbutton(self.left_pane, text="Danio Rerio")                               
        self.chk2.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.chk3 = ttk.Checkbutton(self.left_pane, text="Tilapia")                               
        self.chk3.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.chk4 = ttk.Checkbutton(self.left_pane, text="CyHV-3")                               
        self.chk4.grid(row=3, column=0, padx=20, pady=10, sticky="w")        

        #### add middle search screens ####

        self.middle_pane = Tkinter.Frame(root, height=800, width=300, bg="#333",
                                         bd=1, relief=Tkinter.SUNKEN)
        self.middle_pane.grid(row=0, column=1, padx=20, pady=20) 
        
        # load swiss annotations and update text accordingly
        
        swiss_file = open("./data/testAssembly.fasta")
        #swiss_data = swiss_file.read()
        #swiss_file.close()
        

        self.swiss_text = Tkinter.Text(self.middle_pane, width=60, height=10)
        self.swiss_text.insert(1.0, swiss_file.read())        
        
        self.swiss_text.grid(row=0, column=0, padx=20, pady=10, 
                              sticky=Tkinter.N+Tkinter.E)
        
        # load pfam annotations              
        self.pfam_text = Tkinter.Text(self.middle_pane, width=60, height=10)
        self.pfam_text.grid(row=1, column=0, padx=20, pady=10,
                              sticky=Tkinter.S+Tkinter.E)
                             
                        





if __name__ == "__main__":
    root = Tkinter.Tk()
    root.geometry("1200x800+100+100")
    app = carp_browser(root)
    root.mainloop()

