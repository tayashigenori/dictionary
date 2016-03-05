# coding: utf-8

ENCODING="shift-jis"

import sys, os
import re
import json

class JsonParser:
    SEP = u",(?={)"
    KEYS = ["kJapaneseOn",
            "kHangul", "kKorean",
            "kMandarin", "kHanyuPinlu",
            "kCantonese",
            "kVietnamese",
            "kTang",]
    def __init(self,):
        return
    def get_list_from_file(self, filename):
        r = []
        pat = re.compile(self.SEP)
        try:
            f = open(filename)
            for l in f.readlines():
                l = unicode(l.strip(), 'utf-8')
                (k,v) = pat.split(l)
                r.append( [k] + self.get_list_from_json(v) )
        finally:
            f.close()
        return r
    def get_list_from_json(self, j):
        r = []
        d = json.loads(j)
        for k in self.KEYS:
            r.append( d.get(k, "") )
        return r

def save_list(l_list, filename):
    SEP = u"\t"
    f = open(filename, "w+")
    try:
        for l in l_list:
            f.write( ("%s\n" %SEP.join(l)).encode('utf8') )
    finally:
        f.close()
    return

def main():
    JP = JsonParser()
    for stroke in range(1, 65):
        input_filename = os.path.join("./dict/", "%s.txt" %(stroke))
        output_filename = os.path.join("./dict_tsv/", "%s.tsv" %(stroke))
        res = JP.get_list_from_file(input_filename)
        save_list(res, output_filename)

if __name__ == '__main__':
    main()
