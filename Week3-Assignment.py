#!/usr/bin/env python
# coding: utf-8

# ### Neighborhoods in Canada Project

# This project includes  the neighborhoods in the city of Toronto. The neighborhood data was not readily available on the internet. It is scraped from Wikipedia by using BeautifulSoup and requests libraries of Python.

# In the first step, libraries imported.

# In[353]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis

import requests #library to handle requests

import sys, json # library to handle JSON data

from bs4 import BeautifulSoup #library for pulling data out of HTML and XML files

import lxml.html as lh #library for processing XML and HTML

print('Libraries imported.')


# ### Scraping Data From Wikipedia

# Wikipedia has been blocked in-country, and I used wiki zero instead of it.

# In[354]:


#Make request to webpage
page = requests.get("https://www.wikizeroo.org/index.php?q=aHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvTGlzdF9vZl9wb3N0YWxfY29kZXNfb2ZfQ2FuYWRhOl9N")
doc=lh.fromstring(page.content)

#filter table elements from page
tr_elements = doc.xpath('//tr')

#Create empty list
col_list=[]
i=0

#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col_list.append((name.strip("\n")))

#Columns of neighborhoods dataframe   
print(col_list)


# In[355]:


#BeautifulSoup used to get table data.

soup= BeautifulSoup(page.text,'html.parser')
list_of_rows = []

for row in soup.find_all('tr'):
    list_of_cells = []
    for col in row.find_all('td'):
        text = col.text
        
        list_of_cells.append(text.strip("\n"))
    if len(list_of_cells) == len(col_list):
        list_of_rows.append(list_of_cells)
    else:
        pass

#Create dataframe from lists
df= pd.DataFrame(list_of_rows,columns=col_list)

#"Not Assigned" neighborhoods replaced with borough.
df[df.Neighbourhood == "Not assigned"]["Neighbourhood"] = df.Borough

#Filter table
neighborhoods = df[df.Borough != "Not assigned"]


# In[356]:


#group neighborhoods by postcodes and combine them into one row with a comma

new_neighborhoods= neighborhoods.groupby(["Postcode"]).Neighbourhood.agg([('count'), ('Neighbourhood', ', '.join)])
neighborhoods=pd.merge(new_neighborhoods,neighborhoods[["Postcode","Borough"]], on="Postcode",how="left")

#Print dataframe shape
print("Neighborhoods in Toronto dataFrame size is: ",neighborhoods.shape[0],"rows", " ",neighborhoods.shape[1],"columns")


# In[357]:


neighborhoods.head()

