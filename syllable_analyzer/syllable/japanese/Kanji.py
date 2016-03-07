# coding: utf-8

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from syllable import AtonalSyllable, Ideogram

class JapaneseSyllable(AtonalSyllable):
    HEADS = ["k", "s", "t", "n", "h", "m", "r",
             "g", "z", "d",      "b",
             "ky", "sh", "sy", "ch", "ty", "ny", "hy", "my", "ry",
             "gy", "j",  "zy",                   "by",
            ]
    SEMI_VOWELS = {
        "ky": ("k", "y"),
        "sh": ("s", "y"), "sy": ("s", "y"),
        "ch": ("t", "y"), "ty": ("t", "y"),
        "ny": ("n", "y"),
        "hy": ("h", "y"),
        "my": ("m", "y"),
        "ry": ("r", "y"),
        "gy": ("g", "y"),
        "j":  ("z", "y"),
        "by": ("b", "y"),
    }
    LASTS = ["ki", "ku", "chi", "tsu", "n", "i", "u"]

    VOWELS_WITH_TONE = {
    }

    def __init__(self, surface):
        AtonalSyllable.__init__(self, surface)

    def get_semi_vowels(self,):
        return self.SEMI_VOWELS.keys()
    def postprocess_semi_vowel(self,):
        for head, (normalized_head, normalized_semi_vowel) in self.SEMI_VOWELS.items():
            if self._head.find(head) != -1:
                self._head = normalized_head
                self._semi_vowel = normalized_semi_vowel
        return

class Kanji(Ideogram):
    def __init__(self, surfaces):
        self._surfaces = []
        if type(surfaces) == str:
            self._surfaces.append( JapaneseSyllable( surfaces ) )
        elif type(surfaces) == list:
            for s in surfaces:
                self._surfaces.append( JapaeseSyllable(s) )
        else:
            raise ValueError("Invalid surace")


def main():
    original = "koku"
    kj = Kanji(original)
    print ( "original: " +  original + ", split: " + kj.__str__())

    original = "jutsu"
    kj = Kanji(original)
    print ( "original: " +  original + ", split: " + kj.__str__())

    original = "kou"
    kj = Kanji(original)
    print ( "original: " +  original + ", split: " + kj.__str__())

    for f in kj.get_all_features():
        print (f)

if __name__ == '__main__':
    main()

