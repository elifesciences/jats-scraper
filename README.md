# pppp-scraper

This a stand-alone xml data scraper utilizing the elife-tools `parseJATS.py` 
library for extracting data from JATS XML files into a single data structure.

When called from the command line, the datastructure is serialized as JSON for
the purposes of pretty-printing.

# usage:

    $ python feeds.py /path/to/xml/dir/

For example:

    $ python feeds.py /home/yourname/devdir/elife-tools/elifetools/sample-xml/
        
Will yield something like:

    [
        {
            "article": [
                {
                    "title_short": "* not implemented *", 
                    "doi": "10.7554/eLife.00013", 
                    "jcode": "eLife", 
                    "version": "* not implemented *", 
                    "category_list": "* not implemented *", 
                    "title": "Bacterial regulation of colony development in the closest living\n                    relatives of animals", 
                    "keyword_list": "None", 
                    "issue": "* not implemented *", 
                    "first_page": "* not implemented *", 
                    "volume": "* not implemented *", 
                    "state": "* not implemented *", 
                    "last_page": "* not implemented *", 
                    "epub": "* not implemented *", 
                    "ppub": "* not implemented *", 
                    "jissn": null, 
                    "subtitle": "* not implemented *", 
                    "type": "research-article", 
                    "slug": "* not implemented *", 
                    "jtitle": "eLife", 
                    "fpub": "* not implemented *", 
                    "authors": [
                        {
                            "first_name": "Rosanna A", 
                            "last_name": "Alegado", 
                            "suffix": null, 
                            "institution": [
                                "University of California, Berkeley", 
                                "Harvard Medical School"
                            ]
                        }, 
                        {
                            "first_name": "Laura W", 
                            "last_name": "Brown", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Shugeng", 
                            "last_name": "Cao", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Renee Kathryn", 
                            "last_name": "Dermenjian", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Richard", 
                            "last_name": "Zuzow", 
                            "suffix": null, 
                            "institution": "Stanford University School of Medicine"
                        }, 
                        {
                            "first_name": "Stephen R", 
                            "last_name": "Fairclough", 
                            "suffix": null, 
                            "institution": "University of California, Berkeley"
                        }, 
                        {
                            "first_name": "Jon", 
                            "last_name": "Clardy", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Nicole", 
                            "last_name": "King", 
                            "suffix": null, 
                            "institution": "University of California, Berkeley"
                        }, 
                        {
                            "first_name": null, 
                            "last_name": null, 
                            "suffix": null, 
                            "institution": "Stanford University School of Medicine"
                        }, 
                        {
                            "first_name": null, 
                            "last_name": null, 
                            "suffix": null, 
                            "institution": null
                        }
                    ]
                }, 
                {
                    "title_short": "* not implemented *", 
                    "doi": "10.7554/eLife.00013", 
                    "jcode": "elife", 
                    "version": "* not implemented *", 
                    "category_list": "* not implemented *", 
                    "title": "A bacterial sulfonolipid triggers multicellular development in the closest living relatives of animals", 
                    "keyword_list": "None", 
                    "issue": "* not implemented *", 
                    "first_page": "* not implemented *", 
                    "volume": "* not implemented *", 
                    "state": "* not implemented *", 
                    "last_page": "* not implemented *", 
                    "epub": "* not implemented *", 
                    "ppub": "* not implemented *", 
                    "jissn": null, 
                    "subtitle": "* not implemented *", 
                    "type": "research-article", 
                    "slug": "* not implemented *", 
                    "jtitle": "eLife", 
                    "fpub": "* not implemented *", 
                    "authors": [
                        {
                            "first_name": "Rosanna A", 
                            "last_name": "Alegado", 
                            "suffix": null, 
                            "institution": "University of California, Berkeley"
                        }, 
                        {
                            "first_name": "Laura W", 
                            "last_name": "Brown", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Shugeng", 
                            "last_name": "Cao", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Renee K", 
                            "last_name": "Dermenjian", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Richard", 
                            "last_name": "Zuzow", 
                            "suffix": null, 
                            "institution": "Stanford University School of Medicine"
                        }, 
                        {
                            "first_name": "Stephen R", 
                            "last_name": "Fairclough", 
                            "suffix": null, 
                            "institution": "University of California, Berkeley"
                        }, 
                        {
                            "first_name": "Jon", 
                            "last_name": "Clardy", 
                            "suffix": null, 
                            "institution": "Harvard Medical School"
                        }, 
                        {
                            "first_name": "Nicole", 
                            "last_name": "King", 
                            "suffix": null, 
                            "institution": "University of California, Berkeley"
                        }
                    ]
                }
            ]
        }
    ]

# Copyright & Licence

Copyright 2015 eLife Sciences, licensed under the [GPLv3](gpl.txt)

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

