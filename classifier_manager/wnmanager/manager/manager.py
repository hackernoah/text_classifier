import collections
import logging
from .utils import *
from .file_handler import *
from .validator import Validator

class WordnetManager():

    def __init__(self,dbfiles_root = 'wordnet\\', langwn_path = 'wordnet\\wn-data-ita.tab', senses_index_path = 'wordnet\\senses_disambiguation.json'):
        self.wndata = WordnetData()
        logging.basicConfig(filename='.\\classifier_manager\\wnmanager\\app.log', filemode='a',format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger()
        self.files_handler = WordnetFilesHandler(dbfiles_root, langwn_path,senses_index_path,self.wndata, self.logger)
        self.validator = Validator(self.wndata, self.logger)
        self.altered_pos = set()
        self.commands_history = []

    def open(self):
        self.files_handler.initialize()
        db_errros_len = len([error for prefix in self.wndata.db_errors for pos in self.wndata.db_errors[prefix] for error in self.wndata.db_errors[prefix][pos]])
        lang_errors_len = len([error for lemma in self.wndata.lang_errors for error in self.wndata.lang_errors[lemma]])
        print('Wordnet loaded with {} errors'.format(db_errros_len))
        print('Lang extension loaded with {} errors'.format(lang_errors_len))

    def add_word(self, word, pos, offset, lang='eng',from_synset= False, from_history = False):
        word = '_'.join(word.lower().split()) if lang == 'eng' else word.lower()
        errors = self.validator.validate_add_word(word,pos,offset,lang)
        if len(errors):
            return errors
        offset = int(offset)
        synset = self.wndata.synsets[pos][offset]
        if(lang == 'eng'):
            entry = self.wndata.lemmas[pos][word] if word in self.wndata.lemmas[pos] else None
            if(entry):
                entry.p_cnt += 1
                entry.sense_cnt += 1
                entry.offsets.append(offset)
            else:
                pointers = list({pointer[0] for pointer in synset.pointers if pointer[3] == '0000' })
                entry = IndexEntry(word,pos, 1, len(pointers), pointers, 1, 0, [offset])
            synset.words.append((entry.lemma,'0'))
            synset.w_cnt += 1
            self.wndata.lemmas[pos][word] = entry
        else:
            entry = LangEntry(offset,pos,lang,'lemma', word)
            if(word in self.wndata.lang_lemmas):
                self.wndata.lang_lemmas[word][offset] = entry
            else:
                self.wndata.lang_lemmas[word] = {}
                self.wndata.lang_lemmas[word][offset] = entry
        self.recalculate_offsets(pos)
        if not from_synset:
            self.altered_pos.add(pos)
            if not from_history:
                self.commands_history.append(self.get_add_word_command_string(word,pos,offset,lang))
            self.logger.info(f"Word <{word}> added succesfully in lang = {lang} to synset '{self.wndata.synsets[pos][offset].words[0][0]}' with offset {offset}")

    def add_synset(self,ss_type, words, pointers = [],gloss='', frames =[], from_history=False):
        pos = SSTYPE_TO_POS[ss_type]
        gloss = ' ' + gloss + '  \n'
        offset = len(''.join([str(self.wndata.synsets[pos][key]) for key in self.wndata.synsets[pos]]).encode('utf-8'))
        synset = None
        changed_pos = []
        errors = self.validator.validate_add_synset(ss_type, words, pointers, gloss)
        if len(errors):
            return errors
        if(ss_type == 'v'):
            synset = DataEntry(offset, '0', ss_type, 0,[],len(pointers),pointers,gloss, len(frames), frames)
        else:
            synset = DataEntry(offset, '0', ss_type, 0,[],len(pointers),pointers,gloss)
        self.wndata.synsets[pos][synset.offset] = synset
        for pointer in synset.pointers:
            if(pointer[0] in REFLEXIVE_POINTERS):
                reflexive_pointer = (REFLEXIVE_POINTERS[pointer[0]], synset.offset, pos, pointer[3])
                self.wndata.synsets[pointer[2]][pointer[1]].pointers.append(reflexive_pointer)
                self.wndata.synsets[pointer[2]][pointer[1]].p_cnt += 1
                changed_pos.append(pointer[2])
                self.recalculate_lemmas_pointers(pos,pointer[1],REFLEXIVE_POINTERS[pointer[0]])
        for word in words:
            self.add_word(word,pos,offset,from_synset=True)
        self.altered_pos.add(pos)
        if not from_history:
            self.commands_history.append(self.get_add_synset_command_string(ss_type,words,pointers,gloss,frames))
        self.logger.info(f"Synset added with word {words} and offset {offset}")
    

    def recalculate_lemmas_pointers(self, pos,offset, new_pointer):
        for key in self.wndata.lemmas[pos]:
            entry = self.wndata.lemmas[pos][key]
            if(entry.pos == pos and (offset in entry.offsets)):
                if(new_pointer not in entry.offsets):
                    entry.pointers.append(new_pointer)
                    entry.p_cnt += 1 


    def recalculate_offsets(self, pos):
        offset_counter = 1740
        changed_offsets = {}
        changed_offsets[pos] = {}
        for key in self.wndata.synsets[pos].copy():
            synset = self.wndata.synsets[pos].pop(key)
            entry_offset = len(str(synset).encode('utf-8'))
            if(synset.offset != offset_counter):
                changed_offsets[pos][key] = offset_counter
                synset.offset = offset_counter
            self.wndata.synsets[pos][offset_counter] = synset
            try:
                assert offset_counter in self.wndata.synsets[pos]
            except AssertionError:
                raise AssertionError("new offset: {} not added to synsets keys")
            offset_counter += entry_offset
        for p in POS_LIST:
            new_pointers = []
            for key in self.wndata.synsets[p]:
                if(SSTYPE_TO_POS[self.wndata.synsets[p][key].ss_type] == p):
                    for pointer in self.wndata.synsets[p][key].pointers:
                        if (pointer[1] in changed_offsets[pos]) and (pointer[2] == pos):
                            new_pointer = (pointer[0], changed_offsets[pos][pointer[1]],pointer[2], pointer[3])
                            new_pointers.append(new_pointer)
                            try:
                                assert new_pointer[1] in self.wndata.synsets[pointer[2]]
                            except AssertionError:
                                raise AssertionError("Offset: {} of synset pointer does not exist ".format(new_pointer[1]))
                        else:
                            new_pointers.append(pointer)
                self.wndata.synsets[p][key].pointers = new_pointers
                new_pointers = []
        new_offsets = []
        for key in self.wndata.lemmas[pos]:
            lemma = self.wndata.lemmas[pos][key]
            if(lemma.pos == pos):
                for offset in lemma.offsets:
                    new_offset = changed_offsets[pos][offset] if offset in changed_offsets[pos] else offset
                    new_offsets.append(new_offset)
                    try:
                        assert new_offset in self.wndata.synsets[pos]
                    except AssertionError:
                        raise AssertionError("offset: {} in lemma offsets does not exists")
            self.wndata.lemmas[pos][key].offsets = new_offsets
            new_offsets = []
        for lemma in self.wndata.lang_lemmas:
            for offset in self.wndata.lang_lemmas[lemma].copy():
                lang_entry = self.wndata.lang_lemmas[lemma].pop(offset)
                if (offset in changed_offsets[pos]) and (lang_entry.pos == pos):
                    lang_entry.offset = changed_offsets[pos][offset]
                self.wndata.lang_lemmas[lemma][lang_entry.offset] = lang_entry
                try:
                    assert lang_entry.offset in self.wndata.synsets[lang_entry.pos]
                except AssertionError:
                    raise AssertionError("there is no corresponding synset to the new offset: {}, of lang entry: {}. in CO: {}".format(lang_entry.offset,lang_entry.lemma, lang_entry.offset in changed_offsets[pos]))
    
    def get_senses(self, lemma,lang):
        senses = []
        if lang == 'eng':
            words = []
            for pos in self.wndata.lemmas:
                if lemma in self.wndata.lemmas[pos]:
                    words.append(self.wndata.lemmas[pos][lemma])
            for word in words:
                for offset in word.offsets:
                    senses.append(self.get_synset_and_hypernym(word.pos,offset))
        if lang == 'ita':
            lemma = ' '.join(lemma.split('_'))
            if lemma in self.wndata.lang_lemmas:
                for offset in self.wndata.lang_lemmas[lemma]:
                    entry = self.wndata.lang_lemmas[lemma][offset]
                    senses.append(self.get_synset_and_hypernym(entry.pos,offset)) 
        return senses

    def get_synset_and_hypernym(self, pos, offset):
        synset = self.wndata.synsets[pos][offset]
        hypernym_pointers = [pointer[1] for pointer in synset.pointers if pointer[0] == '@' and pointer[2] == pos]
        hypernym = self.wndata.synsets[pos][hypernym_pointers[0]] if len(hypernym_pointers) else None
        hypernym_name = hypernym.words[0][0] if hypernym else ''
        return hypernym_name, synset

    def get_sense_index(self, word):
        if word in self.wndata.senses_index:
            return self.wndata.senses_index[word]
        else:
            if is_number(word):
                return -1
            else:
                return 0
    
    def add_sense_disambiguation(self, word, index, from_history = False):
        word = word.lower()
        errors = self.validator.validate_add_sense_disambiguation(word,index)
        if(errors):
            return errors
        self.wndata.senses_index[word] = int(index) - 1
        if not from_history:
            self.commands_history.append(self.get_sense_disambiguation_add_command(word,index))
        self.logger.info(f"Sense disambiguation added for word '{word}' and sense index '{int(index) - 1}'")
   
    def commit_changes(self):
        self.files_handler.commit_changes(self.altered_pos, self.commands_history)
        self.altered_pos = set()
        self.commands_history = []
        self.logger.info(f"ALL CHANGES COMMITTED")

    def get_add_synset_command_string(self,ss_type, words, pointers = [],gloss='', frames =[]):
        new_pointers = []
        for pointer in pointers:
            new_pointers.append((pointer[0],self.get_offset_command_string(SSTYPE_TO_POS[ss_type],pointer[1]), pointer[2], pointer[3]))
        command_string = "wm.add_synset('{}', {}, ".format(ss_type, words)
        command_string += "[ "
        for i in range(len(new_pointers)):
            s,o,p,t = new_pointers[i]
            if i > 0:
                command_string += ', '
            command_string += "('{}', {}, '{}', '{}')".format(s,o,p,t) 
        command_string += "], "
        command_string += "'{}' ".format(gloss.strip())
        if len(frames):
            command_string += ", {}".format(frames)
        command_string += ", from_history = True)"
        return command_string

    def get_add_word_command_string(self, words, pos, offset, lang):
        command_string = "wm.add_word('{}', '{}', {}, lang='{}', from_history = True)".format(words,pos,self.get_offset_command_string(pos,offset),lang)
        return command_string
    
    def get_sense_disambiguation_add_command(self, word, index):
        command = "wm.add_sense_disambiguation('{}', {}, from_history = True)".format(word, index)
        return command

    def get_offset_command_string(self,pos,offset):
        reference_word = self.wndata.synsets[pos][offset].words[0][0]
        offset_index = self.wndata.lemmas[pos][reference_word].offsets.index(offset)
        offset_command_string = "wm.wndata.lemmas['{}']['{}'].offsets[{}]".format(pos,reference_word,offset_index)
        return offset_command_string

    def get_commands_history(self):
        return self.commands_history



    # def check_if_lang_offsets_updated(self):
    #     for lemma in self.wndata.lang_lemmas:
    #         for offset in self.wndata.lang_lemmas[lemma]:
    #             entry = self.wndata.lang_lemmas[lemma][offset]
    #             if offset not in self.wndata.synsets[entry.pos]:
    #                 return False
    #             if entry.offset not in self.wndata.synsets[entry.pos]:
    #                 return False
    #     return True
