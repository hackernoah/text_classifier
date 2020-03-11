import json
import sys
import os
import types
import joblib
import classifier_manager.model_interface.dataset_provider as dm
from classifier_manager.model_interface.models import * 


class ModelInterface():

    def __init__(self, model_name, path='LDC.xlsx', sheet_name = 'LDC', level=1):
        MLAlgo= types.new_class(model_name).__class__
        desc, labels = dm.read_xlsx(path, sheet_name, level)
        self.path = path
        self.tax_dict = {}
        args = (desc,labels,9)
        self.model = MLAlgo.__init__(*args)

    
    def evaluate_model(self):
        results = self.model.kfold_cross_validation("kfold_export.xlsx")
        return results
        
    def save_model(self):
        self.model.save('saved_models\\')
        d = dm.read_taxonomies(self.path,'EType',7)
        with open('saved_models\\taxonomies_dictionary.json','w') as td:
            json.dump(d, td)

    
    def load_model(self):
        cd = os. getcwd()
        self.model.load(cd)
        with open(cd + "\\taxonomies_dictionary.json", 'r') as j:
            self.tax_dict = json.load(j)
    
    def predict(self, text, bank):
        prediction = self.model.predict(text)
        return self.tax_dict[prediction][bank]