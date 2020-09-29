# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:22:15 2020

@author: zh4448
"""

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


'''C:\Users\zh4448\Documents\GoogleDrive_TAMU'''
abs_path = 'C:/Users/zh4448/Documents/Datasets/'

msline = pd.DataFrame()

    
filename = abs_path + 'rateBeer/breweries_info/rateBeer_breweries_info_all.csv'

'''Convert dataframe to list of dictionary'''
df_rateBeer = pd.read_csv(filename)

'''Create a new column for brewery name without Company  Co. Co '''
df_rateBeer['NCompany'] = df_rateBeer['Company'].str.replace("Company","").str.replace(" Co.","").str.replace(" Co","")



filename = abs_path+'Merge/merge_rateBeer_BA_all.csv'
df_merge = pd.read_csv(filename)

msline = df_rateBeer[df_rateBeer['City'].isnull()]
# indx_r = 0
# indx_m = 0
# while df_rateBeer.iloc[indx_r].any():
#     if df_rateBeer.iloc[indx_r]['Company']!=df_merge.iloc[indx_m]['RB_Company']:
#         msline = msline.append(df_rateBeer.iloc[indx_r], ignore_index=True)
#         indx_r+=1
#     else:
#         indx_m+=1
#         indx_r+=1


path = abs_path+'Merge/'
filename = 'missingValue_rateBeer.csv'
exportCSV(msline,filename,path)
        

