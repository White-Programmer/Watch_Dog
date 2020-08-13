#!/usr/bin/env python
"""
Author : White Programmer
OS : Winodows/Linux
Developer : White Programmer
Date : 26-07-2020
Version : COVID-19-STABLE-FINAL-3
Stable For : Python3
Recommended : Python 3.6.9 64 bit or +
Operation System : Only Linux and windows
tested on : elementary os (linux) and windows 10
Helpers : Internet And My Knowledge :)
"""
from matplotlib import pyplot as plt
import json_activity as js
from datetime import datetime

def pie_usage():
    activities = js.get_stored_activity()
    date = datetime.now().strftime("%d-%m-%Y")
    time = []
    name = []
    final_time = []
    final_name = []
    for i in activities:
        if js.get_info(i, "date", date) == date:
            total_used = js.get_info(i, "total_use", date)
            h, m, s = list(map(int, total_used.split(":")))
            total_used = js.second(h, m, s)
            time.append(total_used)
            name.append(i)
    for i in range(0, 4):
        maxnum = 0
        index = 0
        time_name = ""
        for j in range(len(time)):
            if time[j] > maxnum:
                maxnum = time[j]
                index = time.index(time[j])
                time_name = name[index]
        time.pop(index)
        final_time.append(maxnum)
        name.pop(index)
        final_name.append(time_name)
    return final_name, final_time

def plot(lacels, time):
    # labels, time = pie_usage()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    explode = (0.06, 0.06, 0.06, 0.06)
    fig1, ax1 =plt.subplots()
    ax1.pie(time, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.80, explode=explode)

    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')
    plt.tight_layout()
    plt.show()
try:
    labels, time = pie_usage()
    plot(labels, time)
except:
    print("< 1 Minute")
