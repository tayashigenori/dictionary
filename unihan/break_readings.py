# coding: utf-8

import sys, os
import re
import json

#from json_parser import JsonParser

def join_dict(d1, d2, sep = " "):
    return dict([ (k, # key
                   sep.join( [d1.get(k, ""), d2.get(k, "")] ).strip() # value
                   ) for k in d1.keys() # iterate over k
                  ] # to generate list
                ) # and convert to dict: k -> v

class ReadingBreakerDispatcher:
    # {"kHangul": "\uc77c",
    # "kMandarin": "y\u012b",
    # "kKorean": "IL",
    # "kVietnamese": "nh\u1ea5t",
    # "kCantonese": "jat1",
    # "kJapaneseOn": "ICHI ITSU",
    # "kHanyuPinlu": "yi1(32747)",
    # "kTang": "*qit qit"}
    def __init__(self, lang):
        if lang == 'kMandarin':
            self._inst = ReadingBreakerMand()
        elif lang == 'kKorean':
            self._inst = ReadingBreakerKore()
        elif lang == 'kVietnamese':
            self._inst = ReadingBreakerViet()
        elif lang == 'kCantonese':
            self._inst = ReadingBreakerCant()
        elif lang == 'kJapaneseOn':
            self._inst = ReadingBreakerJapa()
        elif lang == 'kHanyuPinlu':
            self._inst = ReadingBreakerPinl()
        elif lang == 'kTang':
            self._inst = ReadingBreakerTang()
        else:
            raise ValueError
    def process(self, col):
        res = {}
        for r in self._inst.get_readings(col):
            res = join_dict(self._inst.break_reading( r ), res )
        return res

class ReadingBreaker:
    SEP = " "
    def __init__(self,):
        self.pat_head_c = re.compile("^" + "(" + "|".join(self.HEAD_C) + ")")
        self.pat_last_c = re.compile("(" + "|".join(self.LAST_C) + ")" + "$")
        self.pat_tone   = re.compile("(" + "|".join(self.TONE) + ")" + "$")
    def get_readings(self, col):
        return col.split(self.SEP)
    def break_reading(self, reading):
        res = {}
        # tone
        match_tone = re.search(self.pat_tone, reading)
        if match_tone: res[self.COLNAME_TONE] = match_tone.group(0)
        else:
            res[self.COLNAME_TONE] = ""
        reading = re.sub(self.pat_tone, "", reading)

        # head_c (initial consonants)
        match_head_c = re.search(self.pat_head_c, reading)
        if match_head_c: res[self.COLNAME_HEAD_C] = match_head_c.group(0)
        else:
            res[self.COLNAME_HEAD_C] = ""
        # tail (wthout head_c)

        res[self.COLNAME_TAIL] = re.sub(self.pat_head_c, "", reading)
        # last_c (ending consonants)
        match_last_c = re.search(self.pat_last_c, reading)
        if match_last_c: res[self.COLNAME_LAST_C] = match_last_c.group(0)
        else:
            res[self.COLNAME_LAST_C] = ""
        # init (wthout last_c)
        res[self.COLNAME_INIT] = re.sub(self.pat_last_c, "", reading)

        # vowel (wthout head_c or last_c)
        res[self.COLNAME_VOWEL] = re.sub(self.pat_head_c, "", res[self.COLNAME_INIT])
        return res

class ReadingBreakerMand(ReadingBreaker):
    HEAD_C = ["b", "p", "m", "f", "d", "t", "n", "l",
              "z", "c", "s", "zh", "ch", "sh", "r",
              "x", "j", "q", "g", "k", "h",]
    LAST_C = ["ng", "n",]
    SEMI_VOWELS = ["y", "w",]
    TONE = []
    COLNAME_HEAD_C = "MandarinHeadC"
    COLNAME_TAIL   = "MandarinTail"
    COLNAME_LAST_C = "MandarinLastC"
    COLNAME_INIT   = "MandarinInit"
    COLNAME_VOWEL  = "MandarinVowel"
    COLNAME_TONE   = "MandarinTone"

class ReadingBreakerKore(ReadingBreaker):
    HEAD_C = ["G", "N", "D", "R", "M", "B", "S",
              "J", "CH", "K", "T", "P", "H",]
    LAST_C = ["K", "T", "P",
              "NG", "L", "M",]
    TONE = []
    COLNAME_HEAD_C = "KoreanHeadC"
    COLNAME_TAIL   = "KoreanTail"
    COLNAME_LAST_C = "KoreanLastC"
    COLNAME_INIT   = "KoreanInit"
    COLNAME_VOWEL  = "KoreanVowel"
    COLNAME_TONE   = "KoreanTone" #

