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
                
        self.chk1 = Tkinter.Checkbutton(self.left_pane, text="Cyprinus carpio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333")                               
        self.chk1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.chk2 = Tkinter.Checkbutton(self.left_pane, text="Danio Rerio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333")                               
        self.chk2.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.chk3 = Tkinter.Checkbutton(self.left_pane, text="Tilapia",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333")                               
        self.chk3.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.chk4 = Tkinter.Checkbutton(self.left_pane, text="CyHV-3",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333")                               
        self.chk4.grid(row=3, column=0, padx=20, pady=10, sticky="w")        

        #### add middle search screens ####

        self.middle_pane = Tkinter.Frame(root, height=800, width=400, bg="#333",
                                         bd=1, relief=Tkinter.SUNKEN)
        self.middle_pane.grid(row=0, column=1, padx=20, pady=20) 
        
        # create swiss text box
        self.swiss_text = Tkinter.Text(self.middle_pane, width=120, height=20,
                                       font=("Consolas", 8), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc")         
        self.swiss_text.grid(row=0, column=0, padx=20, pady=10, 
                              sticky=Tkinter.N+Tkinter.E+Tkinter.W)
                 

        self.load_swiss()
        
    def load_swiss(self):
        
        # load swiss annotations and update text accordingly
    
        swiss_file = open("./data/swiss.genome_browser")
        swiss_data = swiss_file.read()
        self.swiss_text.insert(1.0, swiss_data) 
        
        # add color to first column
        self.swiss_text.tag_configure("id_column", foreground="#cc9393")
#        swiss_lines = int(self.swiss_text.index("end-1c").split(".")[0])
#        for lines in range(swiss_lines):
#            colour_start = str(lines) + ".0"
#            colour_end = str(lines) + ".11"
#            self.swiss_text.tag_add("id_column", colour_start, colour_end)
        for index, lines in enumerate(swiss_data):
             colour_start = str(index) + ".0"
             colour_end = str(index) + ".11"
             self.swiss_text.tag_add("id_column", colour_start, colour_end)
 

if __name__ == "__main__":
    root = Tkinter.Tk()
    root.geometry("1200x800+100+100")
    app = carp_browser(root)
    root.mainloop()

