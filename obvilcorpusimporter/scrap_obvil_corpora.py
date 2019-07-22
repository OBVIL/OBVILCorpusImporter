# -*- coding: utf-8 -*-


import re
from optparse import OptionParser

from scrapy.crawler import CrawlerProcess
from spiders.obvil_bib_spider import (
    ObvilBibTEISpider,
    ObvilBaseCritiqueSpider,
    ObvilEcoleSpider,
    ObvilMoliereSpider,
    ObvilGongoraSpider,
    ObvilSainteBeuveSpider
)

from omeka.tei_to_omeka_csv import parse_tei_documents as parse_tei_documents_omeka
from nakala.tei_to_nakala_csv import parse_tei_documents as parse_tei_documents_nakala

import logging
import json


###########################################################
#                          CRAWLING
###########################################################

"""def crawl_obvil(save_directory='crawled_data'):
    spiders = [
        ObvilBibTEISpider,
        ObvilBaseCritiqueSpider,
        ObvilEcoleSpider,
        ObvilMoliereSpider,
        ObvilGongoraSpider,
        ObvilSainteBeuveSpider
    ]

    process = CrawlerProcess({
        'USER_AGENT': 'Pasted from github (+https://github.com/Valerie-Hanoka)'
    })

    for spider in spiders:
        process.crawl(spider, save_directory=save_directory)
    process.start()"""

def crawl_obvil(save_directory='crawled_data'):
    """ Crawl the OBVIL Library."""
    spiders = [ObvilBibTEISpider,
        ObvilBaseCritiqueSpider,
        ObvilEcoleSpider,
        ObvilGongoraSpider,
        ObvilMoliereSpider,
    ]

    process = CrawlerProcess({
        'USER_AGENT': 'Pasted from github (+https://github.com/Valerie-Hanoka)'
    })

    for spider in spiders:
        process.crawl(spider, save_directory=save_directory)
    process.start()

if __name__ == "__main__":

    usage = """usage: ./%prog [--saveInDirectory]
    Crawls the specified OBVIL Corpora available at http://obvil.sorbonne-universite.site/bibliotheque and:
        • saves XML/TEI version of the texts in the specified directory;
        • extract the relevant header meta-data to be exposed in the OAI-PMH repository
        • create a thumbnail ("vignette") for each document.
        • builds one Omeka csv import file per specified project with all the necessary information.
    
    To have an example of configuration files, see ../configs/.
    To successfully import the documents into the OAI-PMH repository, you will need to:
        • Run this script with the right options and configuration
        • Put the generated vignettes at the right place on the server
        • Manually import the generated CSV file into Omeka, with proper rights and mappings.  
    """
    parser = OptionParser(usage)
    parser.add_option("-s", "--saveInDirectory",
                      dest="save_directory",
                      default='crawled_data',
                      help="Saves the corpus info in the specified directory.")

    parser.add_option("-c", "--config",
                      dest="config_file",
                      help="The configuration file to use. See the template config.json.")

    (options, args) = parser.parse_args()

    # Crawling
    crawl_obvil(options.save_directory)

    # Extracting XML-TEI documents metadata
    if options.config_file:
        with open(options.config_file) as jsonfile:
            config = json.load(jsonfile)
            debug_size = config.get("debug_size", None)
            corpora = config["corpora"]

        #TODO: Améliorer la logique ... Hack rapide
        if re.search("omeka", options.config_file):
            parse_tei_documents_omeka(corpora, omeka_csv_folder=options.save_directory)
        elif re.search("nakala", options.config_file):
            parse_tei_documents_nakala(corpora, nakala_csv_folder=options.save_directory)
        else:
            logging.error("""Your config file should be named:
                    - 'config_omeka.json' or
                    - 'config_nakala.json'""")
            exit(1)
    else:
        logging.error("No configuration file given for TEI metadata extraction")
        exit(1)

