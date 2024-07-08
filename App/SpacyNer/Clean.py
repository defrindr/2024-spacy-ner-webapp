import pandas as pd
import re

import spacy

import nltk
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
sFactory = StemmerFactory()
stemmer = sFactory.create_stemmer()

stopwordFactory = StopWordRemoverFactory()

class Clean():
  def cleaning(self, text):
      # remove link
      text = re.sub(
          r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)", "", text)
      # remove hashtag
      text = re.sub(r"(\#[\w]+)", "", text)
      # remove username
      text = re.sub(r"(@[\w]*)", "", text)

      return text


  def cleaning(self, text):
      # remove link
      text = re.sub(
          r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)", "", text)
      # remove hashtag
      text = re.sub(r"(\#[\w]+)", "", text)
      # remove username
      text = re.sub(r"(@[\w]*)", "", text)

      return text


  def casefolding(self, text):
      return text.lower()


  def tokenisasi(self, text):
      return nltk.tokenize.word_tokenize(text)


  def filtering(self, text):
      return [item for item in text if item not in stopwordFactory.get_stop_words()]


  def stemming(self, text):
      return stemmer.stem(' '.join(text)).split(' ')


  def ready(self, text):
      return ' '.join(text)


  def ner(self, text):
      # result= nlp(' '.join(text))
      # for doc in result:
          # print(doc.label)
      return text