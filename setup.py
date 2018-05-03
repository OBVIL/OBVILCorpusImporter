from setuptools import setup

setup(
    name='OBVILCorpusImporter',
    version='',
    packages=[
        'obvilcorpusimporter',
        'obvilcorpusimporter.spiders',
        'obvilcorpusimporter.omeka'
    ],
    url='',
    license='',
    author='Valérie Hanoka',
    author_email='',
    description='',
    install_requires=[
        'scrapy',
        'teiexplorer',
        'json',
        'csv',
        'glob'
    ]
)
