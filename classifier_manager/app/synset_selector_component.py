from tkinter import *
from tkinter import ttk

class SynsetSelectorComponent:

    def __init__(self, parent, controller, startRow, startColumn):
        self.parent = parent
        self.controller = controller
        #search bar
        self.synset_search_frame = ttk.Frame(self.parent)
        self.synset_search_frame.grid(row=startRow, column= startColumn, columnspan=2,padx=20)
        self.search_var = StringVar()
        self.search_label = Label(self.synset_search_frame, text='Search sense:', font=('Arial', 12, 'normal') )
        self.search_label.grid(row=0,column=0,sticky=W)
        self.search_entry = Entry(self.synset_search_frame, textvariable=self.search_var)
        self.search_entry.grid(row= 0,column =1,sticky='W')
        self.lang_search_var = StringVar()
        self.lang_search_dropdown = ttk.Combobox(self.synset_search_frame, width=8,textvariable=self.lang_search_var, state='readonly')
        self.lang_search_dropdown.grid(row= 0,column =2)
        self.lang_search_dropdown['values']=('eng','ita')
        self.lang_search_dropdown.current(0)
        self.search_btn = ttk.Button(self.synset_search_frame,text='Search',command = self.search_senses)
        self.search_btn.grid(row=0,column = 3, sticky='W')
        #synset display
        self.synset_list_frame = ttk.Frame(self.parent)
        self.synset_list_frame.grid(row=startRow+1, column= startColumn, rowspan=10, columnspan=10,padx=20)
        self.synset_list = Listbox(self.synset_list_frame, height=20, width=150,font=('Arial', 12, 'normal'))
        self.synset_list.grid(row=1, column=0, rowspan=6,columnspan=9)
        self.synset_yscrollbar = Scrollbar(self.synset_list_frame,orient=VERTICAL,command=self.synset_list.yview)
        self.synset_yscrollbar.grid(row =1, column=9,rowspan=6,sticky='ns')
        self.synset_xscrollbar = Scrollbar(self.synset_list_frame,orient=HORIZONTAL,command=self.synset_list.xview)
        self.synset_xscrollbar.grid(row =7, column=0,columnspan=9,sticky='we')
        self.synset_list.configure(yscrollcommand=self.synset_yscrollbar.set,xscrollcommand=self.synset_xscrollbar.set)
        self.synset_ids = []
        self.select_btn = ttk.Button(self.synset_list_frame,text='Confirm selection')
        self.select_btn.grid(row=8,column = 0, sticky='W')
        self.selected_synset_index = -1
    
    def configure_command(self, method, **kwargs):
        def f():
            return method(**kwargs)
        self.select_btn.configure(command=f)
    
    def search_senses(self):
        word = '_'.join(self.search_var.get().split()).lower()
        senses,self.synset_ids = self.controller.search_senses(word,self.lang_search_dropdown.get())
        self.synset_list.delete(0,END)
        self.selected_synset_index = -1
        for sense in senses:
            self.synset_list.insert(END,sense)
    
    def confirm_synset_selection(self, offsetholder=None, indexholder = None):
        entry = offsetholder
        index = indexholder
        if entry:
            entry.delete(0,END)
        selection = self.synset_list.curselection()
        if selection:
            self.selected_synset_index = selection[0]
            if entry:
                entry.insert(END, self.synset_ids[selection[0]])
            if index:
                index = selection[0]
    
    def get_sense_index(self):
        return self.selected_synset_index
    
    def get_search_lang(self):
        return self.lang_search_var.get()

    def get_search_word(self):
        return self.search_var.get()
    
    def clear(self):
        self.synset_list.delete(0, END)