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

import json
from getpass import getuser
from datetime import datetime as dt, timedelta
import sys
from os import listdir


system = sys.platform
if system.lower() in ['linux', 'linux2']:
    remote_path = f"/home/{getuser()}/"
    path_to_file_application = f"/home/{getuser()}/.watch_dog.user.data.json"
    path_to_file_browser = f"/home/{getuser()}/.watch_dog.user.browser.data.json"
    path_appdata = f"/home/{getuser()}/.watch_dog.App_Data.json"
else:
    remote_path = f"C:\\Users\{getuser()}\\"
    path_to_file_application = f"C:\\Users\{getuser()}\\.watch_dog.user.data.json"
    path_to_file_browser = f"C:\\Users\\{getuser()}\\.watch_dog.user.browser.data.json"
    path_appdata = f"C:\\Users\\{getuser()}\\.watch_dog.App_Data.json"

''' This Method Returns Activities Name List Sorted In Json Data/File With RT Browser/
    Any Other Application If Window == browser Than It Returns Site Name '''
def get_stored_activity(window=""):
    if "browser" in window:
        path = path_to_file_browser
        name = "site"
        request = "Browser"
    else:
        path = path_to_file_application
        name = "name"
        request = "activities"
    try:
        with open(path, "r") as f:
            data = json.load(f)
            activity = []
            for i in data[request]:
                activity.append(i[name])
    except Exception as e:
        print(e)
        with open(path, 'w') as f:
            pass
        activity = []
    return activity

''' This Method Writes Data(Json Dictonary) Into Json File '''
def write_data(data, window=""):
    if "browser" in window.lower():
        path = path_to_file_browser
    elif "app" in window:
        path = path_appdata
    else:
        path = path_to_file_application
    with open(path, "w") as f:
        json.dump(data, f, indent=3)

''' This Method Takes Three Main Argument And One Optional Argument Winodw to Return Specific
    data Of Specific Application Form Json Data '''
def get_info(name, n, date, window=""):
    if "browser" in window:
        activities = get_stored_activity(window="browser")
        path = path_to_file_browser
        request = "Browser"
    else:
        activities = get_stored_activity()
        path = path_to_file_application
        request = "activities"
    if name in activities:
        index = activities.index(name)
    with open(path, "r") as f:
        data = json.load(f)
    try:
        req = data[request][index][n]
        return req
    except:
        index = activities.index(name)
        d = data[request][index]["time"]
        for i in d:
            if i["date"] == date:
                K = i[n]
                return K

def second(h, m, s):
    seconds = h*(60*60) + m*(60) + s
    return seconds

def date_index(index, date, window=""):
    if "browser" in window:
        path = path_to_file_browser
        req = "Browser"
    else:
        path = path_to_file_application
        req = "activities"
    with open(path, "r") as f:
        data = json.load(f)
        d = data[req][index]["time"]
    for i in d:
        if i["date"] == date:
            time = d.index(i)
    return time

