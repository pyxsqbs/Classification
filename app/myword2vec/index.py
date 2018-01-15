#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import *

""" 向量化 """

__author__ = '秦宝帅'


class MyWord2Vec(object):
    __slots__ = ('__input_url', '__output_url')  # 用tuple定义允许绑定的属性名称

    def __init__(self, input_url="", output_url=""):
        self.__input_url = input_url
        self.__output_url = output_url

    @property
    def input_url(self):
        return self.__input_url

    @input_url.setter
    def input_url(self, input_url):
        if isinstance(input_url, str):
            self.__input_url = input_url
        else:
            raise ValueError('input_url must be a string!')

    @property
    def output_url(self):
        return self.__output_url

    @output_url.setter
    def output_url(self, output_url):
        if isinstance(output_url, str):
            self.__output_url = output_url
        else:
            raise ValueError('output_url must be a string!')

    def word_2_vec(self):
        print '向量化 start'

        sentences = []
        sentences_word = []

        with open(self.__input_url, 'r') as f:
            for line in f.readlines():
                line = line.strip().decode('utf-8')  # 把末尾的'\n'删掉
                sentences.append(line)
                line = line.split(' ')
                sentences_word.append(line)

        # print sentences_word

        ''' 获取tf-idf矩阵 '''
        vectorizer = TfidfVectorizer()
        tf_idf = vectorizer.fit_transform(sentences)
        word = vectorizer.get_feature_names()
        tf_idf = tf_idf.toarray()
        sentences_tf_idf = []

        print len(sentences_word), len(word)

        for si, sv in enumerate(sentences_word):
            for wi, wv in enumerate(sv):
                sentences_tf_idf.append([])
                if wv in word:
                    sentences_tf_idf[si].append(tf_idf[si][word.index(wv)])
                else:
                    sentences_tf_idf[si].append(0.1)
            print si + 1, len(sentences_tf_idf[si]), sentences_tf_idf[si]

        model = Word2Vec(sentences_word, size=200, window=5, min_count=10, workers=4)

        # if not os.path.exists('./model'):
        #     os.mkdir('./model')
        # model.save('./model/word.model')
        # print 'model saved success to ./model/word.model'

        print '输出到 ' + self.output_url
        print '向量化 done\n'


if __name__ == '__main__':
    pub_src = "../../source"
    myWord2Vec = MyWord2Vec()
    # 向量化
    myWord2Vec.input_url = pub_src + "/thulac_out.txt"
    myWord2Vec.output_url = pub_src + "/word2vec_out.txt"
    myWord2Vec.word_2_vec()
