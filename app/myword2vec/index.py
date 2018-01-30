#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
<<<<<<< HEAD
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy as np
import os, math
=======
from numpy import *
>>>>>>> 462e1f07bcea55733cc4fd15b92b17f756fa7e95

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
<<<<<<< HEAD
                    sentences_tf_idf[si].append(0.0)
                    # print si + 1, len(sentences_tf_idf[si]), sentences_tf_idf[si]

        model = Word2Vec(sentences_word, size=200, min_count=10)

        if not os.path.exists('./model'):
            os.mkdir('./model')
        model.save('./model/word.model')
        print 'model saved success to ./model/word.model'

        print model
        # for i in model.most_similar(u'贷款'):
        #     print i[0], i[1]

        sentences_word_vec = []
        sentences_vec = []

        for si, sv in enumerate(sentences_word):
            sum_x = np.array([0.0 for x in range(0, 200)])
            for wi, wv in enumerate(sv):
                sentences_word_vec.append([])
                x = []
                if wv in model.wv:
                    for ci, cv in enumerate(model.wv[wv]):
                        x.append(cv)
                else:
                    x.append(0.0)
                # print x
                sentences_word_vec[si].append(np.array(x) * sentences_tf_idf[si][wi])
                # sentences_word_vec[si].append(x)
                sum_x += np.array(x)
            # print si + 1, len(sentences_word_vec[si]), sum_x
            sentences_vec.append(sum_x)

        # print sentences_vec
        # 调用kmeans类
        clf = KMeans(n_clusters=15)
        s = clf.fit(sentences_vec)
        print s

        # 4个中心
        # print '中心', clf.cluster_centers_

        # 每个样本所属的簇
        print len(clf.labels_), clf.labels_

        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
        print clf.inertia_

        # 进行预测
        print clf.predict(sentences_vec)

        # 保存模型
        # joblib.dump(clf, 'c:/km.pkl')

        # 载入保存的模型
        # clf = joblib.load('c:/km.pkl')


        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
        # clfinertia = []
        # for i in range(5, 30):
        #     clf = KMeans(n_clusters=i)
        #     s = clf.fit(sentences_vec)
        #     clfinertia.append(clf.inertia_)
        #     print i, clf.inertia_
        #
        # clfinertia_sum = 0
        # con = 4000000
        # for i in range(0, 23):
        #     # sum_i = math.atan(
        #     #     clfinertia[i] / con * (i + 3) - clfinertia[i + 1] / con * (i + 3)) - math.atan(
        #     #     clfinertia[i + 1] / con * (i + 3) - clfinertia[i + 2] / con * (i + 3))
        #     sum_i = clfinertia[i] - clfinertia[i + 1] - (clfinertia[i + 1] - clfinertia[i + 2])
        #
        #     if clfinertia_sum < sum_i:
        #         clfinertia_sum = sum_i
        #         print i + 6, sum_i

        print '输出到 ' + self.output_url
        print '向量化 done\n'
        fr = open('../../source/prepro_out.txt', 'r')
        line_x = []
        for line in fr.readlines():
            line_x.append(line)
        for i in range(0, len(clf.labels_)):
            class_i = clf.labels_[i]
            with open('./class_%d.txt' % class_i, 'a') as fw:
                fw.write(str(line_x[i]))
                # print line_x[i]
        fr.close()
=======
                    sentences_tf_idf[si].append(0.1)
            print si + 1, len(sentences_tf_idf[si]), sentences_tf_idf[si]

        model = Word2Vec(sentences_word, size=200, window=5, min_count=10, workers=4)

        # if not os.path.exists('./model'):
        #     os.mkdir('./model')
        # model.save('./model/word.model')
        # print 'model saved success to ./model/word.model'

        print '输出到 ' + self.output_url
        print '向量化 done\n'
>>>>>>> 462e1f07bcea55733cc4fd15b92b17f756fa7e95


if __name__ == '__main__':
    pub_src = "../../source"
    myWord2Vec = MyWord2Vec()
    # 向量化
    myWord2Vec.input_url = pub_src + "/thulac_out.txt"
    myWord2Vec.output_url = pub_src + "/word2vec_out.txt"
    myWord2Vec.word_2_vec()
