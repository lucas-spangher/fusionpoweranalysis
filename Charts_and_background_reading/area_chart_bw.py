"""
Author: Scott Vitter
Date: July 11, 2017
Figure: 3x2 figure of fleetwide evolution with varying market entry/ceiling by fusion power plants
Purpose: Remake figure from R using greyscale and texture. 3x2, six case framework
"""

import matplotlib.pyplot as plt
import scipy
import pandas

#Define some lists which will be used for building the 3x2 figure
file_list = ['2030_10_mean.csv', '2030_50_mean.csv', '2050_10_mean.csv', '2050_50_mean.csv', '2070_10_mean.csv', '2070_50_mean.csv'] #file names
caption_list = ['Market entry: 2030, ceiling: 10%','Market entry: 2030, ceiling: 50%','Market entry: 2050, ceiling: 10%','Market entry: 2050, ceiling: 50%','Market entry: 2070, ceiling: 10%','Market entry: 2070, ceiling: 50%'] #captions
title_list = ['CoalGrowth', 'PetroleumGrowth', 'NGCCGrowth', 'NGCTGrowth', 'NGSTGrowth', 'NuclearGrowth', 'HydroGrowth', 'WindGrowth', 'PVGrowth', 'fusionGrowth']#column names
tech_list = ['Coal', 'Petroleum', 'NGCC', 'NGCT', 'NGST', 'Fission', 'Hydropower', 'Wind', 'Solar', 'Fusion'] #tech names for legend
hatch_list = [ "/" , "*" , "-" , "o" , "\\" , "x", "o", "|", ".", "O" ] #list of hatch patterns to use
color_list = ['.05','.15','.25','.35','.45','.55','.65','.75','.85','.95'] #list of colors

#Define empty figure
fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(10,10))
fig.subplots_adjust(wspace=0.3, hspace=0.3, top=0.9, bottom=0.12, left=.1, right=.9) #adjust spacing
axarr = ax.ravel() #ravel ax array into a list

ld = {} #empty dictionary that will store "lines" from matplotlib.  Needed for shared legend creation

#Define an outer loop for each of the six files
for fn, file in enumerate(file_list):
	df = pandas.read_csv(file, index_col=0) #read data

	#define temp variables to add up data needed for stacked area plot
	temp = scipy.zeros_like(df.CoalGrowth)
	data_dict = {}

	#
	for i, tl in enumerate(title_list):
		#print i, tl
		tempdf = getattr(df, tl) #for example, access "df.CoalGrowth" using getattr()
		temp += tempdf.values #add values to temp counter, grow the stack
		temp2 = temp.copy() #make a copy for assignment purposes
		data_dict[i] = temp2 #store to temp dict
		#print temp

	#Plot each level of the data_dict using fill between
	for key, val in sorted(data_dict.iteritems()):
		if key == 0: #for key=0, corresponding to coal, use ax.fill_between() between 0 and data_dict[0]
			ld[key] = axarr[fn].fill_between(scipy.arange(2014,2101), 0, data_dict[0]/1000., linestyle='-',hatch=hatch_list[key], edgecolor='white', color=color_list[key])
		else: #for all other keys, use ax.fill_between() between data_dict[key-1] and data_dict[key]
			ld[key] = axarr[fn].fill_between(scipy.arange(2014,2101), data_dict[key-1]/1000., data_dict[key]/1000., linestyle='-', hatch=hatch_list[key], edgecolor='white', color=color_list[key])

		#plot black lines to help differentiate the shaded areas
		axarr[fn].plot(scipy.arange(2014,2101), data_dict[key]/1000., color='k')

	#set x/y limits, ticks, and lables
	axarr[fn].set_xlim(2012,2102)
	axarr[fn].set_ylim(0,1500)
	axarr[fn].set_xticks([2025,2050,2075,2100])
	axarr[fn].set_xlabel('Year', fontsize=14)
	axarr[fn].set_ylabel('Installed Capacity (GW)', fontsize=14)
	#add cpations about market entry and ceiling
	axarr[fn].text(2015, 1400, caption_list[fn], weight='bold', horizontalalignment='left', verticalalignment='center', fontsize=8)

#Add a single shared legend in five columns at the lower center of the overall plot
fig.legend((ld[0], ld[1], ld[2], ld[3], ld[4], ld[5], ld[6], ld[7], ld[8], ld[9]) , (tech_list[0], tech_list[1], tech_list[2], tech_list[3], tech_list[4], tech_list[5], tech_list[6], tech_list[7], tech_list[8], tech_list[9]), 'lower center', ncol=5, fontsize=12)

#Save the figure to a high quality .png file
fig.savefig('area_chart_11jul_3_2.png', dpi=500, bbox_inches='tight', pad_inches=.2)


"""
Author: Scott Vitter
Date: July 11, 2017
Figure: Single chart EIA Business as usual reference case
Purpose: Remake figure from R using greyscale and texture. EIA Reference case
"""

df = pandas.read_csv('2014_bau.csv', index_col=0)
fig, ax = plt.subplots(1, figsize=(7,4))

title_list = ['CoalGrowth', 'PetroleumGrowth', 'NGCCGrowth', 'NGCTGrowth', 'NGSTGrowth', 'NuclearGrowth', 'HydroGrowth', 'WindGrowth', 'PVGrowth']
tech_list = ['Coal', 'Petroleum', 'NGCC', 'NGCT', 'NGST', 'Fission', 'Hydropower', 'Wind', 'Solar']
hatch_list = ['o', None, '.', None, 'o', None, 'o', None, 'o']
color_list = ['.05','.15','.25','.35','.45','.55','.65','.75','.85']
ld = {} #empty dictionary that will store "lines" from matplotlib.  Needed for shared legend creation

#Define temporary variable and dictionary for summing data for stacked area plot
temp = scipy.zeros_like(df.CoalGrowth)
data_dict = {}

#Loop through the dataframe
for i, tl in enumerate(title_list):
	print i, tl
	tempdf = getattr(df, tl)
	temp += tempdf.values
	temp2 = temp.copy()
	data_dict[i] = temp2
	print temp

for key, val in sorted(data_dict.iteritems()):
	if key == 0:
		ld[key] = ax.fill_between(scipy.arange(2014,2101), 0, data_dict[0]/1000., linestyle='-',hatch=hatch_list[key], edgecolor='white', color=color_list[key], label=tech_list[key])
	else:
		ld[key] = ax.fill_between(scipy.arange(2014,2101), data_dict[key-1]/1000., data_dict[key]/1000., linestyle='-', hatch=hatch_list[key], edgecolor='white', color=color_list[key], label=tech_list[key])

	axarr[fn].plot(scipy.arange(2014,2101), data_dict[key]/1000., color='k')

ax.set_xlim(2012,2102)
ax.set_ylim(0,1700)
ax.set_xticks([2025,2050,2075,2100])
ax.set_xlabel('Year', fontsize=14)
ax.set_ylabel('Installed Capacity (GW)', fontsize=14)

handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc=[1.02, .1], fontsize=14)

