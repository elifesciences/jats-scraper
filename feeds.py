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

@fattrs('this as article')
def citations(article):
    citation_list = {}
    refs = article.refs
    for ref in refs:
        citation = {}

        copy_attribute(ref, 'article_title', citation, destination_key='title', process=tidy_whitespace)
        copy_attribute(ref, 'reference_id', citation, destination_key='doi')
        copy_attribute(ref, 'authors', citation)
        copy_attribute(ref, 'year', citation)
        copy_attribute(ref, 'source', citation, destination_key='source', process=tidy_whitespace)
        copy_attribute(ref, 'comment', citation)
        citation_list[ref['id']] = citation
    return citation_list

def tidy_whitespace(string):
    string = re.sub('\n', ' ', string)
    string = re.sub(' +', ' ', string)
    string = string.strip()
    return string

def copy_attribute(source, source_key, destination, destination_key=None, process=None):
    if destination_key is None:
        destination_key = source_key
    if source is not None:
        if source is not None and destination is not None and source_key in source:
            value = source[source_key]
            if process is not None:
                value = process(value)
            destination[destination_key] = value


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
    if article.is_poa is True:
        return 'content/early/e' + article.publisher_id
    else:
        return 'content/' + article.volume + '/e' + article.publisher_id


@fattrs('this as article')
def issn_electronic(article):
    return article.journal_issn(pub_format='electronic')


@fattrs('this as article')
def article_full_version(article):
    return article.publisher_id  + '.' + str(_VERSION)


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
            interests[conflict['id']] = tidy_whitespace(footnote_text(conflict['text']))
    return interests

@fattrs('this as article')
def contribution(article):
    cons = {}
    contributions = article.__getattr__('author_contributions', fntype_filter='con')
    if contributions is not None:
        for con in contributions:
            cons[con['id']] = tidy_whitespace(footnote_text(con['text']))
    return cons

def fragment_path_token(fragment_type, ordinal):
    if fragment_type == 'abstract':
        return 'abstract-' + str(ordinal)

    if fragment_type == 'fig':
        return 'F' + str(ordinal)

    if fragment_type == 'supplementary-material':
        return 'DC' + str(ordinal)

    if fragment_type == 'sub-article':
        return str(ordinal)

    if fragment_type == 'table-wrap':
        return 'T' + str(ordinal)

    if fragment_type == 'boxed-text':
        return 'B' + str(ordinal)

    if fragment_type == 'media':
        return 'media-' + str(ordinal)

    if fragment_type == 'chem-struct-wrap':
        return 'C' + str(ordinal)

def fragment_path(fragment, volume, manuscript_id):
    path = "content/" + str(volume) + '/e' + manuscript_id

    if fragment.get('parent_parent_type'):
        path += "/" + fragment_path_token(fragment.get('parent_parent_type'),
                                 fragment.get('parent_parent_ordinal'))

    if fragment.get('parent_type'):
        path += "/" + fragment_path_token(fragment.get('parent_type'),
                                 fragment.get('parent_ordinal'))

    path += "/" + fragment_path_token(fragment.get('type'),
                       fragment.get('ordinal'))

    return path

def component_fragment(component, volume):

    fragment = {}

    # Quick test for eLife component DOI only
    if 'doi' in component and not component['doi'].startswith('10.7554/'):
        return None

    copy_attribute(component, 'type', fragment)
    copy_attribute(component, 'doi', fragment, destination_key='doi')
    copy_attribute(component, 'ordinal', fragment)

    if fragment['type'] in ['sub-article','abstract'] and component.get('full_title'):
        copy_attribute(component, 'full_title', fragment,
                       destination_key='title', process=tidy_whitespace)
        
    elif fragment['type'] not in ['sub-article','abstract'] and component.get('full_label'):
        copy_attribute(component, 'full_label', fragment,
                       destination_key='title', process=tidy_whitespace)

    if fragment['type'] == 'sub-article' and component.get('contributors'):
        copy_attribute(component, 'contributors', fragment)

    parent_properties = ['parent_type', 'parent_ordinal',
                         'parent_parent_type', 'parent_parent_ordinal']
    for property in parent_properties:
        copy_attribute(component, property, fragment)

    manuscript_id = component.get('article_doi').split('.')[-1]
    fragment['path'] = fragment_path(fragment, volume, manuscript_id)

    return fragment

