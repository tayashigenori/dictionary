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
OUTPUT_PATH_BASE = os.path.dirname(os.path.abspath(__file__)) + "/split/%d.tsv"

def remove_bracket(v):
    pat = re.compile(u"\(\d+\)")
    return re.sub(pat, "", v)

def split(v):
    pat = re.compile(u"\s+")
    return re.split(pat, v)

def usage():
    #TODO
    return

def get_csv_from_hanzi(hz):
    if hz == '':
        return ''
    r = []
    for sur in hz._surfaces:
        l = [str(part) for part in sur.__list__()]
        r.append( ",".join( l ) )
    return "|".join(r)

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
                                   "t:",
                                   ["type="])
    except getopt.GetoptError as err:
        # ヘルプメッセージを出力して終了
        print ( str(err) ) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    t = None
    for o, a in opts:
        if o in ("-t", "--type"):
            t = a
        else:
            assert False, "unhandled option"

    if t == None:
        usage()
        sys.exit(2)

    for i in range(1, 30):
        source_filename = SOURCE_PATH_BASE %i
        output_filename = OUTPUT_PATH_BASE %i
        f_result = []
        try:
            sf = open(source_filename)
            for l in sf.readlines():
                l = l.rstrip("\n")
                #l = l.encode("utf-8")
                line_r = []
                try:
                    (char, ja, ko, ko_roman, mand, mand_num, cant, viet, tang) = l.split(u"\t")
                    if t.lower() in ["split"]:
                        line_r.append( Hanzi( split(mand), is_tone_numeral = False) if mand != '' else '' )
                        line_r.append( Honzi( split(cant) )                         if cant != '' else '' )
                        line_r.append( Hanja( split(ko_roman) )                     if ko   != '' else '' )
                        line_r.append( Hantu( split(viet) )                         if viet != '' else '' )
                        line_r.append( Kanji( split(ja) )                           if ja   != '' else '' )
                        csv_list = list( map( get_csv_from_hanzi, line_r) )
                        f_result.append( "\t".join( [char] + csv_list ) )

                except TypeError:
                    sys.stderr.write("TypeError. skipped: %s\n" %l)
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

