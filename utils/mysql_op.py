# -*- coding:utf-8 -*-
# @Time      : 2021-06-11 09:43
# @Author    : 年少无为呀！
# @FileName  : mysql_op.py
# @Software  : PyCharm
import jieba
import numpy as np
import pymysql
from predict import *
from tqdm import tqdm

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
                                  charset=self.charset)
        # 获取游标
        self.cursor = self.db.cursor()

    # 关闭数据库
    def close_mysql(self):
        self.db.close()

    # 查询数据
    def select_sql(self,table,*args):
        keys = ','.join([k for k in args])

        '''select a.CASE_ID,a.CASE_NAME,a.CASE_TYPE,a.CASE_CONTENT,b.CAUSE_OF_ACTION,b.NATURE_OF_DOCUMENTS 
            from klm_case_info as a INNER JOIN klm_case_struct as b 
            on a.CASE_ID=b.CASE_ID'''

        select_sql = f'''select {keys} from {table}  where CASE_ID <10'''
        try:
            results = self.cursor.execute(select_sql)
            datas = self.cursor.fetchall()
            if results >= 1:
                return datas
            else:
                return None
        except Exception as e:
            raise e

    def select_sql_v1(self):
        select_sql = '''select a.CASE_ID,a.CASE_NAME,a.CASE_TYPE,a.CASE_CONTENT,b.CAUSE_OF_ACTION,b.NATURE_OF_DOCUMENTS,b.COURT 
                        from klm_case_info as a INNER JOIN klm_case_struct as b 
                        on a.CASE_ID=b.CASE_ID '''
        try:
            results = self.cursor.execute(select_sql)
            datas = self.cursor.fetchall()
            if results >= 1:
                return datas
            else:
                return None
        except Exception as e:
            raise e


    # 数据插入
    def install_info(self,table,key,vector,CASAE_ID):
        install_sql = f'''inster into {table}({key}) VALUES ({vector})  where CASE_ID = {CASAE_ID}'''
        try:
            # 执行sql语句
            self.cursor.execute(install_sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            print(e)
            # 如果报错回滚
            self.db.rollback()


    # 数据库更新数据 UPDATE {table} SET {key} = {vector}
    def updata_info(self,table,key,vector,CASAE_ID):
        updata_sql = f'''UPDATE {table} SET {key} = "{vector}"  where CASE_ID = {CASAE_ID}'''
        try:
            # 执行sql语句
            self.cursor.execute(updata_sql)
            # 提交到数据库执行
            self.db.commit()

        except Exception as e:
            print(e)
            # 如果报错回滚
            self.db.rollback()



if __name__ == '__main__':
    # 模型加载
    doc_model = doc_lod_model(doc_model_path)
    word_model = word_lod_model(word_model_path)
    fasttext_model = fasttext_lod_model(fast_model_path)
    # 实例化数据库
    sql_obj = My_Sql('127.0.0.1','root','root','zhfw')
    # 打开数据库
    sql_obj.connecting_database()
    # 查询数据库
    # result = sql_obj.select_sql('klm_case_info','CASE_ID','CASE_CONTENT','CASE_NAME','CASE_TYPE','CASE_VECTOR')
    result = sql_obj.select_sql_v1()
    if not result == None:
        # 输出查询结果
        with tqdm(total=len(result)) as pbar:
            for info in result:
                pbar.set_description('开始批量数据向量转换入库:')
                case_id = info[0]              # 案件入库id
                case_name = info[1]            # 案件标题
                case_type = info[2]            # 案件类型
                case_of_action = info[4]       # 案由
                documents = info[5]            # 文书性质
                case_court = info[6]           # 审理法院
                trial_after = info[3]          # 案情简介/审理经过 or 全文信息
                # print(case_name,case_type,case_of_action,documents,case_court)
                # 全文向量
                CASE_VECTOR_voc = get_text_vecter(trial_after, doc_model)
                # 特征词向量
                feature_word = [word for word in jieba.cut(''.join([case_name,case_type,case_of_action,documents,case_court]))]
                voc_list = get_fasttext_vecter(feature_word, fasttext_model)
                # 向量合并
                final_vector = voc_connect(CASE_VECTOR_voc, voc_list)
                final_vector_str = '|'.join([str(v) for v in list(final_vector)])
                sql_obj.updata_info(table='klm_case_info',key='CASE_VECTOR',vector=final_vector_str,CASAE_ID=case_id)
                pbar.update(1)
    # 关闭数据库
    sql_obj.close_mysql()

