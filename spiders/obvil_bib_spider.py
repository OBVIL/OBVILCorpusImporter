#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Valérie Hanoka
"""

import re
import os
import scrapy


class ObvilBaseSpider(scrapy.Spider):

    name = "obvil_base_spider"

    available_formats = {
        'epub': '.epub',
        'xml': '.xml',
    }

    def __init__(self, save_directory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_directory = save_directory.rstrip('/')

    def errback_obvil_files(self, failure):
        """Logs all failures"""
        self.logger.error(repr(failure))

    def harvest_file(self, response):
        """ Find and download a XML-TEI or epub file."""

        file_info = {}
        url_match = re.match(self.RE_OBVIL_CORPUS_FILE_URL, response.url)

        if url_match:
            file_info.update(url_match.groupdict())

        base_filename = u"%s_%s.%s" % (
            file_info['corpus_name'],
            file_info['file_name'],
            file_info['file_ext'],
        )

        # The XML-TEIs are stored by collections, in different folders in the save_directory
        is_file_xml = file_info['file_ext'] == 'xml'
        if is_file_xml:
            collection_folder = u'%s/%s' % (self.save_directory, file_info['corpus_name'])
            if not os.path.exists(collection_folder):
                os.makedirs(collection_folder)

            local_filename = u"%s/%s" % (
                collection_folder,
                base_filename
            )

        # Whereas the epubs (and other formats) are stored altogether in the save_directory
        # This is done for Omeka-s sideload import, which requires
        else:
            local_filename = u"%s/%s" % (
                self.save_directory,
                base_filename
            )

        with open(local_filename, 'wb') as f:
            f.write(response.body)

        # If the file is already stored in the collection directory,
        # we create a symbolic link from it to the save_directory
        # in order to neable mass import from sideload.
        if is_file_xml:
            os.symlink(local_filename, u"%s/%s" % (self.save_directory, base_filename))


        yield file_info


########################################
#     Parsing canonical corpora
########################################

class ObvilBibTEISpider(ObvilBaseSpider):
    name = "obvil_bib_tei_spider"

    corpora = [
        'fabula-numerica',
        'apollinaire',
        'challe',
        'danse',
        'ecole',
        'gongora',
        'haine-theatre',
        'historiographie-theatre',
        'mdf-italie',
        'mercure-galant',
        'mythographie',
        'sainte-beuve',
    ]

    # One URL per corpus
    start_urls = ['http://132.227.201.10:8086/corpus/%s/xml' % c for c in corpora]

    # REGEXPS
    RE_OBVIL_CORPUS_FILE_URL = re.compile(
        'http://132.227.201.10:8086/corpus/'
        '(?P<corpus_name>[^/]*)/'
        '(?P<format>[^/]*)/'
        '(?P<file_name>[^\.]*)\.'
        '(?P<file_ext>.*)')

    RE_TAGS = re.compile('<[^>]*>')

    def parse(self, response):

        # Gathering the documents which constitutes the corpus
        links = response.xpath('//body/table//a/@href').extract()

        for link in links:

            # A document is only valid if it's in xml format.
            if '.xml' in link:

                corpus_location = response.url.strip('xml/')
                file_name = link.rsplit('.xml')[0]
                self.logger.info("••••••••••••••••••••••••••••••••• Found text file %s (%s)" % (file_name, link))

                # Get related documents in other formats
                for doc_format, ext in self.available_formats.items():
                    related_file = "%s/%s/%s%s" % (corpus_location, doc_format, file_name, ext)

                    yield scrapy.Request(
                        related_file,
                        callback=self.harvest_file,
                        errback=self.errback_obvil_files,
                    )



########################################
#     Parsing special corpora
########################################

class ObvilUnconventional(ObvilBaseSpider):

    name = "obvil_unconventional_tei_spider"

    corpus_name = ''  # E.g. "ecole"
    corpora = []      # E.g. ["manuels"]

    def __init__(self, save_directory, *args, **kwargs):
        super().__init__(save_directory=save_directory, *args, **kwargs)
        self.start_url = "http://132.227.201.10:8086/corpus/%s/" % self.corpus_name
        self.start_urls = ['%s%s' % (self.start_url, c) for c in self.corpora]

        # REGEXPS
        self.RE_OBVIL_CORPUS_FILE_URL = re.compile(
            'http://132.227.201.10:8086/corpus/'
            '(?P<corpus_name>%s)/'
            '(?P<format>[^/]*)?/?'
            '(?P<file_name>[^\.]*)\.'
            '(?P<file_ext>.*)' % self.corpus_name)

    def parse(self, response):

        # Gathering the documents which constitutes the corpus
        links = response.xpath('//body/table//a/@href').extract()

        for link in links:

            # A document is only valid if it's in xml format.
            if '.xml' in link:

                file_name = link.rsplit('.xml')[0]
                self.logger.info("••••••••••••••••••••••••••••••••• Found text file %s (%s)" % (file_name, link))

                # Get related documents in other formats
                for doc_format, ext in self.available_formats.items():

                    if doc_format == 'xml':
                        related_file = "%s%s%s" % (response.url, file_name, ext)
                    else:
                        related_file = "%s%s/%s%s" % (self.start_url, doc_format, file_name, ext)

                    yield scrapy.Request(
                        related_file,
                        callback=self.harvest_file,
                        errback=self.errback_obvil_files,
                    )


class ObvilBaseCritiqueSpider(ObvilUnconventional):
    name = "obvil_critique_bib_tei_spider"

    corpus_name = 'critique'
    corpora = [
        "adam-et-feneon", "aderer", "agoult", "albalat", "alembert", "article", "asselineau", "auger", "auguis",
        "bainville", "baju", "ballanche", "barante", "barbey-aurevilly", "barine", "barres", "bashkirtseff",
        "baudelaire", "chamfort", "egger", "gautier", "champfleury", "charpentier", "chateaubriand", "claretie",
        "bazalgette", "beaunier", "beauzee", "becq-de-fouquieres", "bellesort", "bergson", "bernard", "bigot", "bloy",
        "bouchaud", "bougle", "bourget", "boutroux", "bovet", "gille", "gobineau", "goncourt-edmond",
        "bremond", "brisson", "brunetiere", "byvanck", "cailhava", "capus", "caro", "carrau", "casella-gaubert",
        "collectif", "comte", "constant", "coulanges", "cousin", "crevel", "darwin", "daudet-leon", "david-sauvageot",
        "delecluze", "deraismes", "deschamps", "deschanel", "des-essarts", "diderot",  "ghil",  "gheon",
        "doumic", "dubos", "du-bos", "du-camp", "du-casse", "du-fresnois", "dumarsais", "dupuy", "durkheim", "duval",
        "equilbecq", "etienne", "faguet", "flat", "fontanes", "fouillee", "france", "frommel", "gaucher", "gaultier",
        "gourmont", "gourmont-jean", "guizot", "guyau", "hazard", "hennequin", "heumann", "hugo", "huret",
        "janet", "janin", "jarry", "kahn", "kufferath", "la-bruyere", "lagardie", "la-grange", "la-harpe",
        "lamartine", "lami", "la-motte", "lanson", "lasserre", "le-blond", "leconte-de-lisle", "le-goffic", "lemaitre",
        "lievre", "mallarme", "marges", "markdown", "marmontel", "martin-du-gard-maurice", "mendes", "mennechet",
        "goncourt-edmond-et-jules", "merimee", "mille", "mirbeau", "mockel", "moland", "monod", "montegut",
        "montesquieu", "moreas", "morice", "muhlfeld", "murger", "nettement", "nisard", "nordau", "palante",
        "pardo-bazan", "paris-gaston", "paulhan", "peguy", "pierre-quint", "planche", "poincare", "poitou",
        "pontmartin", "prevost-paradol", "raynaud", "rebell", "reggio", "regnier", "renan", "renard",
        "revue-action", "revue-wagnerienne", "reymond", "ribot", "rivarol", "riviere", "rod", "roederer", "ryner",
        "sacy", "sainte-beuve", "salomon", "sarcey", "sauvebois", "savine", "segalen", "seignobos", "souday",
        "souriau", "spronck", "stael", "stapfer", "stendhal", "st-victor", "taillandier", "taine", "taschereau",
        "thibaudet", "thomas", "topin", "vacherot", "verlaine", "vico", "viennet", "villemain", "vinet",
        "visan", "vogue", "voltaire", "weiss", "wilde", "wyzewa", "zola", "gautier-judith", "geoffroy"
    ]

    def __init__(self, save_directory, *args, **kwargs):

        super().__init__(save_directory=save_directory, *args, **kwargs)
        self.start_url = "http://132.227.201.10:8086/corpus/%s/" % self.corpus_name
        self.start_urls = ['%s%s' % (self.start_url, c) for c in self.corpora]



class ObvilEcoleSpider(ObvilUnconventional):
    name = "obvil_ecole_bib_tei_spider"

    corpus_name = 'ecole'
    corpora = ['manuels']

    def __init__(self, save_directory, *args, **kwargs):

        super().__init__(save_directory=save_directory, *args, **kwargs)
        self.start_url = "http://132.227.201.10:8086/corpus/%s/" % self.corpus_name
        self.start_urls = ['%s%s' % (self.start_url, c) for c in self.corpora]



class ObvilMoliereSpider(ObvilUnconventional):
    name = "obvil_moliere_bib_tei_spider"

    corpus_name = 'moliere'
    corpora = ['critique']

    def __init__(self, save_directory, *args, **kwargs):

        super().__init__(save_directory=save_directory, *args, **kwargs)
        self.start_url = "http://132.227.201.10:8086/corpus/%s/" % self.corpus_name
        self.start_urls = ["http://132.227.201.10:8086/corpus/%s/epub/" % self.corpus_name]

    def parse(self, response):

        # Gathering the documents which constitutes the corpus
        links = response.xpath('//body/table//a/@href').extract()

        for link in links:

            # A document is only valid if it's in xml format.
            if '.epub' in link:

                file_name = link.rsplit('.epub')[0]
                self.logger.info("••••••••••••••••••••••••••••••••• Found epub file %s (%s)" % (file_name, link))

                # Get related documents in other formats
                for doc_format, ext in self.available_formats.items():

                    if doc_format == 'xml':
                        for corpus in self.corpora:
                            related_file = "%s%s/%s%s" % (self.start_url, corpus, file_name, ext )
                    else:
                        related_file = "%s%s/%s%s" % (self.start_url, doc_format, file_name, ext)

                    yield scrapy.Request(
                        related_file,
                        callback=self.harvest_file,
                        errback=self.errback_obvil_files,
                    )
