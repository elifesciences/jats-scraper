import base
import json
import os
from os.path import join
import feeds
import scraper
import logging

logging.basicConfig()
LOG = logging.getLogger(__name__)

class TestSnippets(base.BaseCase):
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
        "for each xml file, look for matching expected EIF"

        def xml_fname_to_eif(xml_fname, xml_path):
            return join(self.source_eif_dir, os.path.splitext(xml_fname)[0] + ".json")
        
        for xml_file, xml_path in self.xml_path_list.items():
            eif_file = xml_fname_to_eif(xml_file, xml_path)
            
            if not os.path.exists(eif_file):
                LOG.info('skipping %s, path `%s` not found', xml_file, eif_file)
                continue
                
            #generated_eif = json.loads(feeds.scrape(xml_path))
            generated_eif = scraper.scrape(feeds, doc=xml_path)[0]['article'][0]
            expected_eif = json.load(open(eif_file))
            
            try:
                # comparing OrderedDict with Dict works in 3.1+
                #self.assertEqual(generated_eif, expected_eif)
                LOG.info("testing %s", xml_path)
                self.assertEqual(dict(generated_eif), expected_eif)
            except AssertionError:
                print 'failed to compare xml %s to eif %s' % (xml_file, eif_file)
                raise

    def test_eif_partials(self):
        "for each xml file, look for partial matching EIF"

        def xml_fname_to_eif_partial(xml_fname, xml_path):
            return join(self.source_partial_dir, os.path.splitext(xml_fname)[0] + "-match.json")
        
        for xml_file, xml_path in self.xml_path_list.items():
            eif_path = xml_fname_to_eif_partial(xml_file, xml_path)
            
            if not os.path.exists(eif_path):
                LOG.info('skipping %s, path `%s` not found', xml_file, eif_path)
                continue

            generated_eif = scraper.scrape(feeds, doc=xml_path)[0]['article'][0]
            expected_eif = json.load(open(eif_path))[0]

            for element, expected_partial_eif in expected_eif.items():
                try:
                    self.assertTrue(generated_eif.has_key(element))
                except AssertionError:
                    raise AssertionError("EIF generated from %r doesn't contain expected element %r (in partial file %r)" % (xml_path, element, eif_path))
                    
                    generated_partial_eif = generated_eif[element]
                    self.assertEqual(dict(generated_partial_eif), expected_partial_eif)
                except AssertionError:
                    raise AssertionError('failed to compare xml %s to partial eif element %r' % (xml_path, element))