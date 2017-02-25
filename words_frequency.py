from pymongo import MongoClient
import treetaggerwrapper
from collections import Counter

import matplotlib
import matplotlib.pyplot as plt   
from wordcloud import WordCloud

def get_tokens(paragraph):
  tokens = []
  for morpheme in tagger.TagText(paragraph):
    tmp = morpheme.split('\t')
    if 2 <= len(tmp):
      pos = tmp[1]
      if pos == 'NP':
        lemma = tmp[2]
        if lemma != 'AWS' and lemma != 'Amazon':
          tokens.append(lemma)
  return tokens

def year_words(year):
  words = []
  for post in collection.find({'year': year}):
    for p in post['body']:
        words.extend(get_tokens(p))
  return words

def year_frequency(year):
  frequency = Counter()
  blog_num = 0
  for post in collection.find({'year': year}):
    # print(post['title'])
    blog_num += 1
    for p in post['body']:
      # print(p)
      frequency.update(get_tokens(p))
  return frequency, blog_num

def word_and_count(frequency, blog_num, num):
  freq = {}
  for token, count in frequency.most_common(num):
    print('{0}\t{1}\t{2}'.format(token, count, (count / blog_num)))
    freq[token] = count
    # freq.append((token, count))
  return freq

client = MongoClient('localhost', 27017)
db = client['aws-blogs']
collection = db['posts']
print('posts count ', collection.count())

tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR='.')

def frequency_per_year(year):
  f, num = year_frequency(year)
  print('{0}, blog num:'.format(year), num)
  ranknum = 30
  return word_and_count(f, num, ranknum)

def gen_word_cloud_per_year(year):
  # print(' '.join(year_words(year)))
  print(frequency_per_year(year))
  wordcloud = WordCloud(stopwords=['AWS', 'Amazon']).generate_from_frequencies(frequency_per_year(year))
  # wordcloud = WordCloud(stopwords=['AWS', 'Amazon']).generate(' '.join(year_words(year)))
  matplotlib.use("Agg")
  plt.imshow(wordcloud)
  plt.axis("off")
  # plt.show()
  plt.savefig("{0}.png".format(year))

gen_word_cloud_per_year(2012)
gen_word_cloud_per_year(2013)
gen_word_cloud_per_year(2014)
gen_word_cloud_per_year(2015)
gen_word_cloud_per_year(2016)
gen_word_cloud_per_year(2017)
