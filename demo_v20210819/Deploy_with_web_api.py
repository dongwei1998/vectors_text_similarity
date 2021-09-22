# coding=utf-8
# =============================================
# @Time      : 2021-08-16 10:23
# @Author    : DongWei1998
# @FileName  : Deploy_with_web_api.py
# @Software  : PyCharm
# =============================================
import sys
sys.path.append('/home/text_voctor_similarity')
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
import sys




from multiprocessing import Pool
import time




app = Flask(__name__)


class Predictor(object):
    def __init__(self, doc2vec_model_file, word2vec_model_file, fasttext_model_file):
        # 加载模型

        self.doc2vec_model = Doc2Vec.load(doc2vec_model_file)
        self.word2vec_model = Word2Vec.load(word2vec_model_file)
        self.fasttext_model = FastText.load(fasttext_model_file)


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


class My_Sql(object):
    def __init__(self, localhost, user, password, database, charset='utf8'):
        # 加载模型
        self.localhost = localhost
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.cursor = None
        self.db = None

    # 连接数据库返回游标
    def connecting_database(self):
        # 连接数据库
        self.db = pymysql.connect(host=self.localhost, user=self.user, password=self.password, database=self.database,
                                  charset=self.charset,port=9566)
        # 获取游标
        self.cursor = self.db.cursor()

    # 关闭数据库
    def close_mysql(self):
        self.db.close()

    # 根据案号查询数据库
    def select_case_number(self,CASE_NO):


        '''
        CASE_TYPE = sql_r[0][2]
        CAUSE_OF_ACTION = sql_r[0][4]
        NATURE_OF_DOCUMENTS
        :param CASE_NO:
        :return:
        '''
        select_sql = f'''select a.CASE_ID,a.CASE_NAME,a.CASE_TYPE,a.CASE_CONTENT,b.CAUSE_OF_ACTION,b.NATURE_OF_DOCUMENTS,b.COURT ,b.CASE_NO,a.CASE_VECTOR
                        from klm_case_info as a INNER JOIN klm_case_struct as b 
                        on a.CASE_ID=b.CASE_ID 
                        where b.CASE_NO = "{CASE_NO}" '''
        try:
            self.cursor.execute(select_sql)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    # 根据关键词查询数据库
    def select_case_key(self,CASE_TYPE,CAUSE_OF_ACTION,NATURE_OF_DOCUMENTS):

        if NATURE_OF_DOCUMENTS is None:
            select_sql = f'''select a.CASE_ID,a.CASE_NAME,a.CASE_TYPE,a.CASE_CONTENT,b.CAUSE_OF_ACTION,b.NATURE_OF_DOCUMENTS,b.COURT ,b.CASE_NO,a.CASE_VECTOR
                                    from klm_case_info as a INNER JOIN klm_case_struct as b 
                                    on a.CASE_ID=b.CASE_ID 
                                    where a.CASE_TYPE = "{CASE_TYPE}" or b.CAUSE_OF_ACTION = "{CAUSE_OF_ACTION} "'''
        else:
            select_sql = f'''select a.CASE_ID,a.CASE_NAME,a.CASE_TYPE,a.CASE_CONTENT,b.CAUSE_OF_ACTION,b.NATURE_OF_DOCUMENTS,b.COURT ,b.CASE_NO,a.CASE_VECTOR
                        from klm_case_info as a INNER JOIN klm_case_struct as b 
                        on a.CASE_ID=b.CASE_ID 
                        where a.CASE_TYPE = "{CASE_TYPE}" or b.CAUSE_OF_ACTION = "{CAUSE_OF_ACTION}" or b.NATURE_OF_DOCUMENTS = "{NATURE_OF_DOCUMENTS}"'''
        try:
            self.cursor.execute(select_sql)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

def cos(array1, array2):
    norm1 = math.sqrt(sum(list(map(lambda x: math.pow(x, 2), array1))))
    norm2 = math.sqrt(sum(list(map(lambda x: math.pow(x, 2), array2))))
    sim = sum([array1[i] * array2[i] for i in range(0, len(array1))]) / (norm1 * norm2)
    # sim = '%.2f' % (sim*100)    # 百分比转换
    return sim

def select_sql(case_number):
    pass


def info_data(infos):
    pass


