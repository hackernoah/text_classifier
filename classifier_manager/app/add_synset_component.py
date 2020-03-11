from tkinter import *
from tkinter import ttk
from .synset_selector_component import SynsetSelectorComponent

class AddSynsetComponent:

    def __init__(self,parent,controller):
        self.controller = controller
        self.parent = parent
        self.inputs_frame = ttk.Frame(self.parent)
        self.inputs_frame.grid(row=0,column=0,rowspan=6,columnspan=4)
        #words
        self.words_label = Label(self.inputs_frame, text='Words', font=('Arial', 12, 'normal'), pady=20, padx=10)
        self.words_label.grid(row=0,column=0,sticky=W)
        self.words_text = Text(self.inputs_frame, width=20, height=3 )
        self.words_text.grid(row= 0,column = 1,sticky='w')
        # #pos
        self.pos_var = StringVar()
        self.pos_label = Label(self.inputs_frame, text='Pos', font=('Arial', 12, 'normal'))
        self.pos_label.grid(row=0,column=2, sticky='we')
        self.pos_dropdown = ttk.Combobox(self.inputs_frame, textvariable=self.pos_var, state='readonly',width=8)
        self.pos_dropdown.grid(row= 0,column = 3)
        self.pos_dropdown['values']=('noun','verb','adjective','adverb')
        self.pos_dropdown.current(1)
        # self.pos_dropdown.bind('<<ComboboxSelected>>')
        #pointers
        self.pointers_frame = LabelFrame(self.inputs_frame,text='Pointers',font=('Arial', 12, 'bold'))
        self.pointers_frame.grid(row=1,column=0,rowspan=4,columnspan=4,pady=10,padx=10)
        self.pointers=[]
        # self.pointers_label = Label(self.pointers_frame, text='Pointers', font=('Arial', 12, 'bold'))
        # self.pointers_label.grid(row=0,column=0, sticky=W)
        #symbols
        self.symbols_label = Label(self.pointers_frame, text='Pointer type', font=('Arial', 12, 'normal'))
        self.symbols_label.grid(row=1,column=0, sticky=W)
        self.symbols_var = StringVar()
        self.symbols_dropdown = ttk.Combobox(self.pointers_frame, textvariable=self.symbols_var, state='readonly',width=8)
        self.symbols_dropdown.grid(row= 1,column =1,sticky='w')
        self.symbols_dropdown['values']=('@','!')
        self.symbols_dropdown.current(0)
        #offsets
        self.offset_var = StringVar()
        self.offset_label = Label(self.pointers_frame, text='Synset', font=('Arial', 12, 'normal'), pady=20)
        self.offset_label.grid(row=1,column=2,sticky=W)
        self.offset_entry = Entry(self.pointers_frame, textvariable=self.offset_var,width=10 )
        self.offset_entry.grid(row= 1,column = 3)
        #pointers list
        self.pointers_list = Listbox(self.pointers_frame, height=4, width=25,font=('Arial', 12, 'normal'))
        self.pointers_list.grid(row=2, column=0, rowspan=2,columnspan=2)
        self.pointers_yscrollbar = Scrollbar(self.pointers_frame,orient=VERTICAL,command=self.pointers_list.yview)
        self.pointers_yscrollbar.grid(row =2, column=2,rowspan=2,sticky='wns')
        self.pointers_list.configure(yscrollcommand=self.pointers_yscrollbar.set)
        #pointers buttons
        self.add_btn = ttk.Button(self.pointers_frame,text='Add Pointer',command = self.add_pointer)
        self.add_btn.grid(row=2,column = 3, sticky='W')
        self.clear_btn = ttk.Button(self.pointers_frame,text='Remove Pointer',command = self.remove_pointer)
        self.clear_btn.grid(row=3,column = 3,sticky='W')
        #gloss
        self.gloss_frame = LabelFrame(self.inputs_frame,text='Gloss',font=('Arial', 12, 'bold'))
        self.gloss_frame.grid(row = 5, column = 0, columnspan = 4, rowspan=2)
        self.gloss_text = Text(self.gloss_frame, width=50, height=4 )
        self.gloss_text.grid(row = 0,column = 0,columnspan=4, rowspan= 2, sticky='w')
        #buttons
        self.buttons_frame = ttk.Frame(self.parent)
        self.buttons_frame.grid(row=6, column = 0, padx=10,sticky = 'W')
        self.add_btn = ttk.Button(self.buttons_frame,text='Add Synset',command = self.add)
        self.add_btn.grid(row=0,column = 0, sticky='W')
        self.clear_btn = ttk.Button(self.buttons_frame,text='Clear Input',command = self.clear)
        self.clear_btn.grid(row=0,column = 1,sticky='W')
        #errors
        self.errors_frame = ttk.Frame(self.parent)
        self.errors_frame.grid(row=7, column= 0, sticky ="W")
        self.errors_var = StringVar()
        self.errors_label = Label(self.errors_frame, font=('Arial', 12, 'normal'), pady=10, foreground="red",justify=LEFT)
        self.errors_label['textvariable'] = self.errors_var
        self.errors_label.grid(row=0,column=0,sticky=W)
         #success
        self.success_frame = ttk.Frame(self.parent)
        self.success_frame.grid(row=7, column= 0, sticky ="W")
        self.success_var = StringVar()
        self.success_label = Label(self.success_frame, font=('Arial', 12, 'normal'), pady=10, foreground="green",justify=LEFT)
        self.success_label['textvariable'] = self.success_var
        self.success_label.grid(row=0,column=0,sticky=W)
        #sense selector
        self.selected_synset_index = 0
        self.sense_selector = SynsetSelectorComponent(self.parent,self.controller, startRow=0, startColumn=6)
        self.sense_selector.configure_command(self.sense_selector.confirm_synset_selection, offsetholder = self.offset_entry, indexholder = self.selected_synset_index)

    def pointer_to_string(self, pointer):
        return pointer[0] + ' ' + pointer[1] + ' ' + pointer[2]

    def add_pointer(self):
        errors = self.validate_add_pointer()
        if len(errors):
            self.errors_var.set('\n'.join([key + ' ' + errors[key] for key in errors]))
        else:
            pointer = (self.symbols_var.get(),self.offset_var.get(),self.pos_var.get(), '0000')
            self.pointers.append(pointer)
            self.pointers_list.insert(END, self.pointer_to_string(pointer))
            

    def remove_pointer(self):
        selection = self.pointers_list.curselection()
        if selection:
            del self.pointers[selection[0]]
            self.pointers_list.delete(0,END)
            self.pointers_list.delete(0,END)
            for pointer in self.pointers:
                self.pointers_list.insert(END, self.pointer_to_string(pointer))

    def add(self):
        self.errors_var.set('') 
        self.success_var.set('')
        errors = self.validate_add_synset()
        if errors:
            self.errors_var.set('\n'.join([key + ' ' + errors[key] for key in errors])) 
        else:
            errors = self.controller.add_synset(self.pos_var.get(), self.get_words(), self.get_pointers(), self.gloss_text.get('1.0',END))
            if errors:
                self.errors_var.set('\n'.join([key + ' ' + errors[key] for key in errors]))
            else:
                self.success_var.set('Synset added with success')

    def get_words(self):
        words = [word.strip().lower() for word in self.words_text.get('1.0',END).split(';')]
        return words

    def get_pointers(self):
        displayed_pointers = self.pointers_list.get(0, END)
        pointers = []
        for pointer in displayed_pointers:
            split = pointer.split()
            pointers.append((split[0], split[1], split[2], '0000'))
        return pointers

    def validate_add_pointer(self):
        self.errors_var.set('')
        errors = {}
        if len(self.offset_var.get()) < 4:
            errors['Add pointer(synset)'] = "synset must be at least 4 digits long"
        else:
            try:
                int(self.offset_var.get())
            except ValueError:
                errors['Add pointer(synset)'] = "synset must be an integer"
        if self.controller.has_searched():
            if self.controller.get_sense_pos(self.selected_synset_index) != self.pos_var.get():
                errors['Add pointer(pos)'] = "you can't add a pointer to a synset with different pos"
        return errors

    def validate_add_synset(self):
        words = [word.strip().lower() for word in self.words_text.get('1.0',END).split(';')]
        pointers =  self.pointers_list.get(0, END)
        gloss =  self.gloss_text.get('1.0',END).split()
        errors = {}
        if len(words[0]) == 0:
            errors['Words'] = ': you need to add at least 1 word'
        if len(pointers) == 0:
            errors['Pointers'] = ': you need to add at least 1 pointer'
        if len(gloss) == 0:
            errors['Gloss'] = ': you need to add the gloss'
        return errors

    def clear(self):
        self.words_text.delete('1.0',END)
        self.offset_entry.delete(0,END)
        self.offset_entry.insert(0,'0')
        self.pos_dropdown.current(0)
        self.pointers_list.delete(0,END)
        self.symbols_dropdown.current(0)
        self.sense_selector.clear()
        self.errors_var.set('') 
        self.success_var.set('')
        # print(self.offset_var.get())
    