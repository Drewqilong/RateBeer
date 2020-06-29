# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 09:58:18 2020

@author: Jerry
"""

import pandas as pd
from generalFunctions import get_general_html, exportCSV
import numpy as np

abbr = 'AL'
abs_path = 'E:/RateBeerDocuments/Newversion/'
filename = abs_path + 'beers_stat/rateBeer_beers_stat_' + abbr + '.csv'
'''Convert dataframe to list of dictionary'''
df_beer = pd.read_csv(filename)
beer_ids = np.sort(df_beer['BeerId'].values)
lt_beer = df_beer.to_dict('records')


#for indx in range(1,len(beer_ids)):
#    if beer_ids[indx] == beer_ids[indx-1]: print(beer_ids[indx])


from pymongo import MongoClient
client = MongoClient()

lost_beers = []
#client = MongoClient("mongodb+srv://dbuser:8fO56qa3wBdNYtsk@cluster0-bhgly.mongodb.net/rateBeer?retryWrites=true&w=majority")
db = client.rateBeer
collection = db.beerReview
db_beers = [d['beer']['id'] for d in list(collection.find({},{'beer.id':1,'_id':0})) if 'beer' in d]
for beer in lt_beer:
    if str(beer['BeerId']) not in db_beers:
        lost_beers.append(beer.copy())
        
#path = abs_path + 'beers_compare'
#filename = 'rateBeer_beers_missing_'+abbr+'.csv'
#exportCSV(lost_beers,filename,path)
    