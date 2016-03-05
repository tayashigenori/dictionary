#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, codecs
sys.stdout = codecs.getwriter('shift-jis')(sys.stdout)
sys.stderr = codecs.getwriter('shift-jis')(sys.stderr)

sep = u"　"
sep_colon = u"："

def get_kr():
    tmp = {}
    file_name = "./han_viet.txt"
    try:
        f = open(file_name)
        for line in f.readlines():
            line = unicode(line.strip(), 'utf-8')
            if line == "":
                continue
            li = line.split(sep)
            grade = li[0].strip()
            kr_pairs = li[1:]
            tmp[ grade ] = kr_pairs
    finally:
        f.close()
    r = {}
    #print tmp
    for grade, kr_pairs in tmp.items():
        r[grade] = {}
        for kr_pair in kr_pairs:
            kr_pair = kr_pair.strip()
            if kr_pair == "":
                continue
            #print kr_pair
            (kanji, reading) = kr_pair.split(sep_colon)
            reading = reading.replace(u",", u" | ")
            r[ grade ].update( { kanji.strip():
                                 reading.strip() } )
    return r

def save_kr(kr):
    file_name = "./han_viet.csv"
    try:
        f = open(file_name, 'w')
        for grade, kr_pair in kr.items():
            for kanji, reading in kr_pair.items():
                message = u"%s,%s,%s\n" %(grade, kanji, reading)
                f.write(message.encode("utf-8"))
    finally:
        f.close()

def main():
    kr_dict = get_kr()
    save_kr(kr_dict)
    return

if __name__ == '__main__':
    main()
