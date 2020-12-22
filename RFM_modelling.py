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
#CHECK NULL OR ZERO IN customer_id
retail_us[retail_us.customer_id=='']
retail_us[retail_us.customer_id=='0']

#-------------------------------------------------------------------
#SUMMARIZE retail_us
print('Summarize')
print('Number of order_code',retail_us['order_code'].nunique())
print('Number of product_code',retail_us['product_code'].nunique())
print('Number of cates', retail_us['cate_name'].nunique())
print('Number of customer_id',retail_us['customer_id'].nunique())
print('Sum of Units', retail_us['units'].sum())
print('Sum of Amount',retail_us['amount'].sum())

#-------------------------------------------------------------------
#RFM ANALYSIS
print('date_created with MAX',retail_us['date_created'].max())
now=dt.date(2020,12,21)
print(now)
retail_us['date_created']=pd.DatetimeIndex(retail_us['date_created']).date
display(retail_us[:10])

#-------------------------------------------------------------------
#SET RECENTLY BY customer_id AND CHECK LAST DATE OF PURCHASING
recently_df=retail_us.groupby(by='customer_id',as_index=False)['date_created'].max()
recently_df.columns=['customer_id','LastPurchaseDate']
recently_df.head(10)

#-------------------------------------------------------------------