import nltk
from nltk.metrics import precision,recall
from pprint import pprint
import random


class BayesClassifier:
    
    records = []
    train_set = []
    test_set = []
    featuresets = []
    all_words = []
    distribution = []
    meaningful_words = []

    def __init__(self):
        self.records = []
        
    def PopulateRecords(self, descriptions, items):
        self.records = []
        for i in range(len(items)):
            item = items[i]
            desc = descriptions[i]
            if( isinstance(item, str) and isinstance(desc, str) and (desc != None) and (item != None)):
                self.records.append((desc,item))
        self.all_words = [word for record in self.records for word in record[0]]
        self.distribution = nltk.FreqDist(w for w in self.all_words)
        self.meaningful_words = list(set([word for word in self.all_words if self.distribution[word] > 2]))

    def description_features(self, description):
        description_words = set(description)
        features = {}
        for word in self.meaningful_words:
            features['contains({})'.format(word)] = (word in description_words)
        return features


    # def labels_count_for_test_set (self, complete_set, test_length):
    #     total = 0
    #     values = []
    #     labels_count = dict()
    #     dist = nltk.FreqDist([l for (f,l) in complete_set])
    #     for key in dist:
    #         total = total + dist[key]
    #         values.append((key,dist[key]))
    #     for value in values:
    #         labels_count[value[0]] = round((value[1]/total)*test_length)
    #     return labels_count


    def create_sets(self, test_length):
        self.featuresets = [(self.description_features(d), et) for (d,et) in self.records]
        original = self.featuresets.copy()
        random.shuffle(original)
        self.train_set = original[test_length:]
        self.test_set = original[:test_length]

    def CreateClassifier(self, test_set_length):
        print("Records: ", len(self.records))
        print(self.records)
        print("with {} labels".format(len(set([record[1] for record in self.records]))))
        self.create_sets(test_set_length)
        print("Trainining set: ",len(self.train_set))
        print("with {} labels".format(len(set([record[1] for record in self.train_set]))))
        print("Test set: ", len(self.test_set))
        print("with {} labels".format(len(set([record[1] for record in self.test_set]))))
        classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        return classifier

    def PrintAccuracy(self, classifier):
        print(nltk.classify.accuracy(classifier, self.test_set))
    
    def PrintConfusionMatrix(self, classifier):
        cm = nltk.ConfusionMatrix([l for (f,l) in self.test_set], classifier.classify_many([f for (f,l) in self.test_set]))
        print(cm.pretty_format(sort_by_count=True, show_percents=True))

    # def PrintPrecisionRecall(self, classifier):
    #     p = precision ([l for (f,l) in self.test_set], classifier.classify_many([f for (f,l) in self.test_set]))
    #     r =  recall([l for (f,l) in self.test_set], classifier.classify_many([f for (f,l) in self.test_set]))
    #     print("precision: ", p)
    #     print("recall: ", r)


#get all syns of lemmas of all syns in synset
# for syn in wn.synsets('floema', lang="ita"):
# 	for lemma in syn.lemma_names('ita'):
# 		for sin in wn.synsets(lemma, lang = 'ita'):
# 			for lemma1 in sin.lemma_names('ita'):
# 				syns.append(lemma1)