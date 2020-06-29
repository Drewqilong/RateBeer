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

def remove_sub(str1, str2):
    s = ''
    indx = 0
    space_loc = 0
    for x in str1:
        s+=x; indx+=1
        if x == ' ': space_loc = indx
        if str2[0:indx]!=s: indx-=1; break
    if x != ' ': indx = space_loc
    return str1[indx:].strip() if str1[indx:].strip() else str1
        

def update_mongodb(collection_name, data, myquery):
    collection = db[collection_name]
    collection.remove(myquery)
    collection.insert(data)

domain = 'https://www.ratebeer.com'
beer_query = 'https://beta.ratebeer.com/v1/api/graphql/?operationName=GetBrewerBeers&variables=%7B%22first%22%3A100%2C%22orderBy%22%3A%22NAME%22%2C%22brewerId%22%3A%22{}%22%2C%22query%22%3A%22%22%2C%22orderDirection%22%3A%22ASC%22%2C%22minRatings%22%3A0%2C%22hideRetired%22%3Afalse%2C%22hideAliased%22%3Afalse%2C%22hideVerified%22%3Afalse%2C%22hideUnverified%22%3Afalse%2C%22hideUserRatedBeers%22%3Afalse%2C%22hideUserHasNotRated%22%3Afalse{}%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22197da784177aba6c136ee0a8703d441cc39a780ecdece1b1110b50f927d2f0c2%22%7D%7D'
brewery_query = 'https://beta.ratebeer.com/v1/api/graphql/?operationName=GetBrewerPageInfo&variables=%7B%22brewerId%22%3A%22{}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22fa70ad9f04baac4471768040a3616a300be7d67ae2b64cfaf060a3ef9930b97e%22%7D%7D'
abs_path = 'C:/Users/zh4448/Documents/RateBeerDocuments/Newversion/'


for abbr in constant.abbr:
    filename = abs_path + 'breweries/rateBeer_breweries_' + abbr + '.csv'
    
    gt_brewers = []
    gt_beers = []

    '''Convert dataframe to list of dictionary'''
    lt_brewery = pd.read_csv(filename, dtype={'Closed': str, 'Est.': str}).to_dict('records')
    
    for index,brewery in enumerate(lt_brewery):
        gt_brewery_id = []
        gt_beer_id = []
        
        print('Brewery No:'+str(index+1)+' /Total No: '+str(len(lt_brewery))+',State: '+abbr)
        brewery_dic = OrderedDict(brewery)   #{'Company': brewery['Name']}  
#        brewery_dic['Closed'] = brewery_dic['Closed'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
        
#                brewery_dic.update({key:brewery[key] for key in ['State','Est.','Closed']})
        try:
            brewery_id = brewery['Link'].split('/')[-2]
#            brewery_id = '12890'
            next_url = brewery_query.format(brewery_id)
            brewery_content = json.loads(get_general_html(next_url))
        except:
            print(brewery_dic['Name'] + ' No beer data')
            continue
        
        del brewery_dic['Name']
        '''Brewery info'''
        brewery_data = brewery_content['data']['brewer']
        if brewery_data['isRetired'] == True:
            brewery_dic['Status'] = 'CLOSED'
        else: brewery_dic['Status'] = ' '
        brewery_dic['Company'] = brewery_data['name']
        brewery_dic['Address'] = brewery_data['streetAddress']+','+brewery_data['city']
        brewery_dic['Zip'] = brewery_data['zip']
        brewery_dic['Website'] = brewery_data['web']
        if brewery_data['phone'] and brewery_data['areaCode']:
            brewery_dic['Phone'] = '('+brewery_data['areaCode']+') '+brewery_data['phone']
        if brewery_data['phone']:
            brewery_dic['Phone'] = brewery_data['phone']
        brewery_dic['BreweryId'] = brewery_data['id']
        gt_brewers.append(brewery_dic.copy())
        
        
        gt_brewery_id.append(brewery_id)
        brewery_condition = { "brewery.id": { "$in": gt_brewery_id } }
        update_mongodb('breweries', {'brewery':brewery_data}, brewery_condition)
        '''Beer list'''
        hasBeer = True
        next_url = beer_query.format(brewery_id,'')
        beer_content = json.loads(get_general_html(next_url))
        beer_list = []
        while hasBeer:
            beers_table = beer_content['data']['brewerBeers']['items']
            beer_list.extend(beers_table.copy())
            for beer_item in beers_table:
                beer_dic = OrderedDict()
                beer_item = beer_item['beer']
                beer_dic.update({key:brewery_dic[key] for key in ['State','Company','BreweryId', 'Est.','Closed','Status']})
                beer_dic['BeerOriginalName'] = beer_item['name']
                beer_dic['BeerName'] = remove_sub(beer_item['name'], beer_dic['Company'])
                beer_dic['BeerId'] = beer_item['id']
                beer_dic['BeerCreated'] = beer_item['createdAt'][:10]
                beer_dic['ABV'] = beer_item['abv']
                beer_dic['Style'] = beer_item['style']['name']
                beer_dic['Ratings'] = beer_item['ratingsCount']
                beer_dic['Avg'] = beer_item['averageQuickRating']
                beer_dic['Archived'] = beer_item['isRetired']
                gt_beers.append(beer_dic.copy())
                gt_beer_id.append(beer_item['id'])
            if beer_content['data']['brewerBeers']['last']:
                next_url = beer_query.format(brewery_id,'%2C%22after%22%3A%22{}%22'.format(beer_content['data']['brewerBeers']['last']))
                beer_content = json.loads(get_general_html(next_url))
            else: hasBeer = False
            
        beer_condition = {"beer.id": {"$in": gt_beer_id}}
        update_mongodb('beers', beer_list, beer_condition)
    path = abs_path + 'breweries_info'
    filename = 'rateBeer_breweries_info_'+abbr+'.csv'
    exportCSV(gt_brewers,filename,path)
   
    path = abs_path + 'beers'
    filename = 'rateBeer_beers_'+abbr+'.csv'
    exportCSV(gt_beers,filename,path)
        