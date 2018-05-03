#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tei_to_omeka_csv.py is part of the project OBVILCorpusImporter
Author: Valérie Hanoka

"""

from teiexplorer.corpusreader import tei_content_scraper as tcscraper
from re import sub
import logging
import glob
import os
import csv

###########################################################
#                     GETTING METADATA
###########################################################


def tei_to_omeka_header(csv_header_info):
    """ Transforms an XML-TEI header path to a Omeka (semantic-web compliant) header."""


    # XML-TEI headers elements to Linked Data correspondences
    xml_tag_to_voc = {
        u"#fileDesc#titleStmt_title": u"dcterms:title",
        u"#fileDesc#titleStmt_author_key": u"dcterms:creator",
        u"#fileDesc#titleStmt_author": u"dcterms:creator",
        u"#fileDesc#editionStmt#respStmt": u"dcterms:contributor",
        u"#fileDesc#publicationStmt_publisher": u"dcterms:publisher",
        u"#profileDesc#creation_when": u"dcterms:date",
        u"#profileDesc#langUsage_ident": u"dcterms:language",
        u"#fileDesc#publicationStmt_idno": u"dcterms:identifier",  # Obligatoire
        u"#fileDesc#titleStmt_editor_key": u"http://schema.org/editor",
        u'#fileDesc#publicationStmt#availability#licence': u"dcterms:rights",
        u"#fileDesc#publicationStmt#availability#licence_": u"dcterms:rights",
        u"#fileDesc#publicationStmt#licence": u"dcterms:rights",
    }

    return {
        xml_tag_to_voc[k]: v
        for (k, v) in csv_header_info.items()
        if xml_tag_to_voc.get(k, False)
    }



def parse_tei_documents(corpora, omeka_csv_folder='crawled_data'):
    """
    Extracting metadata from all the XML-TEI documents in corpora.
    :param corpora: Corpora locations where TEI files are stored
    :param omeka_csv_folder: The folder where the transformed metadata
                             information in Omeka CSVimport format should
                             be written.
    :return:
    """

    # Creating the folder if it does not exists
    if not os.path.exists(omeka_csv_folder):
        os.makedirs(omeka_csv_folder)

    # The 'corpus_tag' corresponds to a label giving a hint on the corpus provenance.
    for (corpus_tag, corpus_location) in corpora.items():

        corpus_location = sub('__SAVE_DIRECTORY__', omeka_csv_folder, corpus_location)
        corpus_info = {}
        csv_headers = set([])

        for document_file in glob.glob(corpus_location):

            logging.info(u"Parsing %s" % document_file)

            document = tcscraper.TeiContent(document_file, corpus_tag)
            csv_header_info = document.header_to_omeka_dict()

            # Translating TEI headers to Semantic Web relations
            csv_header_info = tei_to_omeka_header(csv_header_info)

            # Adding other attributes
            csv_header_info.update({u"dcterms:format": "text/xml; text/epub"})

            # Getting all the related URLs
            csv_url_files = sub(r'\.xml$', '.csv', document_file)
            with open(csv_url_files, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                original_identifier = csv_header_info.get("dcterms:identifier", u'')
                csv_header_info["dcterms:identifier"] = "%s%s%s" % (
                    original_identifier,
                    document.OMEKA_SPLIT_CHAR,
                    document.OMEKA_SPLIT_CHAR.join([row[1] for row in reader])
                )

            csv_headers.update(csv_header_info.keys())
            corpus_info[document_file] = csv_header_info
            del document

        csv_file = u'%s/%s.csv' % (omeka_csv_folder, corpus_tag)

        with open(csv_file, 'w', encoding='utf-8') as f:
            w = csv.DictWriter(f, csv_headers)
            w.writeheader()

            for doc_id, doc_metadata in corpus_info.items():
                w.writerow(doc_metadata)