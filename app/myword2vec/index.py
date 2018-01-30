#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy as np
import os, math
from numpy import *

reload(sys)
sys.setdefaultencoding('utf-8')

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

        '''格式化数据'''
        sentences = []
        sentences_word = []
        with open(self.__input_url, 'r') as f:
            for line in f.readlines():
                line = line.strip().decode('utf-8')  # 把末尾的'\n'删掉
                sentences.append(line)
                line = line.split(' ')
                sentences_word.append(line)

        ''' 获取tf-idf矩阵 '''
        vectorizer = TfidfVectorizer()
        tf_idf = vectorizer.fit_transform(sentences)
        word = vectorizer.get_feature_names()  # 返回词数组
        tf_idf = tf_idf.toarray()  # 返回词tf_idf值的数组
        print '句数：%d 词数：%d' % (len(sentences_word), len(word))

        '''格式化每句每词的tf_idf值'''
        sentences_tf_idf = []
        for si, sv in enumerate(sentences_word):
            for wi, wv in enumerate(sv):
                sentences_tf_idf.append([])
                if wv in word:
                    sentences_tf_idf[si].append(tf_idf[si][word.index(wv)])
                else:
                    sentences_tf_idf[si].append(0.0)
                    # print si + 1, len(sentences_tf_idf[si]), sentences_tf_idf[si]

        '''训练词向量模型'''
        word2vec_size = 2000
        if not os.path.exists('./source/model'):
            os.mkdir('./source/model')
        if os.path.exists('./source/model/word.model'):
            model = Word2Vec.load('./source/model/word.model')
            print 'model loaded success'
        else:
            model = Word2Vec(sentences_word, size=word2vec_size, min_count=0)
            model.save('./source/model/word.model')
            print 'model saved success to ./source/model/word.model'

        '''格式化 句-词向量 and 句向量'''
        sentences_word_vec = []
        sentences_vec = []
        for si, sv in enumerate(sentences_word):
            sum_x = np.array([0.0 for x in range(0, word2vec_size)])
            for wi, wv in enumerate(sv):
                sentences_word_vec.append([])
                temp = []
                if wv in model.wv:
                    for ci, cv in enumerate(model.wv[wv]):
                        temp.append(cv)
                else:
                    temp.append(0.0)
                # 句向量 = （tf_idf * 词向量）的和
                sentences_word_vec[si].append(np.array(temp) * sentences_tf_idf[si][wi])
                sum_x += np.array(temp)
            # print si + 1, len(sentences_word_vec[si]), sum_x
            sentences_vec.append(sum_x)

        print '向量化 done\n'

        '''kmeans聚类'''
        print '聚类 start'
        # 调用kmeans类
        clf = KMeans(n_clusters=7)
        s = clf.fit(sentences_vec)
        print s
        print '聚类 done\n'

        # 7个中心
        # print '中心', clf.cluster_centers_

        # 每个样本所属的簇
        # print len(clf.labels_), clf.labels_

        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
        # print clf.inertia_

        # 进行预测
        # print clf.predict(sentences_vec)

        # # 保存模型
        # joblib.dump(clf, 'c:/km.pkl')
        #
        # # 载入保存的模型
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

        '''输出每类tf_idf值 and 分类文件'''
        print '输出分类 start'
        word_class_vec = [[] for x in range(0, len(clf.cluster_centers_))]
        fr = open('./source/thulac_out.txt', 'r')
        line_x = []
        for line in fr.readlines():
            line_x.append(line)
        for i in range(0, len(clf.cluster_centers_)):
            class_filename = './source/classes/class_%d.txt' % i
            if os.path.exists(class_filename):
                os.remove(class_filename)
        for i in range(0, len(clf.labels_)):
            class_i = clf.labels_[i]
            word_class_vec[class_i].append(tf_idf[i])
            class_filename = './source/classes/class_%d.txt' % class_i
            with open(class_filename, 'a') as fw:
                fw.write(str(line_x[i]))
                # print line_x[i]
        print '输出分类 保存到 ./source/classes/'
        fr.close()
        print '输出分类 done\n'

        '''统计关键词词频'''
        print '统计词频 start'
        word_n = [[] for x in range(0, len(clf.cluster_centers_))]
        if not os.path.exists('./source/word_n'):
            os.mkdir('./source/word_n')
        for i in range(0, len(clf.cluster_centers_)):
            word_n[i] = [0.0 for x in range(0, len(word))]
            for si, sv in enumerate(word_class_vec[i]):
                for wi, wv in enumerate(sv):
                    word_n[i][wi] += wv
            word_n_filename = './source/word_n/word_n%d.txt' % i
            if os.path.exists(word_n_filename):
                os.remove(word_n_filename)
            for si, sv in enumerate(word_n[i]):
                if int(sv) > 0:
                    with open(word_n_filename, 'a') as fw:
                        fw.write('%s %d\n' % (word[si], int(sv)))
                        # print len(word_n[i])
            print '输出词频 保存到 %s' % word_n_filename
        print '统计词频 done\n'


if __name__ == '__main__':
    pub_src = "../../source"
    myWord2Vec = MyWord2Vec()
    # 向量化
    myWord2Vec.input_url = pub_src + "/prepro_out.txt"
    myWord2Vec.output_url = pub_src + "/word2vec_out.txt"
    myWord2Vec.word_2_vec()
