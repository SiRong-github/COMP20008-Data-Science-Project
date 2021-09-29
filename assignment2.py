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
    
    #Extension - First Phase (2020)

    #IMPORTANT
    #we can prolly use regex for the value after None to be postcode and before None to be Count (see "THIS WORKS" below)
    # then we can directly go w/ the formula according to the documentation for openpyxl    
    # we'll basically just reuse the code for First and Second Quarter
    
            #THIS WORKS
            #for row in first_phase.values:
            #    for value in row:
            #        print(value)    


            #THIS DOESN'T WORK
            #first_phase_postcode = first_phase["Postcode"]

            #apr_jobkeeper = first_phase["April Application Count"]
            #may_jobkeeper = first_phase["May Application Count"]
            #jun_jobkeeper = first_phase["June Application Count"]
            #jul_jobkeeper = first_phase["July Application Count"]
            #aug_jobkeeper = first_phase["August Application Count"]
            #sep_jobkeeper = first_phase["September Application Count"]

    #Extension - First Quarter (2020)

    #first_quarter_postcode = first_quarter["Postcode"]    
    
    #oct_jobkeeper = first_quarter["October Application Count"]
    #nov_jobkeeper = first_quarter["November Application Count"]  
    #dec_jobkeeper = first_quarter["December Application Count"]    
  
    #Extension - Second Quarter (2021)
    
    #second_quarter_postcode = second_quarter["Postcode"]
    
    #jan_jobkeeper = second_quarter["January Application Count"]
    #feb_jobkeeper = second_quarter["February Application Count"]
    #mar_jobkeeper = second_quarter["March Application Count"]
  
    return


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
    column_names = ["postcode code", "postcode name"]
    postcode_with_name_data = pd.DataFrame(records, columns=column_names) 
    
    return