''' This Method Store Data(Python Dictionary) To Json File '''
def store_data_in_json(activity_name, last_used, date, total_used, window=""):
    if "browser" in window:
        activities = get_stored_activity(window="browser")
        try:
            name = activity_name.split("   ")
            site = name[-1]
            name.pop(-1)
            what = ""
            for i in name:
                what = what + " " + i
            if what == "":
                what = site
            what = what + " : " + date
            for i in range(5):
                if site[0] == " ":
                    site = site[1:]
                if what[0] == " ":
                    what = what[1:]
            visit = []
            visit.append(what)
        except:
            site = activity_name
            what = site + " : " + date
            for i in range(5):
                if site[0] == " ":
                    site = site[1:]
                if what[0] == " ":
                    what = what[1:]
            visit = []
            visit.append(what)
        if ".com" in site or "www" in site:
            what = site + " : " + date
            site = "Connecting To Website"
        if activities == []:
            data = {"Browser":[{"site":site, "what":visit, "last_used":last_used, "time_limit":"Not Set", "tracking":"On", "time":[{"date":date, "total_use":total_used}]}]}
            write_data(data, "browser")
        elif site in activities:
            index = activities.index(site)
            if get_info(site, "date", date, "browser") != date:
                time = {"date": date, "total_use": total_used}
                with open(path_to_file_browser, "r") as f:
                    read = json.load(f)
                    read["Browser"][index]["what"].append(what)
                    read["Browser"][index]["time"].append(time)
                    read["Browser"][index]["last_used"] = last_used
                    write_data(read, "browser")
            elif get_info(site, "date", dt.now().strftime("%d-%m-%Y"), "browser") == dt.now().strftime("%d-%m-%Y"):
                s_time = get_info(site, "total_use", date, "browser")
                f_time = list(map(int, total_used.split(":")))
                s_time = list(map(int, s_time.split(":")))
                new_time = second(s_time[0], s_time[1], s_time[2]) + second(f_time[0], f_time[1], f_time[2])
                new_time = str(timedelta(seconds=new_time))
                time = {"date": date, "total_use": new_time}
                with open(path_to_file_browser, "r") as f:
                    read = json.load(f)
                    dindex = date_index(index, date, "browser")
                    read["Browser"][index]["time"][dindex] = time
                    if what not in read["Browser"][index]["what"]:
                        read["Browser"][index]["what"].append(what)
                    read["Browser"][index]["last_used"] = last_used
                    write_data(read, "browser")
        else:
            data = {"site":site, "what":visit, "last_used":last_used, "time_limit":"Not Set", "tracking":"On", "time":[{"date":date,"total_use":total_used}]}
            with open(path_to_file_browser, "r") as f:
                read = json.load(f)
                read["Browser"].append(data)
                write_data(read, "browser")
    else:
        activities = get_stored_activity()
        time = {"date": date, "total_use": total_used}
        if activities == []:
            data = {"activities": [{"username":getuser(), "name": activity_name, "last_used": last_used, "tracking": "On", "time_limit":"Not Set", "time": [{"date": date, "total_use": total_used}]}]}
            write_data(data)
        elif activity_name in activities:
            index = activities.index(activity_name)
            if get_info(activity_name, "date", date) != date:
                time = {"date": date, "total_use": total_used}
                with open(path_to_file_application, "r") as f:
                    read = json.load(f)
                    read["activities"][index]["time"].append(time)
                    read["activities"][index]["last_used"] = last_used
                    write_data(read)
            elif get_info(activity_name, "date", dt.now().strftime("%d-%m-%Y")) == dt.now().strftime("%d-%m-%Y"):
                s_time = get_info(activity_name, "total_use", date)
                f_time = list(map(int, total_used.split(":")))
                s_time = list(map(int, s_time.split(":")))
                new_time = second(s_time[0], s_time[1], s_time[2]) + second(f_time[0], f_time[1], f_time[2])
                new_time = str(timedelta(seconds=new_time))
                time = {"date": date, "total_use": new_time}
                with open(path_to_file_application, "r") as f:
                    read = json.load(f)
                    dindex = date_index(index, date)
                    read["activities"][index]["time"][dindex] = time
                    read["activities"][index]["last_used"] = last_used
                    write_data(read)

        else:
            data = {"username": getuser(), "name": activity_name, "last_used": last_used, "tracking": "On", "time_limit":"Not Set", "time": [{"date": date, "total_use": total_used}]}
            with open(path_to_file_application, "r") as f:
                Read = json.load(f)
                Read["activities"].append(data)
            write_data(Read)
def store_app_data():
    try:
        if ".watch_dog.App_Data.json" not in listdir(remote_path):
            data = {"app_data":[{"tracking":True, "boots":1}]}
            write_data(data, "app")
        else:
            boot = app_get_info("boots")
            with open(path_appdata, "r") as f:
                data = json.load(f)
                data["app_data"][0]["boots"] = boot + 1
            write_data(data, "app")
    except:
        data = {"app_data":[{"tracking":True, "boots":1}]}
        write_data(data, "app")        

def app_get_info(n):
    with open(path_appdata, "r") as f:
        data = json.load(f)
        req = data["app_data"][0][n]
    return req
