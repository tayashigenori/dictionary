# coding: utf-8

from functools import reduce
import numpy as np

"""
==================================================
| HEAD (c) | TAIL                                |
|          | SEMI_VOWEL | RHYME (v+c)            |
|                       | NUCLEUS (v) | LAST (c) |
==================================================
  - v: vowel
  - c: consonant
only NUCLEUS is mandatory

and the following features are also retrievable from this class
==================================================|
| INIT                                 | LAST (c) |
| HEAD+ (c + semi-vowel) | NUCLEUS (v) |          |
| HEAD (c) | SEMI_VOWEL  |                        |
==================================================|
==================================================|
| HEAD (c) |                           | LAST (c) |
==================================================|
"""

def find_longest(haystack, needles, at="beginning"):
    found = {}
    for needle in needles:
        if at == "beginning" and haystack.startswith(needle) == True:
            found[needle] = len(needle)
        elif at == "end" and haystack.endswith(needle) == True:
            found[needle] = len(needle)
    value_sorted = sorted(found.items(), key=lambda x: x[1])
    if len(value_sorted) > 0:
        # return longest
        return value_sorted[-1]
    else:
        return ("", 0)

class SyllableError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Syllable:
    def __init__(self, surface):
        if len(surface) == 0:
            raise SyllableError("Invalid surface")
        self._surface = surface
        self.analyze()
        return
    def __str__(self,):
        return str( self.get_all_parts() )
    def __list__(self,):
        return self.get_all_parts()

    """
    analyze syllable
    """
    def analyze(self,):
        self._surface = self._surface.lower()

        self.preprocess_tone()
        self.analyze_tone()
        self.postprocess_tone()

        self.preprocess_head()
        self.analyze_head()
        self.postprocess_head()

        self.preprocess_semi_vowel()
        self.analyze_semi_vowel()
        self.postprocess_semi_vowel()

        self.preprocess_last()
        self.analyze_last()
        self.postprocess_last()
        self.postprocess_nucleus()

        self.validate_nucleus()

    def preprocess_tone(self,):
        return
    def analyze_tone(self,):
        if self._has_tone == False:
            self._tone = None
            return
        self._tone = int (self._surface[-1] )
        self._surface = self._surface[:-1]
        return
    def postprocess_tone(self,):
        return

    def preprocess_head(self,):
        return
    def analyze_head(self,):        
        (head, head_length) = find_longest(self._surface, self.get_all_heads())
        self._head = head
        self._tail = self._surface[ head_length: ]
        return
    def postprocess_head(self,):
        return

    def preprocess_semi_vowel(self,):
        return
    def analyze_semi_vowel(self,):
        (semi_vowel, semi_vowel_length) = find_longest(self._tail, self.get_all_semi_vowels())
        self._semi_vowel = semi_vowel
        self._rhyme = self._tail[ semi_vowel_length : ]
        return
    def postprocess_semi_vowel(self,):
        return

    def preprocess_last(self,):
        return
    def analyze_last(self,):
        (last, last_length) = find_longest(self._rhyme, self.get_all_lasts(), at="end")
        self._last = last
        self._nucleus = self._rhyme[ : -last_length ] if last_length > 0 else self._rhyme
        return
    def postprocess_last(self,):
        return
    def postprocess_nucleus(self,):
        return
    def validate_nucleus(self,):
        if self._nucleus not in self.NUCLEUS:
            raise SyllableError("Irregular syllable: %s" %(self._surface) )
        return

    """
    getters
    """
    def get_all_parts(self,):
        return [ self._head, self._semi_vowel, self._nucleus, self._last, self._tone ]
    def get_all_heads(self,):
        return self.HEADS
    def get_all_semi_vowels(self,):
        return self.SEMI_VOWELS
    def get_all_lasts(self,):
        return self.LASTS
    def get_all_nucleus(self,):
        return self.NUCLEUS
    def get_all_tones(self,):
        return range( self.TONE_MAX + 1 ) 

    def get_all_features(self,):
        return [ self._head, self._semi_vowel, self._nucleus, self._last, self._tone,
                 self.get_init(),
                 self.get_head_plus(),
                 self.get_head_last(),
               ]
    def get_init(self,):
        return "".join([s for s in [self._head, self._semi_vowel, self._nucleus] if s is not None])
    def get_head_plus(self,):
        return "".join([s for s in [self._head, self._semi_vowel] if s is not None])
    def get_head_last(self,):
        return ",".join([s for s in [self._head, self._last] if s is not None])

    """
    vectorizer
    """
    def vectorize_head(self,):
        li = [h == self._head for h in self.get_all_heads()]
        return np.array(li, dtype=bool)
    def vectorize_semi_vowel(self,):
        li = [s == self._semi_vowel for s in self.get_all_semi_vowels()]
        return np.array(li, dtype=bool)
    def vectorize_nucleus(self,):
        li = [n == self._nucleus for n in self.get_all_nucleus()]
        return np.array(li, dtype=bool)
    def vectorize_last(self,):
        li = [l == self._last for l in self.get_all_lasts()]
        return np.array(li, dtype=bool)
    def vectorize_tone(self,):
        li = [l == self._tone for l in self.get_all_tones()]
        return np.array(li, dtype=bool)

    """
    make transaction
    """
    def make_transaction_head(self,):
        return "[%s:%s]%s" %(self.__class__.__name__[:4], "hd", self._head)
    def make_transaction_semi_vowel(self,):
        return "[%s:%s]%s" %(self.__class__.__name__[:4], "sv", self._semi_vowel)
    def make_transaction_nucleus(self,):
        return "[%s:%s]%s" %(self.__class__.__name__[:4], "nc", self._nucleus)
    def make_transaction_last(self,):
        return "[%s:%s]%s" %(self.__class__.__name__[:4], "lt", self._last)
    def make_transaction_tone(self,):
        return "[%s:%s]%s" %(self.__class__.__name__[:4], "tn", str( self._tone ))


