import pandas as pd

from sklearn import preprocessing
from sklearn.cluster import KMeans

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from matplotlib.pyplot import figure

import networkx as nx
from pyvis.network import Network


import os
from os import listdir

import re 
import string

from datetime import datetime

def analyze_data():
  # IMPORT FILES
  filelist = os.listdir()
  files = []
  for i in filelist:
    if i.endswith('.csv'):
      files.append(i)
  print(files)

  for i in files:
    print(i)
    #contact history file
    if i == 'Accumulated duration Contact History(20May).csv':
      df2 = pd.read_csv(i)
    #trail analysis file
    if i == 'Trail Analysis Report (2).csv' :
      df_TA = pd.read_csv(i)
    #Event Attendance
    if i == 'Event Attendance for (Thu May 20 2021).csv':
      df_EA = pd.read_csv(i)
    #Unauthorised Contact
    if i =='Unauthorized Contact for (Tue Jun 01 2021).csv':
      df_UC = pd.read_csv(i)
    #At Risk User
    if i == 'At Risk user for Thu May 20 2021.csv':
      df_HighRisk = pd.read_csv(i)
    #Cleaned Contact History(w/o accumulating the sum of the duration)
    if i =='Transformed Contact History.csv':
      df_transformed_CH = pd.read_csv(i)








  #Count the number of attendees in each category
  passengerList = df2['Attendee01'].unique().tolist()
  contactDict = {}
  for passenger in passengerList:
    contactDict[passenger] = [0,0,0]
  for index, row in df2.iterrows():
    if row['Contact Category'] == 'TRANSIENT':
      contactDict[row['Attendee01']][0] += 1  
    if row['Contact Category'] == 'NORMAL':
      contactDict[row['Attendee01']][1] += 1
    if row['Contact Category'] == 'CLOSE':
      contactDict[row['Attendee01']][2] += 1
  contactCountDF = pd.DataFrame.from_dict(contactDict, orient='index', columns=['Transient', 'Normal', 'Close'])
  print("Number of Contacts by Type:")
  print(contactCountDF.describe())



  # df2['Accumulated duration'] = np.array(df2['Accumulated duration']).astype(np.int64)

  df2col = df2[['Contact Category', 'Accumulated duration']].copy()
  #theres no transient(uncomment this if theres transient)
  # df2TC = df2col.loc[df2["Contact Category"] == "TRANSIENT"]
  df2NC = df2col.loc[df2["Contact Category"] == "NORMAL"]
  df2CC = df2col.loc[df2["Contact Category"] == "CLOSE"]

  # PLOT HISTOGRAM
  plt.figure(figsize=(20, 10), dpi= 120)
  plt.rc('font', size= 15)
  plt.rc('axes', labelsize= 30)
  # df2CC["Accumulated duration"].hist(bins = 100, color= 'red')
  ax=df2CC["Accumulated duration"].hist(bins = 100, range=(0,300), color= 'red')
  plt.xlabel('Duration (min)')
  plt.ylabel('Counts')
  # plt.xlim((15,300))
  plt.title('Number of Close Contact',fontsize=30)
  # plt.xticks(size=10)
  # plt.yticks(size=10)
  ## For annotating the histogram
  # for p in ax.patches: 
  #   ax.annotate(np.round(p.get_height(),decimals=2),(p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 10),textcoords='offset points',fontsize=10)
  plt.savefig('CC.png')
  # plt.show()


  plt.figure(figsize=(20, 10), dpi= 120)
  ax = df2NC["Accumulated duration"].hist(bins = 50, color= 'orange')
  # range=(0,300)
  plt.xlabel('Duration (min)')
  plt.ylabel('Counts')
  plt.xlim((5,15))
  plt.title('')
  plt.title('Number of Normal Contact',fontsize=30)
  # plt.xticks(size=10)
  # plt.yticks(size=10)
  ##For annotating the historgram
  # for p in ax.patches: 
  #   ax.annotate(np.round(p.get_height(),decimals=2),(p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 10),textcoords='offset points',fontsize=10)
  plt.savefig('NC.png')
  # plt.show()

  #no Transient contact for event
  # plt.figure(figsize=(20, 10), dpi= 120)
  # df2TC["Accumulated duration"].hist(bins = 5, color= 'green')
  # # range=(0,300)
  # plt.xlabel('Duration (min)')
  # plt.ylabel('Counts')
  # plt.xlim((0,5))

  # plt.savefig('TC.png')
  # plt.show()

  # PLOT SCATTERPLOT OF CONSOLIDATED CONTACTS REGARDLESS OF CONTACT TYPE
  # log accumulated duration
  df2log = pd.DataFrame(np.log10(df2['Accumulated duration']))
  # cut time into bins for counting
  dfbin = pd.cut(df2log['Accumulated duration'], bins=100)
  # dfbin = pd.cut(df2['Accumulated duration'], bins=100)


  dfbin.value_counts()
  dfbinn = pd.DataFrame(dfbin.value_counts())
  dfbinn.reset_index(inplace=True)




  #set column to be max of each bin value (bin 1 = 0-15: MAX = 15)
  maxList = []
  for index, row in dfbinn.iterrows(): 
    split = str(row['index']).split(",")
    max = float(split[-1].strip(' ]'))
    maxList.append(max)
  dfbinn['Max'] = maxList
  ###########################################
  # INITIAL PLOT
  plt.scatter(dfbinn['Max'], dfbinn['Accumulated duration'])
  plt.labelsize = "medium"

  plt.xlabel('Time')
  plt.ylabel('Counts')
  plt.title('Initial scatter plot')
  # plt.show()

  # kmeans clustering
  k = dfbinn.copy()
  k.drop('index', axis='columns', inplace=True)

  # from elbow method, 3 was the optimal group number
  kmeans = KMeans(3)
  kmeans.fit(k)
  clusters = k.copy()
  clusters['cluster_pred'] = kmeans.fit_predict(k)

  # plotting parameters
  plt.scatter(clusters['Max'], clusters['Accumulated duration'], c = clusters['cluster_pred'], cmap = 'rainbow')
  plt.xlabel('Time', fontsize=16)
  plt.ylabel('Counts')
  plt.title('Cluster of all Accumulated duration')

  # plt.ylim(0, 10000)
  # plt.show()

  ###################################################
  # ZOOM INTO THE TOP, MIDDLE AND BOTTOM OF THE GRAPH

  df2CClog = pd.DataFrame(df2CC['Accumulated duration'])
  df2NClog = pd.DataFrame(df2NC['Accumulated duration'])
  # df2TClog = pd.DataFrame(df2TC['Accumulated duration'])

  # if plotting a logged graph, can uncomment below and comment the above block of codes
  # df2CCbin = pd.cut(df2CClog['Accumulated duration'], bins=100)
  # df2NCbin = pd.cut(df2NClog['Accumulated duration'], bins=100)
  # df2TCbin = pd.cut(df2TClog['Accumulated duration'], bins=100)

  df2CCbin = pd.cut(df2CClog['Accumulated duration'], bins=100)
  ##uncomment the below part if there is normal and transient contact
  # df2NCbin = pd.cut(df2NClog['Accumulated duration'], bins=100)
  # df2TCbin = pd.cut(df2TClog['Accumulated duration'], bins=100)

  dfCCbinn = pd.DataFrame(df2CCbin.value_counts())
  dfCCbinn.reset_index(inplace=True)
  maxList = []
  for index, row in dfCCbinn.iterrows(): 
    split = str(row['index']).split(",")
    max = float(split[-1].strip(' ]'))
    maxList.append(max)
  dfCCbinn['Max'] = maxList

  ##uncomment the below part if there is normal and transient contact

  # dfNCbinn = pd.DataFrame(df2NCbin.value_counts())
  # dfNCbinn.reset_index(inplace=True)
  # maxList = []
  # for index, row in dfNCbinn.iterrows(): 
  #   split = str(row['index']).split(",")
  #   max = float(split[-1].strip(' ]'))
  #   maxList.append(max)
  # dfNCbinn['Max'] = maxList

  ##Uncomment this if there is transient data
  # dfTCbinn = pd.DataFrame(df2TCbin.value_counts())
  # dfTCbinn.reset_index(inplace=True)
  # maxList = []
  # for index, row in dfTCbinn.iterrows(): 
  #   split = str(row['index']).split(",")
  #   max = float(split[-1].strip(' ]'))
  #   maxList.append(max)
  # dfTCbinn['Max'] = maxList

  # Closer examination of Close Contact counts (bottom of graph)
  k1 = dfCCbinn.copy()
  k1.drop('index', axis='columns', inplace=True)
  kmeans = KMeans(3)
  kmeans.fit(k1)
  clusters = k1.copy()
  clusters['cluster_pred'] = kmeans.fit_predict(k1)
  plt.figure(figsize=(20, 10), dpi= 120)
  ax = plt.scatter(clusters['Max'], clusters['Accumulated duration'], c = clusters['cluster_pred'], cmap = 'rainbow')
  plt.xlabel('Time')
  plt.ylabel('Counts')
  plt.title('Closer examination of Close Contact counts (Bottom of graph)')
  plt.ylim(0, 100)
  # plt.xlim(0, 3)
  plt.savefig('scatterplot1.png')
  # plt.show()

  ##uncomment the below part if there is normal contact
  ## Closer examination of Normal Contact counts (middle of graph)
  # k2 = dfNCbinn.copy()
  # k2.drop('index', axis='columns', inplace=True)
  # kmeans = KMeans(3)
  # kmeans.fit(k2)
  # clusters = k2.copy()
  # clusters['cluster_pred'] = kmeans.fit_predict(k2)
  # plt.figure(figsize=(20, 10), dpi= 120)
  # plt.scatter(clusters['Max'], clusters['Accumulated duration'], c = clusters['cluster_pred'], cmap = 'rainbow')
  # plt.xlabel('Time')
  # plt.ylabel('Counts')
  # plt.title('Closer examination of Normal Contact counts (Middle of graph)')
  # plt.ylim(0, 10000)
  # plt.xlim(0, 3)

  # plt.savefig('scatterplot2.png')
  ## plt.show()

  # k3 = dfTCbinn.copy()
  # k3.drop('index', axis='columns', inplace=True)
  # kmeans = KMeans(3)
  # kmeans.fit(k3)
  # clusters = k3.copy()
  # clusters['cluster_pred'] = kmeans.fit_predict(k3)
  # plt.figure(figsize=(20, 10), dpi= 120)

  # plt.scatter(clusters['Max'], clusters['Accumulated duration'], c = clusters['cluster_pred'], cmap = 'rainbow')
  # plt.xlabel('Time')
  # plt.ylabel('Counts')
  # plt.title('Closer examination of Transient Contact counts (Top of graph)')

  # plt.ylim(0, 10000)
  # plt.xlim(0, 3)


  # plt.savefig('scatterplot3.png')
  # plt.show()



  ##################
  # BOX PLOT OF ALL

  close = df2CC['Accumulated duration'].tolist()
  # normal = df2NC['Accumulated duration'].tolist()
  # transient = df2TC['Accumulated duration'].tolist()
  transient = 0
  normal = 0

  my_dict = {'CloseCon': close, 'NormCon': normal, 'TransCon': transient }


  fig, ax = plt.subplots()

  ax.boxplot(my_dict.values())
  ax.set_xticklabels(my_dict.keys())
  plt.ylim(0, 100)

  fig.set_size_inches(18.5, 10.5)
  ax.set_title('Boxplot of contact types',fontsize = 30)
  ax.set_ylabel('Accumulated duration')

  plt.savefig('boxplot.png')
  # plt.show()


  # Logged values
  close = np.log10(df2CC['Accumulated duration']).tolist()
  normal = np.log10(df2NC['Accumulated duration']).tolist()
  # transient = np.log10(df2TC['Accumulated duration']).tolist()

  my_dict = {'CloseCon': close, 'NormCon': normal, 'TransCon': transient }


  fig, ax = plt.subplots()

  ax.boxplot(my_dict.values())
  ax.set_xticklabels(my_dict.keys())
  fig.set_size_inches(18.5, 10.5)
  ax.set_title('Boxplot of contact types', fontsize = 30 )
  ax.set_ylabel('Accumulated duration')

  plt.savefig('boxplotLogged.png')
  # plt.show()

  print("Close Contact:")
  print(df2CC.describe())
  print("Normal Contact:")
  print(df2NC.describe())
  # print("Transient Contact:")
  # print(df2TC.describe())


  # #####################
  # To map the attendees to their company

  #Find who is not in the event attendance
  df2["InEventAttendance"] = df2.Attendee01.isin(df_EA.User).astype(int)
  df2[df2['InEventAttendance']== 0]
  Not_In_Attendance = []
  for i in range(len(df2.index)):
    if df2.iloc[i]['InEventAttendance'] == 0 :
      if df2.iloc[i]['Attendee01'] not in Not_In_Attendance:
        Not_In_Attendance.append(df2.iloc[i]['Attendee01'])

          
  print(Not_In_Attendance)   


  #Add these people into the attendance list
  Not_In_AttendanceList= list(set(Not_In_Attendance)-set(df_EA['User']))
  df_EA = df_EA.append(pd.DataFrame({'User': Not_In_AttendanceList}), ignore_index=True)
  df_EA['Email']=df_EA['Email'].fillna("Not_in_AttendanceList")
  print(Not_In_Attendance)   


  #find the domain of the email and ignore personal emails
  def get_domain_name(email):
    '''Make text lowercase and get the domain name of the email.'''
    if email =='Not_in_AttendanceList':
      return email
    else:
      email = email.split("@")[1].split(".")[0]
      if email == 'hotmail' or email =='yahoo' or email == 'gmail' or email == 'outlook':
        email = 'None'
        return email
      else: 
        return email

  df_EA['Email'] = pd.DataFrame(df_EA['Email'].apply(get_domain_name))
  print(df_EA)

  #Mapping the email to the attendees
  df_name_email = df_EA[['User','Email','Entry Time']].copy()
  df2['Attendee01_email'] = df2['Attendee01']
  df2['Attendee02_email'] = df2['Attendee02']
  df2['Attendee01_email'] = df2['Attendee01_email'].map(df_name_email.set_index('User')['Email'])
  df2['Attendee02_email'] = df2['Attendee02_email'].map(df_name_email.set_index('User')['Email'])
  df2['Attendee01_email'] = df2['Attendee01_email'].replace(np.nan,'None')
  df2["Attendee01"] = df2["Attendee01"] +" - "+ df2["Attendee01_email"]
  df2["Attendee02"] = df2["Attendee02"] +" - "+ df2["Attendee02_email"]
  print(df2.head(50))






  ##################
  # Network Analysis

  G = nx.Graph()
  print("Compiling Network...")
  df2CC = df2
  # df2CC =df2
  for index, row in df2CC.iterrows():
    name = row['Attendee01']
    contName = row['Attendee02']
    G.add_node(name)
    G.add_node(contName)
    G.add_edge(name, contName, weight = int(row['Accumulated duration']))


  print('Network Density = '+ str(nx.density(G)))
  print('Network Transitivity = ' + str(nx.transitivity(G)))
  degree_centrality = nx.degree_centrality(G)
  degCenList = dict(sorted(degree_centrality.items(), key=lambda item: item[1], reverse = True))
  degCenListSlice = dict(list(degCenList.items())[:10])
  print("Degree Centrality: Demographics of top 10 Influencers-")


  print(degCenListSlice)
  # for k,v in degCenListSlice.items():
  #   resultsDC = []
  #   x = df2CC.loc[df2CC['Attendee01'] == k]
  #   # print(x)
  #   resultsDC.append(x.iloc[0]["Attendee01"])
  #   # resultsDC.append(v)
  #   # resultsDC.append(x.iloc[0]["Cabin No"])
  #   # resultsDC.append(x.iloc[0]["Age"])
  #   # resultsDC.append(x.iloc[0]["Gender"])
  #   print(resultsDC)

  bet_centrality = nx.betweenness_centrality(G, normalized = True, endpoints = False)
  betCenList = dict(sorted(bet_centrality.items(), key=lambda item: item[1], reverse = True))
  betCenListSlice = dict(list(betCenList.items())[:10])

  print("Betweenness Centrality: Demographics of top 10 Influencers-")
  print(betCenListSlice)
  # for k,v in betCenListSlice.items():
  #   resultsBC = []
  #   x = df2CC.loc[df2CC['Attendee01'] == k]
  #   resultsBC.append(x.iloc[0]["Attendee01"])
  #   resultsBC.append(v)
  #   # resultsBC.append(x.iloc[0]["Cabin No"])
  #   # resultsBC.append(x.iloc[0]["Age"])
  #   # resultsBC.append(x.iloc[0]["Gender"])
  #   print(resultsBC)

  close_centrality = nx.closeness_centrality(G)
  closeCenList = dict(sorted(close_centrality.items(), key=lambda item: item[1], reverse = True))
  closeCenListSlice = dict(list(closeCenList.items())[:10])


  print("Closeness Centrality: Demographics of top 10 Influencers-")
  print(closeCenListSlice)
  # for k,v in closeCenListSlice.items():
  #   resultsCC = []
  #   x = df2CC.loc[df2CC['Attendee01'] == k]
  #   resultsCC.append(x.iloc[1]["Attendee01"])
  #   resultsCC.append(v)
  #   # resultsCC.append(x.iloc[0]["Cabin No"])
  #   # resultsCC.append(x.iloc[0]["Age"])
  #   # resultsCC.append(x.iloc[0]["Gender"])
  #   print(resultsCC)

  print("Top 10 with highest edges")
  degree = G.degree
  degree1 = dict(list(degree))
  degList = dict(sorted(degree1.items(), key=lambda item: item[1], reverse = True))
  print(degList)
  ## UNcomment the bottom part if the name list is > 10
  # degListSlice = dict(list(degList.items())[:10])
  # top10 = list(degList.items())[9:10]
  # top10th = top10[0][1]
  # print(degListSlice)

  #change if needed
  # df2CC = df2CC.loc[(df2CC["Accumulated duration"] >= 50)]


  #Plotting the Network Diagram
  got_net = Network(height='750px', width='100%')
  sources = df2CC['Attendee01'].tolist()
  targets = df2CC['Attendee02']
  weights = df2CC['Accumulated duration']

  edge_data = zip(sources, targets, weights)

  for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]
    # num1 = 0
    # num2 = 0
    Size1 = degree1[src]
    Size2 = degree1[dst]

    # if Size1 <= 10:
    #   num1 = 1
    # elif Size1 >= top10th:
    #   num1 = Size1/2
    # else:
    #   num1 = Size1/10
    # Size2 = degree1[dst]
    # if Size2 <= 10:
    #   num2 = 1
    # elif Size2 >= top10th:
    #   num1 = Size1/2
    # else:
    #   num2 = Size2/10
    got_net.add_node(src, src, title=src , size = Size1)
    got_net.add_node(str(dst), str(dst), title=str(dst), size = int(Size2))
    got_net.add_edge(src, str(dst), value=w)

  got_net.show_buttons(filter_=['physics'])
  got_net.show('network.html')

  got_net.save_graph('Network.html')



  #######################
  # To find the zone density


  # Remove data that are still "ongoing"
  df_TA = df_TA[df_TA['Duration (Minutes)'] != 'On-going']

  #Filter out the Date
  new_list = []
  for i in range(len(df_TA)):
    if '20/05/2021' in df_TA.iloc[i]['Start Time']:
      new_list.append(df_TA.iloc[i]['Start Time'])

  # DF for events from 20/05/2021
  df_TA = df_TA.loc[df_TA['Start Time'].isin(new_list)]
  df_TA.reset_index(inplace=True)

  #Filter out the Date
  new_list = []
  for i in range(len(df_transformed_CH)):
    if '20/05/2021' in df_transformed_CH.iloc[i]['Start Time']:
      new_list.append(df_transformed_CH.iloc[i]['Start Time'])

  # DF for events from 20/05/2021
  df_transformed_CH = df_transformed_CH.loc[df_transformed_CH['Start Time'].isin(new_list)]
  df_transformed_CH.reset_index(inplace=True)



  #Edit this to filter out the zone that you want to plot out
  zone = df_TA['Zone'].unique().tolist()
  print(zone)
  # zone = ['Bentley', 'Main Event Ballroom', 'Main Event Ballroom C','Main Event Ballroom L', 'Main Event Ballroom R', 'Meeting Area 1', 'Meeting Area 2', 'Reception (Level 4)','Reception Level 5','Trimble']

  #Convert the timing to unix time
  for index, row in df_TA.iterrows():
    starttime = row['Start Time'] 
    yyyymmdd = starttime[6:10] + "-" + starttime[3:5] + "-" + starttime[:2]
    start_time = yyyymmdd + ' ' + starttime[-5:]
    endtime = row['End Time'] 
    yyyymmdd = endtime[6:10] + "-" + endtime[3:5] + "-" + endtime[:2]
    end_time = yyyymmdd + ' ' + endtime[-5:]
    dt1 = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    dt2 = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
    st = int(dt1.timestamp() * 1000)
    et = dt2.timestamp() * 1000
    df_TA.loc[index, 'Start Time'] = int(st)
    df_TA.loc[index, 'End Time'] = int(et)
  df_TA.head(10)

  #Create a new DF to count the number of ppl entering and leaving the zone
  def create_DF_for_the_time_range(startdate, num_of_intervals , intervals):
    #convert to unix
    timing = datetime.strptime(startdate, '%Y-%m-%d %H:%M')
    startkey = int(timing.timestamp()*1000)
    time_dict1= {}
    for i in range(num_of_intervals):
      time_dict1[startkey] = 0
      startkey += intervals
    print(time_dict1)
    df_new = pd.DataFrame(index=time_dict1, columns= zone)
    df_new = df_new.fillna(0) # with 0s rather than NaNs
    df_new.reset_index(inplace =True)
    df_new
    return(df_new)




  #Adjust the starttime accordingly
  starttdate = df_transformed_CH.iloc[0]['Start Time']
  date_of_event = starttdate[6:10] + "-" + starttdate[3:5] + "-" + starttdate[:2]
  startdate = date_of_event + " "+ '8:00'
  #Adjust the time range accordingly(in hours)
  num_of_intervals = 30
  intervals = 1800000
  df_= create_DF_for_the_time_range(startdate,num_of_intervals,intervals)

  print(df_)
  #To count the number of ppl entering a zone within a certain timing ## RMB to change the zone for the different event
  for index, row in df_TA.iterrows():
    for j in zone:
      if row['Zone'] == j:
        for i in range(len(df_['index'].values)): 
          if row['Start Time'] >= df_['index'][i] and row['Start Time'] < df_['index'][i]+intervals:
            df_[j][i] += 1

  for i in range(len(df_['index'].values)):
    if i != 0:
      for j in zone:
        df_[j].values[i] += df_[j].values[i-1]

            
  for index, row in df_TA.iterrows():
    for j in zone:
      if row['Zone'] == j:
        for i in range(len(df_['index'].values)): 
          if row['End Time'] >= df_['index'][i] and row['End Time'] < df_['index'][i]+intervals:
            if df_['index'][i] !=df_['index'].values[-1]:
              df_[j][i+1] -= 1
              for k in range(i+2,num_of_intervals):
                df_[j][k] -= 1
  print(df_)
  #convert the Unix timing back to readable format
  def convert_to_dates(timing):
    timing2 = timing + intervals-60000
    timing = datetime.fromtimestamp(int(timing)/1000).strftime('%Y-%m-%d %H:%M:%S')
    timing2 = datetime.fromtimestamp(int(timing2)/1000).strftime('%Y-%m-%d %H:%M:%S')
    timing_final = timing + " - " + timing2[11:]
    return timing_final

  df_['index'] = pd.DataFrame(df_['index'].apply(convert_to_dates))
  df_.rename(columns = {'index' : 'Timing'}, inplace = True)
  df_

  plt.rcParams['figure.dpi'] = 360
  df_.plot(kind="bar", stacked=True, figsize=(30, 20), x = 'Timing',grid =True,colormap='hsv')
  plt.title('Zone Density from 8am to 11pm 20 May', x=0.5, y=1.05, ha='center', fontsize=40)
  plt.xlabel('Timing',fontsize=20)
  plt.ylabel('Number of people in the zone within that hour',fontsize=20)
  plt.xticks(size=15)
  plt.yticks(size=15)
  plt.legend(fontsize=16)
  plt.savefig('Zone density from 8am to 11pm on 20 May stacked bars.png')
  # plt.show()




  ###########################################
  #Unauthorised Contact

  # find the count of the user appearing in the unauthorised Contact
  name_dict = {}
  for i, row in df_UC.iterrows():
    if row["User1"] not in name_dict:
      name_dict[row["User1"]] = 1
      if row["User2"] not in name_dict:
        name_dict[row["User2"]] = 1
      elif row["User2"] in name_dict:
        name_dict[row["User2"]] += 1
    elif row["User1"] in name_dict:
      name_dict[row["User1"]] += 1
      if row["User2"] not in name_dict:
        name_dict[row["User2"]] = 1
      elif row["User2"] in name_dict:
        name_dict[row["User2"]] += 1
  name_dict = dict(sorted(name_dict.items(), key=lambda item: item[1], reverse = True))
  df_name = pd.DataFrame(list(name_dict.items()),columns = ['User','Count']) 
  print('Top 10 attendees who made the most number of unauthorised contact:' , df_name.head(10))

  #Plot the graph to show the number of unauthorised contact
  df_count = df_name.groupby(['Count']).count()
  df_count.reset_index(inplace =True)
  df_count.rename(columns = {'User' :'Number of Users', 'Count' : 'Number of Unauthorised Contact'}, inplace = True)

  ax = df_count.plot(kind='bar', x='Number of Unauthorised Contact', y='Number of Users', 
      figsize=(15, 10), legend=False, color='powderblue', rot=0)
  plt.xlabel('Number of Unauthorised Contact',fontsize=20)
  plt.ylabel('Number of Users',fontsize=20)
  plt.title('Frequency of Unauthorized Contact',fontsize=30)
  # plt.xticks(size=10)
  # plt.yticks(size=10)
  for p in ax.patches: 
    ax.annotate(np.round(p.get_height(),decimals=2),(p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 10),textcoords='offset points',fontsize=10)
  plt.savefig('Frequency of Unauthorized Contact.png')



  ####################################
  #Analyse the people who are high risk(have interaction for >30 mins)
  #Sort in descending order
  df_HighRisk.sort_values(by=['Total High Risk Contact (Above 30 mins)'], inplace=True, ascending=False)
  print('Top 10 attendees who are "high risk":' , df_HighRisk.head(10))

  df_HR_count = df_HighRisk.groupby(['Total High Risk Contact (Above 30 mins)']).count()
  df_HR_count.reset_index(inplace =True)
  df_HR_count.drop(['No'], axis = 1, inplace =True)
  df_HR_count.rename(columns = {'User' :'Number of Users'}, inplace = True)

  ax = df_HR_count.plot(kind='bar', x='Total High Risk Contact (Above 30 mins)', y='Number of Users', figsize=(15, 10), legend=False, color='powderblue', rot=0)
  plt.xlabel('Number of High Risk Contact',fontsize=20)
  plt.ylabel('Number of Users',fontsize=20)
  plt.title('Frequency of High Risk Contact(above 30 mins)',fontsize=30)
  # plt.xticks(size=10)
  # plt.yticks(size=10)
  for p in ax.patches: 
    ax.annotate(np.round(p.get_height(),decimals=2),(p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 10),textcoords='offset points',fontsize=10)
  plt.savefig('Frequency of High Risk Contact(above 30 mins).png')



  ############################
  # Find the zone where most of the close and normal contact occurred

  # Convert the timing to a standard format

  #remove data that is not within the event duration
  new_list = []
  for i in range(len(df_transformed_CH)):
    if '20/05/2021' in df_transformed_CH.iloc[i]['Start Time']:
      new_list.append(df_transformed_CH.iloc[i]['Start Time'])
    # elif 'March 25' in df_transformed_CH.iloc[i]['Start Time']:
    #   new_list.append(df_transformed_CH.iloc[i]['Start Time'])

  # DF for events from 20 May
  df_2 = df_transformed_CH.loc[df_transformed_CH['Start Time'].isin(new_list)]
  df_2.reset_index(inplace =True)
  df_2


  df_2 = df_2.dropna()

  #Convert to Unix timing
  for index, row in df_2.iterrows():
    starttime = row['Start Time'] 
    yyyymmdd = starttime[6:10] + "-" + starttime[3:5] + "-" + starttime[:2]
    start_time = yyyymmdd + ' ' + starttime[-5:]
    endtime = row['End Time'] 
    yyyymmdd = endtime[6:10] + "-" + endtime[3:5] + "-" + endtime[:2]
    end_time = yyyymmdd + ' ' + endtime[-5:]
    dt1 = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    dt2 = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
    st = int(dt1.timestamp() * 1000)
    et = dt2.timestamp() * 1000
    df_2.loc[index, 'Start Time'] = int(st)
    df_2.loc[index, 'End Time'] = int(et)
  print('cleaned contact history' ,df_2.head(10))

  #Work on the trail analysis data
  print(df_TA.head(10))

  cleanIntMapped = []
  for index, row in df_2.iterrows():
    starttime1 = row['Start Time']
    endtime1 = row['End Time']
  #   print(row['Name'])
  #   print(starttime1)
  #   print(endtime1)
  #   x = cleanedTrailDF.loc[starttime1 < cleanedTrailDF["endtime"] ]
  #   print("endtime")
  #   print(x)

  #   x = cleanedTrailDF.loc[cleanedTrailDF['starttime'] < endtime1]
  #   print("starttime")

  #   print(row.tolist())
    interaction = row.tolist()
  #   break

  #   x = cleanedTrailDF.loc[(cleanedTrailDF["Personnel"] == row['Name']) & (starttime1 < cleanedTrailDF["endtime"]) & (cleanedTrailDF['starttime'] < endtime1)]
    query = df_TA.loc[(df_TA["Name"] == row['Attendee01']) & (starttime1 <= df_TA["End Time"]) & (df_TA['Start Time'] <= endtime1)].values.tolist()
    zone = []
    for i in query:
      zone.append(i[3]) 
  #   print(zone)
  #   s1 e1
  #   s2 e2
  #   s1 <= e2
  #   s2 <= e1
  #   print(x)


  # if len(x.index) >= 1:
    # interaction.append(zone)
    # cleanIntMapped.append(interaction)
  #   print(cleanIntMapped)

  cleanIntMappedDF = pd.DataFrame(cleanIntMapped, columns = ["index","Attendee01","Attendee02","Start Time","End Time","interaction","Duration (Minutes)","Zones"])
  cleanIntMappedDF

  cleanIntMappedDF= cleanIntMappedDF.reset_index()
  del cleanIntMappedDF['index']
  cleanIntMappedDF

  zoneList = df_TA['Zone'].unique().tolist()

  contactCat = []
  for index, row in cleanIntMappedDF.iterrows():
    line = row.tolist()
    if row['Duration (Minutes)'] < 5:
      line.append('transient')
    elif row['Duration (Minutes)'] < 15:
      line.append('normal')
    elif row['Duration (Minutes)'] >= 15:
      line.append('close')
    contactCat.append(line)


  cleanIntMappedDF2 = pd.DataFrame(contactCat, columns = 
  [          "index",
            "Attendee01",
            "Attendee02",
            "Start Time",
            "End Time",
            "interaction",
            "Duration (Minutes)",
            "Zones",
            "Contact Category"
          ])
  cleanIntMappedDF2


  zoneDictTransient = {}
  zoneDictNormal = {}
  zoneDictClose = {}
  for zone in zoneList:
    zoneDictTransient[zone] = 0
    zoneDictNormal[zone] = 0
    zoneDictClose[zone] = 0
  for index, row in cleanIntMappedDF2.iterrows():
    zones = row['Zones']
    myset = list(set(zones))
    for zone in myset:
      if row['Contact Category'] == 'transient':
        zoneDictTransient[zone] += 1 
      if row['Contact Category'] == 'normal':
        zoneDictNormal[zone] += 1 
      if row['Contact Category'] == 'close':
        zoneDictClose[zone] += 1 

  print('Number of Normal Contacts in each zone:' ,zoneDictNormal)
  print('Number of Close Contacts in each zone:' ,zoneDictClose)

  transient = list(zoneDictTransient.values())
  normal = list(zoneDictNormal.values())
  close = list(zoneDictClose.values())
  zones = zoneList
  df = pd.DataFrame({
    'transient': transient,
    'normal': normal,
    'close':close}, index=zones)
  # import matplotlib.pyplot as plt
  df.plot.bar(figsize=(20,15));
  plt.title('Number of Transient, Normal and Close contact within each zone',fontsize=30 )
  plt.xlabel('Zones',fontsize=18)
  plt.ylabel('Number of Contacts',fontsize=18)
  plt.xticks(size=12)
  plt.yticks(size=12)
  plt.savefig('Contacts in different zones.png')
