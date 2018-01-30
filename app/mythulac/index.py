#!/usr/bin/env python
# -*- coding: utf-8 -*-
import thulac

""" 分词 """

__author__ = '秦宝帅'


class MyThuLac(object):
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

    def sep_words(self):
        print '分词 start'
        thu1 = thulac.thulac(T2S=True, seg_only=True)  # 繁体转化为简体，只进行分词，不进行词性标注
        # text = thu1.cut("我爱北京天安门", text=True)  # 进行一句话分词，返回文本
        thu1.cut_f(self.__input_url, self.__output_url)  # 对input.txt文件内容进行分词，输出到output.txt
        print '输出到 ' + self.output_url
        print '分词 done\n'

if __name__ == '__main__':
    pass
