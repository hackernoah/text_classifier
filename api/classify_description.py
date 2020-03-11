import sys
from models.svm import SVMClassifier
from dataset_manager import read_xlsx,read_xlsx1
import joblib
import json


desc =  "usura" if sys.gettrace() else sys.argv[1]
bank = "Sparkasse" if sys.gettrace() else sys.argv[2]

svm = joblib.load("C:\\Users\\don\\Documents\\Python\\ET-classifier\\saved_models\\svm")
vectorizer = joblib.load("C:\\Users\\don\\Documents\\Python\\ET-classifier\\saved_models\\vectorizer")
with open("C:\\Users\\don\\Documents\\Python\\ET-classifier\\saved_models\\translation_dictionary.json", 'r') as j:
    traduction = json.load(j)
with open("C:\\Users\\don\\Documents\\Python\\ET-classifier\\saved_models\\taxonomies_dictionary.json", 'r') as j:
    tax_dict = json.load(j)
prova_tfidf = vectorizer.transform([desc])
prediction = svm.predict(prova_tfidf)
print("{}".format(tax_dict[traduction[prediction[0]]][bank]), end="")