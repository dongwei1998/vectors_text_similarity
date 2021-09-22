# coding=utf-8
# =============================================
# @Time      : 2021-09-09 10:41
# @Author    : DongWei1998
# @FileName  : model_load.py
# @Software  : PyCharm
# =============================================
import jieba
import numpy as np
from flask import Flask, jsonify, request
import pymysql
from config.config import *
import math
import time
import re
from ygbg import get_bg,get_yg
from difflib import SequenceMatcher
from gensim.models.doc2vec import Doc2Vec
from gensim.models.word2vec import Word2Vec
from gensim.models.fasttext import FastText
import threading
import time


from multiprocessing import Pool
import time

class Predictor(object):
    def __init__(self, doc2vec_model_file, word2vec_model_file, fasttext_model_file):
        # 加载模型

        self.doc2vec_model = Doc2Vec.load(doc2vec_model_file)
        self.word2vec_model = Word2Vec.load(word2vec_model_file)
        self.fasttext_model = None


    # 向量合并 v1
    def voc_connect_v1(self,text_voc, word_voc):
        final_vector = list(text_voc)
        c = np.zeros(128, dtype=np.float32)
        n = 0
        for v in word_voc:
            c += v
            n += 1
        word_voc = list(c / n)
        final_vector.extend(word_voc)

        return np.array(final_vector)

    # 向量合并
    def voc_connect(self, word_voc):
        c = np.zeros(len(word_voc[0]), dtype=np.float32)
        n = 0
        for v in word_voc:
            c += v
            n += 1
        word_voc = list(c / n)
        return np.array(word_voc)

    # 获取文档向量
    def get_text_vecter(self, test_text):
        text_list = [word for word in jieba.cut(test_text)]
        inferred_vector_dm = self.doc2vec_model.infer_vector(text_list, steps=1000)
        return inferred_vector_dm

    # 获取 word 向量
    def get_word_vecter(self, test_text):
        voc_list = []
        for word in test_text:
            vector_dm = self.word2vec_model.wv.__getitem__(word)
            voc_list.append(vector_dm)
        word_voc = self.voc_connect(voc_list)
        return word_voc

    # 获取 fasttext 向量
    def get_fasttext_vecter(self, test_text):
        voc_list = []
        for word in test_text:
            vector_dm = self.fasttext_model.wv.__getitem__(word)
            voc_list.append(vector_dm)
        fasttext_voc = self.voc_connect(word_voc=voc_list)
        return fasttext_voc

    # 计算相似度
    def cos(self, array1, array2):
        norm1 = math.sqrt(sum(list(map(lambda x: math.pow(x, 2), array1))))
        norm2 = math.sqrt(sum(list(map(lambda x: math.pow(x, 2), array2))))
        sim = sum([array1[i] * array2[i] for i in range(0, len(array1))]) / (norm1 * norm2)
        return sim

    def voc_convert(self, text):
        case_number = text[0]
        case_txt = [word for word in jieba.cut(text[1])]
        feature_list = text[2].split('|')
        feature_word_list = []
        for sent in feature_list:
            for word in jieba.cut(sent):
                feature_word_list.append(word)
        text_voc = list(self.get_text_vecter(case_txt))
        fasttext_voc = list(self.get_fasttext_vecter(feature_word_list))

        text_voc.extend(fasttext_voc)
        return [case_number, text_voc]
# 加载模型路径
start = time.time()
doc2vec_model_file = doc_model_path
word2vec_model_file = word_model_path
fasttext_model_file = fast_model_path

if os.path.exists(doc2vec_model_file) and os.path.exists(fasttext_model_file) and os.path.exists(
        word2vec_model_file):
    # 初始化模型
    detector = Predictor(
        doc2vec_model_file,
        word2vec_model_file,
        fasttext_model_file
    )
else:
    print('未找到模型持久化文件，请检查模型路径！！！')
end = time.time()
print('模型加载耗时 %s 秒' % (end - start))