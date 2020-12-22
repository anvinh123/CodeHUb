# DESCRIPTION
# DATA SOURCE ='D:/Work/Automous/Autonomous Code Hub/CodeHUb/purchasing_data_2020.csv'
# LINK FOR REFERENCE = https://www.kaggle.com/sarahm/customer-segmentation-using-rfm-analysis
# LIBRARY : numpy, pandas, time, warnings, datetime, matplotlib.pyplot, seaborn
#-----------------------------------------------------------------------
import numpy as np
import pandas as pd
import time,warnings
import datetime as dt
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
%matplotlib inline
import seaborn as sns
warnings.filterwarnings("ignore")

url='D:/Work/Automous/Autonomous Code Hub/CodeHUb/purchasing_data_2020.csv'
data_customer=pd.read_csv(url)
data_customer.dtypes
#----------------------------------------------------------------------
#CHANGING TYPE OF COLUMNS
data_customer['order_code'].astype(str)
data_customer['product_code'].astype(str)
data_customer['date_created']=pd.to_datetime(data_customer['date_created'])
print('Done')

#-------------------------------------------------------------------
#OVERVIEWING DATA BY GROUP BY 'COUNTRY'
data_customer.groupby(by=['country'], as_index=False).agg({
    'order_code':'count',
    'units':'sum',
    'amount':'sum'
}).sort_values(by=['amount'], ascending=False)

#-------------------------------------------------------------------
# SELECT SAMPLE FOR RUNNING FIRST LOCATED AT US
retail_us=data_customer[data_customer['country']=='US']
retail_us.groupby(by=['country'], as_index=False).agg({
    'order_code':'count',
    'units':'sum',
    'amount':'sum'
}).sort_values(by=['amount'], ascending=False)
#-------------------------------------------------------------------

#-------------------------------------------------------------------

#-------------------------------------------------------------------

#-------------------------------------------------------------------

#-------------------------------------------------------------------