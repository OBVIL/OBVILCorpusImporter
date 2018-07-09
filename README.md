![OBVILCorpusImporter](https://github.com/Valerie-Hanoka/OBVILCorpusImporter/blob/master/illustration.jpg)


# OBVILCorpusImporter

This project is intended to ease the mass import of the
[OBVIL Library](http://132.227.201.10:8086/bibliotheque) into
the [OBVIL OAI-PMH repository](http://obvil.lip6.fr/omeka/). 


#### What is this script doing 

Once launched with the proper command, (for instance  
``python3 scrap_obvil_corpora.py -s "crawled_data" -c ../configs/config_omeka.json 
`` ) this will crawls the specified<sup id="a1">[1](#f1)</sup> 
OBVIL Corpora available in the 
[OBVIL Library](http://132.227.201.10:8086/bibliotheque). 

It will: 
* saves XML/TEI version of the texts in the specified directory (I.e. ``"crawled_data"``);
* extracts the relevant header meta-data to be exposed in the OAI-PMH repository
 (eg. dc:creator, dc:relation, dc:rights, dc:format, dc:identifier, dc:title, dc:contributor...)
* creates a thumbnail ("vignette") for each document. All the thumbnails have been generated once 
 and are stored [here](http://132.227.201.10:8086/corpus/vignettes_corpus/). In case some are missing,
  you may consider scp them directly with your admin privileges. 
* builds one Omeka csv import file per specified project with all the necessary information in the
 specified directory (I.e. ``"crawled_data"``);.

###### Tl;dr:
* ``python3 scrap_obvil_corpora.py -s "crawled_data" -c ../configs/config_omeka.json 
`` 
* All you need is in the folder `crawled_data`. 



#### What it does not do (i.e. DIY)

To successfully import the documents into the OAI-PMH repository, you will need to:
 * Run this script with the right options and configuration.
 * Put the generated vignettes on [the right place on the 
    server](http://132.227.201.10:8086/corpus/vignettes_corpus/) if they are missing.
 * Manually import the generated CSV file into 
    [Omeka](http://obvil.lip6.fr/omeka/admin/users/login), with proper rights and mappings.  


#### Disclamer

 - Should you run this spiders, you are going to scrap A LOT of data.
   Use at your own risk !

 - The text provided by the OBVIL are copyrighted.



<b id="f1">1</b> To specify which corpora should be imported, you will need to custom 
a configuration file. See the "configs" directory of this repo. [↩](#a1)