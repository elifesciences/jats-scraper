import os
import scraper

mod = __import__("feeds")
doc_str = open("elife-kitchen-sink.xml", "r").read()
res = scraper.scrape(mod, doc=doc_str)

import json
print json.dumps(res, indent=4)
