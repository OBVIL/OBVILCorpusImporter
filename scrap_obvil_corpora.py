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
    (options, args) = parser.parse_args()

    spiders = [
        #ObvilBibTEISpider,
        #ObvilBaseCritiqueSpider,
        #ObvilEcoleSpider,
        #ObvilMoliereSpider,
        ObvilGongoraSpider
    ]

    process = CrawlerProcess({
        'USER_AGENT': 'Pasted from github (+https://github.com/Valerie-Hanoka)'
    })

    for spider in spiders:
        process.crawl(spider, save_directory=options.save_directory)
    process.start()
