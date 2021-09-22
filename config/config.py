
# -*- coding:utf-8 -*-
# @Time      : 2021-04-23 16:48
# @Author    : 年少无为！
# @FileName  : config.py
# @Software  : PyCharm
# 获取当前的文件绝对路径
import os

def load_file():
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    # config.ini文件路径,获取当前目录的父目录的父目录与congig.ini拼接
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."), 'config.ini')
    print('当前目录:' + current_path)
    print('当前父目录:' + father_path)
    print('config.ini路径:' + config_file_path)


current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
o_data_path = os.path.join(father_path,'datas/all_fawu_data.xlsx')
train_data_path = os.path.join(father_path,'out/fawu_train_cut.txt')
text_data_path = os.path.join(father_path,'out/fawu_text_cut.txt')
wangyi_title_cut = os.path.join(father_path,'out/wangyi_title_cut.txt')
doc_model_path = os.path.join(father_path,'models/doc2vec/fawu_doc_model')
word_model_path = os.path.join(father_path,'models/word2vec/fawu_word_model')
fast_model_path = os.path.join(father_path,'models/fasttext/fawu_fast_model')
stop_word_path = os.path.join(father_path,'config/count_dice_falv.txt')


