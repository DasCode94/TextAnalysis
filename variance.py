from sklearn import decomposition
import numpy as np
import matplotlib.pyplot as plt
import csv
reader = csv.reader(open('new_output.csv'))
X = np.zeros((11037,2721),dtype='float64')
i=0
for row in reader:
    X[i]=row
    i=i+1
print "done"
ncomps = 1200
svd = decomposition.TruncatedSVD(n_components=ncomps,algorithm='arpack')
svd_fit = svd.fit(X)
Y = svd.fit_transform(X)
out = open('new_result.csv','w')
for row in Y:
	for column in row:
		out.write('%s,' % column)
	out.write('\n')
out.close()
print('Variance preserved by n components == {:.2%}'.format(
        svd_fit.explained_variance_ratio_.cumsum()[-1]))
