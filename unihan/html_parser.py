# coding: utf-8

import re
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
