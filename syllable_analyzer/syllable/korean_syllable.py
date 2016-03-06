# coding: utf-8

from syllable import Syllable

class KoreanSyllable(Syllable):
    HEADS = ["g", "n", "d", "r", "m", "b", "s",
             "j", "ch", "k", "t", "p", "h",]
    LASTS = ["k", "l", "p",
             "ng", "n", "m",]
    SEMI_VOWELS = [] # ??

    VOWELS_WITH_TONE = {
    }

    def __init__(self, surface):
        Syllable.__init__(self, surface)
        self._has_tone = False

def main():
    original = "il"
    ks = KoreanSyllable(original)
    ks.analyze()
    print ( "original: " +  original + ", split: " + ks.__str__())

if __name__ == '__main__':
    main()

