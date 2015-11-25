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
from collections import OrderedDict

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
    def __init__(self, soup, path = None, version = None):
        self.soup = soup
        self.path = path
        self.version = version

    def __getattr__(self, attr, *args, **kwargs):
        def awooga(*args, **kwargs):
            logger.warn('* WARNING: I have no attribute %s' % attr)
            return None

        return getattr(parser, attr, awooga)(self.soup, *args, **kwargs)


def article_wrapper(path,version=None):
    soup = parser.parse_document(path)
    # return a wrapper around the parser module that injects the soup when a function is called
    return ParserWrapper(soup,path,version)

@fattrs('this as article')
def citations(article):
    citation_list = []
    refs = article.refs
    for ref in refs:
        citation = {}

        copy_attribute(ref, 'full_article_title', citation, destination_key='title', process=tidy_whitespace)
        copy_attribute(ref, 'reference_id', citation, destination_key='doi')
        copy_attribute(ref, 'authors', citation, destination_key='authors', process=tidy_citation_authors)
        copy_attribute(ref, 'year', citation, destination_key='year', process=tidy_numeric)
        copy_attribute(ref, 'source', citation, destination_key='source', process=tidy_whitespace)
        copy_attribute(ref, 'comment', citation)
        
        citation_by_id = {}
        citation_by_id[ref['id']] = citation
        
        citation_list.append(citation_by_id)
        
    return list_to_ordered_dict(citation_list)

def tidy_citation_authors(authors):
    tidy_authors = []
    # Only keep authors that have a group-type
    for author in authors:
        if 'group-type' in author:
            tidy_authors.append(author)
    return tidy_authors

def tidy_numeric(string):
    """ Remove all non-numeric characters """
    string = re.sub('\D', '', string)
    return string

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

def list_to_ordered_dict(list):
    """
    Given a list of dicts, convert to an ordered dict that retains the
    original order they were in the list
    """
    ordered_dict = OrderedDict()
    if list:
        for list_item in list:
            for key in list_item.keys():
                ordered_dict[key] = list_item[key]
    return ordered_dict

def footnote_text(raw_footnote_text):
    match = re.search('.*?<p>(.*?)</p>', raw_footnote_text, re.DOTALL)
    if match is None:
        return ""
    text = match.group(1)
    return text


@fattrs('doc', 'article_version')
def article_list(doc, article_version):
    if os.path.isfile(doc):
        return [article_wrapper(doc, article_version)]
    elif os.path.isdir(doc):
        # Note: Converting an entire directory does not use article_version value
        return map(article_wrapper, glob.glob(doc + "*.xml"))
    elif doc.startswith("<?xml"):
        return [ParserWrapper(parser.parse_xml(doc), version=article_version)]

@fattrs('this as article')
def volume(article):
    volume = article.volume
    if not volume:
        # No volume on unpublished PoA articles, calculate based on current year
        volume = time.gmtime()[0] - 2011
    return volume

@fattrs('this as article')
def article_path(article):
    return ('content/' + str(volume(article)) + '/e' + article.publisher_id
            + 'v' + str(version(article)))


@fattrs('this as article')
def issn_electronic(article):
    return article.journal_issn(pub_format='electronic')


@fattrs('this as article')
def article_full_version(article):
    return article.publisher_id  + '.' + version(article)

def version_from_path(file_path):
    """ E.g. file name elife-04996-v1.xml is version 1 """
    if file_path is None:
        return None
    
    bit = file_path.split('-')[-1]
    bit = bit.split('.')[0]
    if bit.find('v') > -1:
        return bit.split('v')[-1]
    else:
        return None
    

@fattrs('this as article')
def version(article):
    if article.version is not None:
        return article.version
    elif version_from_path(article.path):
        return version_from_path(article.path)
    else:
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
def foot_notes(article):
    foot_notes = {}
    notes = article.__getattr__('full_author_notes')
    if notes is not None:
        for note in notes:
            if 'id' in note and note['id'].startswith('fn'):
                foot_notes[note['id']] = {
                    'type': note['fn-type'],
                    'value': footnote_text(note['text'])
                }
    return foot_notes

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

def fragment_path_token(fragment_type, ordinal, asset):
    if fragment_type == 'abstract':
        if int(ordinal) == 1:
            return 'abstract'
        else:
            return 'abstract' + str(ordinal)

    if fragment_type == 'fig':
        if asset and asset == 'figsupp':
            return 'figure-supp' + str(ordinal)
        else:
            return 'figure' + str(ordinal)

    if fragment_type == 'supplementary-material':
        return 'supp-material' + str(ordinal)

    if fragment_type == 'sub-article':
        if int(ordinal) == 1:
            return 'decision'
        elif int(ordinal) == 2:
            return 'response'
        else:
            return 'sub-article' + str(ordinal)

    if fragment_type == 'app':
        return 'appendix' + str(ordinal)

    if fragment_type == 'table-wrap':
        return 'table' + str(ordinal)

    if fragment_type == 'boxed-text':
        return 'box' + str(ordinal)

    if fragment_type == 'media':
        return 'media' + str(ordinal)

    if fragment_type == 'chem-struct-wrap':
        return 'C' + str(ordinal)

