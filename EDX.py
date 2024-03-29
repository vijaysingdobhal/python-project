#!/usr/bin/env python
# coding: utf-8

# # Scriping and Anaylyzing Basketball Statistic with Python 
# 

# # description 

# Web scripting involves extracting data from website. in this assignment you will web scrape basketball statistics from wikipedia of some of the greatest basketball players. you will perform some anyasis on the data using pandas, PLT some basic questions then store the data on IBM cloud.

# In[3]:


import bs4
import requests
import pandas as pd
import numpy as np
import boto3


# In[4]:


def get_basketball_stats(link='https://en.wikipedia.org/wiki/Michael_Jordan'):
    # read the webpage 
    response = requests.get(link)
    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # the player stats are defined  with the attribute CSS class set to 'wikitable sortable'; 
    #therefore we create a tag object "table"
    table = soup.find(class_='wikitable sortable')

    #the headers of the table are the first table row (tr) we create a tag object that has the first row  
    headers = table.tr
    #the table column names are displayed  as an abbreviation; therefore we find all the abbr tags and returs an Iterator
    titles = headers.find_all("abbr")
    #we create a dictionary  and pass the table headers as the keys 
    data = {title['title']:[] for title in titles}
   #we will store each column as a list in a dictionary, the header of the column will be the dictionary key 

    #we iterate over each table row by fining each table tag tr and assign it to the objed
    for row in table.find_all('tr')[1:]:
    
        #we iterate over each cell in the table, as each cell corresponds to a different column we all obtain the correspondin key corresponding the column n 
        for key,a in zip(data.keys(),row.find_all("td")[2:]):
            # we append each elment and strip any extra HTML contnet 
            data[key].append(''.join(c for c in a.text if (c.isdigit() or c == ".")))

    # we remove extra rows by finding the smallest list     
    Min=min([len(x)  for x in data.values()])
    #we convert the elements in the key to floats 
    for key in data.keys():
    
        data[key]=list(map(lambda x: float(x), data[key][:Min]))
       
    return data


# In[5]:


import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display


# The list links contain the link the wikipedia article for each player. the list names contains the names of each player.

# In[6]:


links=['https://en.wikipedia.org/wiki/Michael_Jordan'       ,'https://en.wikipedia.org/wiki/Kobe_Bryant'      ,'https://en.wikipedia.org/wiki/LeBron_James'      ,'https://en.wikipedia.org/wiki/Stephen_Curry']
names=['Michael Jordan','Kobe Bryant','Lebron James','Stephen Curry']


# for each player create a Python dictionary from the table Regular season table 

# In[7]:


dicts = []

for link in links:
    dicts.append(get_basketball_stats(link))

For each player display the first five rows of the Dataframe, print the name of each player above the Dataframe.
# In[9]:


dfs = []

for d in dicts:
    dfs.append(pd.DataFrame(d))


# In[10]:


for i, df in enumerate(dfs):
    print('\n' + names[i])
    display(df.head())


# Question 2: plot the Point per game for a player using the fuction plt.plot()

# In[11]:


import matplotlib.pyplot as plt


# Using the function plt.plot() plot the Point per game for one player just a note you can plot a dataframe column like a numpy array. you can aslo them each player.find out how to add a xlabel 'years' Point per game and a legend.

# In[17]:


#Indivisual
for i, df in enumerate(dfs):
    plt.figure()
    plt.plot(df[['Points per game']],label=names[i])
    plt.legend()
    plt.xlabel('Years since first one')
    plt.ylabel('Points per game')


plt.show()


# Question 3: Store the player Statistical in Object Storage (optional).
# 
# Save one player's dataframe as a csv file using the method
# dataframe.to_csv(csv_name). The string that contains the name of the csv file should be assigned the csv_name

# In[25]:


csv_name = []

for i, df in enumerate(dfs):
    csv_name.append(names[i].replace(' ','_')+'.csv')
    df.to_csv(csv_name[i])
    print(i)


# In[22]:


dfs


# In[ ]:




