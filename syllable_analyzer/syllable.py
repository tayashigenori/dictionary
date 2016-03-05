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

def find_longest(haystack, needles, at=0):
    found = {}
    for needle in needles:
        if haystack.find(needle) == at:
            found[needle] = len(needle)
    value_sorted = sorted(found.items(), key=lambda x: x[1])
    if len(value_sorted) > 0:
        return value_sorted[0]
    else:
        return ("", 0)

class Syllable:
    def __init__(self, surface, romanization_scheme, is_tone_numeral = True):
        self._surface = surface
        self._rs = romanization_scheme
        self._is_tone_numeral = is_tone_numeral
        return
    def __str__(self,):
        return [ self._head, self._semi_vowel, self._nucleus, self._last, self._tone ].__str__()

    def get_heads(self,):
        return self.HEADS
    def get_semi_vowels(self,):
        return self.SEMI_VOWELS
    def get_lasts(self,):
        return self.LASTS

    def analyze(self,):
        if self._is_tone_numeral == False:
            self.normalize_tone()
        self.analyze_tone()
        self.analyze_head()
        self.analyze_semi_vowel()
        self.normalize_semi_vowel()
        self.analyze_last()

    def analyze_tone(self,):
        self._tone = int (self._surface[-1] )
        self._surface = self._surface[:-1]
        return
    def analyze_head(self,):        
        (head, head_length) = find_longest(self._surface, self.get_heads())
        self._head = head
        self._tail = self._surface[ head_length: ]
        return
    def analyze_semi_vowel(self,):
        (semi_vowel, semi_vowel_length) = find_longest(self._tail, self.get_semi_vowels())
        self._semi_vowel = semi_vowel
        self._rhyme = self._tail[ semi_vowel_length : ]
        return
    def analyze_last(self,):
        (last, last_length) = find_longest(self._rhyme, self.get_lasts(),
                                             at=len(self._rhyme)-1
                                             )
        self._last = last
        self._nucleus = self._rhyme[ : -last_length ]
        return

    def normalize_tone(self,):
        return
    def normalize_head(self,):
        return
    def normalize_semi_vowel(self,):
        return
    def normalize_last(self,):
        return


class MandarinSyllable(Syllable):
    HEADS = ["b", "p", "m", "f", "d", "t", "n", "l",
             "zh", "ch", "sh", "r", "z", "c", "s",
             "x", "j", "q", "g", "k", "h",]
    SEMI_VOWELS = {"i": "y",
                   "u": "w"
                  }
    LASTS = ["ng", "n",]

    VOWELS_WITH_TONE = {
        "ā": ("a", 1), "ē": ("e", 1), "ō": ("o", 1), "ī": ("i", 1), "ū": ("u", 1), "ǖ": ("v", 1),
        "á": ("a", 2), "é": ("e", 2), "ó": ("o", 2), "í": ("i", 2), "ú": ("u", 2), "ǘ": ("v", 2),
        "ǎ": ("a", 3), "ě": ("e", 3), "ǒ": ("o", 3), "ǐ": ("i", 3), "ǔ": ("u", 3), "ǚ": ("v", 3),
        "à": ("a", 4), "è": ("e", 4), "ò": ("o", 4), "ì": ("i", 4), "ù": ("u", 4), "ǜ": ("v", 4),
    }
    def get_semi_vowels(self,):
        return self.SEMI_VOWELS.keys()
    def normalize_tone(self,):
        for c, (normalized_c, tone_num) in self.VOWELS_WITH_TONE.items():
            if self._surface.find(c) != -1:
                self._surface = self._surface.replace(c, normalized_c) + str( tone_num )
        return
    def normalize_semi_vowel(self,):
        #for c, normalized in self.SEMI_VOWELS.items():
        #    if self._semi_vowel.find(c) != -1:
        #        self._semi_vowel = self._semi_vowel.replace(c, normalized)
        return


def main():
    original = "tian2"
    ms = MandarinSyllable(original, romanization_scheme="pinyin", is_tone_numeral=True)
    ms.analyze()
    print ( "original: " +  original + ", split: " + ms.__str__())

    original = "tián"
    ms = MandarinSyllable(original, romanization_scheme="pinyin", is_tone_numeral=False)
    ms.analyze()
    print ( "original: " +  original + ", split: " + ms.__str__())

if __name__ == '__main__':
    main()

