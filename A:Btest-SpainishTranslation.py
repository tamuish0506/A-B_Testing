#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 19:31:15 2019

@author: tinahuang
"""

print()

import pandas as pd
import numpy as np
from scipy import stats as ss
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

experiment=pd.read_csv('~tinahuang/desktop/test_table.csv')
user=pd.read_csv('~tinahuang/desktop/user_table.csv')

experiment.head(10)
user.head(10)

# check if any duplicate user is existed
len(experiment['user_id']) == len(experiment["user_id"].unique())
len(user['user_id']) == len(user['user_id'].unique())
# no duplicate in each table

# compaere sample size in each table
experiment.info()
user.info()
# User table has less observations that test table -> join observation from 2
# tables using the same user_id
data_inner=pd.merge(experiment, user, on='user_id', how='inner')# inner join
data_inner.head(5)
data_inner.info()
data_inner.describe(include='all')

conversion_by_country=data_inner.groupby('country')['conversion'].mean()
conversion_by_country.plot(kind='bar')

conversion_by_test=data_inner.groupby('test')['conversion'].mean()
conversion_by_test.plot(kind='bar')

# Spain has higer conversion rate compared with other Spanish-spoken countries,
# so I decided to drop all observations w/Spain.
data_no_spain = data_inner.loc[data_inner.country != 'Spain',:]
data_no_spain.groupby("test")[["conversion"]].mean()

# T-test
conv_in_test = data_no_spain.loc[experiment.test==1,"conversion"]
conv_in_ctrl = data_no_spain.loc[experiment.test==0,"conversion"]

ss.ttest_ind(conv_in_test,conv_in_ctrl)

# Is conversion rate in these countries other than Spain different by dates?
# Conver dates to standard format
data_inner['date'] = pd.to_datetime(data_inner['date'], infer_datetime_format = True)
time_diff=data_inner.groupby(['date', 'test'])['conversion'].mean() 
time_diff

