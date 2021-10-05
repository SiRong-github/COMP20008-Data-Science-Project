#libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import openpyxl
import unicodedata
import csv
import re
import os
from numpy import arange
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import plotly.express as px 

#variables for datasets

covid_data = "COVID19 Data Viz Postcode data - postcode.csv"
jobkeeper_data = "jobkeeperdata-20210625_1.xlsx"
postcode_data = "https://www.worldpostalcodes.org/l1/en/au/australia/list/r1/list-of-postcodes-in-victoria"

def extract_covid():
    #covid_data     
    covid = pd.read_csv(covid_data)  
    #variables for required columns
    postcode_covid = covid["postcode"]
    cases_covid = covid["cases"]
    population_covid = covid["population"]
    #concatenate everything onto one dataframe
    covid_pd = pd.concat([postcode_covid, cases_covid, population_covid], axis=1)
    covid_pd.drop([702,703], inplace = True)
    return covid_pd






def extract_jobkeeper():
    #IMPORTANT
    # https://stackoverflow.com/questions/51478413/select-a-column-by-its-name-openpyxl
    #jobkeeper_data
    jobkeeper = openpyxl.load_workbook(jobkeeper_data)
    #variables for each sheet
    first_phase = jobkeeper["First Phase"]
    first_quarter = jobkeeper["Extension - First Quarter"]
    second_quarter = jobkeeper["Extension - Second Quarter"]

    first_phase_df = pd.DataFrame()
    first_quarter_df = pd.DataFrame()
    second_quarter_df = pd.DataFrame()

    first_phase_postcodes = []
    first_quarter_postcodes = []
    second_quarter_postcodes = []
        
    for cell in first_phase['A']:
        first_phase_postcodes.append(cell.value)

    for cell in first_quarter['A']:
        first_quarter_postcodes.append(cell.value)
    
    for cell in second_quarter['A']:
        second_quarter_postcodes.append(cell.value)

    columns = ['B', 'C', 'D', 'E', 'F', 'G']

    for column in columns:
        temp = []
        for cell in first_phase[column]:
            temp.append(cell.value)
        first_phase_df[temp[1]] = temp[2:-2]

    first_phase_df.index = first_phase_postcodes[2:-2]
    for column in columns[:3]:
        temp = []
        for cell in first_quarter[column]:
            temp.append(cell.value)
        first_quarter_df[temp[1]] = temp[2:-2]

    first_quarter_df.index = first_quarter_postcodes[2:-2]
    
    for column in columns[:3]:
        temp = []
        
        for cell in second_quarter[column]:
            temp.append(cell.value)
    
        second_quarter_df[temp[1]] = temp[2:-2]
    
    second_quarter_df.index = second_quarter_postcodes[2:-2]
    all_phases_df = pd.concat([first_phase_df, first_quarter_df, second_quarter_df], axis=1)
    all_phases_df = all_phases_df.drop(all_phases_df.index[:649])
    all_phases_df = all_phases_df.drop(all_phases_df.index[663:])
    all_phases_mean = all_phases_df.mean(axis=1)
    all_phases_mean_df = pd.DataFrame({'postcode':all_phases_mean.index, 'application count':all_phases_mean.values})
    
    return all_phases_mean_df


def extract_postcode():
    #IMPORTANT    
    # btw, we can't use read_html since there's a 403 error (need access)
    #postcode_data 
    #specifying the page to download for postcodes
    page = requests.get(postcode_data)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("table")
  
    #variables
    rows = table.find_all("tr")
    cells = []
    records = []
    
    #iterating thru all rows in the table
    for row in rows[2:]:
        cell = row.find_all("td")     
        #removing ads
        if re.search("adsbygoogle", str(cell)) == None:
            cells.append(cell)
    
    #iterating thru each cell
    for i in range(len(cells)):
        #to join each code and name 
        record = []



        #code
        postcode_code = unicodedata.normalize("NFKD", cells[i][0].text.strip())
        record.append(postcode_code)
  
        #name
        postcode_name = unicodedata.normalize("NFKD", cells[i][1].text.strip())
        record.append(postcode_name)
      
        #joining all lists containing code and name
        records.append(record)
    
    #creating dataframe
    column_names = ["postcode", "postcode name"]
    postcode_with_name_data = pd.DataFrame(records, columns=column_names) 
    
    return postcode_with_name_data
  
def combination():
    covid = extract_covid()
    jobkeeper = extract_jobkeeper()        
    postcode = extract_postcode()
    
    covid["postcode"] = covid["postcode"].astype(int)
    jobkeeper["postcode"] = jobkeeper["postcode"].astype(int)
    postcode["postcode"] = postcode["postcode"].astype(int)
    
    com1 = pd.merge(postcode, covid, on='postcode')
    combination = pd.merge(com1, jobkeeper, on='postcode')

    return combination


x = combination()
new  = pd.merge(x, land, left_on = 'postcode name', right_on= 'SUBURB')


# plotly 
fig = px.line(x, x='postcode', y='cases')

fig.update_layout(legend=dict(
    yanchor="top",
    y=1.12,
    xanchor="right",
    x=1.00
))

# Show plot 
fig.show()


# plotly 
fig = px.line(x, x='postcode', y='population')

fig.update_layout(legend=dict(
    yanchor="top",
    y=1.12,
    xanchor="right",
    x=1.00
))

# Show plot 
fig.show()


x['prop'] = x['cases']/x['population']
x_trans = x.groupby(['postcode name']).sum()
#x_trans.to_csv('new.csv')
x_new = pd.read_csv('new.csv')
x_new['cases proportion'] = (x_new['cases']/x_new['population'])*100
x_new['application proportion'] = (x_new['application count']/x_new['population'])*100

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode name',y='cases proportion',data=x_new)
plt.setp(plt.xticks()[1], rotation=90)

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode name',y='application proportion',data=x_new)
plt.setp(plt.xticks()[1], rotation=90)

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='application count',data=x);

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='population',data=x);

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='cases',data=x);

x_new.describe()

tax_data = pd.read_excel('ts19individual06taxablestatusstateterritorypostcode.xlsx', sheet_name = 'Table 6B')
tax_x = pd.merge(x, tax_data, left_on='postcode', right_on='Postcode')

plt.figure(figsize=(30,10))
sns.heatmap(tax_x.corr())

# plotly 
fig = px.line(tax_x, x='postcode', y='Number of individuals\nno.')

fig.update_layout(legend=dict(
    yanchor="top",
    y=1.12,
    xanchor="right",
    x=1.00
))

# Show plot 
fig.show()


plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='Number of individuals\nno.',data=tax_x);

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='People with private health insurance\nno.',data=tax_x);

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='Number of individuals\nno.',data=tax_x);


plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='Private health insurance - your Australian Government rebate received\nno.',data=tax_x);


plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='Low and middle income tax offset\nno.',data=tax_x);

plt.figure(figsize=(15,5))
plt.grid(True)
sns.scatterplot(x='postcode',y='Low income tax offset\n$',data=tax_x);