def populate_children(fragment, fragments):
    """
    Given a fragment with a parent_type and parent_ordinal,
    find its parent in fragments and if found add the fragment to its children
    """
    parent_fragment = None

    for search_fragment in fragments:

        if search_fragment.get('type') == fragment['parent_type'] \
           and str(search_fragment['ordinal']) == str(fragment['parent_ordinal']):
            parent_fragment = search_fragment
            break

    if not parent_fragment:
        return

    if parent_fragment:
        if not parent_fragment.get('fragments'):
            parent_fragment['fragments'] = []

        parent_fragment['fragments'].append(fragment)


def clean_fragments(fragments):
    # Recursive fragment cleaner
    for fragment in fragments:
        if 'fragments' in fragment:
            clean_fragments(fragment['fragments'])
        clean_fragment(fragment)

def clean_fragment(fragment):
    # Remove some values
    remove_properties = ['parent_type', 'parent_ordinal',
                         'parent_parent_type', 'parent_parent_ordinal',
                         'article_doi', 'ordinal']
    for property in remove_properties:
        if property in fragment:
            del(fragment[property])

@fattrs('this as article')
def email(article):
    cor = article.__getattr__('full_correspondence')
    if cor is not None:
        return cor
    else:
        return {}



@fattrs('this as article')
def fragments(article):
    fragments = []
    components = article.__getattr__('components')
    if components is not None:

        # First populate with fragments having no parent
        for component in components:
            fragment = component_fragment(component, article.volume)

            if fragment and not fragment.get('parent_type'):
                fragments.append(fragment)

        # Populate fragments whose parents are already populated
        for component in components:
            if 'parent_type' in component:
                fragment = component_fragment(component, article.volume)
                populate_children(fragment, fragments)

        # Populate fragments of fragments
        for component in components:
            if 'parent_type' in component:
                fragment = component_fragment(component, article.volume)
                for parent_fragment in fragments:
                    if 'fragments' in parent_fragment:
                        populate_children(fragment, parent_fragment['fragments'])

        # Remove tags by cleaning fragments recursively
        clean_fragments(fragments)

    return fragments

DESCRIPTION = [
    ('article', {
        'iterable': article_list,
        'attrs': {
            'title': ('this.title', None, tidy_whitespace),
            'impact-statement': 'this.impact_statement',
            'version': 'version',
            'doi': 'this.doi',
            'publish': ('"1"', "1", str),  # 1 or 0 means publish immediately or don't publish immediately
            'force': ('"1"', "1", str),  # overwrite if present
            'volume': ('this.volume', "0", str),
            'article-id': 'this.doi',
            'article-version-id': 'article_full_version',
            'pub-date': ('this.pub_date', None, \
                         lambda t: datetime.fromtimestamp(time.mktime(t)).strftime("%Y-%m-%d") \
                         if t is not None else None),
            'path': 'article_path',
            'article-type': 'this.article_type',
            'status': 'article_status',
            'categories': 'this.full_subject_area',
            'keywords': 'this.full_keyword_groups',
            'contributors': 'this.contributors',
            'fragments': 'fragments',
            'citations': 'citations',
            #'related-articles': 'unsupported', # TODO but leave for now

            'referenced': {
                'present-address': 'present_address',
                'equal-contrib': 'equal_contrib',
                'email': "email",
                'funding': 'this.full_award_groups',
                'competing-interest': 'competing_interests',
                'contribution': 'contribution',
                'affiliation': 'this.full_affiliation',
                'related-object': 'this.related_object_ids',
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
        if 'referenced' in res:
            for referenced in res['referenced']:
                if len(res['referenced'][referenced]) == 0:
                    del res['referenced'][referenced]
        import json
        res = json.dumps(res, indent=4, ensure_ascii = False)
        return res

def main(args):
    if not len(args) == 1:
        print 'Usage: python feeds.py <xml [dir|file]>'
        exit(1)
    docs_dir = args[0]
    print scrape(docs_dir).encode('utf8')


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
