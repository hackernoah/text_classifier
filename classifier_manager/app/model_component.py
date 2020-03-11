from tkinter import *
from tkinter import ttk
from .synset_selector_component import SynsetSelectorComponent

class ModelComponent:

    def __init__(self,parent,controller):
        self.controller = controller
        self.parent = parent
        self.config_frame = LabelFrame(self.parent,text='Configuration',font=('Arial', 12, 'bold'))
        self.config_frame.grid(row=0,column=0,rowspan=2,columnspan=4, sticky = 'w')
        self.use_frame = LabelFrame(self.parent,text='Usage parameters',font=('Arial', 12, 'bold'))
        self.use_frame.grid(row=3,column=0,rowspan=2,columnspan=4, sticky='w')
        #algo
        self.name_var = StringVar()
        self.name_label = Label(self.config_frame, text='Algorithm', font=('Arial', 12, 'normal'), pady=20, padx=20)
        self.name_label.grid(row=0,column=0,sticky='we')
        self.name_dropdown = ttk.Combobox(self.config_frame, textvariable=self.name_var, state='readonly',width=10)
        self.name_dropdown.grid(row= 0,column =1)
        self.name_dropdown['values']=('Support Vector Machine','Random Classifier','Naive Bayes')
        self.name_dropdown.current(0)
        #level
        self.level_var = StringVar()
        self.level_label = Label(self.config_frame, text='Level', font=('Arial', 12, 'normal'), padx=20)
        self.level_label.grid(row=0,column=2, sticky='we')
        self.level_dropdown = ttk.Combobox(self.config_frame, textvariable=self.level_var, state='readonly',width=10)
        self.level_dropdown.grid(row= 0,column =3)
        self.level_dropdown['values']=('1','2','3')
        self.level_dropdown.current(0)
        # self.kfold_dropdown.bind('<<ComboboxSelected>>')
        #config buttons
        self.config_buttons_frame = ttk.Frame(self.parent)
        self.config_buttons_frame.grid(row=2, column = 0, sticky = 'W')
        self.create_btn = ttk.Button(self.config_buttons_frame,text='Create', command = self.create_model )
        self.create_btn.grid(row=0,column = 0, sticky='W')
        #preprocess
        self.preprocess_var = StringVar()
        self.preprocess_label = Label(self.use_frame, text='Preprocess', font=('Arial', 12, 'normal'), padx=20)
        self.preprocess_label.grid(row=1,column=0, sticky=W)
        self.preprocess_dropdown = ttk.Combobox(self.use_frame, textvariable=self.preprocess_var, state='readonly',width=8)
        self.preprocess_dropdown.grid(row= 1,column =1)
        self.preprocess_dropdown['values']=('yes','no')
        self.preprocess_dropdown.current(0)
        #keep only wordnet
        self.wordnet_var = StringVar()
        self.wordnet_label = Label(self.use_frame, text='Wordnet only', font=('Arial', 12, 'normal'), pady=20, padx=20)
        self.wordnet_label.grid(row=1,column=2,sticky='we')
        self.wordnet_dropdown = ttk.Combobox(self.use_frame, textvariable=self.preprocess_var, state='readonly',width=8)
        self.wordnet_dropdown.grid(row= 1,column = 3)
        self.wordnet_dropdown['values']=('yes','no')
        self.wordnet_dropdown.current(0)
        #usage buttons
        self.usage_buttons_frame = ttk.Frame(self.parent)
        self.usage_buttons_frame.grid(row=5, column = 0, sticky = 'W')
        self.evaluate_btn = ttk.Button(self.usage_buttons_frame,text='Evaluate' )
        self.evaluate_btn.grid(row=0,column = 0, sticky='W')
        self.save_model_btn = ttk.Button(self.usage_buttons_frame,text='Save Model' )
        self.save_model_btn.grid(row=0,column = 1,sticky='W')
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

    def create_model(self):
        name = self.name_var.get()
        level = int(self.level_var.get())
        self.controller.create_model(name, level)