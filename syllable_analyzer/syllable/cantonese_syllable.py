# coding: utf-8

from syllable import TonalSyllable

class CantoneseSyllable(TonalSyllable):
    HEADS = ["b", "p", "m", "f", "d", "t", "n", "l",
             "z", "c", "s", "zh", "ch", "sh", "r",
             "x", "q", "g", "k", "h",
            ]
    LASTS = ["ng", "n", "m",
             "k", "t", "p",]
    SEMI_VOWELS = [
        "j", "w",
    ] # ??

    VOWELS_WITH_TONE = {
    }

    def __init__(self, surface, is_tone_numeral=True, romanization_scheme="jyutping"):
        self._rs = romanization_scheme
        TonalSyllable.__init__(self, surface, is_tone_numeral)

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
            self._nucleus = self._semi_vowel
            self._semi_vowel = None

def main():
    original = "jat1"
    cs = CantoneseSyllable(original)
    print ( "original: " +  original + ", split: " + cs.__str__())

if __name__ == '__main__':
    main()