# 通过法院层级判断
# todo 目前没有法律层级表，待收集构建
def court_level_judgment(tag_case_courts,tags_case_courts):
    # 一审为基于级别管辖取得管辖权的各级法院。二审为一审法院的上一级法院。再审则是原审法院、上级法院或最高人民法院
    return False

# 判断原告被告是否相似  plaintiff   defendant
def plaintiff_defendant(sql_r,sim_case):
    '''
    输入的参数为两篇文章的正文部分【提取原告以及被告模型调用】
    :return:
    '''
    type = 2  # 代表同审理案件
    try:
        t_plaintiff = get_yg(sql_r)['原告']
    except:
        t_plaintiff = None
    try:
        t_defendant = get_bg(sql_r)['被告']
    except:
        t_defendant = None
    try:
        s_plaintiff = get_yg(sim_case)['原告']
    except:
        s_plaintiff = None
    try:
        s_defendant = get_bg(sim_case)['被告']
    except:
        s_defendant = None
    if t_plaintiff is None or s_plaintiff is None:
        if t_defendant is None or s_defendant is None:
            return 2
        else:
            t_defendant.replace('^','').replace('#','').replace('@','')
            s_defendant.replace('^','').replace('#','').replace('@','')
            sim = title_similarity(t_defendant, s_defendant)
            if sim > 0.80:
                return 1
    else:

        # todo 判断原告
        t_plaintiff.replace('^', '').replace('#', '').replace('@', '')
        s_plaintiff.replace('^', '').replace('#', '').replace('@', '')
        sim = title_similarity(t_plaintiff, s_plaintiff)
        if sim > 0.90:
            return 1
        else:
            if t_defendant is not None or s_defendant is not None:
                # todo 判断被告
                t_defendant.replace('^', '').replace('#', '').replace('@', '')
                s_defendant.replace('^', '').replace('#', '').replace('@', '')
                sim = title_similarity(t_defendant, s_defendant)
                if sim > 0.80:
                    return 1
            else:return 2







# 通过标题判断
def title_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() #引用ratio方法，返回序列相似性的度量



# 历审  同审   案件
def data_formatting(sql_r,sim_list,limit):
    tag_title = sql_r[0][1]
    datas = []
    for sim_case in sim_list:
        type = 2
        if '二审' in tag_title :
            if '一审' in sim_case[1]:
                sim = title_similarity(tag_title, sim_case[1])
                if sim > 0.95:
                    type = 1
            datas.append({"case_id": sim_case[0], "case_no": sim_case[-2], "type": type, "score": sim_case[-1]})
        elif '再审' in tag_title:
            if '一审' in sim_case[1] or '二审' in sim_case[1]:
                sim = title_similarity(tag_title, sim_case[1])
                if sim > 0.95:
                    type = 1
            datas.append({"case_id": sim_case[0], "case_no": sim_case[-2], "type": type, "score": sim_case[-1]})
        elif sql_r[0][-2] != '':
            if sql_r[0][-2] in sim_case[4]: # 判断目标案件的案号是否在相似案件中
                type = 1
            datas.append({"case_id": sim_case[0], "case_no": sim_case[-2], "type": type, "score": sim_case[-1]})
        elif sql_r[0][4] !='' and  sim_case[5] != '': # 判断两篇文章中的原告被告
            type = plaintiff_defendant(sql_r[0][4], sim_case[5])
            datas.append({"case_id": sim_case[0], "case_no": sim_case[-2], "type": type, "score": sim_case[-1]})
        else:
            datas.append({"case_id":sim_case[0],"case_no":sim_case[-2],"type":type,"score":sim_case[-1]})
    if limit == '':
        return datas[:20]
    return datas[:limit]




# todo 优化计算速度
def sim_calculate_threading(sql_r,sql_rs,sim_list):

    # print('========================= Start ==============================')
    # print(sql_r,sql_rs[:10])
    # print('========================= End ==============================')
    tag_info = sql_r[0][-1]
    if tag_info == '' or tag_info is None:
        # 特征词向量
        CASE_VECTOR_voc = detector.get_text_vecter(sql_r[0][4])
        feature_word = ['原告', '被告']
        voc_list = detector.get_fasttext_vecter(feature_word)
        # 向量合并
        final_vector = detector.voc_connect_v1(CASE_VECTOR_voc, voc_list)
        final_vector_str = '|'.join([str(v) for v in list(final_vector)])  # 目标案件向量
        tag_info = np.array([float(i) for i in final_vector_str.split('|')])
    else:
        tag_info = np.array([float(i) for i in tag_info.split('|')])


    for info in sql_rs:

        if info[-1] != None:
            tag_infos = np.array([float(i) for i in info[-1].split('|')])
            sim = cos(tag_info, tag_infos)
            # list(info).extend([sim])
            sim_list.append([info[0],info[1],info[2],info[6],info[7],info[3],info[-2],sim])
            # sim_list.extend(info)
        else:
            pass
    # sim_list = sorted(sim_list, key=lambda x: x[-1], reverse=True)
    return sim_list

