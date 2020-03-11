from ..wnmanager.manager import WordnetManager
from ..wnmanager.tagger import Tagger
from ..model_interface import ModelInterface

class ManagerController:

    POS_TRANSLATION = {
        'noun':'n',
        'verb':'v',
        'adjective':'a',
        'adverb':'r',
        'n':'noun',
        'v':'verb',
        'a':'adjective',
        'r':'adverb',
        's':'adjective'
    }

    MODEL_NAMES = {
        'Support Vector Machine' : 'SVMClassifier'
    }

    def __init__(self):
        self.manager = WordnetManager()
        self.model = None
        self.manager.open()
        self.tagger = Tagger(self.manager)
        self.senses = []
        self.hypernyms = []

    def add_word(self, word, pos, offset, lang):
        return self.manager.add_word(word,self.POS_TRANSLATION[pos],offset,lang)

    def add_synset(self, ss_type, words, pointers, gloss):
        gloss = gloss.strip()
        pointers = [(pointer[0], int(pointer[1]),self.POS_TRANSLATION[pointer[2]], pointer[3]) for pointer in pointers]
        return self.manager.add_synset(self.POS_TRANSLATION[ss_type], words, pointers, gloss)

    def search_senses(self, lemma, lang):
        results = self.manager.get_senses(lemma,lang)
        self.senses = [result[1] for result in results]
        senses_display = []
        senses_offsets = []
        for hyp,sense in results:
            prefix = '(' + hyp + ') ' if hyp else ''
            senses_display.append(prefix + lemma + '(' + sense.ss_type + '): ' + sense.gloss)
            senses_offsets.append(sense.offset)
        return senses_display,senses_offsets
    
    def add_sense_disambiguation(self, word, index):
        return self.manager.add_sense_disambiguation(word,index)

    def get_sense_pos(self, index):
        return self.POS_TRANSLATION[self.senses[index].ss_type]

    def tag_text(self, text, n):
        tags = self.tagger.tag_text(text,n=int(n))
        return tags

    def has_searched(self):
        flag = True if len(self.senses) else False
        return flag
    

    def save(self):
        self.manager.commit_changes()

    def reset(self):
        self.senses = []
    
    def unsaved_changes(self):
        history = self.manager.get_commands_history()
        return len(history)
    
    def create_model(self, name, level):
        self.model = ModelInterface(self.MODEL_NAMES[name], level = level)
