# -*- coding: utf-8 -*-

import os,sys
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../syllable/')

import re
import getopt


from syllable import SyllableError
from mandarin.hanzi import Hanzi
from cantonese.honzi import Honzi
from japanese.kanji import Kanji
from korean.hanja import Hanja
from vietnamese.hantu import Hantu

SOURCE_PATH_BASE = os.path.dirname(os.path.abspath(__file__)) + "/../../crawler/unihan/dict_tsv/%d.tsv"

def remove_bracket(v):
    pat = re.compile(u"\(\d+\)")
    return re.sub(pat, "", v)

def split(v):
    pat = re.compile(u"\s+")
    return re.split(pat, v)

def usage():
    #TODO
    return

def get_transaction_from_hanzi(hz):
    if hz == '':
        return ''
    return list( hz.make_transaction2( with_header = True ) )

def write_to_file(output_filename, result):
    of = open(output_filename, 'w+')
    try:
        for l in result:
            #l = l.encode("utf-8")
            of.write( "%s\n" %l )
    finally:
        of.close()

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

    output_filename = os.path.dirname(os.path.abspath(__file__)) + "/../../rule_extractor/%s/all.txt" %(lang)
    f_result = []
    for i in range(1, 30):
        source_filename = SOURCE_PATH_BASE %i
        try:
            sf = open(source_filename)
            for l in sf.readlines():
                hz = None
                l = l.rstrip("\n")
                #l = l.encode("utf-8")
                line_r = []
                try:
                    (char, ja, ko, ko_roman, mand, mand_num, cant, viet, tang) = l.split(u"\t")
                    if lang == 'mandarin':
                        if mand != '': hz = Hanzi( split(mand), is_tone_numeral = False )
                    if lang == 'cantonese':
                        if cant != '': hz = Honzi( split(cant) )
                    if lang == 'korean':
                        if ko   != '': hz = Hanja( split(ko_roman) )
                    if lang == 'vietnamese':
                        if viet != '': hz = Hantu( split(viet) )
                    if lang == 'japanese':
                       if ja   != '': hz = Kanji( split(ja) )
                    if hz:
                        transaction_list = get_transaction_from_hanzi( hz )
                        if len(transaction_list) > 0:
                            f_result += transaction_list
                #except TypeError:
                #    sys.stderr.write("TypeError. skipped: %s\n" %l)
                #except ValueError:
                #    sys.stderr.write("ValueError. skipped: %s\n" %l)
                except SyllableError as e:
                    sys.stderr.write("%s. skipped: %s\n" %(e.value, l) )
        finally:
            sf.close()
    write_to_file(output_filename, f_result)
    return


if __name__ == '__main__':
    main()

