import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   

def get_tokens(tagger, paragraph, pos_set, stopwords={}):
  tokens = []
  pos_map = {}
  for morpheme in tagger.TagText(paragraph):
    tmp = morpheme.split('\t')
    if 2 <= len(tmp):
      pos = tmp[1]
      if pos_set is None or pos in pos_set:
        lemma = tmp[2]
        if (pos.startswith('V')):
          pos_map[pos] = lemma
        if lemma not in stopwords:
          tokens.append(lemma)
  # print(pos_map, file=sys.stderr)
  return tokens

def writecsv_frequency(outpath, vals_gen, delimiter=','):
  with open(outpath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=delimiter)
    # writer = csv.DictWriter(csvfile, fieldnames=['word', 'count', 'frequency'], delimiter=delimiter)
    writer.writerow(['word', 'count', 'frequency'])
    # writer.writeheader()
    for token, count, freq in vals_gen:
      writer.writerow([token, count, freq])

def stdout_frequency(vals_gen):
  print('{0}\t{1}\t{2}'.format('word', 'count', 'count/blog number of the year'))
  print('{0}\t{1}\t{2}'.format('----', '-----', '-----------------------------'))
  for token, count, freq in vals_gen:
    print('{0}\t{1}\t{2}'.format(token, count, freq))

def word_and_count_gen(frequency, num, totalnum):
  freq = {}
  for token, count in frequency.most_common(num):
    freq = count / totalnum
    yield token, count, freq

def save_image(content, fpath):
  plt.imshow(content)
  plt.axis("off")
  plt.savefig(fpath)
