from xlrd import open_workbook #importing xlrd to read excel file
import re #importing regular expression
import csv
import numpy as np
import enchant
from pprint import pprint
excel = open_workbook('Data.xlsx') #Opening excel file
s = excel.sheet_by_index(1) #Selecting the sheet
#Adding Sheet 1 for the first set of data
values = [] #Declaring an empty list
result = {} #Declaring an empty dictionary
d1 = enchant.Dict("en_US")
d2 = enchant.Dict("en_UK")
units= ["cm","mm","m","\"","\'","watt","w","cm2","feet","inch","inches","ft","kg","litre","in","kg/cm2","kg/sq cm","deg","mtrs","v","volts","volt","kw","k","amps","amp","a","sq mtr","hf","fl","l","ltr","c","ml","ltrs","pf","w","gm","wts","v","watts","va","vac","sv","h","vdc","mfd","mv","mh","wb","square mm","ka","sq mm","wt","mtrs","sq mm","mc","watt sq","watt square","sqmm","kv","kva","kgs","st","ohm","k ohm","R","mf","deg c","g","kg cm2","ton","bar","micron","psi","kg/sqcm","lts"]
#Reading data from the PO Short Text
for row in range(1,s.nrows):
    for col in range(3,4):
        cell=s.cell(row,col).value
        values.append(cell)
l=[]
#Reading each sentence from PO Short Text and counting unique word
for i,val in enumerate(values):
    l=re.findall(r"[a-zA-Z0-9-]+",val.lower())
    for j,word in enumerate(l):
        if (d1.check(word)==True or d2.check(word)==True):
		l=re.findall(r"[^0-9-]+",word)
		for j,word in enumerate(l):
			if (len(word)>1 and result.has_key(word)==False):
				result[word]=1
#Reading each sentence from PO Short Text and counting the numerical data
for i,val in enumerate(values):
    for k,u in enumerate(units):
        l=re.findall(r"\d+(?:\.\d+)?(?:\/\d+)?[\ ]?"+u+"+$",val.lower())
        if l:
            for j,word in enumerate(l):
                if ("\"" in word)==True or ("\'" in word):
			t=re.findall(r"\d+(?:\")?(?:\')?",word)
			word=t[0]
                if(result.has_key(word)==False):
                    result[word]=1
row=len(values)
data = []
out = open('output.csv','w')
for i,val in enumerate(result):
	data.append(val)
data = sorted(data)
col=len(data)
output = np.zeros((row,col),dtype='int64')
for i in range(0,row):
    temp = values[i].lower()
    for j in range(0,col):
		if ("\"" in data[j])==True or ("\'" in data[j])==True:
			if(data[j] in temp):
				match=1
			else:
				match=0
		else:
			match=re.search(r"\b"+data[j]+"\\b",temp)
		if bool(match)==True:
			output[i][j]=output[i][j]+1
for i,val in enumerate(values):
	values[i]=val.encode('utf-8').replace(',','').replace(';',' ')
	if("\'" in values[i]):
		values[i] = '"%s"' % values[i]
	else:
		values[i] = "'%s'" % values[i]
final=[]
data.insert(0," ")
final.append(data)
for i in range(0,row):
    t=[]
    t.append(values[i])
    for j in range(0,col):
	t.append(output[i][j])
    final.append(t)
for row in final:
	for column in row:
		out.write('%s,' % column)
	out.write('\n')
out.close()
