# coding: utf-8

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from syllable import TonalSyllable, Ideogram

class CantoneseSyllable(TonalSyllable):
    HEADS = ["b", "p", "m", "f", "d", "t", "n", "l",
             "z", "c", "s", "zh", "ch", "sh", "r",
             "x", "q", "g", "k", "h", "ng",
            ]
    LASTS = ["ng", "n", "m",
             "k", "t", "p",]
    SEMI_VOWELS = {
        "jyu": "iu",
        "jiu": "iu",
        "jy": "i",
        "yu": "iu",
        "iu": "iu",
        "wu": "u",
        "y": "i",
        "w": "u",
        "j": "i",
        "i": "i",
        "u": "u",
    }

    VOWELS_WITH_TONE = {
    }
    NUCLEUS = [
        'a', 'aa', 'ai', 'aai', 'au', 'aau',
        'i',
        'u',
        'o', 'oi', 'ou', 'oe',
        'e', 'ei', 'eu', 'eo', 'eoi',
        '@',
    ]

    def __init__(self, surface, is_tone_numeral=True, romanization_scheme="jyutping"):
        self._rs = romanization_scheme
        TonalSyllable.__init__(self, surface, is_tone_numeral)

    def get_semi_vowels(self,):
        return self.SEMI_VOWELS.keys()

    def postprocess_semi_vowel(self,):
        for c, normalized in self.SEMI_VOWELS.items():
            if self._semi_vowel.find(c) != -1:
                self._semi_vowel = self._semi_vowel.replace(c, normalized)
        return
    def postprocess_last(self,):
        if self._last in ["k", "t", "p"]:
            if self._tone == 1:
                self._tone = 7
            if self._tone == 3:
                self._tone = 8
            if self._tone == 6:
                self._tone = 9
    def postprocess_nucleus(self,):
        if self._nucleus == '' and self._semi_vowel != '':
            ###
            if self._nucleus == '' and self._semi_vowel == 'iu':
                self._semi_vowel = 'i'
                self._nucleus = 'u'
            else:
                self._nucleus = self._semi_vowel
                self._semi_vowel = ''
        if self._head in ['ng', 'm'] and self._nucleus == '':
            self._nucleus = "@"
        if self._head == 'h' and self._last == 'ng':
            self._nucleus = "@"
    def validate_nucleus(self,):
        return

class Honzi(Ideogram):
    def __init__(self, surfaces):
        self._surfaces = []
        if type(surfaces) == str:
            self._surfaces.append( CantoneseSyllable( surfaces ) )
        elif type(surfaces) == list:
            for s in surfaces:
                self._surfaces.append( CantoneseSyllable(s) )
        else:
            raise ValueError("Invalid surace")


def main():
    original = "jat1"
    hz = Honzi(original)
    print ( "original: " +  original + ", split: " + str(hz) )

if __name__ == '__main__':
    main()

