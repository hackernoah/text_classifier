from dataset_manager import read_xlsx,read_xlsx1
import random
import numpy as np
import tensorflow
import ktrain
from ktrain import text 
from ktrain.text.preprocessor import TransformerSequence

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

# print_grouping(test_grouping, 'TEST')
# print(f'TEST: {len(set([l for d,l in test]))}')
# # print_grouping(train_grouping, 'TRAIN')
# print(f'TRAIN: {len(set([l for d,l in train]))}')

x_train = np.array([d for d,l in train])
y_train = np.array([traduction[l] for d,l in train])
x_test = np.array([d for d,l in test])
y_test = np.array([traduction[l] for d,l in test])

print(f'TEST: {len(set( y_test))}')
print(f'TRAIN: {len(set(y_train))}')


t = text.Transformer('bert-base-multilingual-cased', maxlen=500, classes= list(set(y_train)), multilabel=True)

trn = t.preprocess_train(x_train, y_train)
val = t.preprocess_test(x_test, y_test)

model = t.get_classifier()
print(type(model))
learner = ktrain.get_learner(model, train_data=val, val_data= trn, batch_size=8)
print(type(learner))

# learner.fit_onecycle(5e-5, 4)



    
                
                
            