#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.mythulac.index import MyThuLac
from app.preprotext.index import PreProText
from app.myword2vec.index import MyWord2Vec

pub_src = "./source"
<<<<<<< HEAD
init_input = pub_src + "/提前结清工单.xlsx"
=======
init_input = pub_src + "/input.txt"
>>>>>>> 462e1f07bcea55733cc4fd15b92b17f756fa7e95

preProText = PreProText()
myThuLac = MyThuLac()
myWord2Vec = MyWord2Vec()

# 预处理文本
preProText.input_url = init_input
preProText.output_url = pub_src + "/prepro_out.txt"
preProText.pre_pro_text()

# 分词
myThuLac.input_url = preProText.output_url
myThuLac.output_url = pub_src + "/thulac_out.txt"
myThuLac.sep_words()

# 向量化
myWord2Vec.input_url = myThuLac.output_url
myWord2Vec.output_url = pub_src + "/word2vec_out.txt"
myWord2Vec.word_2_vec()
