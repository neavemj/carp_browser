# -*- coding: utf-8 -*-
"""
Genome browser for carp

"""

import Tkinter
import re
from pyfaidx import Fasta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sb
from Bio import Phylo
from Bio.Align.Applications import ClustalwCommandline


## define global color palette

root_background = "#d9dddd"
side_bar_color = "#34495e"
side_bar_text_color = "#bdc3c7"
global_font = "Verdana"
window_background = "white"
window_text_gray = "#626e6f"
window_text_red = "#e74c3c"
window_text_green = "#2ecc71"
highlight_color = "#e1e3e5"
header_background_blue = "#3498db"
header_text_white = "white"
entry_background = "#dce0e0"
clouds = "#ecf0f1"

## other globals
figure_size = (6.6, 3)
widget_padx = 10
widget_pady = 10


class carp_browser:

    def __init__(self, root):
        
        self.root = root
        root.configure(background=root_background)
        root.title(" Carp Genome Browser ")
        
        self.root.iconbitmap(r"./data/kitchen_fish_icon.ico") # change little TK icon     
        
        ## initialize GUI ##
        
        # add a menu bar, then items within it   
#        self.menu_bar = Tkinter.Menu(root)
#        
#        self.file_menu = Tkinter.Menu(self.menu_bar, tearoff=0)
#        self.file_menu.add_command(label="Open")       
#        self.edit_menu = Tkinter.Menu(self.menu_bar, tearoff=0)        
#        self.edit_menu.add_command(label="Undo", accelerator="Ctrl + Z", 
#                              compound="left")        
#        
#        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
#        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
#        root.config(menu=self.menu_bar)        
        
        #### add left option pane ####

        self.left_pane = Tkinter.Frame(root, height=800, width=200, bg=side_bar_color,
                                       bd=0)
        self.left_pane.grid(row=0, column=0, padx=0, pady=0, sticky="nes")        
        
        self.left_pane_label = Tkinter.Label(self.left_pane, text="",
                                        bg=side_bar_color, fg=side_bar_text_color, 
                                        font=(global_font, 10))                               
        self.left_pane_label.grid(row=0, column=0, padx=20, pady=5, sticky="we")
        # add frame for each label so can "highlight" species box in left side-bar        
        
        self.carp_frame = Tkinter.Frame(self.left_pane, bg=side_bar_color, bd=0, 
                                        relief=Tkinter.GROOVE, padx=20, pady=20, cursor="hand2")                                      
        self.carp_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nesw")      
        self.chk1 = Tkinter.Label(self.carp_frame, text="Cyprinus carpio",
                                        bg=side_bar_color, fg=side_bar_text_color, 
                                        activebackground="#333",
                                        cursor="hand2", font=(global_font, 12))
        self.chk1.grid(row=0, column=1, padx=10, pady=5, sticky="w")        
        self.fish_icon = Tkinter.PhotoImage(file="./data/kitchen_fish_icon_2.gif") # image is 60 x 42 pixels
        self.carp_icon_label = Tkinter.Label(self.carp_frame, image=self.fish_icon,
                                        borderwidth=0, bg=side_bar_color) 
        self.carp_icon_label.grid(row=0, column=0, sticky="w")                                
        self.carp_frame.bind("<1>", self.load_carp)        
        self.chk1.bind("<1>", self.load_carp)
        self.carp_icon_label.bind("<1>", self.load_carp)                                            
        
        self.dRerio_frame = Tkinter.Frame(self.left_pane, bg=side_bar_color, bd=0, 
                                        relief=Tkinter.GROOVE, padx=20, pady=20, cursor="hand2")                                      
        self.dRerio_frame.grid(row=2, column=0, padx=0, pady=0, sticky="nesw")          
        self.chk2 = Tkinter.Label(self.dRerio_frame, text="Danio rerio",
                                        bg=side_bar_color, fg=side_bar_text_color, 
                                        activebackground="#333",
                                        cursor="hand2", font=(global_font, 12))                               
        self.chk2.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.dRerio_icon_label = Tkinter.Label(self.dRerio_frame, image=self.fish_icon,
                                        borderwidth=0, bg=side_bar_color) 
        self.dRerio_icon_label.grid(row=0, column=0, sticky="w") 
        self.dRerio_frame.bind("<1>", self.load_dRerio) 
        self.chk2.bind("<1>", self.load_dRerio)
        self.dRerio_icon_label.bind("<1>", self.load_dRerio)
        
        self.tilapia_frame = Tkinter.Frame(self.left_pane, bg=side_bar_color, bd=0, 
                                        relief=Tkinter.GROOVE, padx=20, pady=20, cursor="hand2")                                      
        self.tilapia_frame.grid(row=3, column=0, padx=0, pady=0, sticky="nesw")
        self.chk3 = Tkinter.Label(self.tilapia_frame, text="Tilapia",
                                        bg=side_bar_color, fg=side_bar_text_color, 
                                        activebackground="#333",
                                        cursor="hand2", font=(global_font, 12))                                       
        self.chk3.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.tilapia_icon_label = Tkinter.Label(self.tilapia_frame, image=self.fish_icon,
                                        borderwidth=0, bg=side_bar_color) 
        self.tilapia_icon_label.grid(row=0, column=0, sticky="w") 
        #self.tilapia_frame.bind("<1>", self.load_tilapia)
        #self.chk3.bind("<1>", self.load_tilapia)
        
        self.khv_frame = Tkinter.Frame(self.left_pane, bg=side_bar_color, bd=0, 
                                        relief=Tkinter.GROOVE, padx=20, pady=20, cursor="hand2")                                      
        self.khv_frame.grid(row=4, column=0, padx=0, pady=0, sticky="nesw")
        self.chk4 = Tkinter.Label(self.khv_frame, text="Cyprinid herpesvirus 3",
                                        bg=side_bar_color, fg=side_bar_text_color, 
                                        activebackground="#333",
                                        cursor="hand2", font=(global_font, 12))                                                                      
        self.chk4.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.khv_icon = Tkinter.PhotoImage(file="./data/Virus2c.gif") # image is 36 x 42 pixels
        self.khv_icon_label = Tkinter.Label(self.khv_frame, image=self.khv_icon,
                                        borderwidth=0, bg=side_bar_color) 
        self.khv_icon_label.grid(row=0, column=0, sticky="w")   
        self.khv_frame.bind("<1>", self.load_khv)
        self.chk4.bind("<1>", self.load_khv)
        self.khv_icon_label.bind("<1>", self.load_khv)

        #### add large middle-right grid for containing all the widgets ####
        self.large_grid = Tkinter.Frame(root, bg=root_background, bd=0)
        self.large_grid.grid(row=0, column=1, padx=20, pady=10, sticky="")

        # create swiss text box including frame to hold all its elements
        
        self.swiss_frame = Tkinter.Frame(self.large_grid, bg=root_background, bd=0)
        self.swiss_frame.grid(row=0, column=0, padx=widget_padx, pady=widget_pady, sticky="n")
        
        self.swiss_text = Tkinter.Text(self.swiss_frame, width=80, height=11,
                                       font=(global_font, 10), padx=0, pady=5, spacing1=5,
                                        bg=window_background, fg=window_text_gray, insertbackground="#dcdccc",
                                        cursor="hand2", relief=Tkinter.FLAT)         
        self.swiss_text.grid(row=2, column=0, padx=0, pady=0, sticky="nsew") 
                                      
        # add scroll bar to swiss text box
        swiss_scroll = Tkinter.Scrollbar(self.swiss_frame)       
        swiss_scroll.grid(row=2, column=1, sticky="nse")
        
        self.swiss_text.config(yscrollcommand=swiss_scroll.set)
        swiss_scroll.config(command=self.swiss_text.yview)
    
        # add blue header for annotation box
        self.swiss_header = Tkinter.Frame(self.swiss_frame, bg=header_background_blue,
                                         bd=0)
        self.swiss_header.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky="ew") 
        
        self.swiss_header_label = Tkinter.Label(self.swiss_header, width = 20, 
                                        bg=header_background_blue, fg=header_text_white,
                                        font=(global_font, 12), text="Annotated proteins")
        self.swiss_header_label.grid(row=0, column=0, sticky="w", padx=0, pady=10) 
        
        # add entry widget for searching annotations (above text widget)                            
        # I'll put this in its own frame
        self.swiss_search_frame = Tkinter.Frame(self.swiss_frame, bg=window_background,
                                         bd=1, relief=Tkinter.GROOVE)
        self.swiss_search_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="ew")          
 
        
        self.search = Tkinter.Entry(self.swiss_search_frame, width=28,
                                          font=(global_font, 11), bg=clouds,
                                            relief=Tkinter.FLAT)
        self.search.bind("<Return>", self.search_text)
        self.search.grid(row=0, column=0, sticky="wns", pady=0)
        
        self.search_icon = Tkinter.PhotoImage(file="./data/search_icon.gif") # image is 25 x 25 pixels       
        self.search_button = Tkinter.Button(self.swiss_search_frame, image=self.search_icon, bg=clouds,
                                            font=(global_font, 10, "underline"), width=50,
                                            command=self.search_text, relief=Tkinter.FLAT)
        self.search_button.grid(row=0, column=1, sticky="ns", pady=0, padx=0)
         
        self.result_count_var = Tkinter.StringVar()
        self.word_count = Tkinter.Label(self.swiss_search_frame, width = 20, 
                                        bg=window_background, fg=window_text_gray,
                                        font=(global_font, 10), textvariable=self.result_count_var)
        self.word_count.grid(row=0, column=3, sticky="e", padx=30)                            
        
        # add clicking and highlighting ability
        
        self.swiss_text.tag_configure("highlight", background=highlight_color)
        self.swiss_text.bind("<1>", self.on_text_click)
        
        # add figure frame
        self.figure_frame = Tkinter.Frame(self.large_grid, bg=window_background,
                                         bd=0, relief=Tkinter.FLAT)
        self.figure_frame.grid(row=1, column=0, padx=widget_padx, pady=widget_pady, sticky="")  
        
        # also add blue header for figure placeholder
        self.figure_header = Tkinter.Frame(self.figure_frame, bg=header_background_blue,
                                         bd=0)
        self.figure_header.grid(row=0, column=0, padx=0, pady=0, sticky="ew") 
        
        self.figure_header_label = Tkinter.Label(self.figure_header, width = 13, 
                                        bg=header_background_blue, fg=header_text_white,
                                        font=(global_font, 12), text="Expression")
        self.figure_header_label.grid(row=0, column=0, sticky="w", padx=0, pady=10)
        
        self.f = Figure(figsize=figure_size, dpi=100)
        self.f.set_facecolor(window_background)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.figure_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        
        #### add right nucleotide and amino acid boxes ####

        self.amino_frame = Tkinter.Frame(self.large_grid, bg=window_background,
                                        bd=0, relief=Tkinter.FLAT)
        self.amino_frame.grid(row=0, column=1, padx=widget_padx, pady=widget_pady, sticky="sn")
        
        # add blue header for annotation box
        self.amino_header = Tkinter.Frame(self.amino_frame, bg=header_background_blue,
                                         bd=0)
        self.amino_header.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky="nsew") 
        
        self.amino_header_label = Tkinter.Label(self.amino_header, width = 20, 
                                        bg=header_background_blue, fg=header_text_white,
                                        font=(global_font, 12), text="Amino Acid Sequence")
        self.amino_header_label.grid(row=0, column=0, sticky="w", padx=0, pady=10) 
        
        # create amino acid text box
        self.amino_text = Tkinter.Text(self.amino_frame, width = 50, height = 12,
                                      font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg=window_background, fg=window_text_gray, insertbackground="#dcdccc",
                                        relief=Tkinter.FLAT)
        self.amino_text.grid(row=1, column=0, padx=0, pady=0, sticky="")
        
        # add scroll bar for amino acid textbox
        amino_scroll = Tkinter.Scrollbar(self.amino_frame)       
        amino_scroll.grid(row=1, column=1, sticky="nse")
        
        self.amino_text.config(yscrollcommand=amino_scroll.set)
        amino_scroll.config(command=self.amino_text.yview)
      
        # add button to copy from amino acid box to alignment box
        self.amino_add_button = Tkinter.Button(self.amino_frame, width = 10, bg=window_background,
                                        font=(global_font, 12, "bold"), text="COPY", fg=window_text_green,
                                        command=self.copy_to_alignment_box, relief=Tkinter.FLAT)
        self.amino_add_button.grid(row=2, column=0, sticky="wn", pady=0, padx=0)  
        
        # add button to clear amino acid box
        self.amino_clear = Tkinter.Button(self.amino_frame, width = 10, bg=window_background,
                                        font=(global_font, 12, "bold"), text="CLEAR", fg=window_text_red,
                                        command=self.clear_amino_window, relief=Tkinter.FLAT)
        self.amino_clear.grid(row=2, column=0, sticky="en", pady=0, padx=0)        

        ## add frame for alignment box
        self.align_frame = Tkinter.Frame(self.large_grid, bg=window_background,
                                        bd=0, relief=Tkinter.FLAT)
        self.align_frame.grid(row=1, column=1, padx=widget_padx, pady=widget_pady, sticky="ns")
        
        # add blue header for alignment box
        self.align_header = Tkinter.Frame(self.align_frame, bg=header_background_blue,
                                         bd=0)
        self.align_header.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky="nsew") 
        
        self.align_header_label = Tkinter.Label(self.align_header, width = 15, 
                                        bg=header_background_blue, fg=header_text_white,
                                        font=(global_font, 12), text="Alignment box")
                                        
        self.align_header_label.grid(row=0, column=0, sticky="w", padx=0, pady=10)                                    
                            
        ## create alignment text box
        self.align_text = Tkinter.Text(self.align_frame, width = 50, height = 13,
                                      font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg=window_background, fg=window_text_gray, insertbackground="#dcdccc",
                                        relief=Tkinter.FLAT)
        self.align_text.grid(row=1, column=0, padx=0, pady=0,
                            sticky="s")
        self.alignment_in_window = False
        
        # add button to initiate alignment
        self.align_button = Tkinter.Button(self.align_frame, width = 9, bg=window_background,
                                        font=(global_font, 12, "bold"), text="ALIGN",
                                        fg=window_text_green, command=self.align_amino_acids, 
                                        relief=Tkinter.FLAT)
        self.align_button.grid(row=2, column=0, sticky="wn", pady=0) 
        
        # add button to draw phylogenetic tree
        self.align_button = Tkinter.Button(self.align_frame, width = 9, bg=window_background,
                                        font=(global_font, 12, "bold"), text="TREE",
                                        fg=header_background_blue, command=self.draw_tree_alignment, 
                                        relief=Tkinter.FLAT)
        self.align_button.grid(row=2, column=0, sticky="n", pady=0) 
        self.tree_in_window = False
        
        # add button to clear alignment window
        self.align_clear = Tkinter.Button(self.align_frame, width = 9, bg=window_background,
                                        font=(global_font, 12, "bold"), text="CLEAR",
                                        fg=window_text_red, command=self.clear_align_window, 
                                        relief=Tkinter.FLAT)
        self.align_clear.grid(row=2, column=0, sticky="en", pady=0)
        
        # add scroll bar for alignment textbox
        align_scroll = Tkinter.Scrollbar(self.align_frame)       
        align_scroll.grid(row=1, column=1, sticky="nse")
        
        self.align_text.config(yscrollcommand=align_scroll.set)
        align_scroll.config(command=self.align_text.yview)   

        # make widgets resize with window
        self.large_grid.grid_columnconfigure(0, weight=1)  
        self.large_grid.grid_columnconfigure(1, weight=1) 
        self.large_grid.grid_rowconfigure(0, weight=1)
        self.large_grid.grid_rowconfigure(1, weight=1)
        
        # boolean variable ensuring nothing happens until some data is loaded
        self.data_loaded = False
                                  
    def load_carp(self, *args):
        
        self.clear_text_box()                             
        self.amino_acids = Fasta("./data/carp.genome_browser.faa")
        self.swiss_handle = "./data/carp.genome_browser.swiss.annot"        
        self.load_swiss()       
        self.exp_df = pd.read_csv("./data/carp.genome_browser.fpkm", delimiter="\t", index_col=0)
        self.count_lines_in_textbox()
        self.expression_y_label = "RPKM"
        self.data_loaded = True
 
    def load_dRerio(self, *args):
        
        self.clear_text_box()                             
        self.amino_acids = Fasta("./data/dRerio.genome_browser.faa")
        self.swiss_handle = "./data/dRerio.genome_browser.annot"        
        self.load_swiss()       
        self.exp_df = None
        self.count_lines_in_textbox()
        self.expression_y_label = "RPKM"
        self.data_loaded = True
        
    def load_khv(self, *args):
        
        self.clear_text_box()                             
        self.amino_acids = Fasta("./data/khv.genome_browser.faa")
        self.swiss_handle = "./data/khv.genome_browser.annot"       
        self.load_swiss()       
        self.exp_df = pd.read_csv("./data/khv.genome_browser.fpkm", delimiter="\t", index_col=0)
        self.count_lines_in_textbox()
        self.expression_y_label = "RPKM (log10)"        
        self.data_loaded = True
                
    def load_swiss(self):
        
        # get a list of where tabs occur so can color columns later        
        self.swiss_file = open(self.swiss_handle)        
        swiss_data = ""        
        line_count = 0
        for line in self.swiss_file:
            line_count += 1
            swiss_data += line         
        self.swiss_text.insert(1.0, swiss_data) 
        #self.swiss_text.config(state=Tkinter.DISABLED)
        self.swiss_file.close()        
        self.color_text_columns()
    
    def color_text_columns(self):
        self.swiss_text.tag_configure("id_column", foreground=window_text_green)
        self.swiss_text.tag_configure("gene_column", foreground=window_text_red)
        countVar = Tkinter.StringVar()
        swiss_lines = int(self.swiss_text.index("end-1c").split(".")[0])       
        for line in range(1, swiss_lines):
            line_str = str(line)
            first_tab = self.swiss_text.search(r"\t", line_str + ".0", line_str + ".end",
                                               regexp=True)
            second_tab_search = self.swiss_text.search(r"\t.*\t", line_str + ".0", line_str + ".end",
                                                regexp=True, count=countVar)
             
            second_tab_split = second_tab_search.split(".")            
            second_tab = second_tab_split[0] + "." + str(int(second_tab_split[1]) + int(countVar.get()))          
            self.swiss_text.tag_add("id_column", line_str + ".0", first_tab)
            self.swiss_text.tag_add("gene_column", first_tab, second_tab)

    def load_amino_acid(self, aa_id):        
        self.amino_text.delete(1.0, "end")
        self.amino_text.insert(1.0, ">" + aa_id + "\n")
        self.amino_text.insert(2.0, self.amino_acids[aa_id])
        
    def load_nucleotides(self, nucl_id):        
        self.nucl_text.delete(1.0, "end")
        self.nucl_text.insert(1.0, ">" + nucl_id + "\n")
        self.nucl_text.insert(2.0, self.carp_nucleotides[nucl_id])
        
    def load_expression_figure(self, gene_id):        
        self.f = Figure(figsize=figure_size, dpi=100)
        a = self.f.add_subplot(111)        
        gene_data = self.exp_df.loc[gene_id]
        #sb.set_style("whitegrid")
        sb.set(rc={"axes.facecolor": window_background, "figure.facecolor": window_background,
                   "grid.color": "#ecf0f1"})        
        
        #treat_colors = {"acute": "#e74c3c", "persistent": "#3498db", "reactivation": "#9b59b6",
        #        "mock": "#2ecc71"}
        
        treat_colors = {"carp1": "#e74c3c", "carp2": "#e74c3c", "carp3": "#e74c3c",
                        "carp4": "#3498db", "carp5": "#3498db", "carp6": "#3498db",
                        "carp7": "#9b59b6", "carp8": "#9b59b6", "carp9": "#9b59b6",
                        "carp11": "#2ecc71", "carp12": "#2ecc71"}

        p = sb.barplot(ax=a, data=gene_data, x="sample", y="RPKM", 
                   palette=treat_colors, alpha=0.75)
                   
        p.set(ylabel=self.expression_y_label)
                   
        # remove previous figure
        if hasattr(self, "canvas"):
            self.canvas.get_tk_widget().grid_forget()
            
        self.canvas = FigureCanvasTkAgg(self.f, master=self.figure_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=0, pady=0, sticky="ew") 
 
    def on_text_click(self, event):
        if self.data_loaded:
            index = self.swiss_text.index("@%s,%s" % (event.x, event.y))
            line, char = index.split(".")            
            line_text = self.swiss_text.get(line + ".0", line + ".end").strip()           
            line_gene_id = line_text.split("\t")[0]
            
            if line_gene_id:
                self.load_amino_acid(line_gene_id)     
                #self.load_nucleotides(line_gene_id) 
                self.load_expression_figure(line_gene_id)  
            
            # if not highlighted, highlight, or else remove highlight
            highlight_tags = self.swiss_text.tag_ranges("highlight")
            if highlight_tags:
                self.swiss_text.tag_remove("highlight", "0.0", "end")
                self.swiss_text.tag_add("highlight", line + ".0", line + ".end")
            else:
                self.swiss_text.tag_add("highlight", line + ".0", line + ".end")

    def clear_text_box(self):
        self.swiss_text.delete(1.0, "end")
        self.amino_text.delete(1.0, "end")

        if hasattr(self, "canvas"):
            self.f = Figure(figsize=figure_size, dpi=100)
            self.f.set_facecolor(window_background)
            self.canvas = FigureCanvasTkAgg(self.f, master=self.figure_frame)
            self.canvas.get_tk_widget().grid(row=1, column=0, padx=0, pady=0, sticky="ew") 
     
    def clear_align_window(self):
        self.align_text.delete(1.0, "end")
        self.alignment_in_window = False
        self.tree_in_window = False

    def clear_amino_window(self):
        self.amino_text.delete(1.0, "end")   
    
    def search_text(self, *args):
        if self.data_loaded:
            self.clear_text_box()
            search_word = self.search.get().lower()
            pat = re.compile(search_word)
            
            swiss_data = open(self.swiss_handle)
            
            for line in swiss_data:
                line = line.strip()
                line_lower = line.lower()
                if re.findall(pat, line_lower):
                    self.swiss_text.insert(Tkinter.INSERT, line + "\n")
            self.color_text_columns()
            self.count_lines_in_textbox()
            swiss_data.close()

    def count_lines_in_textbox(self):
        swiss_lines = int(self.swiss_text.index("end-1c").split(".")[0]) - 1
        if swiss_lines == 1:
            self.result_count_var.set(str(swiss_lines) + " result")
        else:
            self.result_count_var.set(str(swiss_lines) + " results")
            
    def copy_to_alignment_box(self):
        if self.alignment_in_window == True or self.tree_in_window == True:
            self.clear_align_window()
        amino_acid = self.amino_text.get(1.0, "end")
        self.align_text.insert(1.0, amino_acid)
        
    def align_amino_acids(self):
        # if statments at the start check: 
        # a) if the same sequence ids are there twice (clustal errors when this happens)
        # b) if an alignment is already present in the window
        # c) if data from a genome has been loaded
        # d) if more than 1 sequence is available for alignment

        if len(self.sequences_present()) == len(set(self.sequences_present())):
            duplicates_absent = True
        else:
            duplicates_absent = False
            print "cannot align sequences with duplicate IDs"
    
        if self.alignment_in_window == False and self.data_loaded and duplicates_absent:
            # this part does new alignment            
            if self.tree_in_window == False and len(self.sequences_present()) > 1 and duplicates_absent:
                amino_acids = self.align_text.get(1.0, "end")
                # seems ridiculous to have to write file just so can read into SeqOject
                tmp_amino_output = open("./tmp_files/tmp_amino_acids.txt", "w")
                tmp_amino_output.write(amino_acids)  
                tmp_amino_output.close()
            
            align_file = ClustalwCommandline(r".\dependencies\clustalw2.exe",
                                             infile="./tmp_files/tmp_amino_acids.txt")
            stdout, stderr = align_file()
            
            self.align_text.delete(1.0, "end")
            clustal_align_file = open(r"./tmp_files/tmp_amino_acids.aln")
            for line in clustal_align_file:            
                self.align_text.insert(Tkinter.INSERT, line)
            
            self.alignment_in_window = True
            
    def draw_tree_alignment(self):
        if self.alignment_in_window == True and self.data_loaded:
            self.clear_align_window()
            tree = Phylo.read(r"./tmp_files/tmp_amino_acids.dnd", "newick")
            with open(r"./tmp_files/tmp_ascii_tree", "w") as fh:
                Phylo.draw_ascii(tree, file=fh, column_width=45)
            
            for line in open(r"./tmp_files/tmp_ascii_tree"):
                self.align_text.insert(Tkinter.INSERT, line)
            self.tree_in_window = True
            
    def sequences_present(self):
        text_present = self.align_text.get(1.0, "end")
        sequences = []
        for line in text_present.split("\n"):
            if line.startswith(">"):
                sequences.append(line)
        return sequences
            
if __name__ == "__main__":
    root = Tkinter.Tk()
    #root.geometry("+100+100")
    app = carp_browser(root)
    root.mainloop()

