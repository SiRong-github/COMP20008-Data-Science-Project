# Subject
This Data Science research project was done in a group of 4 for COMP20008 Elements of Data Processing of the University of Melbourne.

# Downloadable Pdfs
[Project Proposal](https://github.com/SiRong-github/COMP20008-Data-Science-Project/blob/main/documents/Project%20Proposal.pdf)

[Research Report](https://github.com/SiRong-github/COMP20008-Data-Science-Project/blob/main/documents/FINAL%20Report.pdf)


# What to Run
assignment2.py

# Research Report

## Research Question
Is there a relation between income and COVID-19 case numbers of each postcode area in Victoria?

## Introduction 
The relationship between COVID-19 cases and income may affect livability in Victoria. Where there is an increase in either case numbers or low income, it has been shown that residents feel increased anxiety about potential outbreaks of disease as well as health problems caused by living conditions. The relationship between income and COVID-19 cases also affects inclusiveness, health, and sustainability of communities. A study by Cash et al. has shown that 90% of reported COVID-19 deaths are in the world’s richest countries, not including the numbers of China, Iran and Brazil . It cites many factors, including poverty, the approach to the pandemic and the locations of care homes for the elderly.

COVID-19 is an international health crisis that has been causing worldwide lockdown, quarantine, and some restrictions. The coronavirus outbreak has rapidly spread across the world, posing enormous health and economic challenges for the human population. New strains have led almost every nation struggling to curb transmission even with testing and treating patients while quarantining potential individuals with the virus through contact tracing or restricting large gatherings.

The goal of this report is to investigate whether there is a correlation between income and COVID-19 cases in Victoria. We aim to understand health and inclusion by examining how the average wealth of individuals in each postcode area might be related with the spread of COVID-19. With the ongoing pandemic, it is important for the government, healthcare sectors and Victorians to remain vigilant so as to prevent another outbreak. This project aims to highlight whether more actions should be taken to improve the health and sustainability of lower income postcodes. It also serves to show which suburbs should remain cautious once lockdowns are eased or lifted and to aid the nation by knowing what areas require more financial support than others rather than marginalising those who need it most.


## Datasets
Datasets found in Table 1 are used in our analysis. The first dataset is used to obtain information on COVID-19 cases for each postcode. As for a measure of income for each suburb, we have decided to use the JobKeeper application numbers for a year, where the higher application numbers signify a lower income in the postcode area. We will be linking the datasets via postal code as it is the common attribute. As such, we will be using the html link to access the names of each postcode area for identification.

The shapefile is used to visualise our data further into our analysis to give us an understanding of the actual locations of the spread of the virus and that of the application numbers.

Table 1: Databases to be used

| Database Descriptions | Data Format | Links to Data |
| --- | --- | --- |
| Victorian coronavirus data - All cases by postcode (file from 11 September - although updated daily) | Excel CSV | https://discover.data.vic.gov.au/dataset/victorian-coronavirus-data/resource/e3c72a49-6752-4158-82e6-116bea8f55c8 |
| Postcodes and respective names in Victoria | Html | https://www.worldpostalcodes.org/l1/en/au/australia/list/r1/list-of-postcodes-in-victoria |
| Jobkeeper Application Count by Postcode (April 2020 - March 2021) | Excel | https://treasury.gov.au/coronavirus/jobkeeper/data |
| Shapefile for Victoria Region | Shapefile | https://s3-ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_LZMU0O.zip from https://datashare.maps.vic.gov.au/search?md=1553f19f-3b03-5e40-924e-6355eb9a3f89 |

## Wrangling and Analysis Methods
Data wrangling is the process of transforming and mapping data from one "raw" form into a more understandable one with the intention to make it more appropriate for analysis.

In order to link these datasets, we used web crawling and scraping techniques on the site listed above to match suburb names with postcodes. We filtered through the html file and obtained this information that is presented in a table on the website. We accessed the excel and csv files by downloading them and using the module openpyxl to read each sheet. As the JobKeeper file separated data by month, we collated all 12 months and took an average of application counts across the year. We also extracted the population number and total number of cases for each postcode from the Victorian cases excel csv.

By using these data wrangling methods, we were able to combine the raw data more efficiently and generate a DataFrame that contained the postcode, postcode area name, case numbers, population, and application count. We then added columns that divided the application count and case numbers over the population of the area, producing the columns: cases proportion and application proportion (Table.1). DataFrames allow us to use data we have processed more efficiently during our analysis process as compared to lists or Series.



Table 2: DataFrame created for further analysis

<img width="436" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/3a81f603-67bc-4257-b3a3-400d09f3be9d">



We printed a correlation matrix and descriptive statistics for our DataFrame to understand the relationship of each column with the others. This is a good preliminary overview to support future analysis and the identification of outliers.

Scatter plots are a great way to show the spread of cases and application count by postcode for users visually. Although it does not show us the geospatial distribution of cases and applications, we use the scatter plot and a corresponding regression line to identify if there is any relationship between case proportion and application proportion. A regression analysis summary is also printed to understand the visual data better. 

We also used geopandas to produce a visual representation of the case proportion and application proportion across the entire state of Victoria through the aforementioned shapefile in Table 1. This gives us a more realistic overview of the spread of both income and cases in the state as the scatter plots do not show geospatial data.

These graphs and data have assisted us in concluding whether there is a relationship between income and case numbers in each postal area across Victoria.

## Key Results of Research

### Preliminary Analysis of Data
While producing graphs and plots, we noticed a significant outlier through a scatter plot shown in Fig.1. One of the largest outliers being postcode 3026 with an application proportion of 680.56 and case proportion of 156.94 which may have stemmed from an error in the data that shows 72 as a population but has 94 cases of COVID-19. 

The descriptive statistics produced without this outlier in Table.2 shows a mean of 45 cases for every 9119 people in each suburb, which in turn shows a mean application proportion of 3.47. As this data heavily skewed our graphs, we decided to remove this outlier to prevent further distortion in our analysis.



Table 3: Descriptive statistics of data after data wrangling

<img width="468" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/246840e5-2de0-4e90-9231-df8ab6f124cf">



Figure 1: Scatter plot of application proportion and cases proportion by postal code

<img width="472" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/899c719c-11c9-464c-a7c0-b171c07792e3">



As seen in our scatter plot in Fig.2, it is unclear if there is a relationship between application proportion and cases proportion in Victoria. We took a look at our regression summary to aid our understanding in Table 3. The adjusted R-squared of 0.367 shows that 36.7% of COVID-19 case proportions data can be explained by application proportions and there is a moderate positive relationship between income and case proportions.

Our correlation analysis in Table 4 also supports this moderate positive relationship with a correlation coefficient of 0.252 between application and case proportions.



Figure 2: Scatter plot of application proportion and cases proportion by postal names

<img width="500" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/97a98842-0e42-4883-befc-81370fd7c249">



Table 3: OLS Regression Results

<img width="470" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/d0be185e-8075-4e5c-b83f-8240c8287ba8">



Table 4: Correlation between columns in DataFrame

<img width="468" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/01807cec-8737-4e9b-bdf9-f6c85c2aa2c9">



### Geospatial Analysis of Data
We also looked at the geospatial data created via GeoPandas. Based on the two spatial graphs in Fig.3 and Fig.4, COVID-19 cases are prevalent around the central part of Victoria (especially around Melbourne), whereas application proportions are spread evenly across the state. However, some exceptionally high application proportions can be observed from the central part of Victoria, which might be related to the inner parts of Victoria being the ground zero of the COVID-19 virus.



Figure 3: Geospatial data of case proportions

<img width="340" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/8893742e-f513-4b26-aba4-d6f32c66d142">



Figure 4: Geospatial data of application proportions

<img width="367" alt="image" src="https://github.com/SiRong-github/COMP20008-Data-Science-Project/assets/62817554/21ee8523-716d-4b40-a3af-1ed09932bbf0">



### Significance and Value of Results
#### Summary of Analysis
Taking into account the results of the scatterplot and descriptive statistics, we can see a moderately positive relationship between the cases proportion and application proportion. This would signify that as the proportion of applications for JobKeeper increases in a postcode area, the proportion of cases also increases.

This conclusion is somewhat supported by the geospatial data we produced, where there are higher application proportions for areas with more cases. However, we also note that there are areas not as significantly affected by the spread of COVID-19 but still see higher proportions of applications in the postcode area.

We can conclude that there is a somewhat positive relationship between income and case numbers in postcode areas.

#### Significance
Through this research, we have found that although there is a significant relationship between income and cases of COVID-19, it is not a very strong one. This would mean that the lower income areas of Victoria are not neglected and that Victoria shows inclusiveness and sustainability of its communities during this fight against COVID-19.

Authorities and Victorians alike should continue to ensure that this level of inclusiveness is maintained as the pandemic is likely to continue to have a significant impact in our lives for the foreseeable future.

### Limitations and Improvement
One limitation of this project is the lack of net income data from 2020-2021. Although it is reasonable to assume areas with lower income would have higher percentages of applications, it is unverifiable without the actual data. While we were able to improvise by making use of Jobkeeper application counts, it would make the results more significant if we had used relevant net income data. 

Another limitation is that the spread of COVID-19 is likely due to many more factors than analysed in our report. Some potential reasons would be the spread of households in a given postcode or with the newly introduced vaccination programme, the percentage of vaccinated people in each postcode area. Hence, our report that focuses on the relationship between income and COVID-19 spread may be skewed by other factors.

We should also note that the scatter plot and regression used do not denote a causal relationship between both variables. It only signifies a relationship, and the spread of COVID-19 cannot be said to depend on income levels.

One way to improve the project for the future would be to use updated and relevant datasets. We could also make use of GeoPandas View or Folium for a more interactive visualisation. 

Another key improvement would be to include more potential factors and their correlation with each other to ensure a more robust analysis on the spread of COVID-19 and livability in Victoria.

