"""
Goal - to read csv data of kingfisher strike success and make plots
"""

#import modules
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

fs = 20
data_directory = '../../data/kingfisher/raw_feeding_success.csv'
raw_data = pd.read_csv(data_directory)
masked_data = raw_data.mask(raw_data['Adult'] == 0.5)
separated = masked_data['Success'].groupby(masked_data['Adult'])
percent_success = separated.mean()
percent_success = percent_success.rename(index={0.0: "Juvenile", 1.0: "Adult"})
#plotting
plt.close('all')
fig = plt.figure(figsize=(10,10))
axes = fig.add_subplot(111)
percent_success.plot.bar(color='k', alpha=0.5, rot = 0, fontsize = 0.8*fs)
axes.set_xlabel('')
fig.suptitle('Percent Strike Success', size = 1.5*fs)
plt.show()
out_dir = '../../output/kingfisher/strike_success_age.png'
fig.savefig(out_dir)

# plot of feeding and currents

bins = [-0.21,0.40,1.00,1.60,2.26]
tide_categories = pd.cut(masked_data['Tide height (m)'], bins)
attempts_tide = pd.value_counts(tide_categories)
#masked_data[['Success','Tide height (m)', 'Adult']]
success_tide = pd.concat([tide_categories,  masked_data[['Success', 'Adult']]],axis = 1)
grouped_mean = success_tide.groupby(['Adult','Tide height (m)']).mean()#, as_index=False).mean()
grouped_mean = grouped_mean.rename(index={0.0: "Juvenile", 1.0: "Adult"})
unstacked = grouped_mean.unstack(level = 'Adult')
#plt.close('all')
fig1, ax1 = plt.subplots()
#fig = plt.figure(figsize=(10,10))
#ax = fig.add_subplot(111)
unstacked.plot.bar(rot = 0)
#ax1.set_ylabel('Percent Strike Success')
#fig1.suptitle('Percent Strike Success', size = 1.5*fs)
#ax1.legend(['Juvenile' , 'Adult'])
plt.show()
out_dir = '../../output/kingfisher/strike_success_age_tide.png'
fig1.savefig(out_dir)


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width, label='Men')
rects2 = ax.bar(x + width/2, women_means, width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
