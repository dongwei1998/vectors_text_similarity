# -*- coding:utf-8 -*-
import re

info = '''
重庆市黔江区人民法院
民 事 判 决 书
（2015）黔法民初字第03975号
原告中国电信股份有限公司重庆分公司，住址重庆市北部新区星光五路189号。
负责人赵强，该公司总经理。
委托代理人杨波，该公司职工。
被告李才品，男，生于1981年，汉族，住重庆市黔江区。
原告中国电信股份有限公司重庆分公司诉被告李才品电信服务合同纠纷一案，原告于2015年3月25日向本院提起诉讼，本院受理后，由本院代理审判员敬也丁独任审判，依法适用简易程序于2015年6月1日公开开庭进行了审理。原告委托代理人杨波到庭参加了诉讼，被告李才品未到庭参加诉讼。本案现已审理终结。
原告中国电信股份有限公司重庆分公司诉称：被告李才品于2013年7月24日到中国电信股份有限公司黔江分公司办理业务，业务号码18996XXXXXX，其承诺资费档次为119元／月，期限为24个月，由此获得对应资费档次手机一部，被告于2014年5月起开始欠缴所办业务通信费用，现已累计达到欠费本金2426.44元，违约金390.49元，剩余应支付手机终端费用275元。原告在被告欠缴费用后，已多次通过电话、信函等催收均无果，为此，原告特诉至人民法院，请求：1、判令被告立即缴纳所办理电信业务欠费违约金，并支付承诺期内剩余应付手机终端款共计3091.47元；2、由被告承担本案的全部诉讼费用。
原告中国电信股份有限公司重庆分公司向本院提交以下证据以支持其诉讼请求：
1.登记单证明记录客户办理了业务；
2.被告身份证复印件证明被告主体适格；
3.协议书一份证明套餐内容等。
被告李才品未向本院提交答辩意见和提交证据。
经审理查明：2013年7月24日，被告李才品到重庆市黔江区电信营业厅办理手机业务，并与原告中国电信股份有限公司重庆分公司签订了中国电信股份有限公司重庆分公司服务协议，约定被告资费档次为119元／月，承诺期限为24个月，被告由此获得中兴ZTEN880F手机一部。被告于2014年5月开始欠费（包括欠费本金及违约金）至今。被告共欠本金为2426.44元，从违约之日起至起诉之日止的违约金为390.49元，手机终端款为275元，共计3091.93元。
本院认为：合法的债权债务应受法律保护。现原告中国电信股份有限公司重庆分公司出示其与被告李才品签订的服务协议要求被告缴纳所办业务欠费本金为2426.44元，从违约之日起至起诉之日止的违约金为390.49元，手机终端款为275元，共计3091.93元的诉讼请求，于法有据，本院依法予以支持。依照《中华人民共和国合同法》第六十条、第一百零七条、第一百一十三条第一款、第一百一十四条第一款，《中华人民共和国民事诉讼法》第六十四条、第一百四十四条之规定，判决如下：
被告李才品于本判决生效之日起五日内向原告中国电信股份有限公司重庆分公司支付所办业务欠费共计3091.47元。
本案案件受理费50元，减半收取25元，由被告李才品负担。
如未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟
延履行期间的债务利息。
如不服本判决，可以在判决书送达之日起十五日内向本院递交上诉状，并按对方当事人的人数或者代表人的人数提出副本，上诉于重庆市第四中级人民法院。同时，直接向本院预交上诉案件受理费。递交上诉状后上诉期满七日内仍未预交诉讼费又不提出缓交申请的，按自动撤回上诉处理。
代理审判员　　敬也丁
二〇一五年七月一日
书　记　员　　张　益
'''


