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
                                       bd=0, relief=Tkinter.SUNKEN)
        self.left_pane.grid(row=0, column=0, padx=20, pady=20, sticky="n")        
          
        self.radio_var = Tkinter.IntVar()
        
        self.chk1 = Tkinter.Radiobutton(self.left_pane, text="Cyprinus carpio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=1,
                                        cursor="hand2", command=self.load_carp)                               
        self.chk1.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.chk2 = Tkinter.Radiobutton(self.left_pane, text="Danio Rerio",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=2,
                                        cursor="hand2")                               
        self.chk2.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.chk3 = Tkinter.Radiobutton(self.left_pane, text="Tilapia",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=3,
                                        cursor="hand2")                               
        self.chk3.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.chk4 = Tkinter.Radiobutton(self.left_pane, text="CyHV-3",
                                        bg="#333", fg="#efef8f", selectcolor="#3f3f3f", 
                                        activebackground="#333", variable=self.radio_var, value=4,
                                        cursor="hand2")                               
        self.chk4.grid(row=3, column=0, padx=20, pady=10, sticky="w")        

        #### add middle search screens ####

        self.middle_pane = Tkinter.Frame(root, height=400, width=400, bg="#333",
                                         bd=0, relief=Tkinter.SUNKEN)
        self.middle_pane.grid(row=0, column=1, padx=0, pady=10, sticky="n") 
        
        # create swiss text box
        self.swiss_text = Tkinter.Text(self.middle_pane, width=80, height=10,
                                       font=("Consolas", 10), padx=5, pady=5, spacing1=5,
                                        bg="#3f3f3f", fg="#dcdccc", insertbackground="#dcdccc",
                                        cursor="hand2")         
        self.swiss_text.grid(row=1, column=0, padx=0, pady=0, 
                              sticky=Tkinter.N+Tkinter.E+Tkinter.W)
                              
        # add entry widget for searching annotations (above text widget)                            
                              
        self.search = Tkinter.Entry(self.middle_pane, width=30,
                                          font=("Consolas", 11), bg="gray")
        self.search.bind("<Return>", self.search_text)
        self.search.grid(row=0, column=0, sticky="w", pady=5)
        
        self.search_button = Tkinter.Button(self.middle_pane, text="Search",
                                            font=("Consolas", 8), width=12,
                                            command=self.search_text)
        self.search_button.grid(row=0, column=0, sticky="", pady=5)
        
        self.result_count_var = Tkinter.StringVar()
        self.word_count = Tkinter.Label(self.middle_pane, width = 20, bg="#333", fg="#dcdccc",
                                        font=("Consolas", 10), textvariable=self.result_count_var)
        self.word_count.grid(row=0, column=0, sticky="e")
                              
        # add scroll bar to swiss text box
        swiss_scroll = Tkinter.Scrollbar(self.middle_pane)
        swiss_scroll.grid(row=1, column=0, sticky="nse")
        
        self.swiss_text.config(yscrollcommand=swiss_scroll.set)
        swiss_scroll.config(command=self.swiss_text.yview)
        
        # add clicking and highlighting ability
        
        self.swiss_text.tag_configure("highlight", background="#333")
        self.swiss_text.bind("<1>", self.on_text_click)
        
        # add figure canvas to bottom of middle pane
       
        
        #### add right nucleotide and amino acid boxes ####

        self.right_pane = Tkinter.Frame(root, height=800, width=400, bg="#333",
                                        bd=0, relief=Tkinter.SUNKEN)
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
        
        # boolean variable ensuring nothing happens until some data is loaded
        self.data_loaded = False
                                  
    def load_carp(self):
        
        self.clear_text_box()
        self.load_swiss()                         
        self.carp_amino_acids = Fasta("./data/V1.0.Commoncarp_gene.pep")
        #self.carp_nucleotides = Fasta("./data/genes.genome_browser")      
        self.exp_df = pd.read_csv("./data/genome_browser_melt_treat.htseq", delimiter="\t", index_col=0)
        self.count_lines_in_textbox()        
        self.data_loaded = True
                
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
            
        self.swiss_text.insert(1.0, swiss_data) 
        #self.swiss_text.config(state=Tkinter.DISABLED)
        swiss_file.close()        
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
        
        f = Figure(figsize=(7,3), dpi=100)
        a = f.add_subplot(111)        
        gene_data = self.exp_df.loc[gene_id]
        sb.set_style("dark", {"figure.facecolor": "white"})
        sb.barplot(ax=a, data=gene_data, x="sample", y="RPKM", hue="treatment")        
        #gene_data.plot(ax=a, kind="bar")
        
        canvas = FigureCanvasTkAgg(f, master=self.middle_pane)
        canvas.get_tk_widget().grid(row=2, column=0, padx=0, pady=20, sticky="s") 
 
    def on_text_click(self, event):
        if self.data_loaded:
            index = self.swiss_text.index("@%s,%s" % (event.x, event.y))
            line, char = index.split(".")
            
            line_gene_id = self.swiss_text.get(line + ".0", line + ".11").strip()
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
        
    def search_text(self, *args):
        if self.data_loaded:
            self.clear_text_box()
            search_word = self.search.get()
            pat = re.compile(search_word)
            swiss_file = open("./data/swiss.genome_browser")
            for line in swiss_file:
                line = line.strip()
                if re.findall(pat, line):
                    self.swiss_text.insert(Tkinter.INSERT, line + "\n")
            self.color_text_columns()
            self.count_lines_in_textbox()

    def count_lines_in_textbox(self):
        swiss_lines = int(self.swiss_text.index("end-1c").split(".")[0]) - 1
        if swiss_lines == 1:
            self.result_count_var.set(str(swiss_lines) + " result")
        else:
            self.result_count_var.set(str(swiss_lines) + " results")
    
if __name__ == "__main__":
    root = Tkinter.Tk()
    #root.geometry("+100+100")
    app = carp_browser(root)
    root.mainloop()

