import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import os
from os import listdir
from datetime import datetime

def transform_data():
  # IMPORT FILES
  filelist = os.listdir()
  files = []
  for i in filelist:
    if i.endswith('.csv'):
      files.append(i)
    if i.endswith('.xlsx'):
      files.append(i)

  #Transforming the file for Contact history
  for i in files:
    print(i)
    if i == 'Contact History Report (All) (5).xlsx':
      df_CH = pd.read_excel(i,header= None)
    if i == 'Trail Analysis Report (2).csv':
      df_TA = pd.read_csv(i)
  
  #convert the contact history file to readable format
  Attendee01 = []
  Attendee02 = []
  Start_Time = []
  End_Time = []
  Duration= []
  new_dict = {'Attendee01': Attendee01,'Attendee02': Attendee02,'Start Time': Start_Time,'End Time': End_Time,'Duration': Duration}

  for i in range(len(df_CH.index)):
    if df_CH.iloc[i][0] == "No":
      j = 1
      while type(df_CH.iloc[i+j][0]) == int and df_CH.iloc[i+j][0] != np.nan:
        if i+j  == df_CH.index[-1]: 
          Attendee01.append(df_CH.iloc[i-1][0])
          Attendee02.append(df_CH.iloc[i+j][1])
          Start_Time.append(df_CH.iloc[i+j][2])
          End_Time.append(df_CH.iloc[i+j][3])
          Duration.append(df_CH.iloc[i+j][4])
          j += 1
          break
        else: 
          Attendee01.append(df_CH.iloc[i-1][0])
          Attendee02.append(df_CH.iloc[i+j][1])
          Start_Time.append(df_CH.iloc[i+j][2])
          End_Time.append(df_CH.iloc[i+j][3])
          Duration.append(df_CH.iloc[i+j][4])
          j += 1

  df = pd.DataFrame.from_dict(new_dict)
  df.head(30)

  #Save as a CSV
  df.to_csv(r'Transformed Contact History.csv')
    
  #create a list to separate the dates
  new_list = []
  for i in range(len(df)):
    if '20/05/2021' in df.iloc[i]['Start Time']:
      new_list.append(df.iloc[i]['Start Time'])

  # DF for events from 20/05/2021
  df_day1 = df.loc[df['Start Time'].isin(new_list)]
  df_day1.reset_index(inplace =True)
  print(df_day1)

  # # DF for events from 25 March
  # df_day2 = df[~df['Start Time'].isin(new_list)]
  # df_day2.reset_index(inplace =True)
  # print(df_day2)


  # Find the accumulated duration between 2 attendees per day for 24 March
  print(df_day1.nunique())
  name_dict = {}
  for i, row in df_day1.iterrows():
    duration = row['Duration']
    name = (row["Attendee01"], row["Attendee02"])
    if name not in name_dict:
      name_dict[name] = duration
    else:
      name_dict[name] += duration

  df_accumulated_day1 = pd.Series(name_dict).rename_axis(['Attendee01', 'Attendee02']).reset_index(name='Accumulated duration')
  df_accumulated_day1.reset_index(inplace = True)
  cut_level = ['TRANSIENT', "NORMAL", 'CLOSE']
  cut_bins =[0, 4, 14, 10000] 
  df_accumulated_day1['Contact Category'] = pd.cut(df_accumulated_day1['Accumulated duration'], bins=cut_bins, labels = cut_level)
  print(df_accumulated_day1)

  #0-4 is transient, 5-14 is normal, 15>=  close
  cut_level = ['TRANSIENT', "NORMAL", 'CLOSE']
  cut_bins =[0, 4, 14, 10000] 
  df_accumulated_day1['Contact Category'] = pd.cut(df_accumulated_day1['Accumulated duration'], bins=cut_bins, labels = cut_level)
  print(df_accumulated_day1)

  #save it as a CSV
  df_accumulated_day1.to_csv(r'Accumulated duration Contact History(20May).csv',index = False)


  #To remove the duplicates
  dup_list=[]
  list1 =[]
  for i, row in df_accumulated_day1.iterrows():
    list2 = [df_accumulated_day1.loc[i, "Attendee01"],df_accumulated_day1.loc[i, "Attendee02"]]
    if list2[::-1] not in list1:
      list1.append(list2)
    else: 
      dup_list.append((df_accumulated_day1.loc[i,"index"]))


  df_accumulated_day1_dup_removed = df_accumulated_day1[~df_accumulated_day1['index'].isin(dup_list)]

  #0-4 is transient, 5-14 is normal, 15>=  close
  cut_level = ['TRANSIENT', "NORMAL", 'CLOSE']
  cut_bins =[0, 4, 14, 10000] 
  df_accumulated_day1_dup_removed['Contact Category'] = pd.cut(df_accumulated_day1_dup_removed['Accumulated duration'], bins=cut_bins, labels = cut_level)
  print(df_accumulated_day1_dup_removed)

  #Save as a CSV
  df_accumulated_day1_dup_removed.to_csv(r'Accumulated duration+remove duplicates Contact History(20 May).csv',index = False)

  # # Find the accumulated duration between 2 attendees per day for 25 March
  # print(df_day2.nunique())
  # name_dict = {}
  # for i, row in df_day2.iterrows():
  #   duration = row['Duration']
  #   name = (row["Attendee01"], row["Attendee02"])
  #   if name not in name_dict:
  #     name_dict[name] = duration
  #   else:
  #     name_dict[name] += duration

  # df_accumulated_day2 = pd.Series(name_dict).rename_axis(['Attendee01', 'Attendee02']).reset_index(name='Accumulated duration')
  # df_accumulated_day2.reset_index(inplace = True)
  # print(df_accumulated_day2)

  # cut_level = ['TRANSIENT', "NORMAL", 'CLOSE']
  # cut_bins =[0, 4, 14, 10000] 
  # df_accumulated_day2['Contact Category'] = pd.cut(df_accumulated_day2['Accumulated duration'], bins=cut_bins, labels = cut_level)

  # #Save as CSV
  # df_accumulated_day2.to_csv(r'Accumulated duration Contact History(25).csv',index = False)

  # # Remove duplicates
  # dup_list=[]
  # list1 =[]
  # for i, row in df_accumulated_day2.iterrows():
  #   list2 = [df_accumulated_day2.loc[i, "Attendee01"],df_accumulated_day2.loc[i, "Attendee02"]]
  #   if list2[::-1] not in list1:
  #     list1.append(list2)
  #   else: 
  #     dup_list.append((df_accumulated_day2.loc[i,"index"]))

  # df_accumulated_day2_dup_removed = df_accumulated_day2[~df_accumulated_day2['index'].isin(dup_list)]

  # cut_level = ['TRANSIENT', "NORMAL", 'CLOSE']
  # cut_bins =[0, 4, 14, 10000] 
  # # cut_bins =[8000, 9000, 10000, 11000,12000,13000,14000,15000,16000,17000,18000]
  # df_accumulated_day2_dup_removed['Contact Category'] = pd.cut(df_accumulated_day2_dup_removed['Accumulated duration'], bins=cut_bins, labels = cut_level)
  # print(df_accumulated_day2_dup_removed)

  # #Save file as CSV
  # df_accumulated_day2_dup_removed.to_csv(r'Accumulated duration+remove duplicates Contact History(25).csv',index = False)



  #Convert the timing of Trail Analysis to a standard timing
  # def convert_dates(Time):
  #   if Time  == np.nan:
  #     return Time
  #   if Date1 in str(Time):
  #     if str(Time[-2:]) == 'AM':
  #       New_Time = format01 + " " + str(Time[-8:-3])
  #       return (New_Time)
  #     elif Time[-2:] == 'PM':
  #       if int(Time[-8:-6]) == 12:
  #         New_Time1  =  format01 + " " + '12' + ':' + str(Time[-5:-3])
  #         return (New_Time1)
  #       elif 10 <= int(Time[-8:-6]) < 12:
  #         Start_Time = int(Time[-8:-6]) + 12
  #         Start_Time = str(Start_Time)
  #         New_Time2  = format01 + " " + str(Start_Time) + ':' + str(Time[-5:-3])
  #         return (New_Time2)
  #       elif int(Time[-8:-6]) <10:
  #         Start_Time = int(Time[-7]) + 12
  #         Start_Time = str(Start_Time)
  #         New_Time3  = format01 + " " + str(Start_Time) + ':' + str(Time[-5:-3])
  #         return (New_Time3)
  #   if Date2 in str(Time):
  #     if Time[-2:] == 'AM':
  #       New_Time4= format02 + " " + Time[-8:-3]
  #       return (New_Time4)
  #     elif Time[-2:] == 'PM':
  #       if str(Time[-8:-6]) == '12':
  #         New_Time5  = format02 + " " + '12' + ':' + str(Time[-5:-3])
  #         return (New_Time5)
  #       elif 10 <= int(Time[-8:-6]) < 12:
  #         Start_Time = int(Time[-8:-6]) + 12
  #         Start_Time = str(Start_Time)
  #         New_Time6  = format02 + " " + str(Start_Time) + ':' + str(Time[-5:-3])
  #         return (New_Time6)
  #       elif int(Time[-8:-6]) <10:
  #         Start_Time = int(Time[-7]) + 12
  #         Start_Time = str(Start_Time)
  #         New_Time7 = format02 + " " + str(Start_Time) + ':' +str(Time[-5:-3])
  #         return (New_Time7)


  # Date1 = 'March 24'
  # format01 = '2021-03-24'
  # Date2 = 'March 23'
  # format02 = '2021-03-23'

  # df_TA["Start Time"] = pd.DataFrame(df_TA["Start Time"].apply(convert_dates))
  # df_TA["End Time"] = pd.DataFrame(df_TA["End Time"].apply(convert_dates))


  # for index, row in df_TA.iterrows():
  #   starttime = row['Start Time'] 
  #   yyyymmdd = starttime[6:10] + "-" + starttime[3:5] + "-" + starttime[:2]
  #   start_time = yyyymmdd + ' ' + starttime[-5:]
  #   endtime = row['Start Time'] 
  #   yyyymmdd = endtime[6:10] + "-" + endtime[3:5] + "-" + endtime[:2]
  #   end_time = yyyymmdd + ' ' + endtime[-5:]
  #   dt1 = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
  #   dt2 = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
  #   st = int(dt1.timestamp() * 1000)
  #   et = dt2.timestamp() * 1000
  #   df_TA.loc[index, 'Start Time'] = int(st)
  #   df_TA.loc[index, 'End Time'] = int(et)




  # print(df_TA.head(10))
  # df_TA.to_csv(r'Cleaned_Trail_Analysis.csv')

