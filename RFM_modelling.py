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
#CALCULATE RECENTLY
recently_df['Recency']=recently_df['LastPurchaseDate'].apply(lambda x:(now - x).days)
recently_df[:10]


#-------------------------------------------------------------------
#DROP LastPurchaseDate by 1
recently_df.drop('LastPurchaseDate',axis=1,inplace=True)

#-------------------------------------------------------------------
#FREQUENCY 
#DROP DUPLICATE CUSTOMER_ID
retail_us_copy=retail_us
retail_us_copy.drop_duplicates(subset=['order_code','customer_id'], keep='first', inplace=True)
#CALCULATE FREQUENCY OF PURCHASES
frequency_df=retail_us_copy.groupby(by=['customer_id'],as_index=False)['order_code'].count()
frequency_df.columns=['customer_id','Frequency']
frequency_df[:10]

#-------------------------------------------------------------------
#NEED TO REVIEW FIRST
retail_us[:10]

#-------------------------------------------------------------------
#CREAT RFM TABLE
#MERGE RECENCY DATAFRAME WITH FREQUENCY DATAFRAME
tem_df = recently_df.merge(frequency_df,on='customer_id')
tem_df[:10]

#-------------------------------------------------------------------
#MERGE WITH MONETARY DATAFRAME TO GET A TABLE WITH HAVING 3 COLUMNS
rfm_df = tem_df.merge(monetary_df,on ='customer_id')
#USE customer_id as index
rfm_df.set_index('customer_id',inplace=True)

#-------------------------------------------------------------------
#RFM QUANTILES
quantiles=rfm_df.quantile(q=[0.5,0.85,0.95])
quantiles

#-------------------------------------------------------------------
#CREATE DICTIONARY
quantiles.to_dict()

#-------------------------------------------------------------------
#CREATION OF RFM SEGMENTS
#ARGUMENTS ( X = VALUES, P = RECENCY , MONETARY_VALUE , FREQUENCY, D = QUARTILES DICT)
def RScore(x,p,d):
    if x <= d[p][0.5]:
        return 4
    elif x <= d[p][0.85]:
        return 3
    elif x <= d[p][0.98]:
        return 2
    else:
        return 1
#ARGUMENS (X = VALUE, P = RECENCY , MONETARY_VALUE, FREQUENCY , K = QUARTILES DICT)
def FScore(x,p,d):
    if x <= d[p][0.5]:
        return 1
    elif x <= d[p][0.85]:
        return 2
    elif x <= d[p][0.98]:
        return 3
    else:
        return 4
print('Done')

#-------------------------------------------------------------------
#CREATE RFM SEGMENTATION TABLE
rfm_segmentation = rfm_df
rfm_segmentation['R_Quartile'] = rfm_segmentation['Recency'].apply(RScore,
                                                                   args=('Recency',quantiles,))
rfm_segmentation['F_Quartile'] = rfm_segmentation['Frequency'].apply(FScore,
                                                                    args = ('Frequency',quantiles,))
rfm_segmentation['M_Quartile'] = rfm_segmentation['Monetary'].apply(FScore,
                                                                   args = ('Monetary',quantiles,))

#-------------------------------------------------------------------
#TEST
rfm_segmentation[:10]

#-------------------------------------------------------------------

#MAKE SCORES
rfm_segmentation['RFMScore'] = rfm_segmentation.R_Quartile.map(str)\
                            + rfm_segmentation.F_Quartile.map(str)\
                            + rfm_segmentation.M_Quartile.map(str)
rfm_segmentation[:10]


#-------------------------------------------------------------------
rfm_segmentation[rfm_segmentation['RFMScore']=='444'].sort_values('Monetary',ascending=False)[:10]
print("Best Customers: ",len(rfm_segmentation[rfm_segmentation['RFMScore']=='444']))
print('Loyal Customers: ',len(rfm_segmentation[rfm_segmentation['F_Quartile']==4]))
print("Big Spenders: ",len(rfm_segmentation[rfm_segmentation['M_Quartile']==4]))
print('Almost Lost: ', len(rfm_segmentation[rfm_segmentation['RFMScore']=='244']))
print('Lost Customers: ',len(rfm_segmentation[rfm_segmentation['RFMScore']=='144']))
print('Lost Cheap Customers: ',len(rfm_segmentation[rfm_segmentation['RFMScore']=='111']))

#-------------------------------------------------------------------
#VISUALLIZE DATA FRAME
test_df=rfm_segmentation.reset_index()
test_view=test_df.groupby(by=['RFMScore'],as_index=False).agg({
    'customer_id':'count',
    'Recency':'mean',
    'Frequency':'mean',
    'Monetary':'sum'
}).sort_values('customer_id', ascending=False)


#-------------------------------------------------------------------
view_df=rfm_segmentation.copy()
#view_df.loc[view_df['RFMScore']=='444' ,'Define_customer'] = 'Best_customer'

#df['Age_group'] = np.where(df.Age<18, 'under 18',
 #                          np.where(df.Age<40,'under 40', '>40'))
view_df['Define_customer']= np.where(view_df.RFMScore == '444', 'Best_customer',
                                    np.where(view_df.F_Quartile==4,'Loyal_customer',
                                            np.where(view_df.M_Quartile==4,'BigSpender_cus',
                                                     np.where(view_df.RFMScore=='244','Alost_lost',
                                                              np.where(view_df.RFMScore=='144','Lost',
                                                                      np.where(view_df.RFMScore=='111','Lost_cheap',
																				np.where(view_df.R_Quartile==4, 'New_customer',
																						np.where( view_df.M_Quartile==4,'Business','Normal'																				
																								)
																						)
																				
                                                                              )
                                                                      )
                                                             )
                                                    )
                                            )
                                    )
view_df_cus[:10]

#-------------------------------------------------------------------
view_df_cus=view_df_cus.groupby(by=['Define_customer'],as_index=False).agg({
    'customer_id':'count'
})

import squarify
squarify.plot(sizes=view_df_cus['customer_id'],
              label=view_df_cus['Define_customer'],
              color=["red","green","blue", "grey","white","yellow"],
              alpha=.4)
plt.axis('off')
plt.show()

#-------------------------------------------------------------------


#-------------------------------------------------------------------


#-------------------------------------------------------------------

#-------------------------------------------------------------------


#-------------------------------------------------------------------



#-------------------------------------------------------------------