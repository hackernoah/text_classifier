import collections
from .utils import *
import json

class WordnetFilesHandler():

    def __init__(self,dbfiles_root, langwn_path, senses_disambiguation_path, wndata, logger):
        self.dbfiles_root = dbfiles_root
        self.langwn_path = langwn_path
        self.senses_disambiguation_path = senses_disambiguation_path
        self.wndata = wndata
        self.logger = logger

    def initialize(self):
        for file in FILES:
            try:
                self.read_db_file(file)
                self.logger.info(f'FILEHANDLER - dbfile {file} loaded  ')
            except FileNotFoundError:
                self.logger.warning(f'FILEHANDLER - dbfile {file} not found  ')
                pass
        try:
            self.read_lang_file(self.langwn_path)
            self.logger.info(f'FILEHANDLER - lang file {file} loaded  ')
        except FileNotFoundError:
            self.logger.warning(f'FILEHANDLER - lang file {file} not found  ')
            pass
        try:
            self.read_sense_index_file(self.senses_disambiguation_path)
            self.logger.info(f'FILEHANDLER - sense disambiguation file loaded  ')
        except FileNotFoundError:
            self.logger.warning(f'FILEHANDLER - sense disambiguation file not found  ')
            pass

    def read_db_file(self,filename):
        with open(self.dbfiles_root + filename, 'r') as dbfile:
            index_line_count = 30
            data_line_count = 30
            for i in range(29):
                dbfile.readline()
            for line in dbfile:
                try:
                    if('index' in filename):
                        entry = self.to_index_entry(line)
                        key = entry.lemma
                        pos = entry.pos
                        self.wndata.lemmas[pos][key] = entry
                        if(line != str(self.wndata.lemmas[pos][key])):
                            self.wndata.db_errors['index'][pos][key] = str(self.wndata.lemmas[pos][key])
                        index_line_count += 1
                    else:
                        entry = self.to_data_entry(line.split('|'))
                        key = entry.offset
                        pos = SSTYPE_TO_POS[entry.ss_type]
                        self.wndata.synsets[pos][key] = entry
                        if(line != str(self.wndata.synsets[pos][key])):
                            self.wndata.db_errors['data'][pos][key] = str(self.wndata.synsets[pos][key])
                        data_line_count += 1
                except (IndexError,ValueError) as e:
                    count = index_line_count if 'index' in filename else data_line_count
                    tup = filename, count, e
                    raise WNManagerError('file %s, line %i: %s' % tup) from e
            dbfile.close()

    def read_lang_file(self, filename):
        with open(filename, 'r') as lang_file:
            count = 0
            words = []
            lang_file.readline()
            for line in lang_file:
                entry = self.to_lang_entry(line)
                key = entry.lemma
                if key in self.wndata.lang_lemmas:
                    self.wndata.lang_lemmas[key][entry.offset] = entry
                else:
                    self.wndata.lang_lemmas[key] = {}
                    self.wndata.lang_lemmas[key][entry.offset] = entry
                if(line != str(entry)):
                    if key in self.wndata.lang_errors:
                        self.wndata.lang_errors[key][entry.offset] = str(entry)
                    else:
                        self.wndata.lang_errors[key] = {}
                        self.wndata.lang_errors[key][entry.offset] = str(entry)
                count += 1
                words.append(key)
    
    def read_sense_index_file(self, filename):
        with open(filename,'r') as ws:
            self.wndata.senses_index = json.load(ws)
    
    def to_data_entry(self, line):
        params = line[0].split()
        # print(params)
        w_cnt = int(params[3],16)
        p_cnt = int(params[ 4 + 2 * w_cnt])
        ss_type = params[2]
        words = [(params[4 + i], params[5+i]) for i in range(0,2*w_cnt, 2) ] if w_cnt > 0 else []
        pointers = [(params[5 + 2*w_cnt + i],int(params[6 + 2*w_cnt + i]),params[7 + 2*w_cnt+i],params[8 + 2*w_cnt+i]) for i in range(0,p_cnt*4,4) ] if p_cnt > 0 else []
        if(ss_type == 'v'):
            frames = []
            start = 5 + (2*w_cnt) + (4*p_cnt)
            fcnt= int(params[start])
            frames = [(params[start+i],int(params[start+i+1]),int(params[start+i+2],16)) for i in range(1,fcnt*3,3)]
            return DataEntry(int(params[0]),params[1], ss_type, w_cnt, words, p_cnt, pointers,line[1], fcnt, frames)
        else:
            return DataEntry(int(params[0]),params[1], ss_type, w_cnt, words, p_cnt, pointers, line[1])

    def to_index_entry(self,line):
        params = line.split()
        p_cnt = int(params[3])
        pointers = [params[4+i] for i in range(p_cnt)]
        offsets = [int(params[ p_cnt + 6 + i ]) for i in range(int(params[2]))]
        return IndexEntry(params[0], params[1], int(params[2]), p_cnt, pointers, int(params[4 + p_cnt]), int(params[5 + p_cnt]), offsets)

    def to_lang_entry(self, line):
        params = line.split('\t')
        ss_reference = params[0].split('-')
        lang_type = params[1].split(':')
        lemma = params[2][0:len(params[2]) - 1]
        return LangEntry(int(ss_reference[0]),ss_reference[1], lang_type[0], lang_type[1],lemma)
        
    def write_db_changes(self,pos):
        index_content = [str(self.wndata.lemmas[pos][key]) for key in self.wndata.lemmas[pos]]
        data_content = [str(self.wndata.synsets[pos][key]) for key in sorted(self.wndata.synsets[pos])]
        index_content.sort()
        with open(self.dbfiles_root + POS_TO_FILE[pos]['index'], 'w',newline='') as f:
            f.write(PREFIX + ''.join(index_content))
        with open(self.dbfiles_root + POS_TO_FILE[pos]['data'], 'w',newline ='') as f:
            f.write(PREFIX + ''.join(data_content))

    def write_lang_changes(self):
        lang_content = [str(self.wndata.lang_lemmas[key][offset]) for key in self.wndata.lang_lemmas for offset in self.wndata.lang_lemmas[key]]
        with open(self.langwn_path, 'w') as f:
            f.write(LANG_PREFIX  + ''.join(lang_content))
    
    def write_commands_history(self, commands_history):
        commands = []
        try:
            with open(self.dbfiles_root + 'wordnet_additions.py','r') as f:
                for line in f:
                    commands.append(line.strip())
        except FileNotFoundError:
            pass
        commands.extend(commands_history)
        with open(self.dbfiles_root + 'wordnet_additions.py','w') as f:
            synset_commands = [command for command in commands if 'add_synset' in command]
            word_commands = [command for command in commands if 'add_word' in command]
            sense_commands = [command for command in commands if 'add_sense_disambiguation' in command]
            f.write('from wnmanager import wm\n\n' + 'wm.open()\n\n' + '\n'.join(synset_commands) + '\n\n' +'\n'.join(word_commands) + '\n\n' + '\n'.join(sense_commands) + '\n\nwm.commit_changes()\n')

    def write_senses_disambiguation(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.wndata.senses_index, f)

    def commit_changes(self, altered_pos, commands_history):
        self.write_commands_history(commands_history)
        for pos in altered_pos:
            self.write_db_changes(pos)
        self.write_lang_changes()
        self.write_senses_disambiguation(self.senses_disambiguation_path)