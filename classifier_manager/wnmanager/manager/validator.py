from .utils import ALLOWED_POINTERS,is_number,WNManagerError

class Validator:

    def __init__(self, wndata, logger):
        self.wndata = wndata
        self.logger = logger

    def validate_add_word(self, word, pos, offset, lang):
        errors = {}
        if pos not in ['n','v','a','r']:
            self.raise_error('Pos', f'{pos} is an invalid pos', errors)
        if not is_number(offset):
            self.raise_error('Offset value', f'offset {offset} must be a number', errors )
        else:
            offset = int(offset)
            if offset not in self.wndata.synsets[pos]:
                self.raise_error('Synset', f"offset {offset} doesn't exists", errors)
            if  word in self.wndata.lang_lemmas and lang == 'ita':
                if offset in self.wndata.lang_lemmas[word]:
                    self.raise_error("Word", f"connection for word '{word}' to core synset '{self.wndata.synsets[pos][offset].words[0][0]}' already exists", errors)
            if word in self.wndata.lemmas and lang == 'eng':
                if offset in self.wndata.lemmas[word].offsets:
                    self.raise_error("Word", f"connection for word '{word}' to core synset '{self.wndata.synsets[pos][offset].words[0][0]}' already exists", errors)
        if lang not in ['ita','eng']:
            self.raise_error('Language', "the only supported languages are ita and english",errors)
        if len(word) < 1:
            self.raise_error('Word value', "word must be at least 1 character long", errors)
        if word in self.wndata.lemmas[pos] and lang == 'eng':
            self.raise_error('Word', f"word {word} already exists in wordnet core", errors)
        return errors

    def raise_error(self,key, string, errors):
        try:
            raise WNManagerError(string)
        except WNManagerError as e:
            errors[key] = ": {}".format(str(e))
            self.logger.exception("Exception occurred")

    def validate_add_synset(self, ss_type, words, pointers, gloss):
        errors = {}
        if ss_type not in ['n','v','a','r']:
            self.raise_error('Pos', f'{ss_type} is an invalid synset type', errors)
        if(len(words) == 0):
            self.raise_error('Words', 'at least 1 word needs to be added to the synset', errors)
        if len(pointers) == 0:
            self.raise_error('Pointers', 'at least one pointer', errors)
        for pointer in pointers:
            if(pointer[0] not in ALLOWED_POINTERS['all']):
                self.raise_error('Pointer(symbol)', f'{pointer[0]} is not a valid pointer'.format(pointer[0]), errors)
            if pointer[2] != ss_type:
                self.raise_error('Pointer(pos)', '{} synset type and {} pointer type are different'.format(ss_type, pointer[2]), errors)
        if len(gloss.split()) == 0:
            self.raise_error('Gloss', 'synset needs a definition', errors)
        return errors
    
    def validate_add_sense_disambiguation(self,word,index):
        errors = {}
        if not is_number(index):
            self.raise_error('Index(type)', 'index must be an integer', errors)
        if word not in self.wndata.lang_lemmas:
            self.raise_error('Word', f'word {word} not present in lang extension', errors)
        elif is_number(index):
            word_senses_len = len(self.wndata.lang_lemmas[word].keys()) 
            if int(index) - 1 >= word_senses_len:
                self.raise_error('Index(value)', f"index ({index}) for selected word exceeds it's sense list length ({word_senses_len})", errors)
        return errors
