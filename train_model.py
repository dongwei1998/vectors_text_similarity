# -*- coding:utf-8 -*-
# @Time      : 2021-04-26 10:46
# @Author    : 年少无为！
# @FileName  : train_model.py
# @Software  : PyCharm

import gensim
from gensim.models.doc2vec import Doc2Vec
from gensim.models.word2vec import Word2Vec,PathLineSentences
from gensim.models.fasttext import FastText
TaggededDocument = gensim.models.doc2vec.TaggedDocument
from  config.config import *
import threading
import time



class myThread (threading.Thread):
    def __init__(self, name, x_train, train_model_path):
        threading.Thread.__init__(self)
        self.name = name
        self.x_train = x_train
        self.train_model_path = train_model_path
    def run(self):
        print ("开始线程：" + self.name + "模型训练")
        train_model(self.name,self.train_model_path,self.x_train)
        print ("退出线程：" + self.name + "模型训练")

def train_model(model_name,model_path,x_train):
    if model_name == 'doc2vec':
        if os.path.exists(model_path) and os.path.isfile(model_path):  # 如果已经有现成model，则load
            # load model
            print("加载Doc2Vec模型，开始训练！！！")
            model = Doc2Vec.load(model_path)
        else:
            print("创建Doc2Vec模型，开始训练！！！")
            model = Doc2Vec(x_train, min_count=1, window=3, vector_size=512, sample=1e-3, negative=5, workers=4)
        updata = model.corpus_count + len(x_train)  # total_examples参数更新


    elif model_name == 'word2vec':
        if os.path.exists(model_path) and os.path.isfile(model_path):  # 如果已经有现成model，则load
            # load model
            print("加载Word2Vec模型，开始训练！！！")
            model = Word2Vec.load(model_path)
        else:
            print("创建Word2Vec模型，开始训练！！！")
            model = Word2Vec(x_train, min_count=1, window=3, size=128, sample=1e-3, negative=5, workers=4)
        updata = model.corpus_count
    elif model_name == 'fasttext':
        if os.path.exists(model_path) and os.path.isfile(model_path):  # 如果已经有现成model，则load
            # load model
            print("加载FastText模型，开始训练！！！")
            model = FastText.load(model_path)
        else:
            print("创建FastText模型，开始训练！！！")
            model = FastText(x_train, min_count=1, window=3, size=128, sample=1e-3, negative=5, workers=4)
        updata = model.corpus_count
    else:
        print('对不起，目前只支持doc2vec或word2vce!!!')
        return
    model.train(x_train, total_examples=updata, epochs=200)  # 完成增量训练
    model.save(model_path)  # 保存模型

# 获取训练数据
def get_datasest(train_data):
    word_train = PathLineSentences(train_data)
    with open(train_data, 'r',encoding='utf-8') as cf:
        docs = cf.readlines()
        print(f'数据长度为{len(docs)}')
    doc_train = []
    # y = np.concatenate(np.ones(len(docs)))
    for i, text in enumerate(docs):
        word_list = text.split(' ')
        l = len(word_list)
        word_list[l - 1] = word_list[l - 1].strip()
        document = TaggededDocument(word_list, tags=[i])
        doc_train.append(document)
        if i == 100:
            break
    return doc_train,word_train


if __name__ == '__main__':

    # 获取数据
    doc_train_data,word_train_data = get_datasest(train_data_path)
    # 创建新线程
    thread1 = myThread("doc2vec",doc_train_data,doc_model_path)
    thread2 = myThread("word2vec",word_train_data,word_model_path)
    thread3 = myThread("fasttext", word_train_data, fast_model_path)
    # 开启新线程
    thread1.start()
    thread2.start()
    thread3.start()
    print("退出主线程")



