import requests
import os
import json
import PyPDF2
from geoparserIO import parseWithGeoparser
from googleNLP import parseWithGoogle
from bs4 import BeautifulSoup
import re
import pandas as pd


def load_stopwords():
    """ Loads NLTK stopwords """
    import nltk
    nltk_dir = 'nltk'
    if nltk_dir not in nltk.data.path:
        nltk.data.path.append(nltk_dir)
    nltk.download('stopwords')


class annotateFile(object):
    """ Class to load, extract, and annotate a text file.

    Input
        file_path       plain string path to text file to annotate. PDF only for now

    """

    def __init__(self, file_path = 'usaid_evaluation_example.pdf'):
        self.file_path = file_path
        _, self.file_extension = os.path.splitext(self.file_path)

        # Straightaway preprocess some of the data
        self.extract_words_from_pdf()
        self.clean_pdf_text()


    def extract_words_from_pdf(self):
        pdfFileObj = open(self.file_path,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        text = ''
        for page in range(0, pdfReader.getNumPages()):
            pageObj = pdfReader.getPage(page)
            text = text + ' ' + pageObj.extractText()
        
        self.pdf_words = text

    def clean_pdf_text(self):
        """ Starts with the raw text from a document, and returns a clean list of words.

        The list can still include duplicates and is in the original order.
        """
        txt_clean = BeautifulSoup(self.pdf_words, "html5lib").get_text()
        txt_clean = re.sub("\n", ' ', txt_clean)
        txt_clean = re.sub("[^a-zA-Z]",           # The pattern to search for
                              " ",                       # The pattern to replace it with
                              txt_clean)
        txt_clean = txt_clean.lower()
        # store for later use
        self.pdf_words_clean = txt_clean
        txt_clean_list = txt_clean.split()               # Split into words, i.e. tokenize

        # remove stop words
        load_stopwords()
        from nltk.corpus import stopwords
        stop = set(stopwords.words('english'))
        txt_clean_list = [word for word in txt_clean_list if word not in stop]
        self.clean_list_of_words = txt_clean_list


    def parse_with_geoparserIO(self, start_at_char=10000, end_at_char=20000):
        self.df_geoparserIO = parseWithGeoparser(self.pdf_words_clean[start_at_char:end_at_char])
        return(self.df_geoparserIO)

    def parse_with_google_NLP(self, start_at_char=10000, end_at_char=20000):
        self.df_googleNLP = parseWithGoogle(self.pdf_words_clean[start_at_char:end_at_char])
        return(self.df_googleNLP)