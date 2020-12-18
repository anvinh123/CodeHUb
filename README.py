# ------------------------------------------------
# IMPORTING LIBRARY
import pandas as pd
import numpy as np
import scipy as sc
url='D:/Work/Automous/Autonomous Code Hub/CodeHUb/Data_source_v1.csv'
data=pd.read_csv(url)
print(data.head(5))
print('\n')
print(data.dtypes)


# ------------------------------------------------
# OVERVIEWING PRODUCT IN DB

product_amount=data.groupby(by=['product_name'],as_index=False).agg({
    'units':'sum',
    'amount': 'sum',
    'customer_id': 'count'
})
product_amount.sort_values(by=['amount'],ascending=False)[:10]


# ------------------------------------------------ CONVERTING DATETIME TYPE HAVING UTC --------- VER 1
# HARD REMOVING UTC IN DATETIME 
db_datetime['date_created']=db_datetime['date_created'].str.split(" UTC",n = 1, expand=True)

# Look overviewing Shape
db_datetime[:10]

# Convert string into Datetime
db_datetime['date_created']=pd.to_datetime(db_datetime['date_created'])
d=0
for i in range(db_datetime.shape[0]):
	a=db_datetime.iloc[i,2].date()
    db_datetime.iloc[i,2]=a
    i=i+1
    d=d+1
	
# ------------------------------------------------ CONVERTING DATETIME TYPE HAVING UTC --------- VER 2
#CONFIG DATA SOURCE
db_datetime=data
db_datetime['date_created']=pd.to_datetime(db_dtime['date_created'])
db_dtime['year']=pd.DatetimeIndex(db_dtime['date_created']).year
db_dtime['month']=pd.DatetimeIndex(db_dtime['date_created']).month
db_dtime['date']=pd.DatetimeIndex(db_dtime['date_created']).date
db_dtime['date']=pd.DatetimeIndex(db_dtime['date_created']).day

# ----------------------------------------- SORT DATETIME ----------------------
db_amount=db_datetime.groupby(by=['date_created'],as_index=False).agg({
    'customer_id': 'count',
    'order_id': 'count',
    'units': 'sum',
    'amount': 'sum'
})
db_amount[:10].sort_values(by='date_created',ascending=True)

db_amount['aov']=round(db_amount['amount']/db_amount['order_id'],2)
db_amount['avg_item']= round(db_amount['units']/db_amount['order_id'],2)
db_amount['amount']=db_amount['amount'].map('{:,.2f}'.format)
db_amount[:10]


# ------------------------------------- MULTIPLES FILTERS -----------------------------------
fill=['1','440','631','555']
db_amount[['date_created','customer_id','amount','units']][db_amount.customer_id.isin(fill)]