def fragment_path(fragment, volume, manuscript_id, version):
    path = "content/" + str(volume) + '/e' + manuscript_id + 'v' + str(version)

    if fragment.get('parent_parent_type'):
        path += "/" + fragment_path_token(fragment_type = fragment.get('parent_parent_type'),
                                          ordinal = fragment.get('parent_parent_path_ordinal'),
                                          asset = fragment.get('parent_parent_asset'))

    if fragment.get('parent_type'):
        path += "/" + fragment_path_token(fragment_type = fragment.get('parent_type'),
                                          ordinal = fragment.get('parent_path_ordinal'),
                                          asset = fragment.get('parent_asset'))

    path += "/" + fragment_path_token(fragment_type = fragment.get('type'),
                                      ordinal = fragment.get('path_ordinal'),
                                      asset = fragment.get('asset'))

    return path

def sibling_components(components, matching_component):
    """
    Given a list of components and a particular component
    compile a list of its siblings
    """
    sibling_components = []
    
    if matching_component.get('parent_type') is not None:
        for comp in components:
            if (comp.get('parent_type') == matching_component.get('parent_type')
                and comp.get('parent_ordinal') == matching_component.get('parent_ordinal')):
                    sibling_components.append(comp)
    else:
        # Look for components with no parent
        for comp in components:
            if (comp.get('parent_type') is None
                and comp.get('parent_ordinal') is None):
                    sibling_components.append(comp)
 
    return sibling_components

def fragment_sibling_ordinal(components, type, ordinal):
    """
    Given a fragment and components, return the numeric index of the fragment
    for fragments of the same type in all of its sibling components
    """
    matching_component = None
    for comp in components:
        if comp.get('type') == type and comp.get('ordinal') == ordinal:
            matching_component = comp
    
    siblings = sibling_components(components, matching_component)

    #print str(type) + '-' + str(ordinal) + '-' + str(len(siblings))

    ordinal = 1
    for sib in siblings:
        if sib.get('type') == matching_component.get('type'):
            if sib.get('ordinal') == matching_component.get('ordinal'):
                # This is the fragment we are searching for, we are done
                break
            ordinal = ordinal + 1
            
    return ordinal
    

def fragment_path_ordinal(components, fragment):
    """
    Look at the fragment and its parentage to set the ordinal to be used in url paths
    """
    
    if fragment.get('parent_parent_type'):
        # Third level element
        fragment['parent_parent_path_ordinal'] = fragment_sibling_ordinal(components,
                                                                          fragment.get('parent_parent_type'),
                                                                          fragment.get('parent_parent_ordinal'))

    if fragment.get('parent_type'):
        raw_path_ordinal = fragment_sibling_ordinal(components, fragment.get('parent_type'),
                                                    fragment.get('parent_ordinal'))
        
        if fragment.get('parent_asset') == 'figsupp':
            fragment['parent_path_ordinal'] = raw_path_ordinal - 1
        else:
            fragment['parent_path_ordinal'] = raw_path_ordinal
    
    
    # First level element
    fragment['path_ordinal'] = fragment_sibling_ordinal(components, fragment.get('type'),
                                                        fragment.get('ordinal'))
    
    return fragment



