# coding: utf-8

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from syllable import AtonalSyllable, Ideogram

class KoreanSyllable(AtonalSyllable):
    HEADS = ["g", "n", "d", "r", "m", "b", "s",
             "j", "ch", "k", "t", "p", "h",]
    LASTS = ["k", "l", "p",
             "ng", "n", "m",]
    SEMI_VOWELS = ["y", "w"] # ??

    VOWELS_WITH_TONE = {
    }

    def __init__(self, surface):
        AtonalSyllable.__init__(self, surface)

class Hanja(Ideogram):
    def __init__(self, surfaces):
        self._surfaces = []
        if type(surfaces) == str:
            self._surfaces.append( KoreanSyllable( surfaces ) )
        elif type(surfaces) == list:
            for s in surfaces:
                self._surfaces.append( KoreanSyllable(s) )
        else:
            raise ValueError("Invalid surace")


def main():
    original = "il"
    hj = Hanja(original)
    print ( "original: " +  original + ", split: " + str(hj) )

if __name__ == '__main__':
    main()

