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
OUTPUT_PATH_BASE = os.path.dirname(os.path.abspath(__file__)) + "/../../rule_extractor/vietnamese/all.txt"

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
    return list( hz.make_transaction() )

def write_to_file(output_filename, result):
    of = open(output_filename, 'w+')
    try:
        for l in result:
            #l = l.encode("utf-8")
            of.write( "%s\n" %l )
    finally:
        of.close()

def main():
    output_filename = OUTPUT_PATH_BASE
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
                    #if mand != '': hz = Hanzi( split(mand), is_tone_numeral = False )
                    #if cant != '': hz = Honzi( split(cant) )
                    #if ko   != '': hz = Hanja( split(ko_roman) )
                    if viet != '': hz = Hantu( split(viet) )
                    #if ja   != '': hz = Kanji( split(ja) )
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

