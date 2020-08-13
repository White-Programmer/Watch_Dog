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
from tkinter import *
import json_activity
from datetime import datetime, timedelta
import time

def longest_season():
    Activity = json_activity.get_stored_activity()
    longest = 0
    longest_name = ""
    short = 0
    for i in Activity:
        found_date = json_activity.get_info(
            i, "date", datetime.now().strftime("%d-%m-%Y"))
        if found_date == datetime.now().strftime("%d-%m-%Y"):
            found_total_use = json_activity.get_info(
                i, "total_use", datetime.now().strftime("%d-%m-%Y"))
            i_time = list(map(int, found_total_use.split(":")))
            short = json_activity.second(i_time[0], i_time[1], i_time[2])
            if short > longest:
                longest = short
                longest_name = i
    return longest_name


def get_screen_time():
    total_time = 0
    Activity = json_activity.get_stored_activity()
    for i in Activity:
        found_total_use = json_activity.get_info(
            i, "total_use", datetime.now().strftime("%d-%m-%Y"))
        if found_total_use != None:
            h, m, s = list(map(int, found_total_use.split(":")))
            total_time = total_time + json_activity.second(h, m, s)
    total_time = str(timedelta(seconds=total_time))
    h, m, s = list(map(int, total_time.split(":")))
    if m != 0:
        if m == 1:
            time_min = "Minute"
        if m > 1:
            time_min = "Minutes"
    if h != 0:
        if m == 1:
            time_hour = "Hour"
        if m > 1:
            time_hour = "Hours"
#  Main Time Calculation Is Started From Here
    if h == 0 and m == 0:
        return "< 1 Minute"
    elif h == 0 and m != 0:
        time = f"{m} {time_min}"
        return time
    elif h != 0 and m == 0:
        time = f"{h} {time_hour}"
        return time
    else:
        time = f"{h} {time_hour} {m} {time_min}"
        return time


class GUI(Tk):

    def make_window(self):
        self.geometry("970x600")
        self.title("Watch Dog")
        self.resizable(0, 0)
        self['bg'] = "white"

    def screen_time(self):
        self.frame = Frame(root, bg="white")
        self.frame.pack(expand=False, fill=X, side=TOP, anchor=NW)
        self.label = Label(self.frame, text=f"Screen Time : {get_screen_time()}", anchor=NW)
        self.label.config(bg="white", font=("Andale Mono IPA", 13))
        self.label.pack(side=LEFT, anchor=W, expand=FALSE, fill=BOTH)

        self.strvar = StringVar()
        date = datetime.now().strftime("%d-%m-%Y")
        self.strvar.set(f"Longest Used Application: {longest_season()}\t\tTracking Status : ON\t\tDate : {date}")
        self.status = Label(root, textvariable=self.strvar, anchor=W, bg="White",highlightcolor="black", font=("Andale Mono IPA", 10), highlightthickness=1)
        self.status.pack(fill=X, side=BOTTOM)


    def hover1(self, event):
        self.button.configure(bg="black", fg="white", activebackground="white", highlightbackground="light blue")
        self.strvar.set("Refreshing....")
        self.status.update()
        self.label.config(text="...")

    def hover2(self, event):
        self.button.configure(
            bg="white", fg="black", activebackground="white", highlightbackground="white")
        self.label.config(text=f"Screen Time : {get_screen_time()}")
        date = datetime.now().strftime("%d-%m-%Y")
        self.strvar.set(f"Longest Used Application: {longest_season()}\t\tTracking Status : ON\t\tDate : {date}")
        self.status.update()

    def repacked(self):
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame.pack(expand=False, fill=X, side=TOP, anchor=NW)

    def button2_hover_enter(self, event):
        self.button2.configure(text="< Back", fg="Blue")
        self.label2.config(fg="Blue")
    def button2_hover_exit(self, event):
        self.button2.configure(text="<", fg="Black")
        self.label2.config(fg="black")
    def settings(self):
        self.frame.pack_forget()
        self.frame2 = Frame(self, bg="White")
        self.frame2.pack(expand=False, fill=X, side=TOP, anchor=NW)
        self.button2 = Button(self.frame2, text="<", anchor=NE, relief=RIDGE, bg="White", bd=0, font=("Andale Mono IPA", 18), command=self.repacked, activebackground="white")
        self.button2.bind("<Enter>", self.button2_hover_enter)
        self.button2.bind("<Leave>", self.button2_hover_exit)
        self.button2.pack(side=LEFT)
        self.label2 = Label(self.frame2, text="Settings", font=("Andale Mono IPA", 18), bg="white", pady=0, anchor=NW)
        self.label2.pack()
        self.frame3 = Frame(self, bg="white")
        self.frame3.pack(expand=True, fill=BOTH)
        self.trackingframe = Frame(self.frame3, bg="white")
        tracking = json_activity.app_get_info("tracking")
        self.trackingframe.pack(expand=False, fill=X, side=TOP, anchor=NW)
        self.tracking = Label(self.trackingframe, text=f"\t\t\t\tTracking : {tracking}", font=("Andale Mono IPA", 14), bg="White")
        self.tracking.pack(side=LEFT, anchor=NW)
        self.Delete = Label(self.frame3, text="Delete Data", font=("Andale Mono IPA", 14), bg="White")
        self.Delete.pack(anchor=NW)
    
    def button(self):
        self.button = Button(self.frame, text="Settings", command=self.settings, anchor=SE)
        self.button.config(bg="white", fg="black", highlightbackground="white")
        self.button.bind("<Enter>", self.hover1)
        self.button.bind("<Leave>", self.hover2)
        self.button.pack(side=RIGHT, anchor=NE, expand=FALSE)


root = GUI()
root.make_window()
root.screen_time()
root.button()
root.mainloop()
