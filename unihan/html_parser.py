# coding: utf-8

SOURCE_URL_PATH_BASE = "../wiktionary/dict/%d.txt"

DICT_PATH_BASE = "./dict/%d.txt"
DICT_SEPARATOR = ","

STROKES_UPPER = 21

import re, json
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from page import Page

class UnihanPage(Page):
    DATA_TYPE = ['kCantonese', 'kMandarin', 'kTang',
                 # 'kHanyuPinlu', 'kHanyuPinyin', 'kXHC1983',
                 'kHangul', 'kKorean',
                 'kJapaneseOn',
                 # 'kJapaneseKun',
                 'kVietnamese', ]
    def get_dictionary(self,):
        return self.get_table(self.DATA_TYPE)

    def get_table(self, target_data_type = []):
        res = {}

        from BeautifulSoup import BeautifulSoup as bs
        #print self._html
        soup = bs(self._html)

        for table in soup.findAll("table", border=1):
            for row in table.findAll('tr')[1:]:
                col = row.findAll('td')
                try:
                    #data_type = col[0].find('a').text
                    data_type = col[0].text
                    data = col[1].text
                    if data_type in target_data_type:
                        res[data_type] = data
                except IndexError:
                    pass
        return res

def store_dictionary(dictname, readings):
    f_d = open(dictname, 'w+')
    try:
        for codepoint,v in readings.items():
            d  = [codepoint]
            d += [json.dumps(v)]
            f_d.write(DICT_SEPARATOR.join(d))
            f_d.write("\n")
    finally:
        f_d.close()

def get_dictionary_from_source_url(source_url_name):
    res = {}
    f_s = open(source_url_name,)
    try:
        for url in f_s.readlines():
            codepoint = url.split("codepoint=")[1].strip()
            page = UnihanPage(url)
            res[codepoint] = page.get_dictionary()
    finally:
        f_s.close()
    return res

def main():
    # urls are supposed to be stored in file
    #UNIHAN_URL_BASE = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=%s"
    #codepoint = "4E00"
    #target_url = UNIHAN_URL_BASE %(codepoint)
    #pages = [target_url]
    for stroke in range(1, STROKES_UPPER):
        # get url and parse
        source_url_name = SOURCE_URL_PATH_BASE %(stroke)
        readings = get_dictionary_from_source_url(source_url_name)
        # store
        dictname = DICT_PATH_BASE %(stroke)
        store_dictionary(dictname, readings)

if __name__ == '__main__':
    main()
