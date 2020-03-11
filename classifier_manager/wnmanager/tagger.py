import string

class Tagger:

    def __init__(self, manager):
        self.manager = manager
    
    def get_tag(self, sense):
        word = sense.words[0]
        tag = word[0] + sense.ss_type + word[1]
        return tag

    def tag_text(self, text, n = 1, keep = True):
        text = text.translate(str.maketrans(string.punctuation,''.join([" " for i in range(len(string.punctuation))]))).split()
        tagged_text = []
        i = 0
        while i < len(text):
            sense = None
            j = n
            while j > 0:
                if(sense is None):
                    words = text[i:i+j]
                    ngram = '_'.join(words).lower()
                    senses = [sense[1] for sense in self.manager.get_senses(ngram, lang = 'ita')]
                    sense_index = self.manager.get_sense_index(ngram)
                    if len(senses) and sense_index >= 0 :
                        sense = senses[sense_index]
                        i += j - 1
                        j = 0
                    else:
                        j -= 1
            if(sense):
                sense_word = sense.words[0]
                tag = sense_word[0] + sense.ss_type + sense_word[1]
                tagged_text.append(tag)
            elif(keep):
                tagged_text.append(text[i])
            i += 1
        return tagged_text
    
    def tag_list(self, corpus, n = 1, keep = True):
        tagged_list = []
        for text in corpus:
            tagged_list.append(self.tag_text(text))
        return tagged_list
