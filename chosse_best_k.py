from sklearn.datasets import make_blobs                  
from sklearn.cluster import KMeans  
import pandas as pd                                      
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
import os
from tslearn.preprocessing import TimeSeriesScalerMeanVariance, TimeSeriesResampler

symbols = list() 
directory = 'close_price' 
for root, dirs, files in os.walk(directory):
    for filename in files:
        symbols.append(filename)

df = pd.read_csv('close_price/'+ symbols[10])
price = df['price'].values.tolist()
data = np.array([price[:500]])

for i, symbol in enumerate(symbols) :
    if i == 0:
      continue
    df = pd.read_csv('close_price/'+ symbol)
    price = df['price'].values.tolist()
    if (len(price) < 500):
      continue
    price = np.array([price[:500]])
    data = np.concatenate([data,price])
data = TimeSeriesScalerMeanVariance().fit_transform(data)
data = data[:,:,0]
print(data.shape)
print(data)

distortions = []
K = range(1,6)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(data)
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()