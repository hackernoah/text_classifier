from collections import OrderedDict

class IndexEntry():

    def __init__(self, lemma, pos, synset_cnt, p_cnt, pointers, sense_cnt, tagsense_cnt, offsets):
        self.lemma = lemma
        self.pos = pos
        self.synset_cnt = synset_cnt
        self.p_cnt = p_cnt
        self.pointers = pointers
        self.sense_cnt = sense_cnt
        self.tagsense_cnt = tagsense_cnt
        self.offsets = offsets

    def __str__(self):
        output = ""
        output += self.lemma + " "
        output += self.pos + " "
        output += str(self.synset_cnt) + " "
        output += str(self.p_cnt) + " "
        output +=' '.join(self.pointers)
        if(self.p_cnt):
            output += ' '
        output += str(self.sense_cnt) + " "
        output += str(self.tagsense_cnt) + " "
        output += " ".join([str(offset).zfill(8) for offset in self.offsets])
        output += "  \n"
        return output
    
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return str(self) == str(other)
    
class DataEntry():

    def __init__(self, offset, lex_filenum, ss_type, w_cnt, words, p_cnt, pointers, gloss, f_cnt = None, frames = None):
        self.offset = offset
        self.lex_filenum = lex_filenum
        self.ss_type = ss_type
        self.w_cnt = w_cnt
        self.words = words
        self.p_cnt = p_cnt
        self.pointers = pointers
        self.f_cnt = f_cnt
        self.frames = frames
        self.gloss = gloss

    def __str__(self):
        output = ""
        output += str(self.offset).zfill(8) + " "
        output += self.lex_filenum.zfill(2) + " "
        output += self.ss_type + " "
        output += str(hex(self.w_cnt)).replace('0x','').zfill(2) + " "
        output += ' '.join([ e for word in self.words for e in word]) + " "
        output += str(self.p_cnt).zfill(3) + " " 
        pointers_output = []
        for pointer in self.pointers:
            pointers_output.append((pointer[0], str(pointer[1]).zfill(8), pointer[2], pointer[3]))
        output += ' '.join([e for pointer in pointers_output for e in pointer])
        if(len(self.pointers)):
            output += ' '
        if(self.ss_type == 'v'):
            output += str(self.f_cnt).zfill(2) + " "
            frames_output = []
            for frame in self.frames:
                frames_output.append((frame[0],str(frame[1]).zfill(2),str(hex(frame[2])).replace('0x','').zfill(2)))
            output += " ".join([f for frame in frames_output for f in frame]) + " "
        output += "|" + self.gloss
        return output
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return str(self) == str(other)

class LangEntry():

    def __init__(self ,offset, pos, lang, entry_type, lemma):
        self.offset = offset
        self.pos = pos
        self.lang = lang
        self.entry_type = entry_type
        self.lemma = lemma

    def __str__(self):
        output = ''
        output += str(self.offset).zfill(8) + '-'
        output += self.pos + '\t'
        output += self.lang + ':'
        output += self.entry_type + '\t'
        output += self.lemma
        return output + '\n'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return str(self) == str(other)

class WordnetData():
    def __init__(self):
        self.lang_lemmas = OrderedDict()
        self.lemmas = {
            'n': OrderedDict(),
            'a': OrderedDict(),
            'v': OrderedDict(),
            'r': OrderedDict()
        }
        self.synsets = {
            'n': OrderedDict(),
            'a': OrderedDict(),
            'v': OrderedDict(),
            'r': OrderedDict()
        }
        self.senses_index = {}
        self.db_errors = {
            'index': {
                'n': {},
                'a': {},
                'v': {},
                'r': {},
            },
            'data': {
                'n': {},
                'a': {},
                'v': {},
                'r': {},
            },
        }
        self.lang_errors = {}

class Lemma:
    
    def __init__(self, lemma, synset):
        self.lemma = lemma
        self.synset = synset
    
    def __str__(self):
        output = 'Lemma({})'.format(self.synset.name + '.' + self.lemma)
        return output
    
    def __repr__(self):
        return str(self)

