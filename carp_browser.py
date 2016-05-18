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

class carp_browser:

    def __init__(self, root):
        
        self.root = root
        root.configure(background="#333")
        root.title(" Carp Genome Browser ")
        
        self.root.iconbitmap(r"./data/kitchen_fish_icon.ico") # change little TK icon     
        
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
                                       bd=0, relief=Tkinter.SUNKEN)
        self.left_pane.grid(row=0, column=0, padx=20, pady=20, sticky="n")        
          
        self.radio_var = Tkinter.IntVar()
        
        self.chk1 = Tkinter.Radiobutton(self.left_pane, text="Cyprinus carpio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=1,
                                        cursor="hand2", command=self.load_carp)                               
        self.chk1.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        self.chk2 = Tkinter.Radiobutton(self.left_pane, text="Danio Rerio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=2,
                                        cursor="hand2")                               
        self.chk2.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.chk3 = Tkinter.Radiobutton(self.left_pane, text="Tilapia",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=3,
                                        cursor="hand2")                               
        self.chk3.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.chk4 = Tkinter.Radiobutton(self.left_pane, text="CyHV-3",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=4,
                                        cursor="hand2")                               
        self.chk4.grid(row=3, column=0, padx=20, pady=5, sticky="w")        

        #### add middle search screens ####

        self.middle_pane = Tkinter.Frame(root, height=800, width=400, bg="#333",
                                         bd=0, relief=Tkinter.SUNKEN)
        self.middle_pane.grid(row=0, column=1, padx=0, pady=10, sticky="n") 
        
        # create swiss text box
        self.swiss_text = Tkinter.Text(self.middle_pane, width=70, height=10,
                                       font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc", insertbackground="#dcdccc",
                                        cursor="hand2")         
        self.swiss_text.grid(row=1, column=0, padx=0, pady=0, 
                              sticky=Tkinter.N+Tkinter.E+Tkinter.W)
        
        # add scroll bar to swiss text box
        swiss_scroll = Tkinter.Scrollbar(self.middle_pane)       
        swiss_scroll.grid(row=1, column=1, sticky="nse")
        
        self.swiss_text.config(yscrollcommand=swiss_scroll.set)
        swiss_scroll.config(command=self.swiss_text.yview)
              
        # add entry widget for searching annotations (above text widget)                            
                              
        self.search = Tkinter.Entry(self.middle_pane, width=28,
                                          font=("Consolas", 11), bg="gray")
        self.search.bind("<Return>", self.search_text)
        self.search.grid(row=0, column=0, sticky="w", pady=5)
        
        self.search_button = Tkinter.Button(self.middle_pane, text="Search", bg="gray",
                                            font=("Consolas", 8), width=12,
                                            command=self.search_text)
        self.search_button.grid(row=0, column=0, sticky="", pady=5)
        
        self.result_count_var = Tkinter.StringVar()
        self.word_count = Tkinter.Label(self.middle_pane, width = 20, bg="#333", fg="#dcdccc",
                                        font=("Consolas", 10), textvariable=self.result_count_var)
        self.word_count.grid(row=0, column=0, sticky="e")                            
        
        # add clicking and highlighting ability
        
        self.swiss_text.tag_configure("highlight", background="#333")
        self.swiss_text.bind("<1>", self.on_text_click)
        
        # add figure placeholder to bottom of middle pane
        self.f = Figure(figsize=(7,3), dpi=100)
        self.f.set_facecolor("#3f3f3f")
        self.canvas = FigureCanvasTkAgg(self.f, master=self.middle_pane)
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=0, pady=35, sticky="ns")
        
        #### add right nucleotide and amino acid boxes ####

        self.right_pane = Tkinter.Frame(root, height=800, width=400, bg="#333",
                                        bd=0, relief=Tkinter.SUNKEN)
        self.right_pane.grid(row=0, column=2, padx=30, pady=10, sticky="n")
        
        # add label for amino acid box
        self.amino_label = Tkinter.Label(self.right_pane, width = 20, bg="#333", fg="#dcdccc",
                                        font=("Consolas", 10), text="Amino acid box")
        self.amino_label.grid(row=0, column=0, sticky="n", pady=5)    
        
        # create amino acid text box
        self.amino_text = Tkinter.Text(self.right_pane, width = 80, height = 10,
                                      font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc", insertbackground="#dcdccc")
        self.amino_text.grid(row=1, column=0, padx=0, pady=0, sticky="")
        
        # add scroll bar for amino acid textbox
        amino_scroll = Tkinter.Scrollbar(self.right_pane)       
        amino_scroll.grid(row=1, column=1, sticky="nse")
        
        self.amino_text.config(yscrollcommand=amino_scroll.set)
        amino_scroll.config(command=self.amino_text.yview)
        
        # add button to copy from amino acid box to alignment box
        self.amino_add_button = Tkinter.Button(self.right_pane, width = 25, bg="gray",
                                        font=("Consolas", 8), text="Copy to alignment box",
                                        command=self.copy_to_alignment_box)
        self.amino_add_button.grid(row=2, column=0, sticky="wn", pady=5)  
        
        # add button to clear amino acid box
        self.amino_clear = Tkinter.Button(self.right_pane, width = 15, bg="gray",
                                        font=("Consolas", 8), text="Clear",
                                        command=self.clear_amino_window)
        self.amino_clear.grid(row=2, column=0, sticky="en", pady=5)        

        # add label for alignment box
        self.align_label = Tkinter.Label(self.right_pane, width = 20, bg="#333", fg="#dcdccc",
                                        font=("Consolas", 10), text="Alignment box")
        self.align_label.grid(row=3, column=0, sticky="s", pady=5)                            
                            
        # create alignment text box
        self.align_text = Tkinter.Text(self.right_pane, width = 80, height = 11,
                                      font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc", insertbackground="#dcdccc")
        self.align_text.grid(row=4, column=0, padx=0, pady=0,
                            sticky="s")
        self.alignment_in_window = False
        
        # add button to initiate alignment
        self.align_button = Tkinter.Button(self.right_pane, width = 15, bg="gray",
                                        font=("Consolas", 8), text="Align",
                                        command=self.align_amino_acids)
        self.align_button.grid(row=5, column=0, sticky="wn", pady=5) 
        
        # add button to draw phylogenetic tree
        self.align_button = Tkinter.Button(self.right_pane, width = 15, bg="gray",
                                        font=("Consolas", 8), text="Draw tree",
                                        command=self.draw_tree_alignment)
        self.align_button.grid(row=5, column=0, sticky="n", pady=5) 
        self.tree_in_window = False
        
        # add button to clear alignment window
        self.align_clear = Tkinter.Button(self.right_pane, width = 15, bg="gray",
                                        font=("Consolas", 8), text="Clear",
                                        command=self.clear_align_window)
        self.align_clear.grid(row=5, column=0, sticky="en", pady=5)
        
        # add scroll bar for alignment textbox
        align_scroll = Tkinter.Scrollbar(self.right_pane)       
        align_scroll.grid(row=4, column=1, sticky="nse")
        
        self.align_text.config(yscrollcommand=align_scroll.set)
        align_scroll.config(command=self.align_text.yview)
        
        # boolean variable ensuring nothing happens until some data is loaded
        self.data_loaded = False
                                  
    def load_carp(self):
        
        self.clear_text_box()                             
        self.carp_amino_acids = Fasta("./data/V1.0.Commoncarp_gene.pep")
        self.swiss_file = open("./data/swiss.genome_browser")        
        self.load_swiss()  
        #self.carp_nucleotides = Fasta("./data/genes.genome_browser")      
        self.exp_df = pd.read_csv("./data/genome_browser_melt_treat.htseq", delimiter="\t", index_col=0)
        self.count_lines_in_textbox()        
        self.data_loaded = True
                
    def load_swiss(self):
        
        # get a list of where tabs occur so can color columns later        
        swiss_data = ""        
        #tab_pat = re.compile(r"\t")
        #tab_dict = {}
        line_count = 0
        for line in self.swiss_file:
            line_count += 1
            swiss_data += line
            #tmp_match = []
            #for matches in re.finditer(tab_pat, line):
            #    tmp_match.append(matches.start())
            #tab_dict[line_count] = tmp_match
            
        self.swiss_text.insert(1.0, swiss_data) 
        #self.swiss_text.config(state=Tkinter.DISABLED)
        self.swiss_file.close()        
        self.color_text_columns()
    
    def color_text_columns(self):
        self.swiss_text.tag_configure("id_column", foreground="#cc9393")
        self.swiss_text.tag_configure("gene_column", foreground="#7f9f7f")
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

    def load_carp_amino_acid(self, aa_id):        
        self.amino_text.delete(1.0, "end")
        self.amino_text.insert(1.0, ">" + aa_id + "\n")
        self.amino_text.insert(2.0, self.carp_amino_acids[aa_id])
        
    def load_carp_nucleotides(self, nucl_id):        
        self.nucl_text.delete(1.0, "end")
        self.nucl_text.insert(1.0, ">" + nucl_id + "\n")
        self.nucl_text.insert(2.0, self.carp_nucleotides[nucl_id])
        
    def load_expression_figure(self, gene_id):        
        self.f = Figure(figsize=(7,3), dpi=100)
        a = self.f.add_subplot(111)        
        gene_data = self.exp_df.loc[gene_id]
        sb.set_style("whitegrid")
        
        treat_colors = {"acute": "#e41a1c", "persistent": "#377eb8", "reactivation": "#984ea3",
                "mock": "#4daf4a"}

        sb.barplot(ax=a, data=gene_data, x="sample", y="RPKM", hue="treatment",
                   palette=treat_colors)
        #for item in p.get_xticklabels():
        #    item.set_rotation(30)
                   
        # remove previous figure
        if hasattr(self, "canvas"):
            self.canvas.get_tk_widget().grid_forget()
            
        self.canvas = FigureCanvasTkAgg(self.f, master=self.middle_pane)
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=0, pady=35, sticky="ns") 
 
    def on_text_click(self, event):
        if self.data_loaded:
            index = self.swiss_text.index("@%s,%s" % (event.x, event.y))
            line, char = index.split(".")
            
            line_gene_id = self.swiss_text.get(line + ".0", line + ".11").strip()
            if line_gene_id:
                self.load_carp_amino_acid(line_gene_id)     
                #self.load_carp_nucleotides(line_gene_id) 
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
            self.f = Figure(figsize=(7,3), dpi=100)
            self.f.set_facecolor("#3f3f3f")
            self.canvas = FigureCanvasTkAgg(self.f, master=self.middle_pane)
            self.canvas.get_tk_widget().grid(row=2, column=0, padx=0, pady=35, sticky="ns") 
     
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
            swiss_file = open("./data/swiss.genome_browser")
            for line in swiss_file:
                line = line.strip()
                line_lower = line.lower()
                if re.findall(pat, line_lower):
                    self.swiss_text.insert(Tkinter.INSERT, line + "\n")
            self.color_text_columns()
            self.count_lines_in_textbox()
            swiss_file.close()

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
                Phylo.draw_ascii(tree, file=fh, column_width=70)
            
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

