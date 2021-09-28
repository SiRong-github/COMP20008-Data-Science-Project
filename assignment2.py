#libraries

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
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
    
    return


def extract_jobkeeper():

    #IMPORTANT
    # https://stackoverflow.com/questions/51478413/select-a-column-by-its-name-openpyxl

    #jobkeeper_data
    jobkeeper = openpyxl.load_workbook(jobkeeper_data)
  
    #variables for each sheet
    first_phase = jobkeeper["First Phase"]
    first_quarter = jobkeeper["Extension - First Quarter"]
    second_quarter = jobkeeper["Extension - Second Quarter"]    
    
    
    
    
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
        if re.search("ad", str(cell)) == None:
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
    postcode_with_name_data = pd.DataFrame(records, columns = column_names) 
    
    return