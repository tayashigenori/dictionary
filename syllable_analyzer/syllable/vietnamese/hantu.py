# coding: utf-8

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from syllable import TonalSyllable, Ideogram

"""
for convenience tones are mapped to 8 numbers as follows
  - a (ngang "level")	-> a1
  - à (huyền "hanging")	-> a2
  - á (sắc "sharp")	-> a3
  - ạ (nặng "heavy")	-> a4
  - ả (hỏi "asking")	-> a5
  - ã (ngã "tumbling")	-> a6
  - ác (sắc "sharp" + ctp)	-> ac7
  - ạc (nặng "heavy" + ctp)	-> ac8
"""

class VietnameseSyllable(TonalSyllable):
    HEADS = [
             "b", "p", "ph", "v", "m", "h",
             "t", "th", "x", "s", "d", "g", "r", "đ",
             "l", "n", "ch", "tr", "nh",
             "c", "k", "q", "kh", "g", "gh", "ng", "ngh",
             "x", "j", "q", "g", "k", "h",]
    LASTS = ["ng", "n", "nh", "m",
             "c", "ch", "t", "p",]
    SEMI_VOWELS = [
        "uy", "iu", "iư", "y", "i", "u", "ư", "o", "ô", "ơ"
    ]

    VOWELS_WITH_TONE = {
#        "a":("a",1), "ă":("ă",1), "â":("â",1), "e":("e",1), "ê":("ê",1), "i":("i",1), "o":("o",1), "ô":("ô",1), "ơ":("ơ",1), "u":("u",1), "ư":("ư",1), "y":("y",1),
        "à":("a",2), "ằ":("ă",2), "ầ":("â",2), "è":("e",2), "ề":("ê",2), "ì":("i",2), "ò":("o",2), "ồ":("ô",2), "ờ":("ơ",2), "ù":("u",2), "ừ":("ư",2), "ỳ":("y",2),
        "á":("a",3), "ắ":("ă",3), "ấ":("â",3), "é":("e",3), "ế":("ê",3), "í":("i",3), "ó":("o",3), "ố":("ô",3), "ớ":("ơ",3), "ú":("u",3), "ứ":("ư",3), "ý":("y",3),
        "ạ":("a",4), "ặ":("ă",4), "ậ":("â",4), "ẹ":("e",4), "ệ":("ê",4), "ị":("i",4), "ọ":("o",4), "ộ":("ô",4), "ợ":("ơ",4), "ụ":("u",4), "ự":("ư",4), "ỵ":("y",4),
        "ả":("a",5), "ẳ":("ă",5), "ẩ":("â",5), "ẻ":("e",5), "ể":("ê",5), "ỉ":("i",5), "ỏ":("o",5), "ổ":("ô",5), "ở":("ơ",5), "ủ":("u",5), "ử":("ư",5), "ỷ":("y",5),
        "ã":("a",6), "ẵ":("ă",6), "ẫ":("â",6), "ẽ":("e",6), "ễ":("ê",6), "ĩ":("i",6), "õ":("o",6), "ỗ":("ô",6), "ỡ":("ơ",6), "ũ":("u",6), "ữ":("ư",6), "ỹ":("y",6),
    }
    TONE_MAX = 8 # 6 tones will be mapped to 8 tones (ru sheng counted as separeted tones)
    DEFAULT_TONE = "1"
    NUCLEUS = [
        'a',
        'ai', 'ay',
        'au',
        'ao',
        'â', 'ă',
        'ây',
        'âu',
        'y',
        #'yêu', 'ya', 'yê'
        'i',
        'ư',
        #'ươ',
        'u', 'uy',
        #'ua',
        'e', 'eo',
        'ê', 'êu',
        'o', 'oe',
        'ô', 'ôi',
        'ơ', 'ơu', 'ơi',
    ]

    def __init__(self, surface, is_tone_numeral = False):
        TonalSyllable.__init__(self, surface, is_tone_numeral)

    """
    analyzer
    """
    def preprocess_tone(self,):
        if self._is_tone_numeral == False:
            matched = False
            for c, (normalized_c, tone_num) in self.VOWELS_WITH_TONE.items():
                if self._surface.find(c) != -1:
                    self._surface = self._surface.replace(c, normalized_c) + str( tone_num )
                    matched = True
            if matched == False:
                self._surface += self.DEFAULT_TONE
        return
    def postprocess_last(self,):
        if self._last in ["c", "ch", "t", "p"]:
            if self._tone == 3:
                self._tone = 7
            if self._tone == 4:
                self._tone = 8
    def postprocess_nucleus(self,):
        if self._nucleus == '' and self._semi_vowel != '':
            ### adhoc
            if self._nucleus == '' and self._semi_vowel == 'iu':
                self._semi_vowel = 'i'
                self._nucleus = 'u'
            else:
                self._nucleus = self._semi_vowel
                self._semi_vowel = ''
        if self._nucleus == '' and self._semi_vowel == 'y':
            self._semi_vowel = ''
            self._nucleus = 'y'

class Hantu(Ideogram):
    def __init__(self, surfaces, is_tone_numeral = False):
        self._surfaces = []
        if type(surfaces) == str:
            self._surfaces.append( VietnameseSyllable( surfaces , is_tone_numeral ) )
        elif type(surfaces) == list:
            for s in surfaces:
                self._surfaces.append( VietnameseSyllable(s, is_tone_numeral ) )
        else:
            raise ValueError("Invalid surace")


def main():
    original = "quôc3"
    ht = Hantu(original, is_tone_numeral=True)
    print ( "original: " +  original + ", split: " + str(ht) )

    original = "quốc"
    ht = Hantu(original, is_tone_numeral=False)
    print ( "original: " +  original + ", split: " + str(ht) )

    original = "Ngữ"
    ht = Hantu(original, is_tone_numeral=False)
    print ( "original: " +  original + ", split: " + str(ht) )

if __name__ == '__main__':
    main()

