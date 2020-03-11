from tokenizer import *
from transformers import AutoTokenizer, TFAutoModel
import ktrain 
from ktrain import text
from ktrain.text.learner import TransformerTextClassLearner
import random
from dataset_manager import read_xlsx

traduction = {
    'A' : 0,
    'B' : 1,
    'C' : 2,
    'D' : 3,
    'E' : 4,
    'F' : 5,
    'G' : 6,
    0 : 'A',
    1 : 'B',
    2 : 'C',
    3 : 'D',
    4 : 'E',
    5 : 'F',
    6 : 'G'
}

def split_set(dataset, test_length):
    indexes = []
    test =  []
    train = []
    for i in range(test_length):
        new = False
        while(not new):
            r = random.randint(0, len(dataset))
            if r not in indexes:            
                new = True
                indexes.append(r)
    for i in range(len(dataset)):
        if i in indexes:
            test.append(dataset[i])
        else:
            train.append(dataset[i])
    if len(test) == 0:
        test.append(train.pop(0))
    return test,train

def group_for_label(records):
    grouping = {}
    for d,l in records:
        if l not in grouping:
            grouping[l] = [(d,l)]
        else:
            grouping[l].append((d,l))
    return grouping

def print_grouping(grouping, label):
    print(f'{label} grouping:')
    for l in grouping:
        length = len(grouping[l])
        print(f'{l}: {length}')



descriptions, items = read_xlsx("LDC.xlsx", "LDC",1)
records = [ (descriptions[i], items[i]) for i in range(len(descriptions))]

grouping = group_for_label(records)

test = []
train = []

for l in grouping:
    length = len(grouping[l])//4
    if l not in ['A','C']:
        usable, spared = split_set(grouping[l], length)
    else:
        usable = grouping[l]
    tmp_test, tmp_train = split_set(usable, len(usable)//5)
    test.extend(tmp_test)
    train.extend(tmp_train)

test_grouping = group_for_label(test)
train_grouping = group_for_label(train)

a = AlBERTo_Preprocessing(do_lower_case=True)


tok = AutoTokenizer.from_pretrained("saved_models/bert_uncased_L-12_H-768_A-12_italian_alb3rt0/vocab.txt")

kargs = {
    'config' : "saved_models/bert_uncased_L-12_H-768_A-12_italian_alb3rt0/config.json"
}
model = TFAutoModel.from_pretrained("saved_models/bert_uncased_L-12_H-768_A-12_italian_alb3rt0/tf_model.h5", **kargs)
print(type(model))
x_train = np.array([tok.tokenize(a.preprocess(d)) for d,l in train])
y_train = np.array([traduction[l] for d,l in train])
x_test = np.array([tok.tokenize(a.preprocess(d)) for d,l in test])
y_test = np.array([traduction[l] for d,l in test])


# learner = ktrain.get_learner(model, train_data=(x_train,y_train), val_data=(x_test, y_test), batch_size=8)

