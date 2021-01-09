# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import netbug as nb

url_data = './data.csv'
url_beta = './beta.csv'
url_beta_blueball = './beta_blueball.csv'

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
    #print(n,m)
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
        rel[k] = np.random.beta(dict_beta[k]['win'], dict_beta[k]['loss'])
        probabilty[k] = dict_beta[k]['win'] / (dict_beta[k]['win'] + dict_beta[k]['loss'])
    series_prob = pd.Series(probabilty)
    series_thomps = pd.Series(rel)
    #
    choice_thomps = series_prob.sort_values().tail(n)
    choice_prob = series_thomps.sort_values().tail(n)
    #
    print(u'有效号码数量{}个'.format(series_thomps.shape))
    print(u'汤普森选号:\n{}'.format(choice_thomps))
    print(u'概率最多的号：\n{}'.format(choice_prob))
    print('-----------------------------------')
    # 
    balls = choice_thomps.sort_index().index
    show_balls = []
    for ball in balls:
        show_balls.append(ball)
    print(show_balls)
    return series_prob,series_thomps
    
    
if __name__=='__main__':
    # 自动增加开奖记录并记录在文件中
    nb.auto_update_data()
    # 开数据文件
    data = open_data()
    # 计算beta红球
    red_data = data.iloc[:6,:] # 6
    calculate_beta(red_data)
    # 计算beta蓝球
    blue_data = data.iloc[:,:]
    calculate_beta_blueball(blue_data)
    # 预测下期开奖红球号码
    create_thompson_sample(color = 'red')
    # 预测下期开奖蓝球号码
    create_thompson_sample(color = 'blue')
    



    
