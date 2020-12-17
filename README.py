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


# ------------------------------------------------ CONVERTING DATETIME TYPE HAVING UTC ---------
# HARD REMOVING UTC IN DATETIME - S1
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
































