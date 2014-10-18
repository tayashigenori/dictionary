# coding: utf-8

from page import Page
import re

class UnihanPage(Page):
    DATA_TYPE = ['kCantonese', 'kMandarin', 'kTang',
                 # 'kHanyuPinlu', 'kHanyuPinyin', 'kXHC1983',
                 'kHangul', 'kKorean',
                 'kJapaneseOn',
                 # 'kJapaneseKun',
                 'kVietnamese', ]
    def get_dictionary(self,):
        return self.get_table(self.DATA_TYPE)


def main():
    # urls are supposed to be stored in file
    UNIHAN_URL_BASE = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=%s"
    codepoint = "4E00"
    target_url = UNIHAN_URL_BASE %(codepoint)
    pages = [target_url]
    for page in pages:
        page = UnihanPage(target_url)
        print page.get_dictionary()

if __name__ == '__main__':
    main()