class TonalSyllable(Syllable):
    def __init__(self, surface, is_tone_numeral = True):
        self._has_tone = True
        self._is_tone_numeral = is_tone_numeral
        Syllable.__init__(self, surface)

class AtonalSyllable(Syllable):
    def __init__(self, surface,):
        self._has_tone = False
        Syllable.__init__(self, surface)

class Ideogram:
    def __init__(self,):
        self._surfaces = []
        return
    def __str__(self,):
        m = self.get_all_parts()
        return str( list(m) )
    def __list__(self,):
        m = self.get_all_parts()
        return list(m)
    def get_all_parts(self,):
        return map(lambda syllable: syllable.get_all_parts(), self._surfaces)
    def get_all_features(self,):
        return map(lambda syllable: syllable.get_all_features(), self._surfaces)

    def vectorize(self,):
        r = []
        # head
        m = map( lambda s : s.vectorize_head(), self._surfaces )
        na = reduce( lambda x, y: np.logical_and(x, y), m)
        r += na.astype(int).tolist()
        # semi vowel
        m = map( lambda s: s.vectorize_semi_vowel(), self._surfaces )
        na = reduce( lambda x, y: np.logical_and(x, y), m)
        r += na.astype(int).tolist()
        # nucleus
        m = map( lambda s: s.vectorize_nucleus(), self._surfaces )
        na = reduce( lambda x, y: np.logical_and(x, y), m)
        r += na.astype(int).tolist()
        # last
        m = map( lambda s: s.vectorize_last(), self._surfaces )
        na = reduce( lambda x, y: np.logical_and(x, y), m)
        r += na.astype(int).tolist()
        # last
        m = map( lambda s: s.vectorize_tone(), self._surfaces )
        na = reduce( lambda x, y: np.logical_and(x, y), m)
        r += na.astype(int).tolist()
        return r

    def make_transaction(self,):
        r = []
        for s in self._surfaces:
            # head
            r.append( s.make_transaction_head() )
            # semi vowel
            r.append( s.make_transaction_semi_vowel() )
            # nucleus
            r.append( s.make_transaction_nucleus() )
            # last
            r.append( s.make_transaction_last() )
            # last
            r.append( s.make_transaction_tone() )
        return r

    def make_transaction2(self, sep="&", with_header=False):
        r = []
        heads = set( map( lambda s: s._head, self._surfaces ) )
        heads_sorted = sorted(heads)
        header = "%s-%s=" %(self.__class__.__name__[:4].upper(), "HEAD") if with_header else ""
        r.append( header + sep.join( heads_sorted ) )

        semi_vowels = set( map( lambda s: s._semi_vowel, self._surfaces ) )
        semi_vowels_sorted = sorted(semi_vowels)
        header = "%s-%s=" %(self.__class__.__name__[:4].upper(), "SEMIVOWEL") if with_header else ""
        r.append( header + sep.join( semi_vowels_sorted ) )

        nucleus = set( map( lambda s: s._nucleus, self._surfaces ) )
        nucleus_sorted = sorted(nucleus)
        header = "%s-%s=" %(self.__class__.__name__[:4].upper(), "NUCLEUS") if with_header else ""
        r.append( header + sep.join( nucleus_sorted ) )

        lasts = set( map( lambda s: s._last, self._surfaces ) )
        lasts_sorted = sorted(lasts)
        header = "%s-%s=" %(self.__class__.__name__[:4].upper(), "LAST") if with_header else ""
        r.append( header + sep.join( lasts_sorted ) )

        tones = set( map( lambda s: str(s._tone), self._surfaces) )
        tones_sorted = sorted(tones)
        header = "%s-%s=" %(self.__class__.__name__[:4].upper(), "TONE") if with_header else ""
        r.append( header + sep.join( tones_sorted ) )
        return r

