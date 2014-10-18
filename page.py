# coding: utf-8

import re

class Page:
    def __init__(self, url):
        self._url = url
        self._html = self.get_html()
        return
    def get_html(self,):
        import urllib2
        response = urllib2.urlopen(self._url)
        return response.read()
    # override me
    def get_hrefs(self,):
        from BeautifulSoup import BeautifulSoup as bs
        soup = bs(self._html)
        return soup.findAll('a')
    """
    def get_href(self,):
        import lxml.html
        res = []
        dom = lxml.html.fromstring(self._html.decode('utf-8'))
        for a in dom.xpath('//a'):
            href = a.get('href')
            if self.is_valid_href(href):
                res.append(href)
        return res
    """
    # override me
    def get_table(self, target_data_type = []):
        res = {}

        from BeautifulSoup import BeautifulSoup as bs
        #print self._html
        soup = bs(self._html)

        for table in soup.findAll("table", border=1):
            for row in table.findAll('tr')[1:]:
                col = row.findAll('td')
                try:
                    res[col[0]] = col[1:]
                except IndexError:
                    pass
        return res
    def is_valid_href(self, href, check_extention = False):
        import urlparse
        if not href:
            return False
        parsed = urlparse.urlparse(href)
        if check_extention and parsed.path.endwith(VALID_EXTENTION):
            return False
        #if parsed.netloc == False:
        #    return False
        return True

