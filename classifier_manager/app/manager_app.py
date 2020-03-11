from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from .add_synset_component import AddSynsetComponent
from .add_word_component import AddWordComponent
from .tagger_component import TaggerComponent
from .manager_controller import ManagerController
from .model_component import ModelComponent

# from tkinter.ttk import *

#crea

class WordnetManagerGui:
    def __init__(self, root):
        self.controller = ManagerController()
        self.root = root
        self.root.title('Wordnet Manager')
        self.root.geometry('1920x600')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.content = ttk.Frame(self.root)
        self.content.grid(row = 0, column = 0)
        self.work_env_frame = ttk.Frame(self.content)
        self.work_env_frame.grid(row = 0, column = 0, rowspan=10, columnspan=20)
        self.work_env = ttk.Notebook(self.work_env_frame)
        self.add_word_tab = ttk.Frame(self.work_env,name="word") 
        self.add_word_tab.grid(row=1,column=0, rowspan=10, columnspan=20)
        self.add_synset_tab = ttk.Frame(self.work_env, name ="synset")  
        self.add_synset_tab.grid(row=1,column=0, rowspan=10, columnspan=20)
        self.tagger_tab = ttk.Frame(self.work_env, name = "tagger")
        self.tagger_tab.grid(row=1,column=0, rowspan=10, columnspan=20)
        self.model_tab = ttk.Frame(self.work_env, name = "model")
        self.model_tab.grid(row=1,column=0, rowspan=10, columnspan=20)
        self.work_env.add(self.add_word_tab, text=' Word')
        self.work_env.add(self.add_synset_tab, text='Synset')
        self.work_env.add(self.tagger_tab, text='Tagger')
        self.work_env.add(self.model_tab, text='Model')
        self.work_env.grid(row=1,column=0,rowspan=10, columnspan=20)
        self.add_word_component = AddWordComponent(self.add_word_tab,self.controller)
        self.add_synset_component = AddSynsetComponent(self.add_synset_tab,self.controller)
        self.tagger_component = TaggerComponent(self.tagger_tab,self.controller)
        self.model_comonent = ModelComponent(self.model_tab,self.controller)
        self.work_env.bind('<<NotebookTabChanged>>',self.change_tab)
        self.save_btn = ttk.Button(self.content,text='Save',command = self.save)
        self.save_btn.grid(row=10,column = 0, sticky='W')
    
    def change_tab(self,event):
        self.add_word_component.clear()
        self.add_synset_component.clear()
        self.controller.reset()
    
    def save(self):
        self.controller.save()
    
    def on_closing(self):
        unsaved_changes = self.controller.unsaved_changes()
        if unsaved_changes:
            result = messagebox.askyesnocancel("Quit", "You have {} unsaved changes. Do you want to save them?".format(unsaved_changes))
            if  result == True:
                self.save()
                self.root.destroy()
            elif result == False:
                self.root.destroy()
            else:
                pass
        else:
            self.root.destroy()


#esegue
root = Tk()
root_gui = WordnetManagerGui(root)
root.mainloop()
