# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import netbug as nb
import os
import datetime

url_data = './data.csv'
url_beta = './beta.csv'
url_beta_blueball = './beta_blueball.csv'
url_guess = './guess.csv'

def open_data():    
    data = pd.read_csv(url_data, encoding = 'utf-8', index_col = 0)
    print(u'数据结构：{}'.format(data.shape))
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

def calculate_beta_blueball(data):
    n,m = data.shape
    print(u'计算的数据{}个'.format(m))
    # 预定义一个字典作为结果的结构
    rel = {str(name):[] for name in np.arange(1,37)}
    temp_data = data.T
    #print(data.index)
    #print(data.columns)
    # 按开奖号特别号7统计每个号码出现的次数
    c = temp_data.columns[-1]
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
    df_beta.to_csv(url_beta_blueball, encoding = 'utf-8', header = True)
    return True

'''
def add_new_period_and_beta():
    pre_df_beta = pd.read_csv(url_beta, encoding = 'utf-8', index_col = 0)
    #print(pre_df_beta.T)
    dict_beta = pre_df_beta.to_dict()
    #print(u'先验beta:\n{}'.format(dict_beta))
    new_data = nb.update_new_period(period_number = '2021007')
    # drop zers
    temp = []
    for i in new_data:
        temp.append(str(int(i)))
    # 伯努利实验
    for number in list(dict_beta.keys()):
        if number in temp: 
            print(u'{}是本次中奖号'.format(number))
            dict_beta[number] = {'win': dict_beta[number]['win']+1, 'loss': dict_beta[number]['loss']+0}
        else:
            print(u'{}没选中'.format(number))
            dict_beta[number] = {'win': dict_beta[number]['win']+0, 'loss': dict_beta[number]['loss']+1}
    #print(u'后验beta:\n{}'.format(dict_beta))
    df = pd.DataFrame(dict_beta)
    #print(df)
    # save to file
    #df.to_csv(url_beta, encoding = 'utf-8', header = True)
    return dict_beta
'''
                  
def create_thompson_sample(color = 'red'):
    if color == 'red':
        pre_df_beta = pd.read_csv(url_beta, encoding = 'utf-8', index_col = 0)
        n = 6
    else:
        pre_df_beta = pd.read_csv(url_beta_blueball, encoding = 'utf-8', index_col = 0)
        n = 1
    #print(pre_df_beta.T)
    dict_beta = pre_df_beta.to_dict()
    rel = {}
    probabilty = {}
    # 产生计算随机
    for k in list(dict_beta.keys()):
        if dict_beta[k]['win']<=0 or dict_beta[k]['loss']<=0:
            print(u'号码{}没有历史先验概率，win:{}次、loss{}次'.format(k,dict_beta[k]['win'],dict_beta[k]['loss']))
            rel[k] = 0
        else:
            rel[k] = np.random.beta(dict_beta[k]['win'], dict_beta[k]['loss'])
        probabilty[k] = dict_beta[k]['win'] / (dict_beta[k]['win'] + dict_beta[k]['loss'])
    series_prob = pd.Series(probabilty)
    series_thomps = pd.Series(rel)
    #
    choice_thomps = series_prob.sort_values().tail(n)
    choice_prob = series_thomps.sort_values().tail(n)
    #
##    print(u'有效号码数量{}个'.format(series_thomps.shape))
##    print(u'汤普森选号:\n{}'.format(choice_thomps))
    print(u'概率最多的号：\n{}'.format(choice_prob))
    print('-----------------------------------')
    # 
    balls = choice_thomps.sort_index().index
    show_balls = []
    for ball in balls:
        show_balls.append(ball)
    print(show_balls)
    #
    
##    prob_keys_list = [int(i) for i in list(probabilty.keys())]
##    beta_keys_list = [int(i) for i in list(dict_beta.keys())]
##    print(prob_keys_list)
##    print(list(probabilty.values()))
##    print(np.random.choice(prob_keys_list,list(probabilty.values()),6))
##    print(np.random.choice(beta_keys_list,list(dict_beta.values()),6))
    return show_balls

# 保存建议的开奖结果
def save_to_file(red_balls,blue_ball):
    date_dt_obj =  datetime.date.today()
    str_date = datetime.date.strftime(date_dt_obj, '%Y-%m-%d')
    red_balls.extend(blue_ball)
    series = pd.Series(red_balls,index = [i for i in np.arange(len(red_balls))])
    if os.path.exists(url_guess):
        df = pd.read_csv(url_guess, encoding = 'utf-8', index_col = 0)
        df[str_date] = series
        print(df)
    else:
        df = pd.DataFrame(series, columns = [str_date])    
    # 保存并替代原文件
    df.to_csv(url_guess, encoding = 'utf-8')
    return True
    
def auto_create_ball(m_pre_data):
    # 自动增加开奖记录并记录在文件中
    nb.auto_update_data()
    # 开数据文件
    data = open_data()
    # 计算beta红球
    red_data = data.iloc[:6,-m_pre_data:] # 6
    calculate_beta(red_data)
    # 计算beta蓝球
    blue_data = data.iloc[:,-m_pre_data:]
    calculate_beta_blueball(blue_data)
    # 预测下期开奖红球号码
    red_balls = create_thompson_sample(color = 'red')
    # 预测下期开奖蓝球号码
    blue_ball = create_thompson_sample(color = 'blue')
    save_to_file(red_balls, blue_ball)
    return data,red_balls,blue_ball

def check_like_two_group(data,red,blue):
    last_ball = data.iloc[:,-1]
    print(last_ball.to_list())
    red.extend(blue)
    win = 0
    for ball in red:
        if int(ball) in last_ball.to_list():
            win += 1
    return win
            

def get_n():
    create_n = np.zeros(shape=(1000,2))
    for i in np.arange(1000):
        n = np.random.randint(36,365,1)[0]
        print(n)
        data,red,blue = auto_create_ball(m_pre_data = n)
        win = check_like_two_group(data,red,blue)
        print(n,win)
        create_n[i,0] = n
        create_n[i,1] = win
    max_ix = np.argmax(create_n, axis = 0)
    print(create_n[max_ix[1],:]) # 13

if __name__=='__main__':
    for i in np.arange(7):
        n = np.random.randint(36,365,1)[0]
        data,red,blue = auto_create_ball(m_pre_data = n)
    data,red,blue = auto_create_ball(m_pre_data = 258)
    #get_n()










    
