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

class Syllable:
    def __init__(self, surface, is_tone_numeral = True):
        self._surface = surface
        self._is_tone_numeral = is_tone_numeral
        return
    def __str__(self,):
        return self.get_all_features().__str__()
    def get_all_features(self,):
        return [ self._head, self._semi_vowel, self._nucleus, self._last, self._tone ]

    def get_heads(self,):
        return self.HEADS
    def get_semi_vowels(self,):
        return self.SEMI_VOWELS
    def get_lasts(self,):
        return self.LASTS

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
        self._nucleus = self._rhyme[ : -last_length ]
        return
    def postprocess_last(self,):
        return
    def postprocess_nucleus(self,):
        return

