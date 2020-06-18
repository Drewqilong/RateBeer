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

domain = 'https://www.ratebeer.com'
abs_path = 'E:/RateBeerDocuments/Newversion/'

gt_states = []

state_link = OrderedDict()

'''Get all the states links'''
url = 'https://www.ratebeer.com/breweries/'
state_content = get_general_html(url)
state_soup = bs4.BeautifulSoup(state_content, 'lxml')
states = state_soup.find('div', id = 'default').find_all('a')
stopSign = states[0].find_next('h3').find_next('a').text
for link in states:
    if link.text == stopSign:
        break
    state_link['State'] = link.text
    state_link['Link'] = link.attrs['href']
    gt_states.append(state_link.copy())

'''Get breweries by state'''
for state in gt_states[:1]:
    gt_brewery = []
    abbr = list(constant.states.keys())[list(constant.states.values()).index(state['State'])]
    next_url = domain+state['Link']
    brewery_content = get_general_html(next_url)
    brewery_soup = bs4.BeautifulSoup(brewery_content, 'lxml')
    '''Get breweries'''
    '''Active and closed breweries'''
    brewery_tables = brewery_soup.find_all('div', {'id':['active','closed']}) #class_ = 'tab-pane active searchable',
    
    for table in reversed(brewery_tables):
        for row in table.find_all('tr'):
            brewery = OrderedDict({'State':abbr})
            if row.parent.name == 'thead':
                head = [value.text for value in row.find_all('th')]
                continue
            columns = [value.text for value in row.find_all('td')]
            columns[0] = row.find('a').text
            for pair in zip(head,columns):
                if pair[0] == 'My Count': continue
                brewery[pair[0]] = pair[1]
            brewery['Link'] = row.find('a').attrs['href']
            gt_brewery.append(brewery.copy())

    path = abs_path + 'breweries'
    filename = 'rateBeer_breweries_'+abbr+'.csv'
    exportCSV(gt_brewery,filename,path)