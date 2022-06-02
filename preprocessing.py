from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import pandas as pd
import matplotlib.pyplot as plt
import os

symbols = list() 
directory = 'close_price' 
for root, dirs, files in os.walk(directory):
    for filename in files:
        symbols.append(filename)

symbols = symbols[8:13]
for i, symbol in enumerate(symbols) :
    df = pd.read_csv('close_price/'+ symbol)
    price = df['price'].values.tolist()
    plt.subplot(5, 2, 1 + i*2)
    plt.plot(price)
    price_normalize = list(TimeSeriesScalerMeanVariance(mu=0,std=1.).fit_transform([price])[:,:,0][0])
    plt.subplot(5, 2, 2 + i*2)
    plt.plot(price_normalize) 
plt.show()