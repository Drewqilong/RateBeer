# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:02:26 2020

@author: Jerry
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


from pymongo import MongoClient
client = MongoClient("mongodb+srv://dbuser:8fO56qa3wBdNYtsk@cluster0-bhgly.mongodb.net/rateBeer?retryWrites=true&w=majority")
db = client.rateBeer
#collection = db.breweries
        

def update_mongodb(collection_name, data, myquery):
    collection = db[collection_name]
    collection.remove(myquery)
    collection.insert(data)

domain = 'https://www.ratebeer.com'
review_query = 'https://beta.ratebeer.com/v1/api/graphql/?operationName=BeerReviews&variables=%7B%22beerId%22%3A%22{}%22%2C%22order%22%3A%22RECENT%22%2C%22first%22%3A30%2C%22includePrivate%22%3Afalse%{}7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%224803219468382b8398ded70fcbf045de7b4ffb5fc785d9e75901e6cd11c64e84%22%7D%7D'
abs_path = 'E:/RateBeerDocuments/Newversion/'


for abbr in constant.abbr[:1]:
    filename = abs_path + 'beers/rateBeer_beers_' + abbr + '.csv'
    
    gt_brewers = []
    gt_beers = []

    '''Convert dataframe to list of dictionary'''
    lt_beer = pd.read_csv(filename).to_dict('records')
    
    for index,beer in enumerate(lt_beer):
        gt_beer_id = []
        gt_review_id = []
        
        print('Brewery No:'+str(index+1)+' /Total No: '+str(len(lt_beer))+',State: '+abbr)
        beer_dic = OrderedDict(beer)    
#        brewery_dic['Closed'] = brewery_dic['Closed'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
        
#                brewery_dic.update({key:brewery[key] for key in ['State','Est.','Closed']})
        try:
            beer_id = beer['BeerId']
            
            next_url = review_query.format(beer_id)
            review_content = json.loads(get_general_html(next_url))
#            next_url = brewery_query.format(brewery_id)
#            brewery_content = json.loads(get_general_html(next_url))
        except:
            print(beer_dic['BeerName'] + ' No review data')
            continue
#        for review_content
        
        
        gt_review_id.append(review_id)
#        brewery_condition = { "brewery.id": { "$in": gt_brewery_id } }
#        update_mongodb('breweries', {'brewery':brewery_data}, brewery_condition)
#        '''Beer list'''
#        beers_table = beer_content['data']['brewerBeers']['items']
#        for beer_item in beers_table:
#            beer_dic = OrderedDict()
#            beer_item = beer_item['beer']
#            beer_dic.update({key:brewery_dic[key] for key in ['State','Company','Est.','Closed','Status']})
#            beer_dic['BeerId'] = beer_item['id']
#            beer_dic['BeerCreated'] = beer_item['createdAt'][:10]
#            beer_dic['ABV'] = beer_item['abv']
#            beer_dic['Style'] = beer_item['style']['name']
#            beer_dic['Ratings'] = beer_item['ratingsCount']
#            beer_dic['Avg'] = beer_item['averageQuickRating']
#            beer_dic['Archived'] = beer_item['isRetired']
#            gt_beers.append(beer_dic.copy())
#            gt_beer_id.append(beer_item['id'])
#        
#        beer_condition = {"beer.id": {"$in": gt_beer_id}}
#        update_mongodb('beers', beers_table, beer_condition)
#    path = abs_path + 'breweries_info'
#    filename = 'rateBeer_breweries_info_'+abbr+'.csv'
#    exportCSV(gt_brewers,filename,path)
#   
#    path = abs_path + 'beers'
#    filename = 'rateBeer_beers_'+abbr+'.csv'
#    exportCSV(gt_beers,filename,path)
        