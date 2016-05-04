import pandas as pd
import numpy as np
import xlrd

input_file = pd.ExcelFile('RawData.xlsx')
df = pd.read_excel(input_file, 'Raw')
foo = df.ix[df['Value'] < 0]
foo.to_excel('OutputError.xlsx', sheet_name='Errors')

columns = ['Time', 'TimeUnit', 'DCS', 'DCA' , 'DCI']
index = np.arange(1000)
dfo = pd.DataFrame(columns=columns, index=index)
foo1 = df.ix[df['Value'] > 0]
foo1.sort_values('Time', ascending = True)
tempTime = ""
tempDCS =""
tempDCA = ""
tempDCI = ""
rowno=0
for index, row in foo1.iterrows():
    newTime = row['Time']
    if (newTime <> tempTime and index <> 0):
        counter = counter + (tempTime - prevTime)/60
        prevTime=tempTime
        dfo.loc[rowno] = pd.Series({'Time':tempTime, 'TimeUnit':counter, 'DCS':tempDCS, "DCA":tempDCA, "DCI":tempDCI})
        rowno=rowno+1
        tempDCA = ""
        tempDCS = ""
        tempDCI = ""
        tempTime=newTime
      
    if index == 0:
        tempTime=newTime
        prevTime=newTime
        counter = 0
    value = row['Value']
    datacenter = row['Datacenter']
    if (datacenter == 'dc=S'):
        tempDCS=value
    if (datacenter == 'dc=A'):
        tempDCA=value
    if (datacenter == 'dc=I'):
        tempDCI=value
counter=counter+1
dfo.loc[rowno] = pd.Series({'Time':tempTime, 'TimeUnit':counter, 'DCS':tempDCS, "DCA":tempDCA, "DCI":tempDCI})        
dfo.to_excel('OutputNormal.xlsx', sheet_name='Normalized')
