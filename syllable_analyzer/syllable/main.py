# -*- coding: utf-8 -*-

import os,sys
import re
import getopt

from syllable import SyllableError
from mandarin.hanzi import Hanzi
from cantonese.honzi import Honzi
from japanese.kanji import Kanji
from korean.hanja import Hanja
from vietnamese.hantu import Hantu

SOURCE_URL_PATH_BASE = os.path.dirname(os.path.abspath(__file__)) + "/../../crawler/unihan/dict_tsv/%d.tsv"

mandarin_nucleus = [
        'a', 'ai', 'ao',
        'i',
        'u',
        'v',
        'e', 'ei', 'er',
        'o', 'ou',
]
cantonese_nucleus = [
        'a', 'aa', 'ai', 'aai', 'au', 'aau',
        'i',
        'u',
        'o', 'oi', 'ou', 'oe',
        'e', 'ei', 'eu', 'eo', 'eoi',
        '@',
]

def remove_bracket(v):
    pat = re.compile(u"\(\d+\)")
    return re.sub(pat, "", v)

def split(v):
    pat = re.compile(u"\s+")
    return re.split(pat, v)

def usage():
    #TODO
    return

def process_mand(mand, mand_num, l):
    r = {}
    if len(mand) > 0:
        #sys.stderr.write("%s\n" %mand)
        hz = Hanzi(split(mand), is_tone_numeral = False)
        #print (str(hz))
        for s in hz._surfaces:
            r[s._nucleus] = {}
            if s._nucleus not in mandarin_nucleus:
                sys.stderr.write("----invalid nucleus %s,%s\n" %(l, str(hz)) )
    if len(mand_num) > 0:
        mand_num = remove_bracket(mand_num)
        #sys.stderr.write("%s\n" %mand_num)
        hz = Hanzi(split(mand_num), is_tone_numeral = True)
        #print (str(hz))
        for s in hz._surfaces:
            r[s._nucleus] = {}
            if s._nucleus not in mandarin_nucleus:
                sys.stderr.write("----invalid nucleus %s,%s\n" %(l, str(hz)) )
    return r

def process_cant(cant, l):
    r = {}
    if len(cant) > 0:
        #sys.stderr.write("%s\n" %cant)
        hz = Honzi(split(cant))
        #print (str(hz))
        for s in hz._surfaces:
            r[s._nucleus] = {}
            if s._nucleus not in cantonese_nucleus:
                sys.stderr.write("----invalid nucleus %s,%s\n" %(l, str(hz)) )
    return r

def main():
    # get options
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "l:",
                                   ["language="])
    except getopt.GetoptError as err:
        # ヘルプメッセージを出力して終了
        print ( str(err) ) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    lang = None
    for o, a in opts:
        if o in ("-l", "--language"):
            lang = a
        else:
            assert False, "unhandled option"

    if lang == None:
        usage()
        sys.exit(2)

    r = {}
    for i in range(1, 30):
        filename = SOURCE_URL_PATH_BASE %i
        try:
            f = open(filename)
            for l in f.readlines():
                l = l.rstrip("\n")
                #l = l.encode("utf-8")
                try:
                    (char, ja, ko, ko_roman, mand, mand_num, cant, viet, tang) = l.split(u"\t")
                    #print ("%s,%s,%s,%s,%s,%s,%s,%s,%s" %(char, ja, ko, ko_roman, man, man_num, can, viet, tang))
                    if lang.lower() in ["m", "man", "mand", "mandarin"]:
                        r.update ( process_mand(mand, mand_num, l) )
                    elif lang.lower() in ["c", "can", "cant", "cantonese"]:
                        r.update ( process_cant(cant, l) )

                #except TypeError:
                #    sys.stderr.write("TypeError skipped: %s\n" %l)
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

