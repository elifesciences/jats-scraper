import unittest
from os import listdir
from os.path import isfile, join
import scraper
import json


class TestBasicScraper(unittest.TestCase):

    def setUp(self):
        self.sources = {}
        self.mod = __import__("feeds")
        source_directory = 'JATS/'
        for f in listdir(source_directory):
            if isfile(join(source_directory, f)):
                with open(source_directory + f, "r") as source_file:
                    self.sources[f] = source_file.read()

    def test_scrape(self):
        for jats in self. sources.keys():
            res = scraper.scrape(self.mod, doc=self.sources[jats])
            json_output = json.dumps(res[0]['article'][0], indent=4)
            self.assertIsNotNone(json_output)
            self.assertTrue('"title"' in json_output)

if __name__ == '__main__':
    unittest.main()
