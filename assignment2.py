#if not installed
# !pip install openpyxl
# !pip install plotly
# !pip install statsmodels
# geopandas via anaconda

#libraries
import geopandas as gpd
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
import statsmodels.api as sm

#variables for datasets
covid_data = "COVID19 Data Viz Postcode data - postcode.csv"
jobkeeper_data = "jobkeeperdata-20210625_1.xlsx"
postcode_data = "https://www.worldpostalcodes.org/l1/en/au/australia/list/r1/list-of-postcodes-in-victoria"

def extract_covid():
    '''Extracting number of covid cases by postcode from csv'''
    
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
    '''Extracting number of jobkeeper application count by postcode from excel worksheet'''
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
    #appending application counts from each sheet respectively    
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
    #concatenate everything onto one dataframe
    all_phases_df = pd.concat([first_phase_df, first_quarter_df, second_quarter_df], axis=1)
    all_phases_df = all_phases_df.drop(all_phases_df.index[:649])
    all_phases_df = all_phases_df.drop(all_phases_df.index[663:])
    all_phases_mean = all_phases_df.mean(axis=1)
    all_phases_mean_df = pd.DataFrame({'postcode':all_phases_mean.index, 'application count':all_phases_mean.values})
    
    return all_phases_mean_df


def extract_postcode():
    '''Extracting postcode and corresponding name of postcode area from website'''
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
    
    #iterating through all rows in the table
    for row in rows[2:]:
        cell = row.find_all("td")     
        #removing ads
        if re.search("adsbygoogle", str(cell)) == None:
            cells.append(cell)
    
    #iterating through each cell to join each code and name
    for i in range(len(cells)):
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
    '''Combining all three dataframes into a singular dataframe for further analysis'''
    #extracting data with functions created above
    covid = extract_covid()
    jobkeeper = extract_jobkeeper()        
    postcode = extract_postcode()
    #converting postcode column to the same type for concatenation
    covid["postcode"] = covid["postcode"].astype(int)
    jobkeeper["postcode"] = jobkeeper["postcode"].astype(int)
    postcode["postcode"] = postcode["postcode"].astype(int)
    #using merge to combine all three dataframes by postcode number
    com1 = pd.merge(postcode, covid, on='postcode')
    combination = pd.merge(com1, jobkeeper, on='postcode')
    
    #deleting an outlier
    for index, row in combination.iterrows():
        if row['postcode'] == 3026:
            combination = combination.drop([index, index + 1], axis=0)
            break

    return combination

def sort_by_postcode():
    '''Sorting combination by postcode number and calculating cases and application proportion'''
    combi = combination
    combi['cases proportion'] = (combi['cases']/combi['population'])*100
    combi['application proportion'] = (combi['application count']/combi['population'])*100
    
    return combi
    
def sort_by_suburb():
    '''Sorting combination by postcode name and calculating cases and application proportion'''
    #sorting and collating the data by suburb
    sorted_by_suburb = combination.groupby(['postcode name']).sum()
    sorted_by_suburb['cases proportion'] = (sorted_by_suburb['cases']/sorted_by_suburb['population'])*100
    sorted_by_suburb['application proportion'] = (sorted_by_suburb['application count']/sorted_by_suburb['population'])*100
    
    return sorted_by_suburb

def scatterplot():
    '''Plotting scatterplot for cases and application proportion'''
    
    plt.figure(figsize=(15,5))
    plt.grid(True)
    sns.regplot(x='application proportion', y='cases proportion', data=sort_by_postal_name, robust=True)
    plt.title('Scatterplot of application and cases proportion')
    plt.savefig("scatterplot_cases_and_application.png")
    
    return

def regression_results(data_used):
    '''Regression analysis of data_used for cases and application proportion'''
    #OLS regression for cases and application proportion
    cases_prop = data_used['cases proportion']
    appli_prop = data_used['application proportion']
    results = sm.OLS(appli_prop, cases_prop).fit()
    print("OLS Regression Results for Cases and Application proportion:")
    print(results.summary())
    
    return

def descriptive_statistics():
    '''Returning descriptive statistics and correlation of dataframe grouped by suburbs'''
    desc_stat = sort_by_postal_name.describe
    correlation = sort_by_postal_name.corr()
    #printing results
    print("Descriptive statistics of dataframe sort_by_postal_name:")
    print(desc_stat)
    
    print("Correlation in dataframe sort_by_postal_name:")
    print(correlation)
    return 

def proportions_csv():
    temp = sort_by_postal_code.loc[:, ['postcode', 'postcode name', 'cases proportion', 'application proportion']]
    temp.rename(columns = {'postcode': 'POSTCODE'}, inplace = True)
    temp.replace([np.nan, np.inf, -np.inf], 0, inplace = True)
    temp.to_csv(r'proportions.csv', index = False)
    proportions = pd.read_csv('proportions.csv')
    return proportions

def shapefile_plot_case_proportion():
    '''Plotting geospatial data for cases proportion'''
    proportions = proportions_csv()
    gdf = gpd.read_file('VicShapefile/POSTCODE_POLYGON.shp')
    gdf.drop(columns = ['PFI', 'PFI_CR', 'UFI', 'UFI_CR', 'UFI_OLD'], inplace = True)
    gdf.sort_values(by = 'POSTCODE', inplace = True)
    gdf["POSTCODE"] = gdf["POSTCODE"].astype(int)
    gdf = gdf.merge(proportions, on = 'POSTCODE')
    gdf.plot("cases proportion", legend = True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Shapefile Plot for Case Proportion")    
    plt.tight_layout()
    plt.savefig("shapefile_plot_case_proportion.png")
    return

def shapefile_plot_application_proportion():
    '''Plotting geospatial data for application proportion'''
    proportions = proportions_csv()
    gdf = gpd.read_file('VicShapefile/POSTCODE_POLYGON.shp')
    gdf.drop(columns = ['PFI', 'PFI_CR', 'UFI', 'UFI_CR', 'UFI_OLD'], inplace = True)
    gdf.sort_values(by = 'POSTCODE', inplace = True)
    gdf["POSTCODE"] = gdf["POSTCODE"].astype(int)
    gdf = gdf.merge(proportions, on = 'POSTCODE')
    gdf.plot("application proportion", legend = True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Shapefile Plot for Application Proportion")    
    plt.tight_layout()
    plt.savefig("shapefile_plot_application_proportion.png")
    return 

#Calling for function to start initial data wrangling
combination = combination()

#Calling for function to start data wrangling
sort_by_postal_code = sort_by_postcode()
sort_by_postal_name = sort_by_suburb()

#running scatterplots, regression and descriptive statistics
scatterplot()
regression_results(sort_by_postal_name)
descriptive_statistics()

#creating shapefiles for case and application proportions
shapefile_plot_case_proportion()
shapefile_plot_application_proportion()
