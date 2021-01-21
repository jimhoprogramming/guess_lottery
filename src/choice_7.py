# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import netbug as nb
import os
import datetime

url_data = '../data/data.csv'
url_beta = '../data/beta.csv'
url_guess = '../data/guess.csv'

def open_data():    
    data = pd.read_csv(url_data, encoding = 'utf-8', index_col = 0)
##    print(u'数据结构：{}'.format(data.shape))
    return data

def calculate_beta(data):
    n,m = data.shape
    #print(n,m)
    # 预定义一个字典作为结果的结构
    rel = {str(name):[] for name in np.arange(1,37)}
    temp_data = data.T
    #print(data.index)
    #print(data.columns)
    # 按开奖号1-6,+7统计每个号码出现的次数
    for c in temp_data.columns:
        #print(c)
        g = temp_data.groupby(by = c)
        df_every_columns = g.count().iloc[:,0]
        #print(df_every_columns)
        # 有出现就把对应号的列表追加一次出现数量
        for i in df_every_columns.index:
            #print(df_every_columns[i])
            rel[str(i)].append(df_every_columns[i])
    # 合并各号的总数，并计算失败总数
    for k in list(rel.keys()):
        rel[k] = [np.sum(rel[k]), m - np.sum(rel[k])]
    #print(rel)
    # 保存成文件形式
    df_beta = pd.DataFrame(rel, index = ['win','loss'])
    df_beta.to_csv(url_beta, encoding = 'utf-8', header = True)
    return True

                  
def create_thompson_sample():
    pre_df_beta = pd.read_csv(url_beta, encoding = 'utf-8', index_col = 0)
    n = 7
    #print(pre_df_beta.T)
    dict_beta = pre_df_beta.to_dict()
    rel = {}
    probabilty = {}
    # 产生计算随机
    for k in list(dict_beta.keys()):
        if dict_beta[k]['win']<=0 or dict_beta[k]['loss']<=0:
            print(u'号码{}没有历史先验概率，win:{}次、loss{}次'.format(k,dict_beta[k]['win'],dict_beta[k]['loss']))
            rel[k] = 0
            probabilty[k] = 0
        else:
            rel[k] = np.random.beta(dict_beta[k]['win'], dict_beta[k]['loss'])
        if (dict_beta[k]['win'] + dict_beta[k]['loss'])<=0:
            probabilty[k] = 0
        else:
            probabilty[k] = dict_beta[k]['win'] / (dict_beta[k]['win'] + dict_beta[k]['loss'])
    series_prob = pd.Series(probabilty)
    series_thomps = pd.Series(rel)
    #
    choice_thomps = series_prob.sort_values().tail(n)
    choice_prob = series_thomps.sort_values().tail(n)
    #
##    print(u'有效号码数量{}个'.format(series_thomps.shape))
##    print(u'汤普森选号:\n{}'.format(choice_thomps))
##    print(u'概率最多的号：\n{}'.format(choice_prob))
    print('-----------------------------------')
    # 
    balls = choice_thomps.sort_index().index
    show_balls = []
    for ball in balls:
        show_balls.append(int(ball))
    show_balls.sort()
    print(show_balls)
    # 利用随机选7
    '''
    prob_keys_list = [int(i) for i in list(probabilty.keys())]
    beta_keys_list = [int(i) for i in list(dict_beta.keys())]
    print(prob_keys_list)
    print(list(probabilty.values()))
    print(np.random.choice(prob_keys_list,list(probabilty.values()),6))
    print(np.random.choice(beta_keys_list,list(dict_beta.values()),6))
    '''
    return show_balls

# 保存建议的开奖结果
def save_to_file(all_balls):
    date_dt_obj =  datetime.date.today()
    str_date = datetime.date.strftime(date_dt_obj, '%Y-%m-%d')
    series = pd.Series(all_balls,index = [i for i in np.arange(len(all_balls))])
    if os.path.exists(url_guess):
        df = pd.read_csv(url_guess, encoding = 'utf-8', index_col = 0)
        df[str_date] = series
##        print(u'收录已有的数据{}'.format(df))
    else:
        df = pd.DataFrame(series, columns = [str_date])    
    # 保存并替代原文件
    df.to_csv(url_guess, encoding = 'utf-8')
    return True
    
def auto_create_ball(m_pre_data, test = False):
    # 自动增加开奖记录并记录在文件中
    if not test:
        nb.auto_update_data()
    # 开数据文件
    data = open_data()
    # 计算beta
    if test:
        test_data = data.iloc[:,-m_pre_data:-1] # 6
    else:
        test_data = data.iloc[:,-m_pre_data:] # 6
    # 产生最新的beta分布文件
    calculate_beta(test_data)
    # 预测下期开奖号码
    all_balls = create_thompson_sample()
    if test:
        save_to_file(all_balls)
    return data,all_balls

def check_like_two_group(data, all_balls):
    last_ball = data.iloc[:,-1]
    print(u'最后一次开奖的结果：{}'.format(last_ball.to_list()))
    win = 0
    for ball in all_balls:
        if int(ball) in last_ball.to_list():
            win += 1
    return win
            

def get_n(n_times):
    create_n = np.zeros(shape=(n_times,2))
    for i in np.arange(n_times):
        m = np.random.randint(1,365,1)[0]
        data, all_balls = auto_create_ball(m_pre_data = m, test = True)
        win = check_like_two_group(data, all_balls)
        print(u'测试{}个数据，和目标数据相同的有中奖号{}个。'.format(m,win))
        create_n[i,0] = m
        create_n[i,1] = win
    max_ix = np.argmax(create_n, axis = 0)
    print(u'测试完成最好的个数的结果是{}'.format(create_n[max_ix[1],:])) # 13

if __name__=='__main__':
    m = input(u'请输入产生多少开奖号码：')
    for i in np.arange(int(m)-1):
        n = np.random.randint(36,365,1)[0]
        data,all_balls = auto_create_ball(m_pre_data = n, test = False)
    data,all_balls = auto_create_ball(m_pre_data = 305, test = False)
##    get_n(n_times = 1000)










    
