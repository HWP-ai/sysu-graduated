#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
from urlparse import urljoin

class APIError(StandardError):
    '''
    raise APIError if got failed.
    '''
    def __init__(self, error_msg, *args):
        self.error_msg = error_msg
        self.args = args;
        StandardError.__init__(self, error_msg % self.args)

    def __str__(self):
        return 'APIError: %s' % (self.error_msg % self.args)

class SysuGraduatedAPIClient:

    '''API client loads data.'''

    _DIGESTABLE = [
        'photo',
        'joke',
        'discounts',
        'message',
        'enterprise'
    ]

    def __init__(self,
                 entry="https://sysu.github.io/graduated/index.html"):
        self._entry = entry
        self._digested_all = None
        self._digested = {}

    def _digest(self, code):
        if self._digested_all == None:
            req = requests.get(self._entry).text
            self._digested_all = pq(req)
        if code in self._digested:
            return True
        table = self._digested_all.find('#%s tbody tr' % code)
        buf = []
        for ele in table:
            if ele.get('class') == 'no':
                continue
            tds = ele.getchildren()
#            if len(tds) == 1 :
#                continue
            if code == 'photo':
                f1 = tds[0].find('img')
                if f1 is not None:
                    f1 = urljoin(self._entry, f1.get('src'))
                else:
                    f1 = ''
                f2 = pq(tds[1]).html().strip()
                links = []
                aaa = tds[2].find('a')
                if aaa is not None:
                    aaa = aaa.iter()
                    for link in aaa:
                        links.append({
                            'text': pq(link).html(),
                            'href': urljoin(self._entry, link.get('href'))
                        })
                buf.append({
                    'photo' : {
                        'src' : f1
                    },
                    'explain' : {
                        'text': f2,
                    },
                    'links' : links 
                })
            elif code == 'joke':
                recorder = tds[1].find('a')
                source = tds[3].find('a')
                buf.append({
                    'record_in': {
                        'text': pq(tds[0]).html().strip()
                    },
                    'recorder': {
                        'text': pq(recorder).html().strip(),
                        'href': recorder.get('href'),
                    },
                    'jokeee': {
                        'text': pq(tds[2]).html(),
                    },
                    'source': {
                        'text': pq(source).html(),
                        'href': source.get('href')
                    }
                })
            elif code == 'discounts':
                buf.append({
                    'unit': {
                        'html': pq(tds[0]).html().strip(),
                    },
                    'constrain': {
                        'html': pq(tds[1]).html().strip(),
                    },
                    'earning': {
                        'html': pq(tds[2]).html().strip(),
                    }
                })
            elif code == 'message':
                buf.append({
                    'datetime': {
                        'html': pq(tds[0]).html().strip(),
                    },
                    'school': {
                        'html' : pq(tds[1]).html().strip(),
                    },
                    'degree': {
                        'html' : pq(tds[2]).html().strip(),
                    },
                    'notes': {
                        'html' : pq(tds[3]).html().strip(),
                    },
                    'person': {
                        'html' : pq(tds[4]).html().strip(),
                    }                    
                })
            elif code == 'enterprise':
                buf.append({
                    'sponsor': {
                        'html': pq(tds[0]).html().strip(),
                    },
                    'keywords': {
                        'html' : pq(tds[1]).html().strip(),
                    },
                    'notice': {
                        'html' : pq(tds[2]).html().strip(),
                    },
                    'channel': {
                        'html' : pq(tds[3]).html().strip(),
                    }
                })
        self._digested[code] = buf
        return True
    
    def data_iter(self, code):
        if code not in self._DIGESTABLE :
            raise APIError('No such table %s', code)
        if code not in self._digested :
            self._digest(code)
        return iter(self._digested[code])

    def req(self, code, index):
        if code not in self._DIGESTABLE :
            raise APIError('No such table %s', code)
        if code not in self._digested :
            self._digest(code)
        buf = self._digested[code]
        if (index >= 0) and (index < len(buf)):
            return buf[index]
        else:
            return None

    def count(self, code):
        if code not in self._DIGESTABLE :
            raise APIError('No such table %s', code)
        if code not in self._digested :
            self._digest(code)
        return len(self._digested[code])

if __name__ == '__main__':
    a = SysuGraduatedAPIClient()
    for code in [
            'photo',
            'joke',
            'discounts',
            'message',
            'enterprise'
    ]:
        print '----[[ %s ]]----' % code
        for it in a.data_iter(code):
            print it
            print
        print 'data for %s total: %s' % (code, a.count(code))
        print
