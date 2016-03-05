# coding: utf-8

from syllable import Syllable

class MandarinSyllable(Syllable):
    HEADS = ["b", "p", "m", "f", "d", "t", "n", "l",
             "zh", "ch", "sh", "r", "z", "c", "s",
             "x", "j", "q", "g", "k", "h",]
    SEMI_VOWELS = {"i": "y",
                   "u": "w"
                  }
    LASTS = ["ng", "n",]

    VOWELS_WITH_TONE = {
        "ā": ("a", 1), "ē": ("e", 1), "ō": ("o", 1), "ī": ("i", 1), "ū": ("u", 1), "ǖ": ("v", 1),
        "á": ("a", 2), "é": ("e", 2), "ó": ("o", 2), "í": ("i", 2), "ú": ("u", 2), "ǘ": ("v", 2),
        "ǎ": ("a", 3), "ě": ("e", 3), "ǒ": ("o", 3), "ǐ": ("i", 3), "ǔ": ("u", 3), "ǚ": ("v", 3),
        "à": ("a", 4), "è": ("e", 4), "ò": ("o", 4), "ì": ("i", 4), "ù": ("u", 4), "ǜ": ("v", 4),
    }

    def __init__(self, surface, is_tone_numeral = True):
        Syllable.__init__(self, surface)
        self._is_tone_numeral = is_tone_numeral
        self._has_tone = True

    def get_semi_vowels(self,):
        return self.SEMI_VOWELS.keys()
    def preprocess_tone(self,):
        if self._is_tone_numeral == False:
            for c, (normalized_c, tone_num) in self.VOWELS_WITH_TONE.items():
                if self._surface.find(c) != -1:
                    self._surface = self._surface.replace(c, normalized_c) + str( tone_num )
        return
    def postprocess_semi_vowel(self,):
        #for c, normalized in self.SEMI_VOWELS.items():
        #    if self._semi_vowel.find(c) != -1:
        #        self._semi_vowel = self._semi_vowel.replace(c, normalized)
        return


def main():
    original = "tian2"
    ms = MandarinSyllable(original, is_tone_numeral=True)
    ms.analyze()
    print ( "original: " +  original + ", split: " + ms.__str__())

    original = "tián"
    ms = MandarinSyllable(original, is_tone_numeral=False)
    ms.analyze()
    print ( "original: " +  original + ", split: " + ms.__str__())

if __name__ == '__main__':
    main()

