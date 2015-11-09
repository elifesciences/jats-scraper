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
    
For installing on OSX it may be necessary to do the following before running requirements.yxy
    
    $ sudo STATIC_DEPS=true pip install lxml==3.4.1 

## testing

Tests can be run with the `./run-tests.sh` script.

Tests can be run individually with:

    python -m unittest path.to.module.suite.test
    
For example:

    python -m unittest tests.test_content
    
would run all tests in `tests/test_content.py` and:

    python -m unittest tests.test_content.TestContent.test_eif
    
would run the `test_eif` test in the `TestContent` test suite in the 
`test_content.py` module.

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
                    "status": "VOR", 
                    "article-type": "research-article", 
                    "doi": "10.7554/eLife.00013", 
                    "force": "1", 
                    "contributors": [
                        {
                            "surname": "Alegado", 
                            "given-names": "Rosanna A", 
                            "references": {
                                "affiliation": [
                                    "aff1"
                                ], 
                                "contribution": [
                                    "con1"
                                ], 
                                "competing-interest": [
                                    "conf2"
                                ], 
                                "funding": [
                                    "par-2"
                                ], 
                                "equal-contrib": [
                                    "equal-contrib"
                                ]
                            }, 
                            "equal-contrib": "yes", 
                            "type": "author", 
                            "id": "author-1668"
                        }, 
                        {
                            "surname": "Brown", 
                            "given-names": "Laura W", 
                            "references": {
                                "affiliation": [
                                    "aff2"
                                ], 
                                "contribution": [
                                    "con2"
                                ], 
                                "competing-interest": [
                                    "conf2"
                                ], 
                                "funding": [
                                    "par-3"
                                ], 
                                "equal-contrib": [
                                    "equal-contrib"
                                ]
                            }, 
                            "equal-contrib": "yes", 
                            "type": "author", 
                            "id": "author-1669"
                        }, 
                        {
                            "surname": "Cao", 
                            "given-names": "Shugeng", 
                            "type": "author", 
                            "id": "author-1670", 
                            "references": {
                                "affiliation": [
                                    "aff2"
                                ], 
                                "contribution": [
                                    "con3"
                                ], 
                                "competing-interest": [
                                    "conf2"
                                ]
                            }
                        }, 
                        {
                            "surname": "Dermenjian", 
                            "given-names": "Renee K", 
                            "type": "author", 
                            "id": "author-1671", 
                            "references": {
                                "affiliation": [
                                    "aff2"
                                ], 
                                "contribution": [
                                    "con4"
                                ], 
                                "competing-interest": [
                                    "conf2"
                                ]
                            }
                        }, 
                        {
                            "surname": "Zuzow", 
                            "given-names": "Richard", 
                            "type": "author", 
                            "id": "author-1672", 
                            "references": {
                                "affiliation": [
                                    "aff3"
                                ], 
                                "contribution": [
                                    "con5"
                                ], 
                                "competing-interest": [
                                    "conf2"
                                ]
                            }
                        }, 
                        {
                            "surname": "Fairclough", 
                            "given-names": "Stephen R", 
                            "type": "author", 
                            "id": "author-1673", 
                            "references": {
                                "affiliation": [
                                    "aff1"
                                ], 
                                "contribution": [
                                    "con6"
                                ], 
                                "competing-interest": [
                                    "conf2"
                                ], 
                                "funding": [
                                    "par-6"
                                ]
                            }
                        }, 
                        {
                            "surname": "Clardy", 
                            "corresp": "yes", 
                            "given-names": "Jon", 
                            "references": {
                                "affiliation": [
                                    "aff2"
                                ], 
                                "contribution": [
                                    "con7"
                                ], 
                                "competing-interest": [
                                    "conf1"
                                ], 
                                "funding": [
                                    "par-4", 
                                    "par-5"
                                ], 
                                "email": [
                                    "cor1"
                                ]
                            }, 
                            "type": "author", 
                            "id": "author-1060"
                        }, 
                        {
                            "surname": "King", 
                            "corresp": "yes", 
                            "given-names": "Nicole", 
                            "references": {
                                "affiliation": [
                                    "aff1"
                                ], 
                                "contribution": [
                                    "con8"
                                ], 
                                "competing-interest": [
                                    "conf2"
                                ], 
                                "funding": [
                                    "par-1", 
                                    "par-5"
                                ], 
                                "email": [
                                    "cor2"
                                ]
                            }, 
                            "type": "author", 
                            "id": "author-1274"
                        }, 
                        {
                            "role": "Reviewing editor", 
                            "surname": "Greenberg", 
                            "given-names": "Peter", 
                            "type": "editor", 
                            "affiliations": [
                                {
                                    "country": "United States", 
                                    "institution": "University of Washington"
                                }
                            ]
                        }
                    ], 
                    "pub-date": "2012-10-15", 
                    "title": "A bacterial sulfonolipid triggers multicellular development in the closest living relatives of animals", 
                    "citations": {
                        "bib48": {
                            "source": "J Antibiot", 
                            "authors": [
                                {
                                    "surname": "Kamiyama", 
                                    "given-names": "T", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Umino", 
                                    "given-names": "T", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Itezono", 
                                    "given-names": "Y", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Nakamura", 
                                    "given-names": "Y", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Satoh", 
                                    "given-names": "T", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Yokose", 
                                    "given-names": "K", 
                                    "group-type": "author"
                                }
                            ], 
                            "year": "1995a", 
                            "title": "Sulfobacins A and B, novel von Willebrand factor receptor antagonists. II. Structural elucidation"
                        }, 
                        "bib49": {
                            "source": "J. Antibiot", 
                            "authors": [
                                {
                                    "surname": "Kamiyama", 
                                    "given-names": "T", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Umino", 
                                    "given-names": "T", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Satoh", 
                                    "given-names": "T", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Sawairi", 
                                    "given-names": "S", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Shirane", 
                                    "given-names": "M", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Ohshima", 
                                    "given-names": "S", 
                                    "group-type": "author"
                                }, 
                                {
                                    "surname": "Yokose", 
                                    "given-names": "K", 
                                    "group-type": "author"
                                }
                            ], 
                            "year": "1995b", 
                            "title": "Sulfobacins A and B, novel von Willebrand factor receptor antagonists. I. Production, isolation, characterization and biological activities"
                        }, 
                        "bib46": {
                            "source": "Memoirs Boston Soc. Of Nat. Hist", 
                            "authors": [
                                {
                                    "surname": "James-Clark", 
                                    "given-names": "H", 
                                    "group-type": "author"
                                }
                            ], 
                            "year": "1867", 
                            "title": "On the spongiae ciliatae as infusoria flagellata; or observations on the structure, animality, and relationship of Leucosolenia botryoides, Bowerbank."
                        }, 
                        
                        ... [snip] ...
                         
                        "bib52": {
                            "source": "Dev Cell", 
                            "authors": [
                                {
                                    "surname": "King", 
                                    "given-names": "N", 
                                    "group-type": "author"
                                }
                            ], 
                            "year": "2004", 
                            "title": "The unicellular ancestry of animal development"
                        }
                    }, 
                    "impact-statement": "The development of colonies of cells in choanoflagellates, water-dwelling organisms that feed on bacteria, is triggered by the presence of very low concentrations of a lipid molecule produced by certain types of bacteria.", 
                    "related-articles": [
                        {
                            "href": "10.7554/eLife.00242", 
                            "type": "commentary"
                        }
                    ], 
                    "referenced": {
                        "foot-note": {}, 
                        "present-address": {}, 
                        "competing-interest": {
                            "conf2": "The remaining authors have no competing interests to declare.", 
                            "conf1": "JC: Reviewing Editor, <italic>eLife</italic>."
                        }, 
                        "funding": {
                            "par-6": {
                                "award-id": "T32 HG00047", 
                                "institution": "National Institutes of Health"
                            }, 
                            "par-5": {
                                "award-id": "R01 GM099533", 
                                "institution": "National Institutes of Health"
                            }, 
                            "par-4": {
                                "award-id": "R01 GM086258", 
                                "institution": "National Institutes of Health"
                            }, 
                            "par-3": {
                                "award-id": "F32 GM089018", 
                                "institution": "National Institutes of Health"
                            }, 
                            "par-2": {
                                "award-id": "F32 GM086054", 
                                "institution": "National Institutes of Health"
                            }, 
                            "par-1": {
                                "institution": "Gordon and Betty Moore Foundation Marine Microbiology Initiative"
                            }
                        }, 
                        "affiliation": {
                            "aff3": {
                                "dept": "Department of Biochemistry", 
                                "country": "United States", 
                                "institution": "Stanford University School of Medicine", 
                                "email": null, 
                                "city": "Stanford"
                            }, 
                            "aff2": {
                                "dept": "Department of Biological Chemistry and Molecular Pharmacology", 
                                "country": "United States", 
                                "institution": "Harvard Medical School", 
                                "email": null, 
                                "city": "Boston"
                            }, 
                            "aff1": {
                                "dept": "Department of Molecular and Cell Biology", 
                                "country": "United States", 
                                "institution": "University of California, Berkeley", 
                                "email": null, 
                                "city": "Berkeley"
                            }
                        }, 
                        "equal-contrib": {
                            "equal-contrib": "These authors contributed equally to this work"
                        }, 
                        "contribution": {
                            "con1": "RA: Conception and design, Acquisition of data, Analysis and interpretation of data, Drafting or revising the article", 
                            "con2": "LB: Conception and design, Acquisition of data, Analysis and interpretation of data, Drafting or revising the article", 
                            "con3": "SC: Acquisition of data, Analysis and interpretation of data, Drafting or revising the article", 
                            "con4": "RD: Acquisition of data, Analysis and interpretation of data", 
                            "con5": "RZ: Acquisition of data, Analysis and interpretation of data", 
                            "con6": "SF: Acquisition of data, Analysis and interpretation of data", 
                            "con7": "JC: Conception and design, Analysis and interpretation of data, Drafting or revising the article", 
                            "con8": "NK: Conception and design, Analysis and interpretation of data, Drafting or revising the article"
                        }, 
                        "email": {
                            "cor1": "jon_clardy@hms.harvard.edu", 
                            "cor2": "nking@berkeley.edu"
                        }, 
                        "related-object": {}
                    }, 
                    "publish": "1", 
                    "article-version-id": "00013.1", 
                    "volume": "1", 
                    "version": "1", 
                    "keywords": {
                        "author-keywords": [
                            "Salpingoeca rosetta", 
                            "Algoriphagus", 
                            "bacterial sulfonolipid", 
                            "multicellular development"
                        ], 
                        "research-organism": [
                            "Other"
                        ]
                    }, 
                    "path": "content/1/e00013v1", 
                    "fragments": [
                        {
                            "doi": "10.7554/eLife.00013.001", 
                            "path": "content/1/e00013v1/abstract", 
                            "type": "abstract"
                        }, 
                        
                        ... [snip] ...
                        
                        {
                            "doi": "10.7554/eLife.00013.008", 
                            "title": "Figure 3.", 
                            "path": "content/1/e00013v1/figure3", 
                            "fragments": [
                                {
                                    "doi": "10.7554/eLife.00013.009", 
                                    "title": "Figure 3—figure supplement 1.", 
                                    "path": "content/1/e00013v1/figure3/figure-supp1", 
                                    "type": "fig"
                                }, 
                                
                                ... [snip] ...
                                
                                {
                                    "doi": "10.7554/eLife.00013.023", 
                                    "title": "Figure 3—figure supplement 15.", 
                                    "path": "content/1/e00013v1/figure3/figure-supp15", 
                                    "type": "fig"
                                }
                            ], 
                            "type": "fig"
                        }, 
                        {
                            "doi": "10.7554/eLife.00013.024", 
                            "title": "Table 3.", 
                            "path": "content/1/e00013v1/table3", 
                            "type": "table-wrap"
                        }, 
                        {
                            "doi": "10.7554/eLife.00013.025", 
                            "title": "Figure 4.", 
                            "path": "content/1/e00013v1/figure4", 
                            "fragments": [
                                {
                                    "doi": "10.7554/eLife.00013.026", 
                                    "title": "Figure 4—figure supplement 1.", 
                                    "path": "content/1/e00013v1/figure4/figure-supp1", 
                                    "type": "fig"
                                }, 
                                {
                                    "doi": "10.7554/eLife.00013.027", 
                                    "title": "Figure 4—figure supplement 2.", 
                                    "path": "content/1/e00013v1/figure4/figure-supp2", 
                                    "type": "fig"
                                }, 
                                {
                                    "doi": "10.7554/eLife.00013.028", 
                                    "title": "Figure 4—figure supplement 3.", 
                                    "path": "content/1/e00013v1/figure4/figure-supp3", 
                                    "type": "fig"
                                }
                            ], 
                            "type": "fig"
                        }, 
                        {
                            "doi": "10.7554/eLife.00013.029", 
                            "contributors": [
                                {
                                    "role": "Reviewing editor", 
                                    "surname": "Greenberg", 
                                    "given-names": "Peter", 
                                    "type": "editor", 
                                    "affiliations": [
                                        {
                                            "country": "United States", 
                                            "institution": "University of Washington"
                                        }
                                    ]
                                }
                            ], 
                            "title": "Decision letter", 
                            "path": "content/1/e00013v1/decision", 
                            "type": "sub-article"
                        }, 
                        {
                            "doi": "10.7554/eLife.00013.030", 
                            "title": "Author response", 
                            "path": "content/1/e00013v1/response", 
                            "type": "sub-article"
                        }
                    ], 
                    "article-id": "10.7554/eLife.00013", 
                    "elocation-id": "e00013", 
                    "categories": {
                        "heading": [
                            "Cell biology"
                        ], 
                        "display-channel": [
                            "Research article"
                        ]
                    }
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

