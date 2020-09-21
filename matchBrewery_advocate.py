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


# '''Get BA dataset'''
# filename = abs_path + 'Founded Date.xlsx'
# df_ba = pd.read_excel(filename)
# df_ba['NCompany'] = df_ba['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")

    
for abbr in constant.abbr[4:5]:
    '''Get beeradvovate dataset'''
    filename = abs_path + 'beerAdvocate/breweries/beerAdvocate_breweries_' + abbr + '.csv'

    df_brewery = pd.read_csv(filename)
    
    '''Create a new column for brewery name without Company  Co. Co '''
    df_brewery['NCompany'] = df_brewery['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")
    
    '''Get rateBeer data'''
    filename = abs_path + 'rateBeer/breweries_info/rateBeer_breweries_info_' + abbr + '.csv'
    df_rateBeer_brewers = pd.read_csv(filename)
    
    '''Create a new column for brewery name without Company  Co. Co '''
    df_rateBeer_brewers['NCompany'] = df_rateBeer_brewers['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")
  

    mData = pd.merge(df_brewery, df_rateBeer_brewers, on='NCompany')
    
    
    ''' Combine two dataframe by permutation'''
    # df_ba_bystate['key'] = 1
    # df_brewery['key'] = 1
    combined_df = df_rateBeer_brewers.merge(df_brewery, on="City", how="left")
    # combined_df = combined_df[combined_df["NCompany_y"].notna()].reset_index()
    combined_df = combined_df.where(pd.notnull(combined_df), None)
    
    # combined_df['score']=partial_match_vector(combined_df['NCompany_x'],combined_df['NCompany_y'])
    combined_df['score']=partial_match_vector(combined_df['Address_x'],combined_df['Address_y'])
    
    # indx = combined_df.groupby(['Company_x'])['score'].transform(max) == combined_df['score']
    indx = combined_df.groupby(['Company_x'])['score'].idxmax()
    combined_df = combined_df.loc[indx]
    # combined_df = combined_df[combined_df.score>=80]

    path = abs_path
    filename = 'merge_rateBeer_beerAdvocate_'+abbr+'.csv'
    exportCSV(combined_df,filename,path)

        