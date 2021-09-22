# -*- coding:utf-8 -*-
# @Time      : 2021-05-11 15:00
# @Author    : 年少无为！
# @FileName  : model_evaluation.py
# @Software  : PyCharm
from config.config import *
from predict import *


# 加载模型
# 模型加载
# doc_model = doc_lod_model(doc_model_path)
# word_model = word_lod_model(word_model_path)
# fasttext_model = fasttext_lod_model(fast_model_path)
# 读取数据
with open('./datas/sim_test.txt','r',encoding='utf-8') as r:
    text_list = r.readlines()
    for t in text_list:
        a,b,l = t.replace('\n','').split('\t')

        break


# 向量转换


# 结果保存
