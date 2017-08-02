import numpy as np
import pandas as pd
from pandas import Series,DataFrame
sites = pd.ExcelFile('Uplift_heights.xlsx')
dframe = sites.parse('Sheet1')
bins = []
bin_dict = {'x21':[],'x22':[],'x23':[],'x24':[],'x25':[],'x26':[],'x27':[],'x28':[],'x29':[],'x30':[],'x31':[]}
bin_dict_kcals = {'x21':[],'x22':[],'x23':[],'x24':[],'x25':[],'x26':[],'x27':[],'x28':[],'x29':[],'x30':[],'x31':[]}
for i,j,k in zip(dframe['Resto_height'],dframe['Bin #'],dframe['kcals/day']):
    if i <= 5:
        j = 21
        bin_dict['x21'].append(i)
        bin_dict_kcals['x21'].append(k)
    elif i <= 10 and i > 5:
        j = 22
        bin_dict['x22'].append(i)
        bin_dict_kcals['x22'].append(k)
    elif i <= 15 and i > 10:
        j = 23
        bin_dict['x23'].append(i)
        bin_dict_kcals['x23'].append(k)
    elif i <= 20 and i > 15:
        j = 24
        bin_dict['x24'].append(i)
        bin_dict_kcals['x24'].append(k)
    elif i <= 25 and i > 20:
        j = 25
        bin_dict['x25'].append(i)
        bin_dict_kcals['x25'].append(k)
    elif i <= 30 and i > 25:
        j = 26
        bin_dict['x26'].append(i)
        bin_dict_kcals['x26'].append(k)
    elif i <= 35 and i > 30:
        j = 27
        bin_dict['x27'].append(i)
        bin_dict_kcals['x27'].append(k)
    elif i <= 40 and i > 35:
        j = 28
        bin_dict['x28'].append(i)
        bin_dict_kcals['x28'].append(k)
    elif i <= 45 and i > 40:
        j = 29
        bin_dict['x29'].append(i)
        bin_dict_kcals['x29'].append(k)
    elif i <= 50 and i > 45:
        j = 30
        bin_dict['x30'].append(i)
        bin_dict_kcals['x30'].append(k)
    elif i > 50:
        j = 31
        bin_dict['x31'].append(i)
        bin_dict_kcals['x31'].append(k)
    bins.append(j)

new_bins = Series(bins)
ser1 = Series(bin_dict)
ser2 = Series(bin_dict_kcals)
#Create data frame of the bin medians.
med_list = []
for i,j in zip(ser1,ser2):
    med = (np.median(i),np.median(j))
    med_list.append(med)
output = DataFrame(med_list,index=range(1,12),columns=['median height','median uplift'])
frame2 = DataFrame([new_bins])
frame2 = frame2.transpose()
final_output = dframe.join(frame2,how='left')
writer = pd.ExcelWriter('Uplift_heights.xlsx')

final_output.to_excel(writer,'Bin_Values')
output.to_excel(writer,'Bin_Medians')
writer.save()