def component_fragment(components, component, volume, version):

    fragment = {}

    # Quick test for eLife component DOI only
    if 'doi' in component and not component['doi'].startswith('10.7554/'):
        return None

    copy_attribute(component, 'type', fragment)
    copy_attribute(component, 'doi', fragment, destination_key='doi')
    copy_attribute(component, 'ordinal', fragment)
    copy_attribute(component, 'asset', fragment)
    
    if fragment['type'] in ['sub-article','abstract'] and component.get('full_title'):
        copy_attribute(component, 'full_title', fragment,
                       destination_key='title', process=tidy_whitespace)
        
    elif fragment['type'] not in ['sub-article','abstract'] and component.get('full_label'):
        copy_attribute(component, 'full_label', fragment,
                       destination_key='title', process=tidy_whitespace)
        
    # Lastly if there is no title found, default to full_title, irrespective of fragment type
    if 'title' not in fragment:
        if component.get('full_title'):
            copy_attribute(component, 'full_title', fragment,
                       destination_key='title', process=tidy_whitespace)

    if fragment['type'] == 'sub-article' and component.get('contributors'):
        copy_attribute(component, 'contributors', fragment)

    parent_properties = ['parent_type', 'parent_ordinal', 'parent_asset',
                         'parent_parent_type', 'parent_parent_ordinal',
                         'parent_parent_asset']
    for property in parent_properties:
        copy_attribute(component, property, fragment)

    # Set the path_ordinal values, which is different than the ordinal or sibling ordinal
    #   depending on where the tag is found
    fragment = fragment_path_ordinal(components, fragment)

    manuscript_id = component.get('article_doi').split('.')[-1]
    fragment['path'] = fragment_path(fragment, volume, manuscript_id, version)

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
    remove_properties = ['parent_type', 'parent_ordinal', 'parent_asset', 'parent_path_ordinal',
                         'parent_parent_type', 'parent_parent_ordinal',
                         'parent_parent_asset', 'parent_parent_path_ordinal',
                         'article_doi', 'ordinal', 'asset', 'path_ordinal']
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
def award_groups(article):
    award_groups = article.__getattr__('full_award_groups')
    return list_to_ordered_dict(award_groups)

@fattrs('this as article')
def affiliation(article):
    affiliations = article.__getattr__('full_affiliation')
    return list_to_ordered_dict(affiliations)

@fattrs('this as article')
def fragments(article):
    fragments = []
    components = article.__getattr__('components')
    if components is not None:

        # First populate with fragments having no parent
        for component in components:
            fragment = component_fragment(components, component, volume(article), version(article))

            if fragment and not fragment.get('parent_type'):
                fragments.append(fragment)

        # Populate fragments whose parents are already populated
        for component in components:
            if 'parent_type' in component:
                fragment = component_fragment(components, component, volume(article), version(article))
                populate_children(fragment, fragments)

        # Populate fragments of fragments
        for component in components:
            if 'parent_type' in component:
                fragment = component_fragment(components, component, volume(article), version(article))
                for parent_fragment in fragments:
                    if 'fragments' in parent_fragment:
                        populate_children(fragment, parent_fragment['fragments'])

        # Remove tags by cleaning fragments recursively
        clean_fragments(fragments)

    return fragments

@fattrs('this as article')
def related_article(article):
    relateds = []
    related_articles = article.__getattr__('related_article')
    if related_articles is not None:

        for related_article in related_articles:
            data = {
                'type': related_article['related_article_type'],
                'href': related_article['xlink_href']
            }
            relateds.append(data)

    return relateds

DESCRIPTION = [
    ('article', {
        'iterable': article_list,
        'attrs': {
            'title': ('this.full_title', None, tidy_whitespace),
            'impact-statement': 'this.impact_statement',
            'version': 'version',
            'doi': 'this.doi',
            'publish': ('"1"', "1", str),  # 1 or 0 means publish immediately or don't publish immediately
            'volume': ('volume', "0", str),
            'elocation-id': 'this.elocation_id',
            'article-id': 'this.publisher_id',
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
            'related-articles': 'related_article',
            'referenced': {
                'present-address': 'present_address',
                'equal-contrib': 'equal_contrib',
                'email': "email",
                'funding': 'award_groups',
                'competing-interest': 'competing_interests',
                'contribution': 'contribution',
                'affiliation': 'affiliation',
                'related-object': 'this.related_object_ids',
                'foot-note': 'foot_notes'
            }  # referenced
        }
    })  # ends article block
]

def delete_key_if_empty(key, obj):
    if key in obj:
        if len(obj[key]) == 0:
            del(obj[key])

def remove_empty_lists(res):
    for item in res:
        if 'article' not in item:
            continue
        for article in item['article']:
            # Delete empty referenced lists or dicts
            if 'referenced' in article:
                for referenced in article['referenced']:
                    delete_key_if_empty(referenced, article['referenced'])
            # Delete empty related-articles lists
            delete_key_if_empty('related-articles', article)
            # Delete empty fragments list
            delete_key_if_empty('fragments', article)
            # Delete empty citations list
            delete_key_if_empty('citations', article)
            # Delete empty impact-statement list
            delete_key_if_empty('impact-statement', article)

    return res

def scrape(docs_dir, process=None, article_version=None):
    if docs_dir is not None:
        import scraper
        mod = __import__(__name__)
        res = scraper.scrape(mod, doc=docs_dir, article_version=article_version)
        res = remove_empty_lists(res)
        if process:
            res = process(res)

        import json
        res = json.dumps(res, indent=4, ensure_ascii = False)
        return res.encode('utf8')

def main(args):
    if not len(args) == 1:
        print 'Usage: python feeds.py <xml [dir|file]>'
        exit(1)
    docs_dir = args[0]
    print scrape(docs_dir)


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
