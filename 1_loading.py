'''
Code to import, clean, and produce key stats from the Companies House dataset
----
0) Modules, Prerequisites, Other
'''

import pandas as pd
from pandas import DataFrame, Series
import numpy as np

import matplotlib.pyplot as plt
# Increase figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14


'''
1) Loading and formatting data
'''

# download latest monthly version at the following:
# http://download.companieshouse.gov.uk/en_output.html
ch_raw = pd.read_csv('BasicCompanyDataAsOneFile-2017-09-01.csv')

#delete unnecessary columns
ch = ch_raw.iloc[:,[0,1,4,5,6,7,8,9,10,11,12,18,19,21,26,27,28,29]]

#rename columns
ch.columns = ['name','crn','address1','address2','postTown','county','country', \
            'postcode','category','status','origin','accounts_lastMadeUpDate','accountCategory',\
            'returns_lastMadeUpDate','sic1','sic2','sic3','sic4']

#missing values
ch.sic1.replace('None Supplied', np.NaN, inplace=True)
ch = ch.dropna(subset=['name']) # delete rows with null business names (only 1 for Sep data)


# Key stats
print '---------'
print 'Number of businesses: %s' %len(ch)
print 'Missing SIC codes: %s' %ch.sic1.isnull().sum()
sic_comp = (1.0 - (float(ch.sic1.isnull().sum())/len(ch)))*100
print 'SIC code completion: %.2f' %sic_comp + '%'
post_comp = (1.0 - (float(ch.postcode.isnull().sum())/len(ch)))*100
print 'Postcode completion: %.2f' %post_comp + '%'
print '---------'
print 'Category breakdown (top 5)'
print ''
print ch.category.value_counts().head()
print '---------'
print 'Account category (top 5)'
print ''
print ch.accountCategory.value_counts().head()
print '---------'
print 'Geographical breakdown (top 5)'
print ''
print ch.origin.value_counts().head()
print '---------'
print 'SIC code breakdown (top 5)'
print ''
print ch.sic1.value_counts().head()

# Export dataset, named after MMYY of ch data
ch.to_csv('ch_0917.csv',index=False)

# Optional : remove non-UK companies
ch_uk = ch[ch['origin'].isin(['United Kingdom','Great Britain','UNITED KINGDOM','GREAT BRITAIN','ENGLAND & WALES','UK'])]
ch_uk.reset_index(inplace=True)


'''
2) Exploration
'''

ch.dtypes # types of each column - all objects

# search for companies
ch.name.str.lower().str.contains('dyson').sum() #number of companies with term
ch[ch.name.str.lower().str.contains('dyson')] #the companies matching the search term

def find_company(name):
    n = ch.name.str.lower().str.contains(name)
    x = raw_input(str(n.sum()) + ' companies found. See list of companies? Y or N? ')
    if x.lower() == 'y':
        return ch[n]
    else:
        return True

find_company('dyson') #210 results

# sic code specific
ch.sic1.describe() #counts occurences and unique values
ch.sort_values('sic1') #sorts by sic code
ch.sic1.value_counts().head(20)
ch.sic1.value_counts().head(30).plot() #shows skew of top categories

# company reference number
ch.crn.describe() # all crns are unique
ch.crn.isnull().sum() # 0

# addresses
ch.address1.describe() # 1.6 million unique addresses
ch.address1.isnull().sum #11,178
ch.address2.isnull().sum() #1.3million
ch.postTown.isnull().sum() #82K
ch.county.isnull().sum() #2m
ch.country.isnull().sum() #2.2m
ch.postcode.isnull().sum() #37K - 30,000 companies at N1 7GU - odd
