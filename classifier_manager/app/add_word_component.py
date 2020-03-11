from tkinter import *
from tkinter import ttk
from .synset_selector_component import SynsetSelectorComponent

class AddWordComponent:

    def __init__(self,parent,controller):
        self.controller = controller
        self.parent = parent
        self.inputs_frame = LabelFrame(self.parent,text='Add Word',font=('Arial', 12, 'bold'))
        self.inputs_frame.grid(row=0,column=0,rowspan=4,columnspan=4)
        #word
        self.word_var = StringVar()
        self.word_label = Label(self.inputs_frame, text='Word', font=('Arial', 12, 'normal'), pady=20, padx=10)
        self.word_label.grid(row=0,column=0,sticky=W)
        self.word_entry = Entry(self.inputs_frame, textvariable=self.word_var )
        self.word_entry.grid(row= 0,column =1)
        #pos
        self.pos_var = StringVar()
        self.pos_label = Label(self.inputs_frame, text='Pos', font=('Arial', 12, 'normal'))
        self.pos_label.grid(row=0,column=2, sticky='we')
        self.pos_dropdown = ttk.Combobox(self.inputs_frame, textvariable=self.pos_var, state='readonly',width=10)
        self.pos_dropdown.grid(row= 0,column =3)
        self.pos_dropdown['values']=('noun','verb','adjective','adverb')
        self.pos_dropdown.current(0)
        # self.pos_dropdown.bind('<<ComboboxSelected>>')
        #lang
        self.lang_var = StringVar()
        self.lang_label = Label(self.inputs_frame, text='Language', font=('Arial', 12, 'normal'))
        self.lang_label.grid(row=1,column=0, sticky=W)
        self.lang_dropdown = ttk.Combobox(self.inputs_frame, textvariable=self.lang_var, state='readonly',width=8)
        self.lang_dropdown.grid(row= 1,column =1)
        self.lang_dropdown['values']=('ita','eng')
        self.lang_dropdown.current(0)
        #offset
        self.offset_var = StringVar()
        self.offset_label = Label(self.inputs_frame, text='Synset', font=('Arial', 12, 'normal'), pady=20)
        self.offset_label.grid(row=1,column=2,sticky='we')
        self.offset_entry = Entry(self.inputs_frame, textvariable=self.offset_var,width=10 )
        self.offset_entry.grid(row= 1,column = 3)
        #buttons
        self.buttons_frame = ttk.Frame(self.inputs_frame)
        self.buttons_frame.grid(row=3, column = 0, sticky = 'W')
        self.add_btn = ttk.Button(self.buttons_frame,text='Add Word',command = self.add)
        self.add_btn.grid(row=0,column = 0, sticky='W')
        self.clear_btn = ttk.Button(self.buttons_frame,text='Clear Input',command = self.clear)
        self.clear_btn.grid(row=0,column = 1,sticky='W')
        #sense disambiguation
        self.add_sense_frame =  LabelFrame(self.parent,text='Sense disambiguation',font=('Arial', 12, 'bold'))
        self.add_sense_frame.grid(row = 4, column = 0, rowspan=3, columnspan=5,pady=10)
        self.get_sense_info_button = Button(self.add_sense_frame, text='Get Sense Info', command = self.get_sense_info)
        self.get_sense_info_button.grid(row =0, column = 0, padx=20, pady=8)
        self.get_sense_info_error_var = StringVar()
        self.get_sense_info_error_label = Label(self.add_sense_frame,font=('Arial', 12, 'normal'),foreground="red",justify=LEFT )
        self.get_sense_info_error_label.grid(row=0, column= 1, columnspan = 3,padx=10)
        self.get_sense_info_error_label['textvariable'] = self.get_sense_info_error_var
        self.add_sense_word_var = StringVar()
        self.add_sense_word_label = Label(self.add_sense_frame, text='For', font=('Arial', 12, 'normal'),padx=10)
        self.add_sense_word_label.grid(row = 1, column = 0)
        self.add_sense_word_entry = Entry(self.add_sense_frame, textvariable=self.add_sense_word_var)
        self.add_sense_word_entry.grid(row=1, column=1)
        self.selected_index = StringVar()
        self.add_sense_index_label = Label(self.add_sense_frame, text='at index', font=('Arial', 12, 'normal'),padx=10)
        self.add_sense_index_label.grid(row = 1, column = 2)
        self.add_sense_index_entry = Entry(self.add_sense_frame, textvariable=self.selected_index, width=8)
        self.add_sense_index_entry.grid(row=1, column=3)
        self.add_sense_button = Button(self.add_sense_frame, text='Add', command = self.add_sense_index)
        self.add_sense_button.grid(row = 1, column = 4, padx=20)
        #errors
        self.errors_frame = ttk.Frame(self.parent)
        self.errors_frame.grid(row=8, column= 0, rowspan = 2,columnspan = 3,sticky ="W", pady=10)
        self.errors_var = StringVar()
        self.errors_label = Label(self.errors_frame, font=('Arial', 12, 'normal'), foreground="red",justify=LEFT,padx=10)
        self.errors_label['textvariable'] = self.errors_var
        self.errors_label.grid(row=0,column=0,sticky='w')
        # success
        self.success_var = StringVar()
        self.success_label = Label(self.errors_frame, font=('Arial', 12, 'normal'),foreground="green",justify=LEFT,padx=10)
        self.success_label['textvariable'] = self.success_var
        self.success_label.grid(row=1,column=0,sticky='w')
        #sense
        self.sense_selector = SynsetSelectorComponent(self.parent,self.controller, startRow=0, startColumn=6)
        self.sense_selector.configure_command(self.sense_selector.confirm_synset_selection, offsetholder=self.offset_entry)

    def add(self):
        self.errors_var.set('')
        self.success_var.set('')
        errors = self.controller.add_word(self.word_var.get(), self.pos_var.get(), self.offset_var.get(), self.lang_var.get())
        if errors:
            self.errors_var.set('\n'.join([key + errors[key] for key in errors]))
        else:
            self.success_var.set('Word added succesfully')

    def add_sense_index(self):
        self.errors_var.set('')
        self.success_var.set('')
        word = self.add_sense_word_entry.get()
        errors = self.controller.add_sense_disambiguation(word, self.add_sense_index_entry.get())
        if errors:
            self.errors_var.set('\n'.join([key + errors[key] for key in errors]))
        else:
            self.success_var.set('Sense disambiguation for "{}" added succesfully'.format(word))

    def get_sense_info(self):
        self.get_sense_info_error_var.set('')
        index = self.sense_selector.get_sense_index() + 1
        lang = self.sense_selector.get_search_lang()
        word = self.sense_selector.get_search_word()
        self.add_sense_index_entry.delete(0,END)
        self.add_sense_word_entry.delete(0,END)
        if index < 0:
            self.get_sense_info_error_var.set('You must select a sense')
        elif lang == 'eng':
            self.get_sense_info_error_var.set('Sense search must be in italian')
        else:
            self.add_sense_index_entry.insert(END, index)
            self.add_sense_word_entry.insert(END, word)


    def clear(self):
        self.word_entry.delete(0,END)
        self.offset_entry.delete(0,END)
        self.offset_entry.insert(0,'0')
        self.lang_dropdown.current(0)
        self.pos_dropdown.current(0)
        self.sense_selector.clear()
        self.errors_var.set('')
        self.success_var.set('')