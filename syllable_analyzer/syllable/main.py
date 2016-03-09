# -*- coding: utf-8 -*-

import os,sys
import re

from syllable import SyllableError
from mandarin.hanzi import Hanzi
from cantonese.honzi import Honzi
from japanese.kanji import Kanji
from korean.hanja import Hanja
from vietnamese.hantu import Hantu

SOURCE_URL_PATH_BASE = os.path.dirname(os.path.abspath(__file__)) + "/../../crawler/unihan/dict_tsv/%d.tsv"

mandarin_nucleus = ['i', '&#xfc;e', 'v', 'ao', '&#xfc;', 'o', 'ai', 'a', 'ue', 'ou', 'ua', 'u', 'er', 'e', 'ei',]

def remove_bracket(v):
    pat = re.compile(u"\(\d+\)")
    return re.sub(pat, "", v)

def split(v):
    pat = re.compile(u"\s+")
    return re.split(pat, v)


def main():
    r = {}
    for i in range(1, 30):
        filename = SOURCE_URL_PATH_BASE %i
        try:
            f = open(filename)
            for l in f.readlines():
                l = l.rstrip("\n")
                #l = l.encode("utf-8")
                try:
                    (char, ja, ko, ko_roman, man, man_num, can, viet, tang) = l.split(u"\t")
                    #print ("%s,%s,%s,%s,%s,%s,%s,%s,%s" %(char, ja, ko, ko_roman, man, man_num, can, viet, tang))
                    if len(man) > 0:
                        #sys.stderr.write("%s\n" %man)
                        hz = Hanzi(split(man), is_tone_numeral = False)
                        #print (str(hz))
                        for s in hz._surfaces:
                            r[s._nucleus] = {}
                            if s._nucleus not in mandarin_nucleus:
                                sys.stderr.write("----%s,%s\n" %(l, str(hz)) )
                    """
                    if len(man_num) > 0:
                        man_num = remove_bracket(man_num)
                        #sys.stderr.write("%s\n" %man_num)
                        hz = Hanzi(split(man_num), is_tone_numeral = True)
                        #print (str(hz))
                        for s in hz._surfaces:
                            r[s._nucleus] = {}
                            if s._nucleus not in mandarin_nucleus:
                                sys.stderr.write("----%s,%s\n" %(l, str(hz)) )
                    """
                except TypeError:
                    sys.stderr.write("TypeError skipped: %s\n" %l)
                except ValueError:
                    sys.stderr.write("ValueError skipped: %s\n" %l)
                except SyllableError as e:
                    sys.stderr.write("%s skipped: %s\n" %(e.value, l) )
        finally:
            f.close()
    print (r.keys())
    return

if __name__ == '__main__':
    main()

