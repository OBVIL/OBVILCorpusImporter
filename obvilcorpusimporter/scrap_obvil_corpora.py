# -*- coding: utf-8 -*-

from optparse import OptionParser

from scrapy.crawler import CrawlerProcess
from spiders.obvil_bib_spider import (
    ObvilBibTEISpider,
    ObvilBaseCritiqueSpider,
    ObvilEcoleSpider,
    ObvilMoliereSpider,
    ObvilGongoraSpider
)

from omeka.tei_to_omeka_csv import parse_tei_documents

import logging
import json


###########################################################
#                          CRAWLING
###########################################################

def crawl_obvil(save_directory='crawled_data'):
    """ Crawl the OBVIL Library."""
    spiders = [
        ObvilBibTEISpider,
        ObvilBaseCritiqueSpider,
        ObvilEcoleSpider,
        ObvilMoliereSpider,
        ObvilGongoraSpider
    ]

    process = CrawlerProcess({
        'USER_AGENT': 'Pasted from github (+https://github.com/Valerie-Hanoka)'
    })

    for spider in spiders:
        process.crawl(spider, save_directory=save_directory)
    process.start()


if __name__ == "__main__":

    usage = """usage: ./%prog [--saveInDirectory]
    Crawls the OBVIL Corpora available at http://obvil.sorbonne-universite.site/bibliotheque and
    saves XML/TEI, epub and html versions of the same texts in the specified directory.
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
    #crawl_obvil(options.save_directory)

    # Extracting XML-TEI documents metadata
    if options.config_file:
        with open(options.config_file) as jsonfile:
            config = json.load(jsonfile)
            debug_size = config.get("debug_size", None)
            corpora = config["corpora"]

        parse_tei_documents(corpora, omeka_csv_folder=options.save_directory)
    else:
        logging.error("No configuration file given for TEI metadata extraction")
        exit(1)

    # Pushing every item in Omeka
    # TODO

