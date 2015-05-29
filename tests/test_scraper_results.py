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
                reference_file_name = f.replace('.xml', '.json')
                with open(source_directory + f, "r") as source_file:
                    source_string = source_file.read()
                    res = scraper.scrape(self.mod, doc=source_string)
                    # a bit odd this but seems worthwhile round tripping to match actual results expected
                    self.results[reference_file_name] = json.loads(json.dumps(res[0]['article'][0], indent=4))
                with open(reference_directory + reference_file_name, "r") as reference_file:
                    self.references[reference_file_name] = json.loads(reference_file.read())

    def get_pairs(self):
        for article in self.results.keys():
            yield (article, self.results[article], self.references[article])

    def test_compare_tree(self):
        for (article, generated, reference) in self.get_pairs():
            self.errors = []
            self.checked = []
            self.compare(article, generated, reference)
            for error in self.errors:
                print error

    def compare(self, path, generated, reference):

        if isinstance(reference, list):
            if not isinstance(generated, list):
                self.errors.append("Generated element at %s is of type %s, expected type %s"
                                   % (path, type(generated), type(reference)))
                return
            elif len(generated) != len(reference):
                self.error.append("Generated list at %s is different length (%i) to reference (%i)"
                                  % (path, len(generated), len(reference)))
                return
            else:
                for i in range(0, len(reference)):
                    new_path = path + "/[" + str(i) + "]"
                    new_reference_element = reference[i]
                    new_generated_element = generated[i]
                    self.compare(new_path, new_generated_element, new_reference_element)
        elif isinstance(reference, dict):
            if not isinstance(generated, dict):
                self.errors.append("Generated element at %s is of type %s, expected type %s"
                                   % (path, type(generated), type(reference)))
                return
            elif set(reference.keys()) != set(generated.keys()):
                self.errors.append("Dictionaries at %s have different keys" % path)
                return
            else:
                for key in reference.keys():
                    new_path = path + "/" + str(key)
                    new_reference_element = reference[key]
                    new_generated_element = generated[key]
                    self.compare(new_path, new_generated_element, new_reference_element)
        else:
            if not (generated == reference):
                self.errors.append("Generated element %s at %s doesn't match reference %s"
                                   % (path, str(generated), str(reference)))
                return
            else:
                self.checked.append("> %s|ref> %s |gen> %s" % (path, str(reference), str(generated)))

if __name__ == '__main__':
    unittest.main()


class CompareError(Exception):
    def __init__(self, message):
        self.message = message
