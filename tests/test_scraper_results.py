import unittest
from os import listdir
from os.path import isfile, join
import scraper
import json

class TestScraperResults(unittest.TestCase):

    def setUp(self):
        self.results = {}
        self.references = {}
        self.mod = __import__("feeds")
        source_directory = 'JATS/'
        reference_directory = 'JSON/'

        for f in listdir(source_directory):
            if isfile(join(source_directory, f)):
                with open(source_directory + f, "r") as source_file:
                    source_string = source_file.read()
                    res = scraper.scrape(self.mod, doc=source_string)
                    # a bit odd this but seems worthwhile round tripping to match actual results expected
                    self.results[f] = json.loads(json.dumps(res[0]['article'][0], indent=4))
                with open(reference_directory + f.replace('.xml', '.json'), "r") as reference_file:
                    self.references[f] = json.loads(reference_file.read())

    def test_title(self):
        for article in self.results.keys():
            self.assertEqual(self.results[article]['title'], self.references[article]['title'])

if __name__ == '__main__':
    unittest.main()
