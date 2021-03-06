from sklearn.mixture import GaussianMixture
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from astropy.io import ascii

data1  = pd.read_csv("C:/Users/legion/Astro_Project/data_trumpler15-result.csv", header=0,usecols=[1,2,3,4,5 ])#pmra,pmdec,parallax,ra,dec
#print(data.describe())
ra = np.array(data1['ra'])
dec = np.array(data1['dec'])
parallax = np.array(data1['parallax'])
pmra = np.array(data1['pmra'])
pmdec = np.array(data1['pmdec'])

index = []

for i in range(len(pmra)):
    if -20 <= pmra[i] <= 20 and -20 <= pmdec[i] <= 20 :
        index.append(i)


data1 = data1.iloc[index, :]

plt.figure(figsize=(25,20))
#plt.rcParams.update({'font.size': 25})
#plt.gcf().set_size_inches((10, 8))
plt.xlabel('PMRA(mas/yr)')
plt.ylabel('PMDEC(mas/yr)')
plt.scatter(data1["pmra"],data1["pmdec"])
plt.savefig("GMM_clustering_Before")
plt.show()

scaler = preprocessing.MinMaxScaler()
names = data1.columns
d = scaler.fit_transform(data1)
data = pd.DataFrame(d, columns=names)
data.head()
GM = GaussianMixture(n_components=3 , init_params='random', max_iter=800,tol=1e-6)
GM.fit(data)

print('Converged:',GM.converged_) # Check if the model has converged
means = GM.means_ 
covariances = GM.covariances_


print(GM.predict_proba(data))
print (GM.predict(data))
print (GM.weights_)
print (GM.score(data))
proba = GM.predict_proba(data)


#proba.to_csv('proba.csv', mode = 'w', sep='\t', index=False, header=False)
ascii.write (proba, 'proba.csv',format='tab')


labels = GM.predict(data)
print(labels)
ascii.write (labels, 'predict.csv',format='tab')
frame = pd.DataFrame(data)
frame['cluster'] = labels
frame.columns = [0,1,2,3,4, 'cluster']
frame.to_csv('frame.csv', mode = 'w', sep='\t', index=False, header=False)


color=['blue','green','red']
for k in range(0,3):
    data = frame[frame["cluster"]==k]
    plt.rcParams.update({'font.size': 25})    
    plt.scatter(data[3],data[4],c=color[k], s=3.5)
    plt.gcf().set_size_inches((10, 8)) 
    plt.xlabel("PMRA(mas/yr)")
    plt.ylabel("PMDEC(mas/yr)")
    print("Value of cluster = {} implies color {} ".format(k, color[k]))


plt.savefig("GMM_clustering_After")
plt.show()