def sim_calculate(sql_r,sql_rs):
    sim_list = []
    tag_info = sql_r[0][-1]
    if tag_info == '' or tag_info is None:
        # 特征词向量
        CASE_VECTOR_voc = detector.get_text_vecter(sql_r[0][4])
        feature_word = ['原告', '被告']
        voc_list = detector.get_fasttext_vecter(feature_word)
        # 向量合并
        final_vector = detector.voc_connect_v1(CASE_VECTOR_voc, voc_list)
        final_vector_str = '|'.join([str(v) for v in list(final_vector)])  # 目标案件向量
        tag_info = np.array([float(i) for i in final_vector_str.split('|')])
    else:
        tag_info = np.array([float(i) for i in tag_info.split('|')])
    for info in sql_rs:
        if info[-1] != None:
            tag_infos = np.array([float(i) for i in info[-1].split('|')])
            sim = cos(tag_info, tag_infos)
            # list(info).extend([sim])
            sim_list.append([info[0],info[1],info[2],info[6],info[7],info[3],info[-2],sim])
            # sim_list.extend(info)
        else:
            pass
    sim_list = sorted(sim_list, key=lambda x: x[-1], reverse=True)
    return sim_list[1:]



def sim_multithreading(block_n,sql_r, sql_rs):
    sql_len = len(sql_rs)//block_n
    l = []
    pool = Pool(processes=block_n)
    start = time.time()
    r1 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[:sql_len], l])
    r2 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[sql_len:sql_len*2], l])
    r3 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[sql_len*2:sql_len*3], l])
    r4 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[sql_len*3:], l])
    pool.close()
    pool.join()
    end = time.time()
    sim_list = r1.get() + r2.get() + r3.get() + r4.get()
    # print(sql_len,sql_len*2,sql_len*3,)
    # print(len(sql_rs[:sql_len])+len(sql_rs[sql_len:sql_len*2])+len(sql_rs[sql_len*2:sql_len*3])+len(sql_rs[sql_len*3:]))
    sim_list = sorted(sim_list, key=lambda x: x[-1], reverse=True)[1:]
    print(f'基于案号相似度计算，多进程用时{end - start}')
    return sim_list


