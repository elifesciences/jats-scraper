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
        source_xml_dir = join(self.this_dir, 'JATS')
        self.source_eif_dir = join(self.this_dir, 'EIF')
        self.source_partial_dir = join(self.this_dir, 'EIF', 'partial')

        # returns a map of {fname: /path/to/fname, ...} for given `dir`
        def path_map(parent):
            paths = map(lambda fname: join(parent, fname), os.listdir(parent))
            paths = filter(os.path.isfile, paths)
            return dict(zip(map(os.path.basename, paths), paths))
        
        # creates absolute paths to the EIF fixtures
        self.xml_path_list = path_map(source_xml_dir)
        self.eif_path_list = path_map(self.source_eif_dir)
        self.partial_eif_path_list = path_map(self.source_partial_dir)

    def tearDown(self):
        pass

    def test_eif(self):
        """each XML file in the JATS dir with a matching *complete* output
        in the EIF directory are equal"""

        def xml_fname_to_eif(xml_fname, xml_path):
            return join(self.source_eif_dir, os.path.splitext(xml_fname)[0] + ".json")

        ddiffs = {}
        
        for xml_file, xml_path in self.xml_path_list.items():
            eif_file = xml_fname_to_eif(xml_file, xml_path)
            
            if not os.path.exists(eif_file):
                LOG.info('skipping %s, path `%s` not found', xml_file, eif_file)
                continue
            
            generated_eif = scraper.scrape(feeds, doc=xml_path)[0]['article'][0]
            expected_eif = json.load(open(eif_file))

            LOG.info("testing %s", xml_path)
            ddiff = DeepDiff(self.byteify(expected_eif), self.byteify(generated_eif))

            if ddiff:
                ddiffs[eif_file] = ddiff

        if len(ddiffs):
            for attr, value in ddiffs.items():
                print attr
                pprint(value)
                print "\n"
            self.assertTrue(False)


    def test_eif_partials(self):
        """each XML file in the JATS dir with a matching *partial*
        output in the EIF/partial directory are present and equal"""

        def xml_fname_to_eif_partial(xml_fname, xml_path):
            return join(self.source_partial_dir, os.path.splitext(xml_fname)[0] + "-match.json")

        ddiffs = {}
        
        for xml_file, xml_path in self.xml_path_list.items():
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

                    if not has_key:
                        ddiff = "EIF generated from %r doesn't contain expected element %r (in partial file %r)"
                        ddiff = ddiff % (xml_path, element, eif_path)

                    if has_key:
                        ddiff = DeepDiff(self.byteify(expected_partial_eif), self.byteify(generated_eif[element]))

                    if ddiff:
                        if not ddiffs.has_key(eif_path):
                            ddiffs[eif_path] = {}

                        ddiffs[eif_path][desc] = ddiff

        if len(ddiffs):
            for attr, values in ddiffs.items():
                print attr

                for desc, value in values.items():
                    print desc.encode('utf-8')
                    pprint(value)
                    print "\n"
            self.assertTrue(False)

    def byteify(self, input):
        if isinstance(input, dict):
            return {self.byteify(key):self.byteify(value) for key,value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
