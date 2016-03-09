# coding: utf-8

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from syllable import TonalSyllable, Ideogram

class MandarinSyllable(TonalSyllable):
    HEADS = ["b", "p", "m", "f", "d", "t", "n", "l",
             "zh", "ch", "sh", "r", "z", "c", "s",
             "x", "j", "q", "g", "k", "h",]
    SEMI_VOWELS = {
        "yu": "iu",
        "y": "i",
        "w": "u",
        "iu": "iu",
        "i": "i",
        "u": "u",
        "ü": "v",
        "&#xfc;": "v"
    }
    LASTS = ["ng", "n",]

    VOWELS_WITH_TONE = {
        "ā": ("a", 1), "ē": ("e", 1), "ō": ("o", 1), "ī": ("i", 1), "ū": ("u", 1), "ǖ": ("v", 1),
        "á": ("a", 2), "é": ("e", 2), "ó": ("o", 2), "í": ("i", 2), "ú": ("u", 2), "ǘ": ("v", 2),
        "ǎ": ("a", 3), "ě": ("e", 3), "ǒ": ("o", 3), "ǐ": ("i", 3), "ǔ": ("u", 3), "ǚ": ("v", 3),
        "à": ("a", 4), "è": ("e", 4), "ò": ("o", 4), "ì": ("i", 4), "ù": ("u", 4), "ǜ": ("v", 4),
    }
    NUCLEUS = [
        'a', 'ai', 'ao',
        'i',
        'u',
        'v',
        'e', 'ei', 'er',
        'o', 'ou',
    ]

    def __init__(self, surface, is_tone_numeral):
        TonalSyllable.__init__(self, surface, is_tone_numeral)

    def get_semi_vowels(self,):
        return self.SEMI_VOWELS.keys()
    def preprocess_tone(self,):
        if self._is_tone_numeral == False:
            matched = False
            for c, (normalized_c, tone_num) in self.VOWELS_WITH_TONE.items():
                if self._surface.find(c) != -1:
                    self._surface = self._surface.replace(c, normalized_c) + str( tone_num )
                    matched = True
            if matched == False:
                self._surface = self._surface.replace(c, normalized_c) + "5"
        return
    def postprocess_semi_vowel(self,):
        for c, normalized in self.SEMI_VOWELS.items():
            if self._semi_vowel.find(c) != -1:
                self._semi_vowel = self._semi_vowel.replace(c, normalized)
        return
    def postprocess_nucleus(self,):
        if self._nucleus == '' and self._semi_vowel != '':
            ###
            if self._nucleus == '' and self._semi_vowel == 'iu':
                self._semi_vowel = 'i'
                self._nucleus = 'u'
            else:
                self._nucleus = self._semi_vowel
                self._semi_vowel = ''


class Hanzi(Ideogram):
    def __init__(self, surfaces, is_tone_numeral):
        self._surfaces = []
        if type(surfaces) == str:
            self._surfaces.append( MandarinSyllable( surfaces, is_tone_numeral ) )
        elif type(surfaces) == list:
            for s in surfaces:
                self._surfaces.append( MandarinSyllable(s, is_tone_numeral) )
        else:
            raise ValueError("Invalid surace")


def main():
    original = "tian2"
    hz = Hanzi(original, is_tone_numeral=True)
    print ( "original: " +  original + ", split: " + str(hz) )

    original = "tián"
    hz = Hanzi(original, is_tone_numeral=False)
    print ( "original: " +  original + ", split: " + str(hz) )

    original = "yan2"
    hz = Hanzi(original, is_tone_numeral=True)
    print ( "original: " +  original + ", split: " + str(hz) )

    original = "tiang2"
    hz = Hanzi(original, is_tone_numeral=True)
    print ( "original: " +  original + ", split: " + str(hz) )

if __name__ == '__main__':
    main()

