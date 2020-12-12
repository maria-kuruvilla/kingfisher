"""
Goal - to read csv data of kingfisher strike success as a function of tide and make plots
"""

#import modules
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

################# tide success #####################
fs = 14
data_directory = '../../data/kingfisher/raw_feeding_success.csv'
raw_data = pd.read_csv(data_directory)
masked_data = raw_data.mask(raw_data['Adult'] == 0.5)
#bins = [-0.20,0.40,1.00,1.60,2.26]
bins = [-0.22,0.40,1.00,1.60,2.26]

tide_categories = pd.cut(masked_data['Tide height (m)'], bins)
attempts_tide = pd.value_counts(tide_categories)
success_tide = pd.concat([tide_categories,  masked_data[['Success', 'Adult']]],axis = 1)
grouped_mean = success_tide.groupby(['Adult','Tide height (m)']).mean()#, as_index=False).mean()
grouped_mean = grouped_mean.rename(index={0.0: "Juvenile", 1.0: "Adult"})
unstacked = grouped_mean.unstack(level = 'Adult')
'''
plt.close('all')
fig = plt.figure(figsize=(10,10))
axes = fig.add_subplot(111)
unstacked.axes.bar(rot = 0)
axes.set_ylabel('Percent Strike Success')
plt.show()
out_dir = '../../output/kingfisher/strike_success_age_tide.png'
fig.savefig(out_dir)
'''
labels = unstacked.index
fig, ax = plt.subplots()
x = np.arange(len(labels))
width = 0.35
ax.bar(x - width/2, unstacked['Success']['Juvenile']*100, width, label = 'Juvenile', color = 'whitesmoke', edgecolor = 'black', linewidth = 0.5 )
ax.bar(x + width/2, unstacked['Success']['Adult']*100, width, label = 'Adult', color = 'gray', edgecolor = 'black', linewidth = 0.5 )
ax.set_ylabel('Percent Strike Success', fontsize = fs)
ax.set_xlabel('Tide height (m)', fontsize = fs)
#ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.show()
out_dir = '../../output/kingfisher/figure1b.jpg'
fig.savefig(out_dir,dpi=600)

#Observation times

current_obs_time = [780,141,512] #minutes for flood, slack, ebb
tide_obs_time = [421,252,355,464] #minutes for low to high


########### current attempt ###############


current = masked_data[['Current Category','Adult','Success']].groupby(['Current Category','Adult']).count().unstack().rename(columns={0.0: "Juvenile", 1.0: "Adult"})
current = current.loc[["ebb", "slack", "flood"]]
labels = current.index
fig, ax = plt.subplots()
x = np.arange(len(labels))
width = 0.35
ax.bar(x - width/2, current['Success']['Juvenile']*60/current_obs_time, width, label = 'Juvenile', color = 'whitesmoke', edgecolor = 'black', linewidth = 0.5 ) #multiply by 60 mins/hr and divide by minutes of obs
ax.bar(x + width/2, current['Success']['Adult']*60/current_obs_time, width, label = 'Adult', color = 'gray', edgecolor = 'black', linewidth = 0.5 )
ax.set_ylabel('Attempts per hour', fontsize = fs)
ax.set_xlabel('Current', fontsize = fs)
#ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.show()
out_dir = '../../output/kingfisher/strike_success_age_current_attempts.png'
fig.savefig(out_dir)


################# tide attempt ############

tide = success_tide[['Tide height (m)','Adult', 'Success']].groupby(['Tide height (m)','Adult']).count().unstack().rename(columns={0.0: "Juvenile", 1.0: "Adult"})
labels = tide.index
fig, ax = plt.subplots()
x = np.arange(len(labels))
width = 0.35
ax.bar(x - width/2, tide['Success']['Juvenile']*60/tide_obs_time, width, label = 'Juvenile', color = 'whitesmoke', edgecolor = 'black', linewidth = 0.5 ) #multiply by 60 mins/hr and divide by minutes of obs
ax.bar(x + width/2, tide['Success']['Adult']*60/tide_obs_time, width, label = 'Adult', color = 'gray', edgecolor = 'black', linewidth = 0.5 )
ax.set_ylabel('Attempts per hour', fontsize = fs)
ax.set_xlabel('Tide height (m)', fontsize = fs)
#ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.show()
out_dir = '../../output/kingfisher/figure1a.jpg'
fig.savefig(out_dir,dpi=600)

############### current success ###################

current_success = masked_data[['Current Category','Adult','Success']].groupby(['Current Category','Adult']).mean().unstack().rename(columns={0.0: "Juvenile", 1.0: "Adult"})

labels = current_success.index
fig, ax = plt.subplots()
x = np.arange(len(labels))
width = 0.35
ax.bar(x - width/2, current_success['Success']['Juvenile']*100, width, label = 'Juvenile', color = 'whitesmoke', edgecolor = 'black', linewidth = 0.5 )
ax.bar(x + width/2, current_success['Success']['Adult']*100, width, label = 'Adult', color = 'gray', edgecolor = 'black', linewidth = 0.5 )
ax.set_ylabel('Percent Strike Success', fontsize = fs)
ax.set_xlabel('Current', fontsize = fs)
#ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.show()
out_dir = '../../output/kingfisher/strike_success_age_current.png'
fig.savefig(out_dir)
