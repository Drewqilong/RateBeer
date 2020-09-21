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

client = MongoClient()

#client = MongoClient("mongodb+srv://dbuser:8fO56qa3wBdNYtsk@cluster0-bhgly.mongodb.net/rateBeer?retryWrites=true&w=majority")
db = client.rateBeer
#collection = db.breweries
        

def update_mongodb(collection_name, data, myquery):
    collection = db[collection_name]
    collection.remove(myquery)
    collection.insert(data)

domain = 'https://www.ratebeer.com'
beerStat_query = 'https://beta.ratebeer.com/v1/api/graphql/?operationName=beer&variables=%7B%22beerId%22%3A%22{}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22a144a56d830595b80cf300e61424e46c22fd85d400ef948d6ea2e32f92b92708%22%7D%7D'
review_query = 'https://beta.ratebeer.com/v1/api/graphql/?operationName=BeerReviews&variables=%7B%22beerId%22%3A%22{}%22%2C%22order%22%3A%22RECENT%22%2C%22first%22%3A30%2C%22includePrivate%22%3Afalse{}%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%224803219468382b8398ded70fcbf045de7b4ffb5fc785d9e75901e6cd11c64e84%22%7D%7D'
abs_path = 'C:/Users/zh4448/Documents/RateBeerDocuments/Newversion/'


for abbr in  constant.abbr[4:5]:#reversed(constant.abbr[:-29]):
    filename = abs_path + 'beers/rateBeer_beers_' + abbr + '.csv'
    
    gt_reviews = []
    gt_beers = []

    '''Convert dataframe to list of dictionary'''
    lt_beer = pd.read_csv(filename).to_dict('records')
    
    for index,beer in enumerate(lt_beer):
        gt_beer_id = []
        
        print('Brewery No:'+str(index+1)+' /Total No: '+str(len(lt_beer))+',State: '+abbr)
        
#        beer_dic = OrderedDict(beer)    
#        brewery_dic['Closed'] = brewery_dic['Closed'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
        
#                brewery_dic.update({key:brewery[key] for key in ['State','Est.','Closed']})
#        try:
        beer_id = beer['BeerId']
        
        next_url = beerStat_query.format(beer_id)
        for i in range(0, 4):
            beer_content = get_general_html(next_url, returnJson=True) #json.loads(get_general_html(next_url))
            if 'errors' not in beer_content and beer_content != " Request Failure ": break  #and beer_content['data']['beer']['brewer']
            else: time.sleep(5)
#        except:
#            print(beer['BeerName'] + ' no review data')
#            continue
        '''Beer statistics'''
        beer_stat = beer_content['data']['beer']
        if not beer_stat: continue
        if beer_stat['brewer']['id'] != str(beer['BreweryId']): continue
    
        beer_dic = OrderedDict({key:beer[key] for key in ['State','Company','BreweryId', 'BeerOriginalName','BeerName','BeerId','Style','ABV','Archived']})
        beer_dic['styleScore'] = beer_stat['styleScore']
        beer_dic['overallScore'] = beer_stat['overallScore']
        beer_dic['averageQuickRating'] = beer_stat['averageQuickRating']
        beer_dic['normalizedAverageReview'] = beer_stat['normalizedAverageReview']
        beer_dic['averageReview'] = beer_stat['averageReview']
        beer_dic['createdAt'] = beer_stat['createdAt'][:10]
        beer_dic['updatedAt'] = (beer_stat['updatedAt'][:10] if beer_stat['updatedAt'] else None)
        beer_dic['ibu'] = beer_stat['ibu']
        beer_dic['calories'] = beer_stat['calories']
        beer_dic['ratingsCount'] = beer_stat['ratingsCount']
        beer_dic['reviewsCount'] = beer_stat['reviewsCount']
        beer_dic['seasonal'] = beer_stat['seasonal']
        gt_beers.append(beer_dic.copy())
        '''Reviews'''
        hasReview = True
        try:
            next_url = review_query.format(beer_id,'')
            for i in range(0, 4):
                review_content = get_general_html(next_url, returnJson=True)
                if review_content != " Request Failure ": break
                time.sleep(3)
#            review_content = get_general_html(next_url, returnJson=True)
        except Exception as e:
            logging.info(index)
            logging.info(str(e))
            logging.warning(review_content)
        review_list = []
        while hasReview:
            review_table = review_content['data']['beerList']['items']
            review_list.extend(review_table.copy())
            for review_item in review_table:
                review_dic = OrderedDict({key:beer[key] for key in ['State','Company','BreweryId', 'BeerOriginalName','BeerName','BeerId']})
                review_dic['Base_score'] = review_item['score']
                review_dic['SubScore'] = ''
                for score_item in list(review_item['scores'].items())[:-1]:
                    review_dic['SubScore']+=str(score_item[0])+':'+str(score_item[1])+' | '
                
                review_dic['Review'] = review_item['comment']
                review_dic['createdAt'] = review_item['createdAt']
                review_dic['updatedAt'] = review_item['updatedAt']
                gt_reviews.append(review_dic.copy())          
            if review_content['data']['beerList']['last']:
                next_url = review_query.format(beer_id,'%2C%22after%22%3A%22{}%22'.format(review_content['data']['beerList']['last']))      
                for i in range(0, 4):
                    review_content = get_general_html(next_url, returnJson=True)
                    if review_content != " Request Failure ": break
                    time.sleep(3)
            else: hasReview = False
#        

        # review_condition = {"beer.id": str(beer_id)}
        # update_mongodb('beerReview', {'beer':beer_stat,'reviews': review_list}, review_condition)
    path = abs_path + 'beers_reviews'
    filename = 'rateBeer_beers_reviews_'+abbr+'.csv'
    exportCSV(gt_reviews,filename,path)
   
    path = abs_path + 'beers_stat'
    filename = 'rateBeer_beers_stat_'+abbr+'.csv'
    exportCSV(gt_beers,filename,path)
        