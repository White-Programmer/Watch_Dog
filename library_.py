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
import subprocess
import psutil
from tkinter import messagebox
from time import sleep
from datetime import datetime, timedelta
import json_activity as JS
import sys

def time_calculator(start, end):
    start = list(map(int, start.split(":")))
    end = list(map(int, end.split(":")))
    start = start[0]*(60*60) + start[1]*(60) + start[2]
    end = end[0]*(60*60) + end[1]*(60) + end[2]
    total_used = end - start
    return str(timedelta(seconds=total_used))

def browser_user_stats(Id, s=''):
    if s == "":
        """ ONLY SUPPORTS GOOGLE CHROME AND FIREFOX FOR NOW ! """
        window = subprocess.run(['xprop', '-id', Id, '_NET_WM_NAME'], stdout=subprocess.PIPE)
        '''unicode-escape raw_unicode_escape "utf-8", "ignore"'''
        window = str(window.stdout.decode("raw_unicode_escape"))
        final = window.split("=")[-1]
        final = final.replace('"', "")
        final = replace_space(final)
        final = final.split("-")
        final.pop(-1)
        name = ""
        for i in final:
            name = name + " " + i
        name = replace_space(name)
        return name
    else:
        from win32 import win32gui
        window = win32gui.GetForegroundWindow()
        name = win32gui.GetWindowText(int(window))
        site_name = name.split("-")[0] + "   " + name.split("-")[1]
        for i in range(3):
            if site_name[0] == " ":
                site_name = site_name[1:]
        return site_name

def replace_space(name):
    for ii in range(0,3):
        if name[0] == " ":
            name = name[1:]
    return name


def Name_Manager(Win_List):
    Name = []
    for i in Win_List:
        i = i.replace("*", "")
        i = i.replace("'", "")
        i = i.replace('"', "")
        i = replace_space(i)
        if "\n" in i:
            i = i.replace("\n", "")
        if "," in i:
            i = i.split(",")
            for j in i:
                j = replace_space(j)
                Name.append(j)
        else:
            Name.append(i)
    return Name

def element_m(name):
    if "." in name and " " not in name:
        Window = name.split(".")[-1]
        return Window.capitalize()
    else:
        return name.capitalize()

def window_name(List):
    not_req = ["?", "save", "open", "delete", "search", "dialog", "warning","about", "help", "settings", "option", "info"]
    for i in List:
        if List.count(i) >= 2:
            Window = i
        if "." in i and " " not in i:
            Window = i.split(".")[-1]
        if "/" in i:
            Window = i.split("/")[-1]
        if "\\" in i:
            Window = i.split("\\")[-1]
        for j in not_req:            
            if j in i.lower():
                Window = "Not Required"
                break
    return Window

def get_active_window():
    system = sys.platform
    if system.lower() in ['linux', 'linux2']:
            root = subprocess.run(["xprop", "-root", "_NET_ACTIVE_WINDOW"],\
                stdout=subprocess.PIPE)
            root = str(root.stdout, "utf-8")
            win_id = root.split()[-1]
            if '0x0' not in win_id:
                process_id = subprocess.check_output(['xprop', '-id', win_id, 'grep', '_NET_WM_PID']).decode("utf-8").split()[-1]
                if 'found' not in process_id:
                    window = psutil.Process(int(process_id))
                    low = element_m(window.name()).lower()
                    if "chrome" in low or "firefox" in low:
                        return "browser" + "-" + win_id
                    else:
                        return element_m(window.name())
                else:
                    List = []
                    data = ['WM_CLASS', 'WM_ICON_NAME', '_NET_WM_ICON_NAME', 'WM_NAME','_NET_WM_NAME']
                    for i in data:
                        win = subprocess.run(['xprop', '-id', win_id, i], stdout=subprocess.PIPE)
                        win = str(win.stdout, 'utf-8')
                        win = win.split("=")[-1]
                        List.append(win)
                    List = Name_Manager(List)
                    return window_name(List)
            else:
                return "Not Required"
    elif str(system).lower() in ['windows', 'win32', 'cygwin']:
        from win32 import win32gui
        window = win32gui.GetForegroundWindow()
        name = win32gui.GetWindowText(int(window))
        name = name.replace("/n", "")
        name = name.replace("*", "")
        name = name.replace("'", "")
        not_req = ["?", "save", "open", "delete", "search", "dialog", "warning","about", "help", "settings", "option", "info"]
        for i in not_req:
            if i in name.lower():
                name = "Not Required"
                return name
        NAME = name.split("-")[-1]
        if "chrome" in NAME.lower() or "firefox" in NAME.lower():
            name = "Browser"
            return name
        elif "/" in name:
            window_name_win = name.split("-")[0]
            return window_name_win
        elif "-" in name:
            window_name_win = name.split("-")[-1]
            return window_name_win
        else:
            return name
    else:
        return "Unknown Window"

