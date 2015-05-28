# jats-scraper

This is a stand-alone xml data scraper utilizing the 
[elife-tools](https://github.com/elifesciences/elife-tools) `parseJATS.py` 
library for extracting data from JATS XML files into a single data structure.

When called from the command line, the datastructure is serialized as JSON for
the purposes of pretty-printing.

## installation

    $ mkvirtualenv jats-scraper
    $ workon jats-scraper
    $ pip install -r requirements.txt

## usage

    $ python feeds.py /path/to/xml/dir/
    
or

    $ python feeds.py /path/to/xml/file.xml
    
For example:

    $ python feeds.py .../elife-tools/elifetools/sample-xml/elife-kitchen-sink.xml
        
Will yield something like:

    [
        {
            "article": [
                {
                    "referenced": {
                        "affiliations": [
                            "* not implemented *"
                        ], 
                        "fundings": "* not implemented *", 
                        "competing-interests": "* not implemented *", 
                        "related-objects": "* not implemented *", 
                        "equal-contrib": "* not implemented *", 
                        "contributions": "* not implemented *", 
                        "emails": [
                            "*For\n                        correspondence: jon_clardy@hms.harvard.edu (JC);", 
                            "nking@berkeley.edu (NK)", 
                            "mharrison@elifesciences.org (MH)"
                        ], 
                        "present-addresses": "* not implemented *"
                    }, 
                    "contributors": [
                        "* not implemented *"
                    ], 
                    "journal_issn": "* not implemented *", 
                    "keywords": {
                        "author-keywords": [
                            "\nSalpingoeca rosetta\n", 
                            "Algoriphagus", 
                            "bacterial sulfonolipid", 
                            "multicellular development"
                        ], 
                        "research-organism": [
                            "Mouse", 
                            "\nC. elegans\n", 
                            "Other"
                        ]
                    }, 
                    "children": [
                        "* not implemented *"
                    ], 
                    "article-type": "research-article", 
                    "title": "Bacterial regulation of colony development in the closest living relatives of animals", 
                    "citations": "* not implemented *", 
                    "impact-statement": "* not implemented *", 
                    "journal_id": "eLife", 
                    "publish": 1, 
                    "version": 1, 
                    "status": "VOR", 
                    "article-id": "10.7554/eLife.00013", 
                    "volume": 3, 
                    "article-version-id": "00013.VOR.1", 
                    "path": "content/3/e00013", 
                    "eissn": "2050-084X", 
                    "categories": {
                        "heading": [
                            "Research article", 
                            "Cell biology", 
                            "Computer science"
                        ], 
                        "display-channel": [
                            "Research article"
                        ]
                    }, 
                    "doi": "10.7554/eLife.00013", 
                    "pub-date": "2014-02-28", 
                    "jousrnal_title": "eLife"
                }
            ]
        }
    ]

## Copyright & Licence

Copyright 2015 eLife Sciences. Licensed under the [GPLv3](gpl.txt)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

