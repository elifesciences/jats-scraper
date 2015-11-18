"""an example of generating tests and attaching them to an empty test suite to be detected by the test running.
in this instance, we're detecting the presence of xml files and partial json files to test in a single monolithic function called `inject_methods` that, when executed, will create unique functions for each test case and attach them to the test suite `TestContent`.

This code has been SUPERCEDED by the `test_content.py` and exists as *example* only.

"""

import base
import json
import os
from os.path import join
import feeds
import scraper
import logging
import pprint
import deepdiff

from deepdiff import DeepDiff
from pprint import pprint

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.ERROR)

class TestContent(base.BaseCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def has_all_keys(d, kl):
    return all(map(lambda k: d.has_key(k), kl))

def inject_methods():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    source_xml_dir = join(this_dir, 'JATS')
    source_eif_dir = join(this_dir, 'EIF')
    source_partial_dir = join(this_dir, 'EIF', 'partial')

    # returns a map of {fname: /path/to/fname, ...} for given `dir`
    def path_map(parent):
        paths = map(lambda fname: join(parent, fname), os.listdir(parent))
        paths = filter(os.path.isfile, paths)
        return dict(zip(map(os.path.basename, paths), paths))

    # creates absolute paths to the EIF fixtures
    xml_path_list = path_map(source_xml_dir)
    eif_path_list = path_map(source_eif_dir)
    partial_eif_path_list = path_map(source_partial_dir)

    def xml_fname_to_eif(xml_fname, xml_path):
        return join(source_eif_dir, os.path.splitext(xml_fname)[0] + ".json")

    for xml_file, xml_path in xml_path_list.items():
        eif_file = xml_fname_to_eif(xml_file, xml_path)

        if not os.path.exists(eif_file):
            LOG.info('skipping %s, path `%s` not found', xml_file, eif_file)
            continue

        def _fn1(xml_path, eif_file):
            def call(self):
                generated_eif = scraper.scrape(feeds, doc=xml_path)[0]['article'][0]
                expected_eif = json.load(open(eif_file))
                self.assertEqual(byteify(expected_eif), byteify(generated_eif))
            return call

        slug = xml_file.replace('-', '_').replace(' ', '').replace('/', '_')
        setattr(TestContent, 'test_eif_%s' % slug, _fn1(xml_path, eif_file))


    # handle partials

    def xml_fname_to_eif_partial(xml_fname, xml_path):
        return join(source_partial_dir, os.path.splitext(xml_fname)[0] + "-match.json")

    for xml_file, xml_path in xml_path_list.items():
        eif_path = xml_fname_to_eif_partial(xml_file, xml_path)

        if not os.path.exists(eif_path):
            LOG.info('skipping %s, path `%s` not found', xml_file, eif_path)
            continue

        generated_eif = scraper.scrape(feeds, doc=xml_path)[0]['article'][0]
        # a list of maps with keys 'description' and 'data'
        eif_partial_tests = json.load(open(eif_path))

        for test in eif_partial_tests:
            if not test.has_key('description') or not test.has_key('data'):
                LOG.debug('description or data elements not found in file %r, skipping', eif_path)
                continue

            desc, expected_eif = test['description'], test['data']
            for element, expected_partial_eif in expected_eif.items():
                has_key = generated_eif.has_key(element)

                def _fn2(eif, expected_partial_eif):
                    def call(self):
                        self.assertTrue(has_all_keys(expected_partial_eif, ['description', 'data']))
                        self.assertEqual(byteify(expected_partial_eif), byteify(eif[element]))
                    return call

                slug = eif_path.replace('-', '_').replace(' ', '').replace('/', '_')
                setattr(TestContent, 'test_partial_%s' % slug, _fn2(xml_path, eif_file))
        

#inject_methods()
