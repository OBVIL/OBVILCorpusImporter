#!/usr/bin/env python

"""
    Obtenir le code ISO-639-2B pour une langue donnée
    Liste disponible sur : https://github.com/serghei-topor/language-list-csv
    https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
"""

import csv

class LanguageCode:

    def __init__(self, src="utils/language_list.csv"):
        """init"""

        self._code_iso = {}
        with open(src, 'r', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                name, common_name, iso_639_1, iso_639_2b, *_ = row
                if iso_639_1 and iso_639_2b:
                    self._code_iso[iso_639_1] = self._code_iso.get(iso_639_1, iso_639_2b)

    def get_iso_code(self, lang):
        """A partir d'un code iso_639_1, retourne 
           le code iso_639_2b"""
        return self._code_iso.get(lang, "")

if __name__ == "__main__":
    l = LanguageCode()
    print(l.get_iso_code('fr'))
    print(l.get_iso_code('es'))
    print(l.get_iso_code('it'))
    print(l.get_iso_code('en'))
    print(l.get_iso_code('la'))