class Synset:
    
    def __init__(self, sense):
        sense_word = sense.words[0]
        self.pos = sense.ss_type
        self.word = sense_word[0]
        self.number = sense_word[1]
    
    def name(self):
        return self.word + self.pos + self.number
    
    def __str__(self):
        output = 'Sysnset({})'.format(self.name())
        return output
    
    def __repr__(self):
        return str(self)

class WNManagerError(Exception):
    """class to handle errors """


def is_number(word):
    try:
        int(word)
        return True
    except ValueError:
        return False

FILES = [
'data.noun',
'data.adj',
'data.verb',
'data.adv',
'index.noun',
'index.adj',
'index.verb',
'index.adv'
]

POS_TO_FILE = {
'n' : {
    'index' : 'index.noun',
    'data' : 'data.noun'
},
'a' : {
    'index' : 'index.adj',
    'data' : 'data.adj',
},
'v' : {
    'index' : 'index.verb',
    'data' : 'data.verb',
},
'r' : {
    'index' : 'index.adv',
    'data' : 'data.adv',
}
}
POS_LIST = ['n','v','a','r']

SSTYPE_TO_POS = {
'n' : 'n',
'v' : 'v',
'r' : 'r',
's' : 'a',
'a' : 'a'
}

PREFIX = """  1 This software and database is being provided to you, the LICENSEE, by  
  2 Princeton University under the following license.  By obtaining, using  
  3 and/or copying this software and database, you agree that you have  
  4 read, understood, and will comply with these terms and conditions.:  
  5   
  6 Permission to use, copy, modify and distribute this software and  
  7 database and its documentation for any purpose and without fee or  
  8 royalty is hereby granted, provided that you agree to comply with  
  9 the following copyright notice and statements, including the disclaimer,  
  10 and that the same appear on ALL copies of the software, database and  
  11 documentation, including modifications that you make for internal  
  12 use or for distribution.  
  13   
  14 WordNet 3.0 Copyright 2006 by Princeton University.  All rights reserved.  
  15   
  16 THIS SOFTWARE AND DATABASE IS PROVIDED "AS IS" AND PRINCETON  
  17 UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR  
  18 IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PRINCETON  
  19 UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT-  
  20 ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE  
  21 OF THE LICENSED SOFTWARE, DATABASE OR DOCUMENTATION WILL NOT  
  22 INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR  
  23 OTHER RIGHTS.  
  24   
  25 The name of Princeton University or Princeton may not be used in  
  26 advertising or publicity pertaining to distribution of the software  
  27 and/or database.  Title to copyright in this software, database and  
  28 any associated documentation shall at all times remain with  
  29 Princeton University and LICENSEE agrees to preserve same.  
"""
LANG_PREFIX = "# MultiWordNet	ita	http://multiwordnet.fbk.eu/english/home.php	CC BY 3.0 \n"
ALLOWED_POINTERS ={
'n' : ['!','@','@i','~','~i','#m','#s','#p','%m','%s','%p','=','+',';c','-c',';r','-r',';u','-u'],
'a' : ['!','@','~','*','>','^','$','+',';c',';r',';u'],
'v' : ['!','&','<','\\','=','^',';c',';r',';u'],
'r' : ['!','\\',';c',';r',';u'],
'all' : ['!','@','@i','~','~i','#m','#s','#p','%m','%s','%p','=','+',';c','-c',';r','-r',';u','-u','*','>','^','$','&','<','\\']
}
REFLEXIVE_POINTERS = {
'!' : '!',
'~' : '@',
'@' : '~',
'~i' : '@i',
'@i' : '~i',
'&' : '&',
'=' : '=',
'$' : '$',
'+' : '+',
'#m' : '%m',
'#s': '%s',
'#p':'%p',
'%m' : '#m',
'%s': '#s',
'%p':'#p',
';c':'-c',
';r':'-r',
';u':'-u',
'-c':';c',
'-r':';r',
'-u':';u'}