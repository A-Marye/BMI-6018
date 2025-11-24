# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 09:47:55 2021

@author: u6026797
"""
#%% libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%% data

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
covid_df = pd.read_csv(url, index_col=0)

#%% Instructions
'''
Overall instructions:
As described in the homework description, each graphic you make must:
   1. Have a thoughtful title
   2. Have clearly labelled axes 
   3. Be legible
   4. Not be a pie chart
I should be able to run your .py file and recreate the graphics without error.
As per usual, any helper variables or columns you create should be thoughtfully
named.
'''

#%% viz 1
'''
Create a visualization that shows all of the counties in Utah as a time series,
similar to the one shown in slide 22 during the lecture. The graphic should
-Show cases over time
-Have all counties plotted in a background color (something like grey)
-Have a single county plotted in a contrasting color (something not grey)
-Have well formatted dates as the X axis
'''
# Filter df and make it long form 
q1 = covid_df[covid_df['Province_State'] == 'Utah']
id_vars = ['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State','Country_Region', 'Lat', 'Long_', 'Combined_Key']
value_vars = q1.columns.difference(id_vars)
q1_long = pd.melt(
    q1,
    id_vars=id_vars,
    value_vars=value_vars,
    var_name='Date',          
    value_name='Confirmed_Cases' 
)
q1_long['Date'] = pd.to_datetime(q1_long['Date'], format='%m/%d/%y')
q1_long['Confirmed_Cases'] = pd.to_numeric(q1_long['Confirmed_Cases'], errors='coerce').fillna(0).astype(int)

# Define county
highlight_county = 'Utah' 
default_color = 'gray'
highlight_color = 'red'
county_names = q1_long['Admin2'].unique()

# Create the custom colors
county_colors = {}
for county in county_names:
    if county == highlight_county:
        county_colors[county] = highlight_color
    else:
        county_colors[county] = default_color

# Get date for label
q1_highlight = q1_long[q1_long['Admin2'] == highlight_county]
date = q1_highlight.loc[q1_highlight['Date'].idxmax()]['Date']

# Plot 
sns.set(style='whitegrid')
sns.lineplot(
        x='Date',
        y='Confirmed_Cases',
        hue='Admin2',    
        data=q1_long,
        linewidth=2.5,
        palette=county_colors,  
        legend=False
    )
plt.text(
    x=date,
    y=250000,
    s=f' {highlight_county}'
)
plt.title(
        'Confirmed Cases Over Time by County', 
        fontsize=16, 
        fontweight='bold', 
        pad=20
    )
plt.xlabel('Date', fontsize=12, labelpad=15)
plt.ylabel('Confirmed Cases', fontsize=12, labelpad=15)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()   
plt.show()

#%% viz 2
'''
Create a visualization that shows the contrast between the county in Utah with
the most cases to date to a county in Florida with the most cases to date.
The graphic should:
-Have only two counties plotted
-Highlight the difference between the two comparison counties
You may use any style of graphic you like as long as it is effective (dense)
and readable
'''
# Get FL data
FL = covid_df[covid_df['Province_State'] == 'Florida']
FL_max_case_county = FL.loc[FL['3/9/23'].idxmax()]['Admin2']
FL_max_case_number = FL.loc[FL['3/9/23'].idxmax()]['3/9/23']

# Get UT data
UT = covid_df[covid_df['Province_State'] == 'Utah']
UT_max_case_county = UT.loc[UT['3/9/23'].idxmax()]['Admin2']
UT_max_case_number = UT.loc[UT['3/9/23'].idxmax()]['3/9/23']

# Create bar plot data frame
q2 = {'County': [FL_max_case_county, UT_max_case_county],
     'Case Count': [FL_max_case_number, UT_max_case_number]}

# Bar plot
sns.set(style='whitegrid')
plt.bar(
    x=q2['County'], 
    height=q2['Case Count'], 
    color=['#4CAF50', '#2196F3'] 
)
plt.xlabel('County', fontsize=12)
plt.ylabel('Case Count (mil)', fontsize=12)
plt.title('Counties with Highest Case Counts (Florida vs. Utah)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

#%% viz 3
'''
Create a visualization that shows BOTH the running total of cases for a single
county AND the daily new cases. The graphic should:
-Use two y-axes (https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html)
-Use color to contrast the two series being plotted
-Have well formatted dates as the X axis
'''
# Sort old dataframe by date
q1_long.sort_values(by=['Admin2', 'Date'], inplace=True)
q1_long['New_Cases'] = q1_long.groupby('Admin2')['Confirmed_Cases'].diff().fillna(0).astype(int)

# Create new filtered dataframe
q3 = q1_long[q1_long['Admin2'] == 'Utah']

# Plot
sns.set(style='whitegrid')

fig, ax1 = plt.subplots()

sns.lineplot(
        x='Date',
        y='Confirmed_Cases',
        data=q3,
        linewidth=2.5, 
        legend=False,
        color = 'red'
    )

ax1.set_xlabel('Date', fontsize=12, labelpad=15)
ax1.set_ylabel('Cumulative Cases', fontsize=12, labelpad=15)

ax2 = ax1.twinx()
sns.lineplot(
        x='Date',
        y='New_Cases',
        data=q3,
        linewidth=2.5, 
        legend=False,
        color = 'blue'
    )
ax2.set_ylabel('New Cases', fontsize=12, labelpad=15)

plt.title(
        f'Cumulative vs. Daily New Cases (Utah County)', 
        fontsize=16, 
        fontweight='bold', 
        pad=20
    )

plt.xticks(rotation=45, ha='right')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
fig.tight_layout()   
plt.show()

#%% viz 4
'''
Create a visualization that shows a stacked bar chart of county contributions
to a given state's total cases. You may choose any state (or states).
(https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py)
The graphic should:
-Have a single column delineate a state
-Have each 'slice' or column compontent represent a county
'''
# Get new filtered dataframe
q4 = covid_df[covid_df['Province_State'].isin(['Utah', 'Colorado', 'New Mexico', 'Arizona', 'Idaho',  'Wyoming', 'Montana', 'Texas'])]

# Reformat dataframe to long form
id_vars = ['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State','Country_Region', 'Lat', 'Long_', 'Combined_Key']
value_vars = q4.columns.difference(id_vars)
q4_long = pd.melt(
    q4,
    id_vars=id_vars,
    value_vars=value_vars,
    var_name='Date',          # The new column that holds the old date headers
    value_name='Confirmed_Cases'  # The new column that holds the numerical values
)
q4_long['Date'] = pd.to_datetime(q4_long['Date'], format='%m/%d/%y')
q4_long['Confirmed_Cases'] = pd.to_numeric(q4_long['Confirmed_Cases'], errors='coerce').fillna(0).astype(int)
latest_date = q4_long['Date'].max()
q4_long = q4_long[q4_long['Date'] == latest_date]

# Get county and state counts into table
aggregated_df = q4_long.groupby(['Province_State', 'Admin2'])['Confirmed_Cases'].sum().reset_index()
aggregated_df.rename(columns={'Confirmed_Cases': 'County_Cases'}, inplace=True)

state_totals = aggregated_df.groupby('Province_State')['County_Cases'].sum().reset_index()
state_totals.rename(columns={'County_Cases': 'State_Total'}, inplace=True)

q4_merged = pd.merge(aggregated_df, state_totals, on='Province_State')

q4_pivot = q4_merged.pivot_table(
        index='Province_State',
        columns='Admin2',
        values='County_Cases',
        fill_value=0 # Counties not in a state will have 0% contribution
    )

# Plot
fig, ax = plt.subplots()

q4_pivot.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        colormap='tab20',
        edgecolor='white',
        legend=False
    )

ax.set_title(
        'County Contribution to Total Confirmed Cases by State',
        fontsize=16,
        pad=15
    )
ax.set_xlabel('County Case Total', fontsize=12)
ax.set_ylabel('State', fontsize=12)

plt.tight_layout()
plt.show()

#%% extra credit (5 points)
'''
Use Seaborn to create a grouped box plot of all reported states. Each boxplot
should be a distinct state. Have the states ordered from most cases (FL) to fewest 
cases. (https://seaborn.pydata.org/examples/grouped_boxplot.html)
'''
