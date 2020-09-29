# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 07:36:58 2020

@author: drewq
"""

import bs4
import re
import pandas as pd
from collections import OrderedDict
import constant
from generalFunctions import get_general_html, exportCSV
import pdb
import logging
import time
import math
import json
        
import numpy as np
from fuzzywuzzy import fuzz

abs_path = 'C:/Users/zh4448/Documents/Datasets/'


def partial_match(x,y):
    return(fuzz.ratio(x,y))
    # return(fuzz.token_sort_ratio(x,y))
partial_match_vector = np.vectorize(partial_match)


'''Get BA dataset'''
filename = abs_path + 'Merged_091920_gh.xlsx'
df_ba = pd.read_excel(filename)
df_ba['NCompany'] = df_ba['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")
df_ba['State'] = df_ba['State Province']
    
filename = abs_path + 'rateBeer/breweries_info/rateBeer_breweries_info_all.csv'

'''Convert dataframe to list of dictionary'''
df_rateBeer = pd.read_csv(filename)

'''Create a new column for brewery name without Company  Co. Co '''
df_rateBeer['NCompany'] = df_rateBeer['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")

'''Add prefix'''
df_ba = df_ba.add_prefix('BA_')
df_rateBeer = df_rateBeer.add_prefix('RB_')



'''Get duplicate rows'''
df_duplicate = df_rateBeer.sort_values(by=['RB_Company', 'RB_State', 'RB_City'])
df_duplicate = df_duplicate[df_duplicate.duplicated(subset=['RB_Company', 'RB_State', 'RB_City'])]


''' Combine two dataframe by permutation'''
# df_ba_bystate['key'] = 1
# df_brewery['key'] = 1
combined_df = df_rateBeer.merge(df_ba, left_on=['RB_State', 'RB_City'], right_on=["BA_State","BA_City"], how="left")
# combined_df = combined_df[combined_df["NCompany_y"].notna()].reset_index()
combined_df = combined_df.where(pd.notnull(combined_df), None)

combined_df['score']=partial_match_vector(combined_df['RB_NCompany'],combined_df['BA_NCompany'])

# indx = combined_df.groupby(['Company_x'])['score'].transform(max) == combined_df['score']
indx = combined_df.groupby(['RB_Company', 'RB_State', 'RB_City'], sort=False)['score'].idxmax()
combined_df = combined_df.loc[indx]
# combined_df = combined_df[combined_df.score>=80]

path = abs_path+'Merge/'
filename = 'merge_rateBeer_BA_all.csv'
exportCSV(combined_df,filename,path)
        
path = abs_path+'Merge'
filename = 'duplicate_rateBeer.csv'
exportCSV(df_duplicate,filename,path)
