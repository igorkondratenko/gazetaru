#from gensim.models.word2vec import Word2Vec
#
import logging
import os.path
import sys
 
from gensim.corpora import WikiCorpus
program = os.path.basename('untitled4.py')
#logger = logging.getLogger(program)
# 
#logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
#logging.root.setLevel(level=logging.INFO)
#logger.info("running %s" % ' '.join(sys.argv))
 
# check and process input arguments
#if len(sys.argv) < 3:
#    print (globals()['__doc__'] % locals())
#    sys.exit(1)
inp = 'ruwiki-latest-pages-articles.xml.bz2'
outp = 'ruwiki.txt'
space = " "
i = 0
 
output = open(outp, 'w')
wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
for text in wiki.get_texts():
    output.write(space.join(text) + "\n")
    i = i + 1
    if (i % 10000 == 0):
        print("Saved " + str(i) + " articles")
 
output.close()
print("Finished Saved " + str(i) + " articles")
    
#model = Word2Vec.load_word2vec_format('news.model.bin', binary=True)
#model = Word2Vec.load_word2vec_format('web.model.bin', binary=True)
#model.save("web")
#model = Word2Vec.load("web")
#print(model.most_similar('путин'))

#model = Word2Vec.load("news_russia")
#print(model.most_similar('украина'))


#print(model.most_similar(positive=['россия', 'украина'], negative=['путин'], topn=5))
#print(model.similarity('россия','путин'))
