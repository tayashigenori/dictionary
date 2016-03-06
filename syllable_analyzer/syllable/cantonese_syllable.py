# coding: utf-8

from syllable import Syllable

class CantoneseSyllable(Syllable):
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

    def __init__(self, surface, romanization_scheme="jyutping"):
        Syllable.__init__(self, surface)
        self._has_tone = True
        self._is_tone_numeral = True

    def postprocess_last(self,):
        if self._last in ["k", "t", "p"]:
            if self._tone == 1:
                self._tone = 7
            if self._tone == 3:
                self._tone = 8
            if self._tone == 6:
                self._tone = 9

def main():
    original = "jat1"
    cs = CantoneseSyllable(original)
    cs.analyze()
    print ( "original: " +  original + ", split: " + cs.__str__())

if __name__ == '__main__':
    main()

