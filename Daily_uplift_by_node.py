import numpy as np
import pandas as pd
from pandas import Series, DataFrame
raw = pd.ExcelFile('solar_loading_multiple_months.xlsx')
dframe1 = raw.parse('ccc_flux')
dframe2 = raw.parse('ntp_flux')
result1 = dframe1.groupby(['Month','Day']).mean()
result2 = dframe2.groupby(['Month','Day']).mean()
writer = pd.ExcelWriter('solar_loading_multiple_months.xlsx')
dframe1.to_excel(writer,'ccc_flux')
dframe2.to_excel(writer,'ntp_flux')
result1.to_excel(writer,'ccc_daily_avgs')
result2.to_excel(writer,'ntp_daily_avgs')
writer.save()
