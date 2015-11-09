import unittest
import os
from os.path import isfile, join
import scraper
import json
import feeds
from base import BaseCase

class TestBasicScraper(BaseCase):
    def setUp(self):
        self.sources = {}
        source_dir = join(self.this_dir, 'JATS/')
        path_list = map(lambda p: join(source_dir, p), os.listdir(source_dir))
        self.sources = filter(isfile, path_list)

    def test_scrape(self):
        for xml_path in self.sources:
            with open(xml_path, 'r') as xml_fp:
                res = scraper.scrape(feeds, doc=xml_fp.read())
                json_output = json.dumps(res[0]['article'][0], indent=4)
                self.assertIsNotNone(json_output)
                self.assertTrue('"title"' in json_output)

if __name__ == '__main__':
    unittest.main()
