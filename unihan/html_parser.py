# coding: utf-8

SOURCE_URL_PATH_BASE = "../wiktionary/dict/%d.txt"

DICT_PATH_BASE = "./dict/%d.txt"
DICT_SEPARATOR = ","

VAR_PATH_BASE = "./var/%d.txt"
VAR_SEPARATOR = ","

STROKES_UPPER = 21

TARGET_READINGS = 1
TARGET_VARIANTS = 2

import re, json
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from page import Page

class UnihanPage(Page):
    READINGS_DATA_TYPE = ['kCantonese', 'kMandarin', 'kTang',
                          'kHanyuPinlu',
                          # 'kHanyuPinyin',
                          # 'kXHC1983',
                          'kHangul', 'kKorean',
                          'kJapaneseOn',
                          # 'kJapaneseKun',
                          'kVietnamese',
                         ]
    VARIANTS_DATA_TYPE = ['kSimplifiedVariant', 'kTraditionalVariant',
                          'kSemanticVariant', 'kSpecializedSemanticVariant',
                          'kZVariant', 'kCompatibilityVariant',
                          ]
    def get_readings(self,):
        return self.get_table(self.READINGS_DATA_TYPE)
    def get_variants(self,):
        return self.get_table(self.VARIANTS_DATA_TYPE)

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

def store_dictionary(dictname, values):
    f = open(dictname, 'w+')
    try:
        for v in values:
            f.write(v)
            f.write("\n")
    finally:
        f.close()

def get_from_source_url(source_url_name, target):
    res = []
    f_s = open(source_url_name,)
    try:
        for url in f_s.readlines():
            sys.stderr.write("getting resource: %s\n" %url)
            codepoint = url.split("codepoint=")[1].strip()
            try:
                page = UnihanPage(url)
            except:
                sys.stderr.write("could not get resource: %s\n" %url)
                continue

            if target == TARGET_READINGS:
                readings = json.dumps(page.get_readings())
                l = DICT_SEPARATOR.join([codepoint, readings])
            else:
                variants = json.dumps(page.get_variants())
                l = VAR_SEPARATOR.join([codepoint, variants])
            res.append(l)
    finally:
        f_s.close()
    return res

def main():
    # urls are supposed to be stored in file
    #UNIHAN_URL_BASE = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=%s"
    #codepoint = "4E00"
    #target_url = UNIHAN_URL_BASE %(codepoint)
    #pages = [target_url]
    target = TARGET_READINGS
    STROKES_UPPER = 65
    for stroke in range(1, 16):
        # get url and parse
        source_url_name = SOURCE_URL_PATH_BASE %(stroke)
        values = get_from_source_url(source_url_name, target)
        # store
        if target == TARGET_READINGS:
            dictname = DICT_PATH_BASE %(stroke)
        else:
            dictname = VAR_PATH_BASE %(stroke)
        store_dictionary(dictname, values)

if __name__ == '__main__':
    main()
