# coding: utf-8

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
        return (None, 0)


class Syllable:
    def __init__(self, surface):
        self._surface = surface
        self.analyze()
        return
    def __str__(self,):
        return self.get_all_parts().__str__()

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
        (head, head_length) = find_longest(self._surface, self.get_heads())
        self._head = head
        self._tail = self._surface[ head_length: ]
        return
    def postprocess_head(self,):
        return

    def preprocess_semi_vowel(self,):
        return
    def analyze_semi_vowel(self,):
        (semi_vowel, semi_vowel_length) = find_longest(self._tail, self.get_semi_vowels())
        self._semi_vowel = semi_vowel
        self._rhyme = self._tail[ semi_vowel_length : ]
        return
    def postprocess_semi_vowel(self,):
        return

    def preprocess_last(self,):
        return
    def analyze_last(self,):
        (last, last_length) = find_longest(self._rhyme, self.get_lasts(), at="end")
        self._last = last
        if last_length > 0:
            self._nucleus = self._rhyme[ : -last_length ]
        else:
            self._nucleus = self._rhyme
        return
    def postprocess_last(self,):
        return
    def postprocess_nucleus(self,):
        return

    def get_all_parts(self,):
        return [ self._head, self._semi_vowel, self._nucleus, self._last, self._tone ]
    def get_heads(self,):
        return self.HEADS
    def get_semi_vowels(self,):
        return self.SEMI_VOWELS
    def get_lasts(self,):
        return self.LASTS

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
        return "".join( map(lambda syllable: syllable.__str__(), self._surfaces) )
    def get_all_features(self,):
        return map(lambda syllable: syllable.get_all_features(), self._surfaces)