if __name__ == '__main__':

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
    # 实例化数据库
    sql_obj = My_Sql('127.0.0.1', 'root', 'root', 'zhfw')
    # 打开数据库
    sql_obj.connecting_database()

    @app.route('/')
    def hello_world():
        return jsonify({
            'result': 'hello word'
        })
    @app.route('/similarity',methods=['POST'])
    def similarity():
        data_dict = request.form.to_dict()
        # print(data_dict)
        # 参数获取
        CASE_NO = data_dict['case_no']                   # 案号
        CASE_ID = data_dict['case_id']                  # 案件id
        CASE_NAME = data_dict['case_name']               # 案件标题
        CASE_TYPE = data_dict['case_type']                  # 案件类型
        CAUSE_OF_ACTION = data_dict['cause_of_action']         # 案由
        COURT = data_dict['court']                          # 审理法院
        TRIAL_AFTER = data_dict['trial_after']              # 案情简介
        LIMIT = int(data_dict['limit'] )                 # 返回条数 输入10就实现返回10条同类数据
        ATTRIBUTE1 = data_dict['attribute1']                 # 扩展字段1
        ATTRIBUTE2 = data_dict['attribute2']                 # 扩展字段2
        ATTRIBUTE3 = data_dict['attribute3']                 # 扩展字段3
        # 模式一：使用案号查库
        if CASE_NO != '':
            # 查库，返回数据
            start = time.time()
            sql_r = sql_obj.select_case_number(CASE_NO)
            if sql_r != []:
                CASE_TYPE = sql_r[0][2]
                CAUSE_OF_ACTION = sql_r[0][4]
                NATURE_OF_DOCUMENTS = sql_r[0][5]
                sql_rs = sql_obj.select_case_key(CASE_TYPE,CAUSE_OF_ACTION,NATURE_OF_DOCUMENTS)
            else:
                return jsonify({
                'status': 0,
                'message': f'未查询到当案号为{CASE_NO}的案件！！！'
            })
            # 相似度计算
            end = time.time()
            print('基于案号查询数据，耗时 %s 秒' % (end - start))
            # print(sql_r)

            # # 多进程
            # l  = []
            # pool = Pool(processes=4)
            # start = time.time()
            # r1 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[:3333],l])
            # r2 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[3332:4444], l])
            # r3 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[4444:6666], l])
            # r4 = pool.apply_async(sim_calculate_threading, [sql_r, sql_rs[6665:9483], l])
            # pool.close()
            # pool.join()
            # end = time.time()
            # sim_list = r1.get() + r2.get() + r3.get() + r3.get()
            # sim_list = sorted(sim_list, key=lambda x: x[-1], reverse=True)[1:]
            # print(f'基于案号相似度计算，多进程用时{end - start}')

            block_n = 4
            sim_list = sim_multithreading(block_n,sql_r,sql_rs)


            # start = time.time()
            # sim_list = sim_calculate_threading(sql_r, sql_rs,l)
            # print(len(sim_list))
            # end = time.time()
            # print('基于案号相似度计算，单进程耗时 %s 秒' % (end - start))
            # 历审 or 同类案件分离  数据格式化
            start = time.time()
            datas = data_formatting(sql_r,sim_list,limit=LIMIT)
            end = time.time()
            print('基于案号历审 or 同类计算，耗时 %s 秒' % (end - start))
            return jsonify({
                  "status": 1,
                  "message": "查询成功",
                  "data": datas
            })
        # 模式二：通过案情简介、案由、案件类型等信息
        # 案件类型、审理法院、案情简介、案由
        elif TRIAL_AFTER != '':
            # 案情简介向量
            start = time.time()
            CASE_VECTOR_voc = detector.get_text_vecter(TRIAL_AFTER)
            # 特征词向量
            feature_word = [word for word in jieba.cut(''.join([CASE_NAME,CASE_TYPE,CAUSE_OF_ACTION,COURT]))]
            if feature_word == []:
                feature_word = ['原告','被告']
            voc_list = detector.get_fasttext_vecter(feature_word)
            # 向量合并
            final_vector = detector.voc_connect_v1(CASE_VECTOR_voc,voc_list)
            final_vector_str = '|'.join([str(v) for v in list(final_vector)]) # 目标案件向量
            # 产库，返回数据
            NATURE_OF_DOCUMENTS = ''    # 文书类型
            # a.CASE_ID,a.CASE_NAME,a.CASE_TYPE,a.CASE_CONTENT ,b.CAUSE_OF_ACTION,b.NATURE_OF_DOCUMENTS,b.COURT ,b.CASE_NO,a.CASE_VECTOR
            sql_r = [[CASE_ID,CASE_NAME,CASE_TYPE,COURT,TRIAL_AFTER,CAUSE_OF_ACTION,NATURE_OF_DOCUMENTS,CASE_NO,final_vector_str]]
            sql_rs = sql_obj.select_case_key(CASE_TYPE, CAUSE_OF_ACTION,NATURE_OF_DOCUMENTS=None)
            end = time.time()
            print('基于案情简介查询数据，耗时 %s 秒' % (end - start))
            # 相似度计算
            start = time.time()
            block_n = 4
            sim_list = sim_multithreading(block_n,sql_r,sql_rs)
            end = time.time()
            print('基于案情简介相似度计算，耗时 %s 秒' % (end - start))
            # 历审 or 同类案件分离
            start = time.time()
            datas = data_formatting(sql_r, sim_list, limit=LIMIT)
            end = time.time()
            print('基于案情简介历审 or 同类计算，耗时 %s 秒' % (end - start))
            return jsonify({
                "status": 1,
                "message": "查询成功",
                "data": datas
            })
        else:
            return jsonify({
                'status': 0,
                'message': '必要字段不能为空 or 参数信息太少！'
            })

    app.run(host='127.0.0.1', port=4399)
