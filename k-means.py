from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import csv
reader = csv.reader(open('new_result.csv'))
X = np.zeros((11037,1200),dtype='float64')
i=0
for row in reader:
    X[i]=row[0:-1]
    i=i+1
print "done"
kmeans = KMeans(n_clusters=7,random_state=0).fit(X)
centers = kmeans.cluster_centers_
labels = kmeans.predict(X)
color=["#1c369c","#5f0778","#ffb900","#0e8a2a","#b50c52",#a6e60e","#80e2dc"]
plt.title("K-means Clustering")
for i in range(len(X)):
    plt.scatter(X[i][0],X[i][1],c=color[labels[i]])
plt.scatter(centers[:,0], centers[:,1], marker="x",c=color)
plt.show()
