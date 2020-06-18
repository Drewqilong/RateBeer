# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 15:17:08 2020

@author: Jerry
"""

import generalFunctions
import json 

next_url = 'https://beta.ratebeer.com/v1/api/graphql/?operationName=GetBrewerBeers&variables=%7B%22first%22%3A100%2C%22orderBy%22%3A%22NAME%22%2C%22brewerId%22%3A%2210920%22%2C%22query%22%3A%22%22%2C%22orderDirection%22%3A%22ASC%22%2C%22minRatings%22%3A0%2C%22hideRetired%22%3Afalse%2C%22hideAliased%22%3Afalse%2C%22hideVerified%22%3Afalse%2C%22hideUnverified%22%3Afalse%2C%22hideUserRatedBeers%22%3Afalse%2C%22hideUserHasNotRated%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22197da784177aba6c136ee0a8703d441cc39a780ecdece1b1110b50f927d2f0c2%22%7D%7D'

content = json.loads(generalFunctions.get_general_html(next_url))