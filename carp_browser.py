# -*- coding: utf-8 -*-
"""
Genome browser for carp

"""

import Tkinter
import re


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
          
        self.radio_var = Tkinter.IntVar()
        
        self.chk1 = Tkinter.Radiobutton(self.left_pane, text="Cyprinus carpio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=1)                               
        self.chk1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.chk2 = Tkinter.Radiobutton(self.left_pane, text="Danio Rerio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=2)                               
        self.chk2.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.chk3 = Tkinter.Radiobutton(self.left_pane, text="Tilapia",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=3)                               
        self.chk3.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.chk4 = Tkinter.Radiobutton(self.left_pane, text="CyHV-3",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=4)                               
        self.chk4.grid(row=3, column=0, padx=20, pady=10, sticky="w")        

        #### add middle search screens ####

        self.middle_pane = Tkinter.Frame(root, height=800, width=400, bg="#333",
                                         bd=1, relief=Tkinter.SUNKEN)
        self.middle_pane.grid(row=0, column=1, padx=20, pady=20, sticky="n") 
        
        # create swiss text box
        self.swiss_text = Tkinter.Text(self.middle_pane, width=80, height=10,
                                       font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc", insertbackground="#dcdccc",
                                        cursor="hand2")         
        self.swiss_text.grid(row=0, column=0, padx=20, pady=0, 
                              sticky=Tkinter.N+Tkinter.E+Tkinter.W)
        
        # add clicking ability
        
        self.swiss_text.bind("<1>", self.on_text_click)
                 
        self.load_swiss()
        
        #### add right nucleotide and amino acid boxes ####

        self.right_pane = Tkinter.Frame(root, height=800, width=400, bg="#333",
                                        bd=1, relief=Tkinter.SUNKEN)
        self.right_pane.grid(row=0, column=2, padx=20, pady=20, sticky="ne")
        
        # create nucleotide text box
        self.nucl_text = Tkinter.Text(self.right_pane, width = 50, height = 10,
                                      font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc", insertbackground="#dcdccc")
        self.nucl_text.grid(row=0, column=0, padx=20, pady=0,
                            sticky=Tkinter.N)

        # create amino acid text box
        self.amino_text = Tkinter.Text(self.right_pane, width = 50, height = 10,
                                      font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc", insertbackground="#dcdccc")
        self.amino_text.grid(row=1, column=0, padx=20, pady=20,
                            sticky=Tkinter.S)                           
                                  
        
    def load_swiss(self):
        
        # load swiss annotations and update text accordingly
    
        swiss_file = open("./data/swiss.genome_browser")

        # get a list of where tabs occur so can color columns later        
        swiss_data = ""        
        tab_pat = re.compile(r"\t")
        tab_dict = {}
        line_count = 0
        for line in swiss_file:
            line_count += 1
            swiss_data += line
            tmp_match = []
            for matches in re.finditer(tab_pat, line):
                tmp_match.append(matches.start())
            tab_dict[line_count] = tmp_match
            
        #swiss_data = swiss_file.read()
        self.swiss_text.insert(1.0, swiss_data) 
        self.swiss_text.config(state=Tkinter.DISABLED)
        
        # add color to first and second column
        self.swiss_text.tag_configure("id_column", foreground="#cc9393")
        self.swiss_text.tag_configure("gene_column", foreground="#7f9f7f")
        
        #swiss_lines = int(self.swiss_text.index("end-1c").split(".")[0])
        for tab_keys in tab_dict.keys():
            id_start = str(tab_keys) + ".0"
            id_end = str(tab_keys) + "." + str(tab_dict[tab_keys][0])
            gene_end = str(tab_keys) + "." + str(tab_dict[tab_keys][1])
            self.swiss_text.tag_add("id_column", id_start, id_end)
            self.swiss_text.tag_add("gene_column", id_end, gene_end)
 
    def on_text_click(self, event):
        index = self.swiss_text.index("@%s,%s" % (event.x, event.y))
        line, char = index.split(".")
        print "you clicked line", line
        self.swiss_text.tag_configure("select_row", background="#333")
        self.swiss_text.tag_add("select_row", line + ".0", line + ".end")
    

if __name__ == "__main__":
    root = Tkinter.Tk()
    #root.geometry("+100+100")
    app = carp_browser(root)
    root.mainloop()
