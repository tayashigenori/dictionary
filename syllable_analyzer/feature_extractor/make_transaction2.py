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
OUTPUT_PATH_BASE = os.path.dirname(os.path.abspath(__file__)) + "/transaction2/%d.tsv"
SEP="\t"
EMPTY_LINE = SEP.join( ["", "", "", "", ""] )

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
    if hz == EMPTY_LINE:
        return EMPTY_LINE
    l = list( hz.make_transaction2() )
    return SEP.join( l )

def write_to_file(output_filename, result):
    of = open(output_filename, 'w+')
    try:
        for l in result:
            #l = l.encode("utf-8")
            of.write( "%s\n" %l )
    finally:
        of.close()

def main():
    for i in range(1, 30):
        f_result = []
        source_filename = SOURCE_PATH_BASE %i
        output_filename = OUTPUT_PATH_BASE %i
        try:
            sf = open(source_filename)
            for l in sf.readlines():
                l = l.rstrip("\n")
                #l = l.encode("utf-8")
                line_r = []
                try:
                    (char, ja, ko, ko_roman, mand, mand_num, cant, viet, tang) = l.split(u"\t")
                    line_r.append( Hanzi( split(mand), is_tone_numeral = False) if mand != "" else EMPTY_LINE)
                    line_r.append( Honzi( split(cant) )                         if cant != "" else EMPTY_LINE)
                    line_r.append( Hanja( split(ko_roman) )                     if ko   != "" else EMPTY_LINE)
                    line_r.append( Hantu( split(viet) )                         if viet != "" else EMPTY_LINE)
                    line_r.append( Kanji( split(ja) )                           if ja   != "" else EMPTY_LINE)
                    transaction_list = list( map( get_transaction_from_hanzi, line_r) )
                    f_result.append( SEP.join( [char] + transaction_list )  )
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

