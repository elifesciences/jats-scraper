__author__ = 'Luke Skibinski <l.skibinski@elifesciences.org>, John Root<john.root@digirati.co.uk>'
__copyright__ = 'eLife Sciences'
__licence__ = 'GNU General Public License (GPL)'
__version__ = 0.1

import glob
import logging
from datetime import datetime
import time
import os
from elifetools import parseJATS as parser
from scraper.utils import fattrs
import re

_VERSION = "1"  # TODO change all uses of this to get article version information from ?

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

    def __getattr__(self, attr, *args, **kwargs):
        def awooga(*args, **kwargs):
            logger.warn('* WARNING: I have no attribute %s' % attr)
            return None

        return getattr(parser, attr, awooga)(self.soup, *args, **kwargs)


def article_wrapper(path):
    soup = parser.parse_document(path)
    # return a wrapper around the parser module that injects the soup when a function is called
    return ParserWrapper(soup)


def unsupported():
    return '* not implemented *'


def unknown():
    return '* source not known *'


def tidy_whitespace(string):
    string = re.sub('\n', ' ', string)
    string = re.sub(' +', ' ', string)
    return string


def footnote_text(raw_footnote_text):
    match = re.search('.*?<p>(.*?)</p>', raw_footnote_text, re.DOTALL)
    if match is None:
        return ""
    text = match.group(1)
    return text


@fattrs('doc')
def article_list(doc):
    if os.path.isfile(doc):
        return [article_wrapper(doc)]
    elif os.path.isdir(doc):
        return map(article_wrapper, glob.glob(doc + "*.xml"))
    elif doc.startswith("<?xml"):
        return [ParserWrapper(parser.parse_xml(doc))]


@fattrs('this as article')
def article_path(article):
    return 'content/' + article.volume + '/e' + article.publisher_id


@fattrs('this as article')
def issn_electronic(article):
    return article.journal_issn(pub_format='electronic')


@fattrs('this as article')
def article_full_version(article):
    return article.publisher_id + '.' + article_status(article) + '.' + str(_VERSION)


@fattrs('this as article')
def version(article):
    return _VERSION

@fattrs('this as article')
def issn_electronic(article):
    return article.__getattr__('journal_issn', pub_format='electronic')


@fattrs('this as article')
def article_status(article):
    return 'POA' if article.is_poa else 'VOR'


@fattrs('this as article')
def equal_contrib(article):
    equal_contribs = {}
    notes = article.__getattr__('full_author_notes', fntype_filter='equal-contrib')
    if notes is not None:
        for note in notes:
            equal_contribs[note['id']] = footnote_text(note['text'])
    return equal_contribs

@fattrs('this as article')
def present_address(article):
    addresses = {}
    notes = article.__getattr__('full_author_notes', fntype_filter='present-address')
    if notes is not None:
        for note in notes:
            addresses[note['id']] = tidy_whitespace(footnote_text(note['text']))
    return addresses


@fattrs('this as article')
def competing_interests(article):
    interests = {}
    conflicts = article.__getattr__('competing_interests', fntype_filter='conflict')
    if conflicts is not None:
        for conflict in conflicts:
            interests[conflict['id']] = footnote_text(conflict['text'])
    return interests


@fattrs('this as article')
def contributors(article):
    return ['* not implemented *']  # TODO implement


@fattrs('this as article')
def affiliations(article):
    return ['* not implemented *']  # TODO implement


@fattrs('this as article')
def children(article):
    return ['* not implemented *']  # TODO implement


DESCRIPTION = [
    ('article', {
        'iterable': article_list,
        'attrs': {
            #'journal_id': 'this.journal_id',
            #'journal_title': 'this.journal_title',
            #'eissn': 'issn_electronic',
            #'journal_issn': 'unsupported',  # TODO issue with params for 'issn_electronic',
            'title': ('this.title', None, tidy_whitespace),
            #'impact-statement': 'unsupported',  # TODO custom-meta-group
            'version': 'version',
            'doi': 'this.doi',
            'publish': ('"1"', "1", str),  # 1 or 0 means publish immediately or don't publish immediately
            'force': ('"1"', "1", str),  # overwrite if present
            'volume': ('this.volume', "0", str),
            'article-id': 'this.doi',
            'article-version-id': 'article_full_version',
            'pub-date': ('this.pub_date', None, lambda t: datetime.fromtimestamp(time.mktime(t)).strftime("%Y-%m-%d")),
            'path': 'article_path',
            'article-type': 'this.article_type',
            'status': 'article_status',
            'categories': 'this.full_subject_area',
            #'keywords': {  # TODO #5 (don't strip tags in parser)
            #    'author-keywords': 'this.keywords',
            #    'research-organism': 'this.research_organism'
            #},
            #'contributors': 'contributors',
            #'children': 'children',
            #'citations': 'unsupported',  # TODO check parser/xml
            #'related-articles': 'unsupported', # TODO Nathan says leave for now

            'referenced': {
                'present-address': 'present_address',  # TODO #1 (+)
                'equal-contrib': 'equal_contrib',  # TODO IP
                'email': "this.full_correspondence",  # TODO #3 IP
                #'funding': 'unsupported',  # TODO #4
                'competing-interest': 'competing_interests',  # TODO #2 (+)
                #'contribution': 'unsupported',  # TODO check parser/xml
                #'affiliation': 'affiliations',
                #'related-object': 'unsupported',  # TODO check parser / xml
            }  # referenced
        }
    })  # ends article block
]

def scrape(docs_dir, process=None):
    if docs_dir is not None:
        import scraper
        mod = __import__(__name__)
        res = scraper.scrape(mod, doc=docs_dir)
        if process:
            res = process(res)
        import json
        res = json.dumps(res, indent=4)
        return res

def main(args):
    if not len(args) == 1:
        print 'Usage: python feeds.py <xml [dir|file]>'
        exit(1)
    docs_dir = args[0]
    print scrape(docs_dir)


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
