# coding=utf-8
# =============================================
# @Time      : 2021-08-16 10:23
# @Author    : DongWei1998
# @FileName  : Web_api_demo.py
# @Software  : PyCharm
# =============================================
import requests
import json
import time

ATTRIBUTE_ = {
    "case_no": "（2015）昆民初字第1029号",  # 案号   6.86s
    "case_id": "110",  # 案件id
    "case_name": "黄恩舫诉山东移动名誉权侵权纠纷",  # 案件标题
    "case_type": "民事案件",  # 案件类型
    "cause_of_action": "合同纠纷",  # 案由
    "court": "济南市市中区人民法院",  # 审理法院
    "trial_after": "原告为山东太古飞机工程公司负责人，2018年1月22日，该公司员工、客户收到陌生号码“15949703177”发来的涉嫌侮辱诽谤原告的短信。此外，原告发现新浪微博博主“包龙图再现江湖”、“雅典娜的新家”发布的微博也载有涉嫌侮辱诽谤原告的内容。原告认为我公司作为手机号码“15949703177”用户的电信运营商，应当向其提供该号码用户的身份证号码、联系方式、家庭住址等注册信息。北京微梦创科网络技术有限公司（以下简称“北京微梦公司”）作为上述两个微博账号的网络运营商，同样应提供该微博账号的相关注册信息。原告遂诉至法院，要求我公司及北京微梦公司提供涉嫌侵权人的身份信息，并赔偿原告经济损失、精神抚慰金20万元。",
    # 案情简介 / 审理经过   7.55s
    "limit": 10,  # 返回条数 输入10就实现返回10条同类数据
    "attribute1": "",  # 扩展字段1
    "attribute2": "",  # 扩展字段2
    "attribute3": "",  # 扩展字段3
}


def similarity():
    url = " http://127.0.0.1:9527/similarity"
    # todo 当case_no案号不为空使用模式一，当case_no案号为空使用模式二并且必填字段不能为空
    data = ATTRIBUTE_
    time.time()
    start =time.time()
    result = requests.post(url=url, data=data)
    end = time.time()
    if result.status_code == 200:
        obj = json.loads(result.text)
        if obj['status'] == 1:
            data = obj['data']
            print(data)
        else:
            print("{} : {} ".format(obj['status'],obj['message']))
    print('Running time: %s Seconds'%(end-start))

if __name__ == '__main__':
    similarity()