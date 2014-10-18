# coding: utf-8

WIKTIONARY_URL_BASE = "http://en.wiktionary.org/wiki/Index:Chinese_total_strokes/%d"
UNIHAN_URL_BASE = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=%s"

from page import Page
import re

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

def main():
    for strokes in range(1,2):
        target_url = WIKTIONARY_URL_BASE %(strokes)
        page = WiktionaryPage(target_url)
        for codepoint in page.get_hrefs():
            #print UNIHAN_URL_BASE %(codepoint.replace("\u", ""))
            print UNIHAN_URL_BASE %(codepoint)

if __name__ == '__main__':
    main()
