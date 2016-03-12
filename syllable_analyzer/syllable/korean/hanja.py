# coding: utf-8

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from syllable import AtonalSyllable, Ideogram

class KoreanSyllable(AtonalSyllable):
    HEADS = ["g", "n", "d", "l", "m", "b", "s",
             "j", "c", "k", "t", "p", "h",
             "ch", "kh", "th", "ph",
             "kk", "pp", "ss",
            ]
    LASTS = ["k", "c", "l", "p",
             "ng", "n", "m",
             "s", # ??
            ]
    SEMI_VOWELS = ["y", "w"] # ??

    VOWELS_WITH_TONE = {
    }
    TONE_MAX = -1
    NUCLEUS = [
        'a',
        'ay',
        'i',
        'u',
        'uy',
        'e',
        'ey',
        'o',
        'oy',
    ]

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

