# coding: utf-8

WIKTIONARY_URL_BASE = "http://en.wiktionary.org/wiki/Index:Chinese_total_strokes/%d"
UNIHAN_URL_BASE = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=%s"

DICT_PATH_BASE = "./dict/%d.txt"
DICT_SEPATATOR = ","

STROKES_UPPER = 65

import sys,os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from page import Page

class WiktionaryPage(Page):
    """
    LANGS = {'Chinese':
             # Chinese is not a language but a set of languages
             ['Mandarin', 'Cantonese', 'Hakka', 'Min Nan', 'Wu']}
    ORTHO = {'Mandarin': ['Pinyin', 'Zhuyin',],
             'Cantonese': ['Jyutping',],
             'Hakka': ['Pha̍k-fa-sṳ',],
             'Min Nan': ['POJ',],
             'Wu': ['WT Romanisation',]
             }
    READINGS = {'Japanese': ['Goon', "Kan'on"]}
    """
    def get_hrefs(self,
                  href_pattern = "^/wiki/",
                  text_pattern = "^.$"
                  ):
        from BeautifulSoup import BeautifulSoup as bs
        #print self._html
        soup = bs(self._html)
        return soup.findAll('a',
                            href=re.compile(href_pattern),
                            text=re.compile(text_pattern),
                            )

def process(stroke):
    dictname = DICT_PATH_BASE %(stroke)
    f = open(dictname, 'w+')
    try:
        target_url = WIKTIONARY_URL_BASE %(stroke)
        sys.stderr.write("getting resource: %s\n" %target_url)
        page = WiktionaryPage(target_url)
        for codepoint in page.get_hrefs():
            codepoint = codepoint.strip()
            if codepoint:
                #d  = [codepoint]
                d = [UNIHAN_URL_BASE %(codepoint)]
                f.write(DICT_SEPATATOR.join(d).encode('utf-8'))
                f.write("\n")
    except:
        sys.stderr.write("could not get resource: %s\n" %target_url)
        pass
    finally:
        f.close()
    return

def main():
    for stroke in range(21, STROKES_UPPER):
        process(stroke)

if __name__ == '__main__':
    main()