def compare_time(total_time, time_limit):
    if time_limit != 'Not Set':
        time_limit = list(map(int, time_limit.split(":")))
        total_time = list(map(int, total_time.split(":")))
        if  total_time[0] >= time_limit[0] and total_time[1] >= time_limit[1]:
            return 'True'
        else:
            return 'False'
    else:
        return 'False'

def kill_application(name):
    root = subprocess.run(["xprop", "-root", "_NET_ACTIVE_WINDOW"],\
            stdout=subprocess.PIPE)
    root = str(root.stdout, "utf-8")
    window_id = root.split()[-1]
    if "0x0" not in window_id:
        process_id = subprocess.check_output(['xprop', '-id', window_id, 'grep', '_NET_WM_PID']).decode("utf-8").split()[-1]
        if 'found' not in process_id:
            y = subprocess.run(['kill', process_id])
##            n = messagebox.askokcancel("Action - Watch Dog", f'You Have Completed Today\'s Screen Time On {name}. So Watch Dog Stops')
    
            
window = ""
JS.store_app_data()
tracking = JS.app_get_info("tracking")
while tracking:
    try:
        Start_time = datetime.now().strftime("%H:%M:%S")
        sleep(1)
        active_window = get_active_window()
        if active_window != window and active_window != "Not Required":
            if "browser" in get_active_window().lower():
                Start_time_b = datetime.now().strftime("%H:%M:%S")
            date = datetime.now().strftime("%d-%m-%Y")
            while "browser" in get_active_window().lower():
                system = sys.platform
                if system.lower() in ['linux', 'linux2']: 
                    window_id = get_active_window().lower().split("-")[-1]
                    name = browser_user_stats(window_id)
                else:
                    name = browser_user_stats("", "win")
                End_Time = datetime.now().strftime("%H:%M:%S")
                last_used = date + " at " + End_Time
                total_use = time_calculator(Start_time, End_Time)
                site = name
                try:
                    track_usage = JS.get_info(site.split("   ")[-1], "tracking", date, "browser")
                    time_limit = JS.get_info(site.split("   ")[-1], "time_limit", date, "browser")
                    total_usage = JS.get_info(site.split("   ")[-1], "total_use", date, "browser")
                except:
                    track_usage = "On"
                    time_limit = "Not Set"
                    total_usage = None
                if track_usage == "On":
                    JS.store_data_in_json(name, last_used, date, total_use, "browser")
                if time_limit != "Not Set":
                    com = compare_time(total_usage, time_limit)
                    if com == 'True':
                        try:
                            kill_application(f"{site} - Browser")
                        except:
                            pass
                Start_time = datetime.now().strftime("%H:%M:%S")
                sleep(1)
                active_window = "Browser"
            try:
                track_usage = JS.get_info(active_window, "tracking", date)
                time_limit = JS.get_info(active_window, "time_limit", date)
                total_usage = JS.get_info(active_window, "total_use", date)
            except:
                track_usage = "On"
                time_limit = "Not Set"
                total_usage = None
            if time_limit != 'Not Set' and total_usage != None:
                if compare_time(total_usage, time_limit) == 'True':
                    try:
                        kill_application(active_window)
                    except Exception as e:
                        pass
            if track_usage == "On":
                End_Time = datetime.now().strftime("%H:%M:%S")
                if "browser" in active_window.lower():
                    Start_time = Start_time_b
                last_used = date + " at " + End_Time
                total_use = time_calculator(Start_time, End_Time)
                if str(sys.platform).lower() in ['windows', 'win32', 'cygwin']:
                    if "\\" in active_window:
                        active_window = active_window.split("\\")[-1]
                JS.store_data_in_json(active_window, last_used, date, total_use)
            active_window = get_active_window()
            Start_time = datetime.now().strftime("%H:%M:%S")
            sleep(1)
    except Exception as e:
        print(e)
        continue
