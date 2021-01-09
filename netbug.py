# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from urllib import request
from bs4 import BeautifulSoup 
import ssl
import re
ssl._create_default_https_context = ssl._create_unverified_context

url_data = './data.csv'

# 访问网站取得数据
def get_value(url):
    # 判断http 或 https
    http = True
    print(url)
    if http:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
        try :
            response = request.urlopen(url, data=None, timeout=10)
        except:
            return None
        #print(response.read())
        try :
            page = response.read()
        except:
            page = response.read().decode('utf-8')
        #print(page)
    else:
        pass
    return page

def get_history_data():
    origin_url = 'https://www.polocai.com/index.php/kj_nyfc36x7_number/'
    data = {}
    for i in np.arange(1,275):  # 275
        html_origin = get_value(url = origin_url.replace('number',str(i)))
        data = take_useful_message(html_origin, data)
        #print(data)
        #break
    return data



# 提取齐整有用信息去掉枝节1
def take_useful_message(html_origin, give_dict):
    rel = give_dict
    condition = ['div', 'ov bb_ocs h38 pd_5_0']
    period_condition = ['span','fl m_0_5 color_gray6 ta_c lh_38 w130 fz_12']
    number_condition = ['span','ball_22 redball_22 fl mr8 mt8']
    number_blue_condition = ['span','ball_22 blueball_22 fl mr8 mt8']
    soup = BeautifulSoup(html_origin, 'html.parser')
    body = soup.body
    #print(body)
    tag = body.find_all(condition[0], condition[1])
    #print(tag)
    for sub_tag in tag:
        period = sub_tag.find(period_condition[0],period_condition[1])
        all_number = sub_tag.find_all(number_condition[0],number_condition[1])
        blue_number = sub_tag.find(number_blue_condition[0],number_blue_condition[1])
        print(period)
        #print(blue_number)
        name = period.string
        rel[name] = [] 
        for number in all_number:
            rel[name].append(number.string)
        rel[name].append(blue_number.string)
    return rel
            

# 提取齐整有用信息去掉枝节2
def take_useful_message_fornew(html_origin):
    rel = []
    number_condition = ['li','ball_orange']
    number_blue_condition = ['li','ball_blue']
    soup = BeautifulSoup(html_origin, 'html.parser')
    body = soup.body
    #print(body)
    all_number = body.find_all(number_condition[0],number_condition[1])
    blue_number = body.find(number_blue_condition[0],number_blue_condition[1])
    #print(blue_number)
    for number in all_number:
        rel.append(str(int(number.string)))
    rel.append(str(int(blue_number.string)))
    return rel
   
def get_before_data_from_net():
    data = get_history_data()
    print(len(data))
    df = pd.DataFrame(data)
    df.to_csv(url_data, encoding = 'utf-8')
    
def check_last_from_file():
    rel = None
    data = pd.read_csv(url_data, encoding = 'utf-8', index_col = 0)
    str_period_list = re.findall('\d*', data.columns[-1])
    for i in str_period_list:
        if len(i)>0:
            rel = str(i)   
    return rel, data

def update_new_period(period_number,pre_data_df):
    continus = True
    origin_url = 'http://kaijiang.500.com/shtml/gdslxq/period_number.shtml'
    html_origin = get_value(url = origin_url.replace('period_number',str(period_number)))
    if html_origin is None:
        continus = False
    else:
        continus = True
        data_list = take_useful_message_fornew(html_origin)
        print(data_list)
        pre_data_df[period_number] = data_list
    return continus, pre_data_df


def auto_update_data():
    period_number, pre_data_df = check_last_from_file()
    if period_number == '2020308':
        period_number = '2021000'
    for i in np.arange(1,100):
        new_number = str(int(period_number) + i)
        continus, pre_data_df = update_new_period(new_number, pre_data_df)
        if not continus:
            break
    #print(pre_data_df)
    pre_data_df.to_csv(url_data, encoding = 'utf-8')
        
    