def get_yg(info):
    '''
    :param info: 案件的正文
    :return: 返回字典 {原告:"",原告律师:""}
    '''
    info = re.sub(' |　|', '', info)
    lines = info.split('\n')
    ygs = []  # 原告  二维列表  第二维【第一个是原告信息，后面都是原告代理人/代理律师...】
    yg_type = '原告'
    ygls_type = '委托代理人'
    _yg_type = []
    _ygls_title = []
    i = 3
    while i < len(lines):
        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
        if len(this_line) > 90: break  # 这一行太长了，已经不是原告/被告行了 提取完了
        yg = re.findall(r'^(被告人?|被申请人|被执行人|被上诉人|原审被上诉人|一审被告)[:：]?(.*)。?', this_line)
        if yg: break
        if re.match(r'^原告|再审申请人|复议申请人|申请执行人|案外人|异议人|上诉人.*', this_line):
            yg = re.findall(r'^(原告|再审申请人|复议申请人|申请执行人|上诉人|案外人|异议人)[:：]?(.*)。?', this_line)
            if yg:
                yg_info = yg[0][1]
                yg_type = yg[0][0]
                _yg_type.append(yg_type)
                yg_desc = re.findall(r'[(（](.*?)[)）]', yg_info)  # 不规则的(）
                true_yg_desc = re.match(f'{yg_type}[(（](?P<yg_desc>.*?)[）)][:：]?', this_line)  # 原告说明判断 是否第一个
                tmp = true_yg_desc.group('yg_desc') if true_yg_desc else ''
                # print('实际原告说明:', tmp)
                # print('原告说明:', yg_desc)
                if yg_desc:
                    if tmp == yg_desc[0]:
                        yg_info = re.sub(f'[(（]?{yg_desc[0]}[)）]?[:：]?', '', yg_info)
                        yg_desc = yg_desc[0]
                    else:
                        yg_desc = ''
                else:
                    yg_desc = ''
                yg_info_list = re.split(',|，|。', re.sub('住所地：?|住址|住|\(\)', '', yg_info))
                yg_info_list = yg_info_list[0:3] + [','.join(yg_info_list[3:])]
                is_company = False
                if '职员' in this_line or '员工' in this_line or '职工' in this_line or \
                        not re.search('公司|馆|开发区|局|部门|委员会|酒店|银行|政府|厂|所', yg_info_list[0] if len(yg_info_list) >= 1 else '') or\
                        ('公司' not in this_line and '局' not in this_line and '厂' not in this_line and
                         '部队' not in this_line and '委员会' not in this_line and '部' not in this_line and
                        '执法局' not in this_line and '酒店' not in this_line and '馆' not in this_line and
                         '所' not in this_line):
                    yg_init = [''] * 5
                    if yg_desc:
                        yg_init[0] = yg_desc
                    yg_init[1] = yg_info_list.pop(0)
                    gender = re.findall('(男|女)', this_line)
                    if gender:
                        yg_init[2] = gender[0]
                        if gender[0] in yg_info_list:
                            yg_info_list.remove(gender[0])
                        if gender[0] + '性' in yg_info_list:
                            yg_info_list.remove(gender[0] + '性')
                    # birth = re.findall(r'(\d+.*?)，', this_line)
                    birth = re.findall(r'[\u4e00-\u9fa5\d]+年[\u4e00-\u9fa5\d]*月?[\u4e00-\u9fa5\d]*日?|\d{16}[1-9xX]{2}', this_line)
                    if birth:
                        yg_init[3] = birth[0]
                        yg_info_list = [re.sub(f'.*{birth[0]}.*[,，。 ]?', '', s) for s in yg_info_list if s]
                        if birth[0] in yg_info_list:
                            yg_info_list.remove(birth[0])
                    else:
                        yg_init[3] = ''
                    yg_init[4] = ','.join(yg_info_list)
                    yg_info_list = yg_init
                    yg_info_list = [re.sub(',|，|。| ', ' ', s)for s in yg_info_list]
                    yg_info_list = [s.lstrip() for s in yg_info_list]
                else:
                    is_company = True
                    company_init = [''] * 5
                    company_init[1] = yg_info_list[0]
                    if re.match(r'^住所?地?|住址?|居住地|公司地址|营业场所|注册地', lines[i + 1]):  # 公司地址在原告和原告律师之间
                        i += 1
                        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
                        addr = re.findall(r'^(住所?地?|住址?|居住地|公司地址|营业场所|注册地)[:：]?(.*)[，。 ]?', this_line)
                        if addr:
                            addr = addr[0][1]
                            yg_info_list.insert(1, addr)
                            company_init[2] = addr
                    else:
                        addr = re.findall('(住所?地?|居住地|地址|公司地址|营业场所|注册地)[:：]?(.*)[。， ]?', this_line)
                        if addr:
                            _addr = re.split('，|。| ', addr[0][1])
                            company_init[2] = _addr[0] if len(_addr) >= 1 else ''
                        else:
                            company_init[2] = addr[0][1] if addr else ''
                    if re.match(r'^法定代表人|代表人|主要负责人|诉讼代表人|经营者|负责人.*', lines[i + 1]):
                        i += 1
                        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
                        fr = re.findall(r'(法定代表人|代表人|负责人|诉讼代表人|经营者|主要负责人)[:：]?(.*)[。，, ]?', this_line)  # 法人
                        if fr:
                            fr = fr[0][1].split('，')[0]
                            yg_info_list.insert(2, fr)
                            company_init[3] = fr
                        else:
                            yg_info_list.insert(2, '')
                    elif re.findall(r'^法定代表人|代表人|主要负责人|诉讼代表人|经营者|负责人.*', lines[i]):
                        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
                        # i += 1
                        fr = re.findall(r'(法定代表人|代表人|负责人|诉讼代表人|经营者|主要负责人)[:：]?(.*)[。，, ]?', this_line)  # 法人
                        if fr:
                            fr = fr[0][1].split('，')[0]
                            yg_info_list.insert(2, fr)
                            company_init[3] = fr
                        else:
                            yg_info_list.insert(2, '')
                            
                    if yg_desc:
                        yg_info_list.insert(0, yg_desc)
                        company_init[0] = yg_desc
                    else:
                        yg_info_list.insert(0, '')
                    yg_info_list = company_init
                    yg_info_list = [re.sub(',|，|。| ', ' ', s) for s in yg_info_list]
                    yg_info_list = [s.strip() for s in yg_info_list]
                    # print('公司原告：', yg_info_list)
                
                yg_info_list.insert(1, '########') if is_company else yg_info_list.append('######')
                if not is_company:
                    yg_info = '##'.join(yg_info_list) + ''
                else:
                    yg_info = ''.join(yg_info_list[0:2]) + "##" + '##'.join(yg_info_list[2:]) + ''
                yg_tmp = []
                yg_tmp.append(yg_info)
                while True:  # 处理原告代理律师
                    if '委托代理人' in lines[i + 1] or '委托诉讼代理人' in lines[i + 1] or '法定代里人' in lines[i + 1] or '法定代理人' in \
                            lines[i + 1] or '共同委托诉讼代理人' in lines[i + 1] or '委托代理' in lines[i + 1]:
                        i += 1
                        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
                        dlr = re.findall(r'(委托代理人?|委托诉讼代理人|法定代里人|法定代理人|共同委托诉?讼?代理人)[:：]?(.*)。?', this_line)
                        if dlr:
                            dlls_init = [''] * 6
                            dlr_info = list(dlr[0])
                            _ygls_title.append(dlr_info[0])
                            dlls_init[0] = dlr_info.pop(0)
                            dlr_info = re.split(r',|，|。', dlr_info[0])
                            gender = re.findall('(男|女)', this_line)
                            if gender:
                                dlls_init[2] = gender[0]
                                if gender[0] in dlr_info:
                                    dlr_info.remove(gender[0])
                                if gender[0]+'性' in dlr_info:
                                    dlr_info.remove(gender[0] + '性')
                            else:
                                dlr_info.insert(1, '')
                                dlls_init[2] = ''
                            # birth = re.findall(r'(\d+.*?)，', this_line)
                            birth = re.findall(
                                r'[\u4e00-\u9fa5\d]+年[\u4e00-\u9fa5\d]*月?[\u4e00-\u9fa5\d]*日?|\d{16}[1-9xX]{2}',
                                this_line)
                            if birth:
                                dlls_init[3] = birth[0]
                                dlr_info = [re.sub(f'.*{birth[0]}.*[,，。 ]?', '', s) for s in dlr_info if s]
                                if birth[0] in dlr_info:
                                    dlr_info.remove(birth[0])
                            else:
                                dlr_info.insert(2, '')
                                dlls_init[3] = ''
                            dlr_type = re.findall(r'[(（](.*)[)）]', dlr_info[0])
                            true_ygls_type = re.match(f'{dlls_init[0]}[(（](?P<ls_desc>.*?)[)）][:：]?', this_line) if dlls_init else None # 律师说明判断
                            ls_type = true_ygls_type.group('ls_desc') if true_ygls_type else None
                            # print('律师真实说明:', ls_type)
                            # print('律师说明:', dlr_type)
                            if dlr_type:  # 律师说明
                                if ls_type == dlr_type[0]:
                                    dlr_info[0] = re.sub(f'[(（]?{dlr_type[0]}[)）]?[:：]?', '', dlr_info[0])
                                    dlls_init[0] = dlr_type[0]
                                else:
                                    dlls_init[0] = ''
                            else:
                                dlls_init[0] = ''
                            # 律师事务所-公司位置
                            workstop = [re.findall('.*所.*?|.*事务所.*?|.*公司.*?|.*中心.*?', s)
                                        for s in dlr_info if s and not re.search('该|系', s) and not re.match(r'^公司', s)]
                            workstop = [s for s in workstop if s]
                            if workstop and len(workstop) >= 1:
                                dlls_init[5] = workstop[0][0] + '####' if workstop[0] else '' + '####'
                                dlr_info = [re.sub(f'{workstop[0][0]}.*', '', s) for s in dlr_info]
                            else:
                                dlls_init[5] = '' + '####'

                            # 共同委托代理人处理(待处理)
                            if re.findall(r'共同委托诉?讼?代理人', lines[i]):
                                dlr_num = re.findall("[两三四五六七八]", lines[i])
                                num_dict = {'两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7}
                                dlr_num = num_dict.get(dlr_num[0]) if len(dlr_num) >= 1 else None
                            
                            if '、' not in dlr_info[0]:
                                try:
                                    res = re.findall(f'{dlls_init[0]}.*?[)）：:]?({dlr_info[0]})', this_line)
                                    if res and res[0] == dlr_info[0]:
                                        dlls_init[1], dlls_init[4] = dlr_info[0], ' '.join(dlr_info[1:])
                                except:
                                    pass
                                finally:
                                    dlls_init[1], dlls_init[4] = dlr_info[0], ' '.join(dlr_info[1:])
                            dlr_info = dlr_info[0:3] + [','.join([s for s in dlr_info[3:] if s])]
                            dlls_init = [s.strip() for s in dlls_init]
                            
                            if dlr_info[0] and '、' in dlr_info[0]:
                                dlr_tmp = dlr_info[0].split('、')
                                index = dlr_info[0].count('、') + 1
                                dlls_init = ["##".join(
                                    [dlls_init[0], dlr_tmp[i]] + dlls_init[2:4] + [s for s in dlr_info[1:] if s] + [
                                        dlls_init[5]]) + '##' for i in range(index)]
                                yg_tmp.extend(dlls_init)
                            else:
                                yg_tmp.append(dlls_init[0] + "##" + '##'.join(dlls_init[1:]) + '##')
                                
                    else:
                        break
                ygs.append(yg_tmp)
        i += 1
    # 整理数据
    result, yg, ygls = {}, [], []  # 最终结果/原告/原告律师/被告/被告律师
    for index, yg_list in enumerate(ygs):
        if yg_list:
            yg.append(f'{yg_list.pop(0)}##{index + 1}')
            if len(yg_list) > 1:
                ygls.append('@@'.join([f'{a}##{index + 1}' for a in yg_list]))
            elif len(yg_list) == 1:
                ygls.append('@@' + f'{yg_list[0]}##{index + 1}')
    for i, q in enumerate(ygls):
        if q.startswith("@@", 0, 2):
            ygls[i] = ygls[i].replace('@@', '')
    result['原告'] = f'{_yg_type[0] if _yg_type else yg_type}^^' + '@@'.join(yg) if yg else None
    result['原告律师'] = f'{_ygls_title[0] if _ygls_title else ygls_type}^^' + '@@'.join(ygls) if ygls else None
    
    return result


def get_bg(info):  # 获取原告/被告/代理律师
    info = re.sub(' |　|', '', info)
    lines = info.split('\n')
    bgs = []  # 被告
    bg_type = '被告'
    _dlr_title = list()
    bg_title = list()
    dlr_type = '委托代理人'
    i = 3
    cfw = 0
    lines = [a for a in lines if a]
    while i < len(lines):
        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
        if len(this_line) > 90:  # 这一行太长了，已经不是原告/被告行了 提取完了
            break
        if re.match(r'^被告人?|被申请人|原?审?第三人|被执行人|被上诉人|原审被上诉人|原审被告|一审被告.*', this_line):
            bg = re.findall(r'^(被告人?|被申请人|原?审?第三人|被执行人|被上诉人|原审被上诉人|原审被告|一审被告)[:：]?(.*)。?', this_line)
            if bg:
                bg_info = bg[0][1]
                bg_type = bg[0][0]
                bg_title.append(bg_type)
                explain = re.findall(r'[(（](.*?)[)）]', bg_info)  # 说明
                true_explain = re.match(f'{bg_type}[(（](?P<bg_explain>.*?)[)）][:：]?', this_line)
                true_explain = true_explain.group('bg_explain') if true_explain else ''
                if explain:
                    if true_explain == explain[0]:
                        bg_info = re.sub(f'[(（]?{explain[0]}[)）]?[:：]?', '', bg_info)
                        explain = explain[0]
                    else:
                        explain = ''
                else:
                    explain = ''
                bg_info_list = re.split(',|，|。', re.sub('住所地：?|住址|住', '', bg_info))
                is_company = False
                # ===============================主体：个人=====================================
                if '职员' in this_line or '员工' in this_line or '职工' in this_line or \
                        not re.search('公司|馆|开发区|局|部门|委员会|酒店|银行|政府|厂|所', bg_info_list[0] if len(bg_info_list) >= 1 else '') or (
                        '公司' not in this_line and '局' not in this_line and '厂' not in this_line and
                        '政府' not in this_line and '部' not in this_line and '委员会' not in this_line and
                        '执法局' not in this_line and '开发区' not in this_line and '酒店' not in this_line and
                        '银行' not in this_line and '馆' not in this_line and '所' not in this_line):
                    bg_init = [''] * 5
                    if explain:
                        bg_init[0] = explain  # 1被告说明
                    bg_init[1] = bg_info_list.pop(0)  # 2被告姓名
                    gender = re.findall('(男|女)', this_line)
                    if gender:
                        bg_init[2] = gender[0]  # 3被告姓别
                        if gender[0] in bg_info_list:
                            bg_info_list.remove(gender[0])
                        if gender[0] + '性' in bg_info_list:
                            bg_info_list.remove(gender[0] + '性')
                    # birth = re.findall(r'(\d+.*?)，|', this_line)
                    birth = re.findall(r'[\u4e00-\u9fa5\d]+年[\u4e00-\u9fa5\d]*月?[\u4e00-\u9fa5\d]*日?|\d{16}[1-9xX]{2}', this_line)
                    # print(birth)
                    if birth:
                        bg_init[3] = birth[0]  # 4身份证号或生日
                        bg_info_list = [re.sub(f'.*{birth[0]}.*[，,。 ]?', '', s) for s in bg_info_list if s]
                        if birth[0] in bg_info_list:
                            bg_info_list.remove(birth[0])
                    bg_init[4] = ','.join([s for s in bg_info_list if s])  # 5人员描述
                    bg_info_list = bg_init

                # ===============================主体：公司=====================================
                else:
                    is_company = True
                    bg_init = [''] * 4
                    if re.match(r'^住所?地?|住址?|居住地|公司地址|营业场所|注册地', lines[i + 1]):  # 公司地址在原告和原告律师之间
                        i += 1
                        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
                        addr = re.findall(r'^(住所?地?|住址?|居住地|公司地址|营业场所|注册地)[:：]?(.*)[，。 ]?', this_line)
                        if addr:
                            addr = addr[0][1]
                            bg_init[1] = addr
                    else:
                        addr = re.findall('(住所?地?|居住地|地址|公司地址|营业场所|注册地)[:：]?(.*)[，。 ]?', this_line)
                        if addr:
                            _addr = re.split('，|。| ', addr[0][1])
                            bg_init[1] = _addr[0] if len(_addr) >= 1 else ''
                        else:
                            bg_init[1] = addr[0][1] if addr else ''
                    if re.match(r'^法定代表人|代表人|主要负责人|诉讼代表人|经营者|负责人.*', lines[i + 1]):
                        i += 1
                        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
                        fr = re.findall(r'(法定代表人|代表人|负责人|诉讼代表人|经营者|主要负责人)[:：]?(.*)。?', this_line)  # 法人
                        if fr:
                            fr = fr[0][1].split('，')[0]
                            bg_init[2] = fr
                    bg_init[0] = bg_info_list[0]
                    bg_info_list = bg_init
                # print(bg_init)
                bg_info = explain + '##########' + '##'.join(bg_info_list) if is_company else '##'.join(
                    bg_info_list) + '########'
                bg_tmp = []
                bg_tmp.append(bg_info)
                # =============================处理被告代理律师============================
                while True:
                    if lines[i + 1].startswith('委托代理人') or lines[i + 1].startswith('辩护人') or lines[i + 1].startswith(
                            '特别授权委托代理人') or lines[i + 1].startswith('两被告共同委托代理人') or lines[i + 1].startswith('委托诉讼代理人')\
                            or lines[i+1].startswith('法定代理人'):
                        i += 1
                        this_line = lines[i][:-1] if lines[i][-1] == '。' else lines[i]
                        dlr = re.findall(r'委托代理人[:：]?(.*)。?', this_line) or re.findall(r'辩护人[:：]?(.*)。?', this_line) \
                              or re.findall(r'特别授权委托代理人[:：]?(.*)。?', this_line) or re.findall(r'两被告共同委托代理人[:：]?(.*)。?', this_line) \
                              or re.findall(r'委托诉讼代理人[:：]?(.*)。?', this_line) or re.findall(r'法定代理人[:：]?(.*)。?', this_line)
                        if dlr:
                            dlls_init = [''] * 6
                            dlr_info = dlr[0].split('，')
                            # print(dlr_info)
                            dlls_init[0] = re.findall('(委托代理人|辩护人|特别授权委托代理人|两被告共同委托代理人|委托诉讼代理人|法定代理人)', this_line)[0]
                            _dlr_title.append(dlls_init[0])
                            dlr_list = dlr_info[0].split('、')
                            dlr_info.pop(0)
                            # print('>>>', dlr_info, dlr)
                            gender = re.findall('(男|女)', this_line)
                            if gender:
                                dlls_init[2] = gender[0]
                                if gender[0] in dlr_info:
                                    dlr_info.remove(gender[0])
                                if gender[0] + '性' in dlr_info:
                                    dlr_info.remove(gender[0] + '性')
                            # birth = re.findall(r'(\d+.*?)，', this_line)
                            birth = re.findall(r'[\u4e00-\u9fa5\d]+年[\u4e00-\u9fa5\d]*月?[\u4e00-\u9fa5\d]*日?|\d{16}[1-9xX]{2}', this_line)
                            if birth:
                                dlls_init[3] = birth[0]
                                dlr_info = [re.sub(f'.*{birth[0]}.*[,，。 ]?', '', s) for s in dlr_info if s]
                                if birth[0] in dlr_info:
                                    dlr_info.remove(birth[0])
                            # dlls_init[4] = re.sub('（|）', '', ','.join(dlr_info))
                            dlr_info = ','.join([s for s in dlr_info if s])
                            dlr_info = re.split(',|，|。', dlr_info)
                            # 事务所&公司-公司位置
                            workstop = [re.findall('.*所.*?|.*事务所.*?|.*公司.*?|.*中心.*?', s)
                                        for s in dlr_info if s and not re.search('该|系', s) and not re.match(r'^公司', s)]
                            workstop = [s for s in workstop if s]
                            if workstop and len(workstop) >= 1:
                                dlls_init[5] = workstop[0][0] + '####' if workstop[0] else '' + '####'
                                dlr_info = [re.sub(f'{workstop[0][0]}.*', '', s) for s in dlr_info]
                            else:
                                dlls_init[5] = '' + '####'
                            dlls_init[4] = ','.join([s for s in dlr_info if s])
                            # print(dlls_init)
                            # print(dlr_info)
                            #-----------新增
                            # 律师说明
                            _dlr_type = re.findall(r'[(（](.*?)[）)]', this_line)
                            true_dlr_type = re.match(f'{dlls_init[0]}[(（](?P<true_dlr>.*?)[）)][:：]?', this_line)
                            # print('>>>', true_dlr_type.group('true_dlr'), _dlr_type, dlls_init[0])
                            #------------
                            for drl_one in dlr_list:
                                dlls_init[1] = drl_one
                                dlls_init[0] = _dlr_type[0] if _dlr_type and true_dlr_type else ''
                                if true_dlr_type:
                                    dlls_init[0] = true_dlr_type.group('true_dlr')
                                    dlls_init[1] = re.sub(f'[（(]{true_dlr_type.group("true_dlr")}[)）][：:]?', '', dlls_init[1])
                                bg_tmp.append('##'.join(dlls_init) + '##')
                    else:
                        break
                bgs.append(bg_tmp)
        i += 1

    # 整理数据
    result, bg, bgls = {}, [], []  # 最终结果/被告/被告律师
    for index, bg_list in enumerate(bgs):
        if bg_list:
            bg.append(f'{bg_list.pop(0)}##{index + 1}')
            if len(bg_list) > 1:
                bgls.append('@@'.join([f'{a}##{index + 1}' for a in bg_list]))
            elif len(bg_list) == 1:
                bgls.append('@@' + f'{bg_list[0]}##{index + 1}')
    for i, q in enumerate(bgls):
        if q.startswith("@@", 0, 2):
            bgls[i] = bgls[i].replace('@@', '')
    
    result['被告'] = f'{bg_title[0] if bg_title else bg_type}^^' + '@@'.join(bg) if bg else None
    result['被告律师'] = f'{_dlr_title[0] if _dlr_title else dlr_type}^^' + '@@'.join(bgls) if bgls else None
    return result


# if __name__ == '__main__':
#     print(get_yg(info))
#     print(get_bg(info))

