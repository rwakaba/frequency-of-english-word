import sys, os
sys.path.append(os.pardir)
from argparse import ArgumentParser
from collections import Counter

from pymongo import MongoClient
import treetaggerwrapper
from wordcloud import WordCloud

from common.functions import get_tokens, word_and_count, save_image

class AwsBlogNP():
  def __init__(self):
    self.client = MongoClient('localhost', 27017)
    self.db = self.client['aws-blogs']
    self.collection = self.db['posts']
    print('posts count ', self.collection.count(), file=sys.stderr)
    
    self.tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR='.')

  def _frequency_per_year(self, year):
    frequency = Counter()
    blog_num = 0
    pos_set = {'NP'}
    stopwords = {'AWS', 'Amazon', 'and'}
    for post in self.collection.find({'year': year}):
      blog_num += 1
      for p in post['body']:
        tokens = get_tokens(self.tagger, p, pos_set=pos_set, stopwords=stopwords)
        frequency.update(tokens)
    print('{0}, blog num:'.format(year), blog_num, file=sys.stderr)
    return word_and_count(frequency, blog_num, num=500)

  def frequency_by_pos(self, pos_set):
    frequency = Counter()
    blog_num = 0
    blog_processed_count = 0
    stopwords = {'AWS', 'Amazon', 'be', 'use', 'create', 'make', 'run', 'start'}
    for post in self.collection.find():
      blog_num += 1
      for p in post['body']:
        tokens = get_tokens(self.tagger, p, pos_set=pos_set, stopwords=stopwords)
        frequency.update(tokens)

      blog_processed_count += 1
      if (blog_processed_count % 100 == 0):
        print("Processed {0} posts..".format(blog_processed_count), file=sys.stderr)

    return word_and_count(frequency, blog_num, num=500)

  def gen_word_cloud_per_year(self, year):
    freq = self._frequency_per_year(year)
    # print(freq, file=sys.stderr)
    wordcloud = WordCloud().generate_from_frequencies(freq)
    save_image(wordcloud, "{0}.png".format(year))

if __name__ == '__main__':
  usage = 'Usage: python {} POS [--out <file>] [--wordcloud] [--help]'\
          .format(__file__)
  argparser = ArgumentParser(usage=usage)
  argparser.add_argument('pos', type=str,
                         help='None, Verb, Adjective or Adverb')
  argparser.add_argument('-o', '--out', type=str,
                         action='store',
                         help='todo')
  argparser.add_argument('-wc', '--wordcloud',
                         action='store_true',
                         help='todo')
  argparser.add_argument('-c', '--cat', type=str,
                         dest='another_file',
                         help='concatnate target file name')
  args = argparser.parse_args()
  if args.out:
    print("out is {0}".format(args.out))
    fpath = args.out
  if args.wordcloud:
    print("word is true")
    # TODO switch way to save to word cloud.

  aws_blog_np = AwsBlogNP()
  if args.pos == 'None':
    for year in range(2012, 2018):
      aws_blog_np.gen_word_cloud_per_year(year)
  elif args.pos == 'Verb':
    pos_set = {'VV', 'VVN', 'VVG', 'VVP', 'VVD', 'VVZ', 'VB', 'VBD', 'VBZ', 'VBG', 'VBN', 'VBP'}
    aws_blog_np.frequency_by_pos(pos_set)
  elif args.pos == 'Adjective':
    pos_set = {'JJ', 'JJR', 'JJS'}
    aws_blog_np.frequency_by_pos(pos_set)
  elif args.pos == 'adverb':
    pos_set = {'RB', 'RBR', 'RBS'}
    aws_blog_np.frequency_by_pos(pos_set)
  else:
    print("Unsupport POS was specified. {0}".format(args.pos))