class ReadingBreakerViet(ReadingBreaker):
    HEAD_C = []
    LAST_C = []
    TONE = []
    COLNAME_HEAD_C = "VietnameseHeadC"
    COLNAME_TAIL   = "VietnameseTail"
    COLNAME_LAST_C = "VietnameseLastC"
    COLNAME_INIT   = "VietnameseInit"
    COLNAME_VOWEL  = "VietnameseVowel"
    COLNAME_TONE   = "VietnameseTone"

class ReadingBreakerCant(ReadingBreaker):
    HEAD_C = ["b", "p", "m", "f", "d", "t", "n", "l",
              "z", "c", "s", "zh", "ch", "sh", "r",
              "x", "j", "q", "g", "k", "h",]
    LAST_C = ["ng", "n", "m",
              "k", "t", "p",]
    TONE = [str(i) for i in range(1,10)]
    COLNAME_HEAD_C = "CantoneseHeadC"
    COLNAME_TAIL   = "CantoneseTail"
    COLNAME_LAST_C = "CantoneseLastC"
    COLNAME_INIT   = "CantoneseInit"
    COLNAME_VOWEL  = "CantoneseVowel"
    COLNAME_TONE   = "CantoneseTone"

class ReadingBreakerJapa(ReadingBreaker):
    HEAD_C = ["K", "S", "T", "N", "H", "M", "R",
                "G", "Z", "D",      "B",]
    LAST_C = ["KI", "KU", "CHI", "TSU", "N"]
    SEMI_BOWELS = ["Y", "W"]
    TONE = []
    COLNAME_HEAD_C = "JapaneseHeadC"
    COLNAME_TAIL   = "JapaneseTail"
    COLNAME_LAST_C = "JapaneseLastC"
    COLNAME_INIT   = "JapaneseInit"
    COLNAME_VOWEL  = "JapaneseVowel"
    COLNAME_TONE   = "JapaneseTone" #

class ReadingBreakerPinl(ReadingBreakerMand):
    TONE = [str(i) for i in range(1,5)]
    COLNAME_HEAD_C = "PinluHeadC"
    COLNAME_TAIL   = "PinluTail"
    COLNAME_LAST_C = "PinluLastC"
    COLNAME_INIT   = "PinluInit"
    COLNAME_VOWEL  = "PinluVowel"
    COLNAME_TONE   = "PinluTone"
    def get_readings(self, col):
        # remove frequency info
        pat = re.compile("\([0-9]+\)")
        return map(lambda x: re.sub(pat, "", x), ReadingBreaker.get_readings(self, col) )

class ReadingBreakerTang(ReadingBreaker):
    HEAD_C = ["b", "p", "m", "f", "d", "t", "n", "l",
              "z", "c", "s", "zh", "ch", "sh", "r",
              "x", "j", "q", "g", "k", "h",]
    LAST_C = ["ng", "n", "m",
              "k", "t", "p",]
    TONE = []
    COLNAME_HEAD_C = "TangHeadC"
    COLNAME_TAIL   = "TangTail"
    COLNAME_LAST_C = "TangLastC"
    COLNAME_INIT   = "TangInit"
    COLNAME_VOWEL  = "TangVowel"
    COLNAME_TONE   = "TangTone"
    def __init__(self,):
        ReadingBreaker.__init__(self)
        self.pat_head_c = re.compile("^" + "[*]?" + "(" + "|".join(self.HEAD_C) + ")")

def save_frequency_list(res, filename):
    f = open(filename, "w+")
    try:
        for l,v in res.items():
            f.write("%s" %l)
            f.write(",%s\n" %v)
    finally:
        f.close()
    return

def get_broken_readings(filename):
    #jp = JsonParser()
    res = {}
    f = open(filename)
    for line in f.readlines():
        sep = re.compile(",(?={)")
        (char, j) = re.split(sep, line.rstrip())
        char_vals = []
        #for lang, lang_col in jp.get_all_from_json(json).items():
        for lang, lang_col in json.loads(j).items():
            try:
                rb = ReadingBreakerDispatcher(lang)
                char_vals.append( str( (rb.process(lang_col)) ) )
            except ValueError:
                sys.stderr.write("No breaking defined for %s\n" %lang)
        res[char] = ",".join(char_vals)
    return res

def main():
    STROKE_MIN = 1
    STROKE_MAX = 5
    for stroke in range(STROKE_MIN, STROKE_MAX):
        input_filename = os.path.join("./dict/", "%s.txt" %(stroke))
        output_filename = os.path.join("./_partial/comparative/", "%s.txt" %(stroke))
        res = get_broken_readings(input_filename)
        save_frequency_list(res, output_filename)

if __name__ == '__main__':
    main()
