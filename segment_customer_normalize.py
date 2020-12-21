import pandas as pd
import numpy as np
import scipy as sc
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

url='D:/Work/Automous/Autonomous Code Hub/CodeHUb/Data_customer_normalize.csv'
customer_df=pd.read_csv(url)
customer_df[:10]


rank_df=customer_df.rank(method='first')
normalized_df=((rank_df - rank_df.mean())/rank_df.std())[:5000]
normalized_df.describe

# Use silhouette coefficient to determine the best number of clusters
from sklearn.metrics import silhouette_score

for n_cluster in [4,5,6,7,8]:
    kmeans = KMeans(n_clusters=n_cluster).fit(
        normalized_df[['TotalSales', 'OrderCount', 'AvgOrderValue']])
    
    silhouette_avg = silhouette_score(
        normalized_df[['TotalSales', 'OrderCount', 'AvgOrderValue']], 
        kmeans.labels_)
    
    print('Silhouette Score for %i Clusters: %0.4f' % (n_cluster, silhouette_avg))