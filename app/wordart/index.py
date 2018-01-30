#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wordcloud import WordCloud, STOPWORDS
import codecs
from scipy.misc import imread
import os, math
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

""" 构建词云图 """

__author__ = '秦宝帅'


class WordArt(object):
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

    def word_art(self):
        print '词云图 start'
        color_mask = imread('../../source/cloud.jpg')  # 读取背景图片
        stopwords = set(STOPWORDS)
        stopwords.add("提前")
        stopwords.add("还款")
        cloud = WordCloud(
            # 设置字体，不指定就会出现乱码
            font_path='../../source/Source Han Sans CN Regular.ttf',
            # 设置背景色
            background_color='white',
            # 词云形状
            mask=color_mask,
            # 允许最大词汇
            max_words=500,
            # 最大号字体
            max_font_size=120,
            stopwords=stopwords,
        )
        for i in range(0, 7):
            word_n_filename = '%s/word_n%d.txt' % (self.input_url, i)
            fr = open(word_n_filename, 'r')
            text = {}
            max_v = 0
            for line in fr.readlines():
                temp = line.strip().split(' ')
                if float(temp[1]) > max_v:
                    max_v = float(temp[1])
                if temp[0] == '提前' \
                        or temp[0] == '还款' \
                        or temp[0] == '结清' \
                        or temp[0] == '申请' \
                        or temp[0] == '周转' \
                        or temp[0] == '玖富' \
                        :
                    continue
                text[temp[0].decode('utf-8')] = float(temp[1])
            # print max_v
            word_cloud = cloud.generate_from_frequencies(text)  # 产生词云
            word_cloud_filename = "../../source/wordclouds/word_art_%d.jpg" % i
            word_cloud.to_file(word_cloud_filename)  # 保存图片
            #  显示词云图片
            plt.figure("word_art_%d.jpg" % i)  # 指定所绘图名称
            plt.imshow(word_cloud)
            plt.axis('off')
            plt.show()
            print "word_art_%d.jpg saved success" % i
        print '输出到 ' + self.output_url
        print '词云图 done\n'


if __name__ == '__main__':
    pub_src = "../../source"
    preProText = WordArt()
    # 词云图
    preProText.input_url = pub_src + "/word_n"
    preProText.output_url = pub_src + "/prepro_out.txt"
    preProText.word_art()
