#!/usr/bin/python3
import datetime
import json
import requests
import sys
from math import sqrt as sqrt
from tkinter import *
from tkinter import messagebox
from dateutil import relativedelta

IKSM_SESSION=""

#######################################################

def showmsg(fatal, title, body):
    if fatal:
        temproot = Tk()
        temproot.withdraw()
        messagebox.showerror(title, body)
        temproot.destroy()
        sys.exit(1)
    else:
        temproot = Tk()
        temproot.withdraw()
        messagebox.showinfo(title, body)
        temproot.destroy()

def quit():
    root.destroy()

if IKSM_SESSION == "":
    showmsg(True, "error", "iksm_session token not defined")

# calc current x rank period 
beginrange = datetime.date.today().replace(day=1)
endofrange = beginrange + relativedelta.relativedelta(months=1)
timespan = beginrange.strftime("%y%m%dT00")+"_"+endofrange.strftime("%y%m%dT00")

initialxpower = oldxpower = newxpower = 0.0

def getjsonfrom(url):
    headers = {"Cookie": "iksm_session="+IKSM_SESSION}
    r = requests.get(url, headers=headers)
    return r.text

def getcurrentmodexpower():
    rotationdata = json.loads(getjsonfrom("https://app.splatoon2.nintendo.net/api/schedules"))
    currentmode = rotationdata["gachi"][0]["rule"]["key"]

    xdata = json.loads(getjsonfrom("https://app.splatoon2.nintendo.net/api/x_power_ranking/"+timespan+"/summary"))

    try:
        newxpower = xdata[currentmode]["my_ranking"]["x_power"]
    except TypeError:
        showmsg(True, "error", "couldn't get current x power, maybe you're not x rank in this mode?")
    
    return newxpower
    
def updatelabels(win, current, newxpower, lose, winc, losec):
    label_win_xpower.config(text="+"+str(int(round(win))))
    label_curr_xpower.config(text=str(current))
    label_lose_xpower.config(text="-"+str(int(round(lose))))
    label_win_chance.config(text=str(int(round(winc)))+"%")
    label_lose_chance.config(text=str(int(round(losec)))+"%")

    global initialxpower

    if initialxpower <= newxpower:
        delta = "+"+str(int(round(newxpower-initialxpower)))
        label_delta_xpower.config(text=delta)
    elif initialxpower > newxpower:
        delta = "-"+str(int(round(initialxpower-newxpower)))
        label_delta_xpower.config(text=delta)
    
    root.update()

def update():
    button_refresh.config(state="disabled")
    root.update()

    currentxpower = getcurrentmodexpower()
    global initialxpower

    losedelta = initialxpower - currentxpower

    try:
        win_lose_abs_delta = ((sqrt(currentxpower/losedelta)+losedelta)/25)*25
        if win_lose_abs_delta > 24.4:
            win_lose_abs_delta = 24.4

        windelta = sqrt(currentxpower/losedelta)-(sqrt(currentxpower/losedelta)-(win_lose_abs_delta-losedelta))
        winchance = windelta/win_lose_abs_delta*100
        losechance = losedelta/win_lose_abs_delta*100

    except:
        showmsg(False, "info", "couldn't calc gainable points & percentages")
        winchance = losechance = windelta = 0.0

    updatelabels(windelta, currentxpower, currentxpower, losedelta, winchance, losechance)
    button_refresh.config(state="normal")

def init():
    global initialxpower
    initialxpower = getcurrentmodexpower() 
    updatelabels(0.0, initialxpower, initialxpower, 0.0, 0.0, 0.0)


# build the ui
root = Tk()
root.title("X Power Predict")
root.geometry("360x260+100+100")
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

frame_left = Frame(master=root, width="200")
frame_left.pack(side="left", padx="5", pady="5", fill=BOTH, expand=1)
frame_left.pack_propagate(0)

frame_right = Frame(master=root, width="160")
frame_right.pack(side="right", padx="5", pady="5", fill=BOTH, expand=1)
frame_right.pack_propagate(0)

label_win_xpower = Label(master=frame_left, bg="#50ea38", font=("sans-serif", 38))
label_win_xpower.pack(side="top", fill=BOTH, expand=1)

label_curr_xpower = Label(master=frame_left, bg="#c7fcfa", font=("sans-serif", 38))
label_curr_xpower.pack(side="top", fill=BOTH, expand=1)

label_delta_xpower = Label(master=frame_left, bg="#afaeae", font=("sans-serif", 38))
label_delta_xpower.pack(side="top", fill=BOTH, expand=1)

label_lose_xpower = Label(master=frame_left, bg="#f74845", font=("sans-serif", 38))
label_lose_xpower.pack(side="top", fill=BOTH, expand=1)

label_win_chance = Label(master=frame_right, bg="#fcab41", font=("sans-serif", 38))
label_win_chance.pack(side="top", fill=BOTH, expand=1)

button_refresh = Button(master=frame_right, text="refresh", command=update, font=("sans-serif", 28))
button_refresh.pack(side="top", fill=BOTH, expand=1)

button_quit = Button(master=frame_right, text="quit", command=quit, font=("sans-serif", 28))
button_quit.pack(side="top", fill=BOTH, expand=1)

label_lose_chance = Label(master=frame_right, bg="#fcab41", font=("sans-serif", 38))
label_lose_chance.pack(side="bottom", fill=BOTH, expand=1)

init()

root.mainloop()
