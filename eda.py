## import some Python modules for handling data and plotting
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

## read in the data file
df = pd.read_csv('MPS Borough Level Crime (most recent 24 months).csv')

## explore the dimensions and columns of the dataset
df.shape
#(1575, 27)

df.head()
#                 crime_group  ... 201911
#0  Arson and Criminal Damage  ...      8
#1  Arson and Criminal Damage  ...     92
#2                   Burglary  ...     30
#3                   Burglary  ...    113
#4              Drug Offences  ...     10
#
#[5 rows x 27 columns]

df.columns
#Index(['MajorText', 'MinorText', 'LookUp_BoroughName', '201712', '201801',
#       '201802', '201803', '201804', '201805', '201806', '201807', '201808',
#       '201809', '201810', '201811', '201812', '201901', '201902', '201903',
#       '201904', '201905', '201906', '201907', '201908', '201909', '201910',
#       '201911'],
#      dtype='object')

## rename my columns
df = df.rename(columns={'MajorText': 'crime_group', 'MinorText': 'crime', 'LookUp_BoroughName': 'boroughs'})

## look at the boroughs we have:
boroughs = df.boroughs.unique()
boroughs
#array(['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley',
#       'Camden', 'Croydon', 'Ealing', 'Enfield', 'Greenwich', 'Hackney',
#       'Hammersmith and Fulham', 'Haringey', 'Harrow', 'Havering',
#       'Hillingdon', 'Hounslow', 'Islington', 'Kensington and Chelsea',
#       'Kingston upon Thames', 'Lambeth', 'Lewisham', 'Merton', 'Newham',
#       'Redbridge', 'Richmond upon Thames', 'Southwark', 'Sutton',
#       'Tower Hamlets', 'Waltham Forest', 'Wandsworth', 'Westminster'],
#      dtype=object)


## look at 1 borough subset
df[df.boroughs == 'Westminster'].iloc[:10,]
#                               crime_group  ... 201911
#1525             Arson and Criminal Damage  ...      8
#1526             Arson and Criminal Damage  ...    147
#1527                              Burglary  ...    247
#1528                              Burglary  ...    196
#1529                         Drug Offences  ...      9
#1530                         Drug Offences  ...    306
#1531  Miscellaneous Crimes Against Society  ...      0
#1532  Miscellaneous Crimes Against Society  ...      0
#1533  Miscellaneous Crimes Against Society  ...      0
#1534  Miscellaneous Crimes Against Society  ...      0


## create a minimised dataset with only the columns we need
temp_df = df.drop(['crime_group', 'crime', '201712', '201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201812'], axis=1)

## create a function that woud give us a single sum for a borough
def add_borough_matrix(input_df):
    col_indx = input_df.shape[1]
    b_sum = 0
    for i in range(1, col_indx):
        b_sum += sum(input_df.iloc[:,i])
        return b_sum


boroughs_crime_count = []
for borough in boroughs:
    b_df = temp_df[temp_df.boroughs == borough]
    b_count = add_borough_matrix(b_df)
    boroughs_crime_count.append(b_count)

df_result = pd.DataFrame({'borough': boroughs, 'crime count': boroughs_crime_count})

## save the result into a CSV file
#df.to_csv('borough_crime_count.csv', index=False, header=True)

## view the first 10 rows we got
df_result.iloc[:10,]
#                borough  crime count
#0  Barking and Dagenham        20042
#1                Barnet        31313
#2                Bexley        17954
#3                 Brent        30481
#4               Bromley        24912
#5                Camden        39394
#6               Croydon        33430
#7                Ealing        31582
#8               Enfield        30219
#9             Greenwich        28705

## plot a histogram
sorted_result = df_result.sort_values(by=['crime count'])
plt.bar(sorted_result.borough, sorted_result['crime count'])
plt.xlabel('Borough')
plt.ylabel('Crime Count')
plt.title('Crime count per borough - 2019')
plt.xticks(rotation=90)
plt.show()

df = df.drop(['crime_group', 'crime', 'boroughs'], axis=1)
df.columns
#Index(['201712', '201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812', '201901', '201902', '201903', '201904', '201905', '201906', '201907', '201908', '201909', '201910', '201911'], dtype='object')

crime_per_month = []
for month in df.columns:
    crime_per_month.append(sum(df[month]))

## plt the result
plt.plot(df.columns, crime_per_month)
plt.xlabel('Month')
plt.ylabel('Crime Count')
plt.title('Crime Count Rate')
plt.xticks(rotation=90)
plt.show()

