#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tei_to_nakala_csv.py is part of the project OBVILCorpusImporter
Author : Valérie Hanoka

Adaptation de tei_to_omeka.py pour prendre en compte la nouvelle
plateforme nakala.
Modified by : 
    Anne-Laure Huet
    Arthur Provenier
"""

import os
import csv
import glob
import logging
from re import sub

from teiexplorer.corpusreader import tei_content_scraper as tcscraper
from vignettes.image_generator import create_image
from utils.language_code import LanguageCode

###########################################################
#                     GETTING METADATA
###########################################################


def tei_to_nakala_header(csv_header_info):
    """ Transforms an XML-TEI header path to a Nakala metadata file (.csv)"""


    # XML-TEI headers elements to Linked Data correspondences
    xml_tag_to_voc = {
        u"#fileDesc#titleStmt_title": u"title",
        u"#fileDesc#titleStmt_author_key": u"creator",
        u"#fileDesc#sourceDesc#bibl_publisher": u"publisher",
        u"#fileDesc#sourceDesc#bibl_pubPlace": u"pubPlace",
        u"#fileDesc#sourceDesc#bibl_date": u"date",
        u"#profileDesc#langUsage_language_ident": u"language",
        u"#fileDesc#sourceDesc#bibl_ref_target":u"relation",
        u"#fileDesc#publicationStmt_idno": u"identifier",  # Obligatoire
        u"#fileDesc#publicationStmt#availability_licence_target": u"rights",
    }


    new_csv_header_info = {xml_tag_to_voc.get(k, k): v for (k, v) in csv_header_info.items()}

    if u"creator" not in new_csv_header_info:
        not_normalized_creator_form = new_csv_header_info.get(u"#fileDesc#titleStmt_author", False)

        if not_normalized_creator_form:
            new_csv_header_info[u"creator"] = not_normalized_creator_form

    return {k: v for (k, v) in new_csv_header_info.items() if not k.startswith('#')}


def parse_tei_documents(corpora, nakala_csv_folder='crawled_data'):
    """
    Extracting metadata from all the XML-TEI documents in corpora.
    :param corpora: Corpora locations where TEI files are stored
    :param nakala_csv_folder: The folder where the transformed metadata
                             information in Omeka CSVimport format should
                             be written.
    :return:
    """

    # Creating the folder if it does not exists
    if not os.path.exists(nakala_csv_folder):
        os.makedirs(nakala_csv_folder)

    # Dictionnary of iso code, from iso_639_1 to iso_639_2b
    language_code = LanguageCode()

    # The 'corpus_tag' corresponds to a label giving a hint on the corpus provenance.
    for (corpus_tag, corpus_location) in corpora.items():

        corpus_location = sub('__SAVE_DIRECTORY__', nakala_csv_folder, corpus_location)

        for document_file in glob.glob(corpus_location):

            logging.info(u"Parsing %s" % document_file)
            document = tcscraper.TeiContent(document_file, corpus_tag)
            csv_header_info = document.header_to_nakala_dict()

            # Translating TEI headers to Semantic Web relations
            csv_header_info = tei_to_nakala_header(csv_header_info)

            #print('csv_header_info_tei' + str(csv_header_info)) = ne trouve que 3 langue
            # Adding other attributes
            csv_header_info.update({u"format": "application/xml"})

            # Usually, the identifiers given in the XML-TEI are faulty.

            identifier = document_file.split('.')[0].split('/')[-1]
            html_identifier = "http://132.227.201.10:8086/corpus/%s/html/%s.html" % (corpus_tag, identifier)
            csv_header_info["identifier"] = html_identifier

            """
            # We need to compute a clean form of it, pointing to the html document.
            csv_url_files = sub(r'\.xml$', '.csv', document_file)
            with open(csv_url_files, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                links_to_document = sorted(
                    set([row[1].replace(' ', '') for row in reader]),
                    key=lambda x: x[-3:]  # sort by the 3 last letters of ext. Silly way to have a constant order
                )

            csv_header_info["identifier"] = document.OMEKA_SPLIT_CHAR.join(links_to_document)
            """

            #Delete 'dcterms:source'
            if u"dcterms:source" in csv_header_info:
                del csv_header_info["dcterms:source"]


            # Normalized form for 'publisher'
            if u"pubPlace" in csv_header_info:
                publisher = csv_header_info.get("publisher")
                pubPlace = csv_header_info.get("pubPlace")
                csv_header_info["publisher"] = str(publisher) + " (" + str(pubPlace) + ") "
                del csv_header_info["pubPlace"]

            # Normalized 'language'
            current_lang = csv_header_info.get(u"language", False)
            if current_lang:
                lang_normalized = language_code.get_iso_code(current_lang)
                csv_header_info[u"language"] = lang_normalized

            # author for vignette
            author_vignette = csv_header_info.get("creator", "Anonyme")
            if ";" in author_vignette:
                author_vignette = author_vignette.replace(";","\n")


            # Producing the vignette
            image_identifier = "%s_%s" % (corpus_tag, identifier)
            create_image(
                identifier=image_identifier,
                title=csv_header_info.get("title", "Sans titre"),
                author=author_vignette,
                save_in_folder= "%s/%s" %(nakala_csv_folder, corpus_tag)
            )

            # Add the link for the vignette in 'relation'
            csv_header_info['relation'] = \
                'http://132.227.201.10:8086/corpus/vignettes_corpus/%s.png' % image_identifier

            #csv_header_info['rights'] = u'Copyright © 2018 Université Paris-Sorbonne, agissant pour le Laboratoire d’Excellence « Observatoire de la vie littéraire » (ci-après dénommé OBVIL). Ces ressources électroniques protégées par le code de la propriété intellectuelle sur les bases de données (L341-1) sont mises à disposition de la communauté scientifique internationale par l’OBVIL, selon les termes de la licence Creative Commons : « Attribution - Pas d’Utilisation Commerciale - Pas de Modification 3.0 France (CC BY-NC-ND 3.0 FR) ». Attribution : afin de référencer la source, toute utilisation ou publication dérivée de cette ressource électroniques comportera le nom de l’OBVIL et surtout l’adresse Internet de la ressource. Pas d’Utilisation Commerciale : dans l’intérêt de la communauté scientifique, toute utilisation commerciale est interdite. Pas de Modification : l’OBVIL s’engage à améliorer et à corriger cette ressource électronique, notamment en intégrant toutes les contributions extérieures, la diffusion de versions modifiées de cette ressource n’est pas souhaitable.'

            # Add 'rights'
            csv_header_info['rights'] = u'http://creativecommons.org/licenses/by-nc-nd/3.0/fr/'

            # Add 'type'
            csv_header_info['type'] = u'Text'

            del document

            ### Write metadata in NAKALA format
            csv_file = u'%s/%s.csv' % (nakala_csv_folder, corpus_tag)
            with open(csv_file, 'w', encoding="utf-8") as fout:
                fout.write('METADONNEES,VALEURS\n')
                for md_name, md_value in csv_header_info.items():
                    fout.write('%s,"%s"\n' %(md_name, md_value)

