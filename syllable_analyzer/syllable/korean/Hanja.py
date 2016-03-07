# coding: utf-8

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from syllable import AtonalSyllable

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

def main():
    original = "il"
    ks = KoreanSyllable(original)
    print ( "original: " +  original + ", split: " + ks.__str__())

if __name__ == '__main__':
    main()

