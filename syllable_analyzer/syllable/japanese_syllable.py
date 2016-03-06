# coding: utf-8

from syllable import AtonalSyllable

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


def main():
    original = "koku"
    js = JapaneseSyllable(original)
    print ( "original: " +  original + ", split: " + js.__str__())

    original = "jutsu"
    js = JapaneseSyllable(original)
    print ( "original: " +  original + ", split: " + js.__str__())

    original = "kou"
    js = JapaneseSyllable(original)
    print ( "original: " +  original + ", split: " + js.__str__())

    print (js.get_all_features())

if __name__ == '__main__':
    main()

