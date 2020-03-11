from tkinter import *
from tkinter import ttk

class TaggerComponent:

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.buttons_frame = ttk.Frame(self.parent)
        self.buttons_frame.grid(row=0,column = 0)
        #ngram
        self.ngram_label = Label(self.buttons_frame, text='Ngram length', font=('Arial', 12, 'normal'))
        self.ngram_label.grid(column= 0, row = 0, pady=20, padx=10)
        self.ngram_var = StringVar()
        self.ngram_dropdown = ttk.Combobox(self.buttons_frame, textvariable=self.ngram_var, state='readonly',width=10)
        self.ngram_dropdown.grid(column = 1, row = 0)
        self.ngram_dropdown['values'] = ('3','2','1')
        self.ngram_dropdown.current(0)
        #source
        self.text_frame = ttk.Frame(self.parent)
        self.text_frame.grid(row=1, column=0)
        self.source_text = Text()
        self.source_text = Text(self.text_frame, width=100, height=10 )
        self.source_text.grid(row= 0,column = 0,sticky='w')
        self.tag_button = ttk.Button(self.text_frame,text='Tag ->',command = self.tag)
        self.tag_button.grid(row=0,column = 1, sticky='W')
        #destination
        self.destination_text = Text()
        self.destination_text = Text(self.text_frame, width=100, height=10 )
        self.destination_text.grid(row= 0,column = 2,sticky='w')

    def tag(self):
        text = self.source_text.get('1.0',END)
        n = self.ngram_dropdown.get()
        tags = self.controller.tag_text(text,n)
        self.destination_text.delete('1.0', END)
        self.destination_text.insert(END, tags)