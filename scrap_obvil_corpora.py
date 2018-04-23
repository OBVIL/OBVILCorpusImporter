#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy.crawler import CrawlerProcess
from spiders.obvil_bib_spider import (
    ObvilBibTEISpider,
    ObvilBaseCritiqueSpider,
    ObvilEcoleSpider,
    ObvilMoliereSpider
)

spiders = [
    ObvilBibTEISpider(),
    ObvilBaseCritiqueSpider(),
    ObvilEcoleSpider(),
    ObvilMoliereSpider()
]

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
})


for spider in spiders:
    process.crawl(spider)
    process.start()

