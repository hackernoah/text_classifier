from ..manager.manager import WordnetManager
from collections import OrderedDict
import unittest



class LoadingTest(unittest.TestCase):
    INITIAL_SYNSET_LOAD = {'n': OrderedDict([(1740, '00001740 03 n 01 entity 0 002 ~ 00001912 n 0000 ~ 00002047 n 0000 | that which is perceived or known or inferred to have its own distinct existence (living or nonliving)  \n'), (1912, '00001912 03 n 01 physical_entity 0 003 @ 00001740 n 0000 ~ 00002200 n 0000 ~ 00002288 n 0000 | an entity that has physical existence  \n'), (2047, '00002047 03 n 02 abstraction 0 abstract_entity 0 001 @ 00001740 n 0000 | a general concept formed by extracting common features from specific examples  \n'), (2200, '00002200 03 n 01 thing 0 001 @ 00001912 n 0000 | a separate and self-contained entity  \n'), (2288, '00002288 03 n 02 object 0 physical_object 0 001 @ 00001912 n 0000 | a tangible and visible entity; an entity that can cast a shadow; "it was full of rackets, balls and other objects"  \n'), (2473, '00002473 03 n 02 whole 0 unit 0 003 @ 00002288 n 0000 ~ 00002695 n 0000 ~ 00002960 n 0000 | an assemblage of parts that is regarded as a single entity; "how big is that part compared to the whole?"; "the team is a unit"  \n'), (2695, '00002695 03 n 01 congener 0 001 @ 00002473 n 0000 | a whole (a thing or person) of the same kind or category as another; "lard was also used, though its congener, butter, was more frequently employed"; "the American shopkeeper differs from his European congener"  \n'), (2960, '00002960 03 n 02 living_thing 0 animate_thing 0 005 @ 00002473 n 0000 ~ 00003139 n 0000 ~ 00003842 n 0000 ~ 00003955 n 0000 ~ 00004039 n 0000 | a living (or once living) entity  \n'), (3139, '00003139 03 n 02 organism 0 being 0 006 @ 00002960 n 0000 ~ 00003378 n 0000 ~ 00003503 n 0000 ~ 00003597 n 0000 ~ 00003723 n 0000 %p 00004039 n 0000 | a living thing that has (or can develop) the ability to act or function independently  \n'), (3378, '00003378 03 n 01 benthos 0 001 @ 00003139 n 0000 | organisms (plants and animals) that live at or near the bottom of a sea  \n'), (3503, '00003503 03 n 01 dwarf 0 001 @ 00003139 n 0000 | a plant or animal that is atypically small  \n'), (3597, '00003597 03 n 01 heterotroph 0 001 @ 00003139 n 0000 | an organism that depends on complex organic substances for nutrition  \n'), (3723, '00003723 03 n 01 parent 0 001 @ 00003139 n 0000 | an organism (plant or animal) from which younger ones are obtained  \n'), (3842, '00003842 03 n 01 life 0 001 @ 00002960 n 0000 | living things collectively; "the oceans are teeming with life"  \n'), (3955, '00003955 03 n 01 biont 0 001 @ 00002960 n 0000 | a discrete unit of living matter  \n'), (4039, '00004039 03 n 01 cell 0 002 @ 00002960 n 0000 #p 00003139 n 0000 | (biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals  \n')]), 'a': OrderedDict(), 'v': OrderedDict(), 'r': OrderedDict()}

    INITIAL_LEMMAS_LOAD = {'n': OrderedDict([('abstract_entity', 'abstract_entity n 1 1 @ 1 0 00002047  \n'), ('abstraction', 'abstraction n 1 1 @ 1 4 00002047  \n'), ('animate_thing', 'animate_thing n 1 2 @ ~ 1 0 00002960  \n'), ('being', 'being n 1 3 @ ~ %p 2 1 00003139  \n'), ('benthos', 'benthos n 1 1 @ 1 0 00003378  \n'), ('biont', 'biont n 1 1 @ 1 0 00003955  \n'), ('cell', 'cell n 1 2 @ #p 7 3 00004039  \n'), ('congener', 'congener n 1 1 @ 3 0 00002695  \n'), ('dwarf', 'dwarf n 1 1 @ 3 1 00003503  \n'), ('entity', 'entity n 1 1 ~ 1 1 00001740  \n'), ('heterotroph', 'heterotroph n 1 1 @ 1 0 00003597  \n'), ('life', 'life n 1 1 @ 1 13 00003842  \n'), ('living_thing', 'living_thing n 1 2 @ ~ 1 1 00002960  \n'), ('object', 'object n 1 1 @ 1 4 00002288  \n'), ('organism', 'organism n 1 3 @ ~ %p 2 1 00003139  \n'), ('parent', 'parent n 1 1 @ 2 1 00003723  \n'), ('physical_entity', 'physical_entity n 1 2 @ ~ 1 0 00001912  \n'), ('physical_object', 'physical_object n 1 1 @ 1 0 00002288  \n'), ('thing', 'thing n 1 1 @ 1 10 00002200  \n'), ('unit', 'unit n 1 2 @ ~ 2 1 00002473  \n'), ('whole', 'whole n 1 2 @ ~ 2 1 00002473  \n')]), 'a': OrderedDict(), 'v': OrderedDict(), 'r': OrderedDict()}
    
    INITIAL_LANG_LEMMAS_LOAD = OrderedDict([('cosa', {1740: '00001740-n\tita:lemma\tcosa\n', 2288: '00002288-n\tita:lemma\tcosa\n'}), ('entitÃ\xa0', {1740: '00001740-n\tita:lemma\tentitÃ\xa0\n'}), ('astrazione', {2047: '00002047-n\tita:lemma\tastrazione\n'}), ('oggetto', {2288: '00002288-n\tita:lemma\toggetto\n'}), ('insieme', {2473: '00002473-n\tita:lemma\tinsieme\n'}), ('tutto', {2473: '00002473-n\tita:lemma\ttutto\n'}), ('essere vivente', {3139: '00003139-n\tita:lemma\tessere vivente\n'}), ('organismo', {3139: '00003139-n\tita:lemma\torganismo\n'}), ('organismo vivente', {3139: '00003139-n\tita:lemma\torganismo vivente\n'}), ('vita', {3842: '00003842-n\tita:lemma\tvita\n'}), ('cellula', {4039: '00004039-n\tita:lemma\tcellula\n'})])


    def setUp(self):
        self.wm = WordnetManager('wnmanager/test/fake_wordnet/','wnmanager/test/fake_wordnet/wn-data-ita.tab')
        self.wm.open()
        self.maxDiff = None
    
    def test_loading_db_errors(self):
        db_errros_len = len([error for prefix in self.wm.wndata.db_errors for pos in self.wm.wndata.db_errors[prefix] for error in self.wm.wndata.db_errors[prefix][pos]])
        self.assertEquals(0, db_errros_len)
    
    def test_loading_lang_errors(self):
        lang_errors_len = len([error for lemma in self.wm.wndata.lang_errors for error in self.wm.wndata.lang_errors[lemma]])
        self.assertEqual(0, lang_errors_len)

    def test_synset_loading(self):
        self.assertEqual(self.wm.wndata.synsets, self.INITIAL_SYNSET_LOAD)

    def test_lemmas_loading(self):
        self.assertEqual(self.wm.wndata.lemmas, self.INITIAL_LEMMAS_LOAD)

    def test_lang_lemmas_loading(self):
        self.assertEqual(self.wm.wndata.lang_lemmas, self.INITIAL_LANG_LEMMAS_LOAD)


if __name__ == '__main__':
    unittest.main()