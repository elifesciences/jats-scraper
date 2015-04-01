import os
from elifetools import parseJATS as parser
from scraper.utils import fattrs

import logging

FORMAT = logging.Formatter("%(created)f - %(levelname)s - %(processName)s - %(name)s - %(message)s")
LOGFILE = "%s.log" % __file__

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

h = logging.FileHandler(LOGFILE)
h.setLevel(logging.INFO)
h.setFormatter(FORMAT)

logger.addHandler(h)

class ParserWrapper(object):
    def __init__(self, soup):
        self.soup = soup
        
    def __getattr__(self, attr):
        def awooga(*args,**kwargs):
            logger.warn('* WARNING: I have no attribute %s' % attr)
            return None
        return getattr(parser, attr, awooga)(self.soup)

def article_wrapper(path):
    soup = parser.parse_document(path)
    # return a wrapper around the parser module that injects the soup when a function is called
    return ParserWrapper(soup)

def unsupported():
    return '* not implemented *'

@fattrs('doc_root')
def article_list(doc_root):
    return map(article_wrapper, [
        os.path.join(doc_root, 'elife-kitchen-sink.xml'),
        os.path.join(doc_root, 'elife00013.xml'),
    ])

@fattrs('parent as article')
def author_list(article):
    x = article.authors
    return x

#
#
#

DESCRIPTION = [
    ('article', {
        'iterable': article_list,
        'attrs': {
            'jcode': 'this.journal_id',
            'jtitle': 'this.journal_title',
            'jissn': 'this.journal_issn',

            'state': 'unsupported',

            'title': 'this.title',
            'title_short': 'unsupported',
            
            'slug': 'unsupported',
            'subtitle': 'unsupported',

            'type': 'this.article_type',
            'doi': 'this.doi',
            'ppub': 'unsupported',
            'epub': 'unsupported',
            'fpub': 'unsupported',

            'first_page': 'unsupported',
            'last_page': 'unsupported',
            'issue': 'unsupported',
            'volume': 'unsupported',

            'category_list': 'unsupported',
            'keyword_list': ('this.keyword_group', None, str),

            'version': 'unsupported'
        },
        'subs': [
            ('authors', {
                'iterable': author_list,
                'attrs': {
                    'first_name': 'this.given_names',
                    'last_name': 'this.surname',
                    'suffix': 'this.suffix',
                    'institution': 'this.institution',
                },
            }),
        ] # ends article.subs block
    }) # ends article block
]

def main(args):
    if not len(args) == 1:
        print 'Usage: python feeds.py <xml dir>'
        exit(1)
    docs_dir = args[0]
    from scraper import scraper
    mod = __import__(__name__)
    res = scraper.scrape(mod, doc_root=docs_dir)
    import json
    print json.dumps(res, indent=4)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
