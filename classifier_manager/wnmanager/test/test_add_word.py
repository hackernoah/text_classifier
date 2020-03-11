from ..manager.manager import WordnetManager
from ..manager.utils import *
from collections import OrderedDict
import unittest



class AddWordTest(unittest.TestCase):
    ADDWORD_SYNSET_TEST = {'n': OrderedDict([(1740, '00001740 03 n 01 entity 0 002 ~ 00001912 n 0000 ~ 00002047 n 0000 | that which is perceived or known or inferred to have its own distinct existence (living or nonliving)  \n'), (1912, '00001912 03 n 01 physical_entity 0 003 @ 00001740 n 0000 ~ 00002200 n 0000 ~ 00002288 n 0000 | an entity that has physical existence  \n'), (2047, '00002047 03 n 02 abstraction 0 abstract_entity 0 001 @ 00001740 n 0000 | a general concept formed by extracting common features from specific examples  \n'), (2200, '00002200 03 n 01 thing 0 001 @ 00001912 n 0000 | a separate and self-contained entity  \n'), (2288, '00002288 03 n 02 object 0 physical_object 0 001 @ 00001912 n 0000 | a tangible and visible entity; an entity that can cast a shadow; "it was full of rackets, balls and other objects"  \n'), (2473, '00002473 03 n 02 whole 0 unit 0 003 @ 00002288 n 0000 ~ 00002695 n 0000 ~ 00002960 n 0000 | an assemblage of parts that is regarded as a single entity; "how big is that part compared to the whole?"; "the team is a unit"  \n'), (2695, '00002695 03 n 01 congener 0 001 @ 00002473 n 0000 | a whole (a thing or person) of the same kind or category as another; "lard was also used, though its congener, butter, was more frequently employed"; "the American shopkeeper differs from his European congener"  \n'), (2960, '00002960 03 n 02 living_thing 0 animate_thing 0 005 @ 00002473 n 0000 ~ 00003139 n 0000 ~ 00003851 n 0000 ~ 00003964 n 0000 ~ 00004048 n 0000 | a living (or once living) entity  \n'), (3139, '00003139 03 n 02 organism 0 being 0 006 @ 00002960 n 0000 ~ 00003378 n 0000 ~ 00003503 n 0000 ~ 00003606 n 0000 ~ 00003732 n 0000 %p 00004048 n 0000 | a living thing that has (or can develop) the ability to act or function independently  \n'), (3378, '00003378 03 n 01 benthos 0 001 @ 00003139 n 0000 | organisms (plants and animals) that live at or near the bottom of a sea  \n'), (3503, '00003503 03 n 02 dwarf 0 midget 0 001 @ 00003139 n 0000 | a plant or animal that is atypically small  \n'), (3606, '00003606 03 n 01 heterotroph 0 001 @ 00003139 n 0000 | an organism that depends on complex organic substances for nutrition  \n'), (3732, '00003732 03 n 01 parent 0 001 @ 00003139 n 0000 | an organism (plant or animal) from which younger ones are obtained  \n'), (3851, '00003851 03 n 01 life 0 001 @ 00002960 n 0000 | living things collectively; "the oceans are teeming with life"  \n'), (3964, '00003964 03 n 01 biont 0 001 @ 00002960 n 0000 | a discrete unit of living matter  \n'), (4048, '00004048 03 n 01 cell 0 002 @ 00002960 n 0000 #p 00003139 n 0000 | (biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals  \n')]), 'a': OrderedDict(), 'v': OrderedDict(), 'r': OrderedDict()}


    ADDWORD_LEMMAS_TEST = {'n': OrderedDict([('abstract_entity', 'abstract_entity n 1 1 @ 1 0 00002047  \n'), ('abstraction', 'abstraction n 1 1 @ 1 4 00002047  \n'), ('animate_thing', 'animate_thing n 1 2 @ ~ 1 0 00002960  \n'), ('being', 'being n 1 3 @ ~ %p 2 1 00003139  \n'), ('benthos', 'benthos n 1 1 @ 1 0 00003378  \n'), ('biont', 'biont n 1 1 @ 1 0 00003964  \n'), ('cell', 'cell n 1 2 @ #p 7 3 00004048  \n'), ('congener', 'congener n 1 1 @ 3 0 00002695  \n'), ('dwarf', 'dwarf n 1 1 @ 3 1 00003503  \n'), ('entity', 'entity n 1 1 ~ 1 1 00001740  \n'), ('heterotroph', 'heterotroph n 1 1 @ 1 0 00003606  \n'), ('life', 'life n 1 1 @ 1 13 00003851  \n'), ('living_thing', 'living_thing n 1 2 @ ~ 1 1 00002960  \n'), ('object', 'object n 1 1 @ 1 4 00002288  \n'), ('organism', 'organism n 1 3 @ ~ %p 2 1 00003139  \n'), ('parent', 'parent n 1 1 @ 2 1 00003732  \n'), ('physical_entity', 'physical_entity n 1 2 @ ~ 1 0 00001912  \n'), ('physical_object', 'physical_object n 1 1 @ 1 0 00002288  \n'), ('thing', 'thing n 1 1 @ 1 10 00002200  \n'), ('unit', 'unit n 1 2 @ ~ 2 1 00002473  \n'), ('whole', 'whole n 1 2 @ ~ 2 1 00002473  \n'), ('midget', 'midget n 1 1 @ 1 0 00003503  \n')]), 'a': OrderedDict(), 'v': OrderedDict(), 'r': OrderedDict()}
    
    ADDWORD_LANG_LEMMAS_TEST = OrderedDict([('cosa', {1740: '00001740-n\tita:lemma\tcosa\n', 2289: '00002289-n\tita:lemma\tcosa\n'}), ('entitÃ\xa0', {1740: '00001740-n\tita:lemma\tentitÃ\xa0\n'}), ('astrazione', {2047: '00002047-n\tita:lemma\tastrazione\n'}), ('oggetto', {2289: '00002289-n\tita:lemma\toggetto\n'}), ('insieme', {2474: '00002474-n\tita:lemma\tinsieme\n'}), ('tutto', {2474: '00002474-n\tita:lemma\ttutto\n'}), ('essere vivente', {3140: '00003140-n\tita:lemma\tessere vivente\n'}), ('organismo', {3140: '00003140-n\tita:lemma\torganismo\n'}), ('organismo vivente', {3140: '00003140-n\tita:lemma\torganismo vivente\n'}), ('vita', {3843: '00003843-n\tita:lemma\tvita\n'}), ('cellula', {4058: '00004058-n\tita:lemma\tcellula\n'})])


    def setUp(self):
        self.wm = WordnetManager('wnmanager/test/fake_wordnet/','wnmanager/test/fake_wordnet/wn-data-ita.tab')
        self.wm.open()
        # self.wm.add_word('midget','n',3504,test=True)
        self.f = open('add_word_test','w')
    
    def tearDown(self):
        self.f.close()
    
    # def test_inexistant_offset(self):
    #     with self.assertRaises(WNManagerError,"add_word: offset inesistente"):
    #         self.wm.add_word('banana', 'n',9999, test=True)

    # def test_word_already_exists(self):
    #     with self.assertRaises(WNManagerError,"add_word: la parola esiste già"):
    #         self.wm.add_word('dwarf', 'n',3503, test=True)

    # def test_synset_connection_already_exists(self):
    #     self.assertRaises(WNManagerError,lambda: self.wm.add_word('organismo', 'n',3139, test=True))

    
    # def test_loading_lang_errors(self):
    #     lang_errors_len = len([error for lemma in self.wm.wndata.lang_errors for error in self.wm.wndata.lang_errors[lemma]])
    #     self.assertEquals(0, lang_errors_len)

    # def test_synset_loading(self):
    #     self.assertEquals(self.wm.wndata.synsets, self.INITIAL_SYNSET_LOAD)

    # def test_lemmas_loading(self):
    #     self.assertEquals(self.wm.wndata.lemmas, self.INITIAL_LEMMAS_LOAD)

    # def test_lang_lemmas_loading(self):
    #     self.assertEquals(self.wm.wndata.lang_lemmas, self.INITIAL_LANG_LEMMAS_LOAD)


if __name__ == '__main__':
    unittest.main()