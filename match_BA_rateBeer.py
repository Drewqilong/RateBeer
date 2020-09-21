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
filename = abs_path + 'Closings_043020_yy.xlsx'
df_ba = pd.read_excel(filename)
df_ba['NCompany'] = df_ba['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")

    
for abbr in constant.abbr[4:5]:
    '''Get beeradvovate dataset'''
    filename = abs_path + 'rateBeer/breweries_info/''rateBeer_breweries_info_' + abbr + '.csv'

    '''Convert dataframe to list of dictionary'''
    df_rateBeer = pd.read_csv(filename)
    
    '''Create a new column for brewery name without Company  Co. Co '''
    df_rateBeer['NCompany'] = df_rateBeer['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")
    
    '''Get BA data by state'''
    df_ba_bystate = df_ba[df_ba['State Province']==abbr].copy()
    
    mData = pd.merge(df_rateBeer, df_ba_bystate, on='NCompany')
    
    
    ''' Combine two dataframe by permutation'''
    # df_ba_bystate['key'] = 1
    # df_brewery['key'] = 1
    combined_df = df_ba_bystate.merge(df_rateBeer, on="City", how="left")
    # combined_df = combined_df[combined_df["NCompany_y"].notna()].reset_index()
    combined_df = combined_df.where(pd.notnull(combined_df), None)
    
    combined_df['score']=partial_match_vector(combined_df['NCompany_x'],combined_df['NCompany_y'])
    
    # indx = combined_df.groupby(['Company_x'])['score'].transform(max) == combined_df['score']
    indx = combined_df.groupby(['Company_x'])['score'].idxmax()
    combined_df = combined_df.loc[indx]
    # combined_df = combined_df[combined_df.score>=80]

    path = abs_path
    filename = 'merge_BA_Closing_rateBeer_'+abbr+'.csv'
    exportCSV(combined_df,filename,path)

        