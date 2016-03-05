# coding: utf-8

from syllable import Syllable

class VietnameseSyllable(Syllable):
    HEADS = ["ng", "q",
             "b", "p", "m", "f", "d", "t", "n", "l",
             "zh", "ch", "sh", "r", "z", "c", "s",
             "x", "j", "q", "g", "k", "h",]
    LASTS = ["ng", "n", "nh", "m",
             "c", "ch", "t", "p",]
    SEMI_VOWELS = [] # ??

    VOWELS_WITH_TONE = {
#        "a":("a",1), "ă":("ă",1), "â":("â",1), "e":("e",1), "ê":("ê",1), "i":("i",1), "o":("o",1), "ô":("ô",1), "ơ":("ơ",1), "u":("u",1), "ư":("ư",1), "y":("y",1),
        "à":("a",2), "ằ":("ă",2), "ầ":("â",2), "è":("e",2), "ề":("ê",2), "ì":("i",2), "ò":("o",2), "ồ":("ô",2), "ờ":("ơ",2), "ù":("u",2), "ừ":("ư",2), "ỳ":("y",2),
        "ả":("a",3), "ẳ":("ă",3), "ẩ":("â",3), "ẻ":("e",3), "ể":("ê",3), "ỉ":("i",3), "ỏ":("o",3), "ổ":("ô",3), "ở":("ơ",3), "ủ":("u",3), "ử":("ư",3), "ỷ":("y",3),
        "ã":("a",4), "ẵ":("ă",4), "ẫ":("â",4), "ẽ":("e",4), "ễ":("ê",4), "ĩ":("i",4), "õ":("o",4), "ỗ":("ô",4), "ỡ":("ơ",4), "ũ":("u",4), "ữ":("ư",4), "ỹ":("y",4),
        "á":("a",5), "ắ":("ă",5), "ấ":("â",5), "é":("e",5), "ế":("ê",5), "í":("i",5), "ó":("o",5), "ố":("ô",5), "ớ":("ơ",5), "ú":("u",5), "ứ":("ư",5), "ý":("y",5),
        "ạ":("a",6), "ặ":("ă",6), "ậ":("â",6), "ẹ":("e",6), "ệ":("ê",6), "ị":("i",6), "ọ":("o",6), "ộ":("ô",6), "ợ":("ơ",6), "ụ":("u",6), "ự":("ư",6), "ỵ":("y",6),
    }

    def __init__(self, surface, is_tone_numeral = True):
        Syllable.__init__(self, surface)
        self._is_tone_numeral = is_tone_numeral
        self._has_tone = True

    def preprocess_tone(self,):
        if self._is_tone_numeral == False:
            matched = False
            for c, (normalized_c, tone_num) in self.VOWELS_WITH_TONE.items():
                if self._surface.find(c) != -1:
                    self._surface = self._surface.replace(c, normalized_c) + str( tone_num )
                    matched = True
            if matched == False:
                self._surface = self._surface.replace(c, normalized_c) + "1"
        return


def main():
    original = "quôc5"
    vs = VietnameseSyllable(original, is_tone_numeral=True)
    vs.analyze()
    print ( "original: " +  original + ", split: " + vs.__str__())

    original = "quốc"
    vs = VietnameseSyllable(original, is_tone_numeral=False)
    vs.analyze()
    print ( "original: " +  original + ", split: " + vs.__str__())

if __name__ == '__main__':
    main()

