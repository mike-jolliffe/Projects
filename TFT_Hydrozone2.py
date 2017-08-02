import numpy as np
import pandas as pd
from pandas import Series,DataFrame

plot_width = 10
temp = 0
area = []
area2 = []
area3 = []
area_final = []


fhandle = raw_input("Please enter the file name: ")
hydro_input = pd.ExcelFile(fhandle)
dframe = hydro_input.parse('Sheet1')
#Block invalid input values.
for i,j in zip(dframe["Hydrozone_Start"],dframe["Hydrozone_End"]):
    if i > j:
        print "Hydrozone Start and End values incorrect."
for i,j in zip(dframe["Plot_Start"],dframe["Plot_End"]):
    if i > j:
        print "Plot Start and End values incorrect."
#Null area for zones that don't overlap
for i,j in zip(dframe["Plot_End"],dframe["Hydrozone_Start"]):
    if i <= j:
        temp = 'Null'
    else:
        temp = 0
    area.append(temp)
for i,j in zip(dframe["Plot_Start"],dframe["Hydrozone_End"]):
    if i >= j:
        temp = 'Null'
    else:
        temp = 0
    area2.append(temp)
#Plot spans the entire hydrozone, so area of hydrozone calculated
for i,j,k,l in zip(dframe["Plot_Start"],dframe["Hydrozone_Start"],
dframe["Plot_End"],dframe["Hydrozone_End"]):
    if i <= j and k >= l:
        temp = (l - j) * plot_width
        area3.append(temp)
#Plot entirely contained within hydrozone
    elif i > j and i <= l:
        if k <= l and k > j:
            temp = (k - i) * plot_width
            area3.append(temp)
#Plot starts within, ends outside, hydrozone
        elif k > l:
            temp = (l - i) * plot_width
            area3.append(temp)
    elif k <= l and k > j:
        temp = (k - j) * plot_width
        area3.append(temp)
    else:
        temp = 0
        area3.append(temp)
#Present the data as a single column.
new_frame = DataFrame([area,area2,area3])
new_new = new_frame.T
for index,row in new_new.iterrows():
    for i in row:
        if i != 0:
            area_final.append(i)
for_append = Series(area_final)
dframe_for_append = DataFrame([for_append])
dframe_for_append = dframe_for_append.transpose()
final_output = dframe.join(dframe_for_append,how='left')
final_output = final_output.rename(columns={0:'Area'})

final_output.to_excel('Hydrozone_dummy_data.xlsx','Areas_Output')
print "Write to file successful."
