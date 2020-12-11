# -*- coding: utf-8 -*-
"""
Preflop Hold'em Trainer
Jeffrey McClure, 2020
"""

# imports
import tkinter as tk
import os
import time
from tkinter import filedialog
from tkinter import ttk
from DealHand import DealHand
from DealPos import DealPos
from InRange import InRange
from RangeViewer import CallViewer, RaiseViewer
from sliderGraphical import sliderGraphical
from TableReplay import TableReplay
from distutils.dir_util import copy_tree
from playsound import playsound
from configparser import ConfigParser
import datetime as dt

# directories
fdir = os.path.dirname(os.path.abspath("gui_v4.py"))

# load in saved user settings
parser = ConfigParser()
parser.read('prefloptrain.ini')

global rangedir, RWEIGHT, SHOWRANGES, TRAINTOL, SHOWHK, SHOWACC, RWEIGHT, AUDIO, SCEN1, SCEN2, SCEN3, SCEN4
rangedir = parser.get('settings','Range Package')
theme = parser.get('settings','Colour Theme')
SHOWRANGES = parser.getint('settings','SHOWRANGES')
TRAINTOL = parser.getint('settings','TRAINTOL')
SHOWHK = parser.getint('settings','SHOWHK')
SHOWACC = parser.getint('settings','SHOWACC')
RWEIGHT = parser.getint('settings','RWEIGHT')
AUDIO = parser.getint('settings', 'AUDIO')
SCEN1 = parser.getint('settings', 'SCEN1')
SCEN2 = parser.getint('settings', 'SCEN2')
SCEN3 = parser.getint('settings', 'SCEN3')
SCEN4 = parser.getint('settings', 'SCEN4')

# constants
LARGE_FONT = ("TkDefaultFont", 28)
SMALL_FONT = ('TkTextFont', 7)
BOLD_FONT = ('TkTextFont', 12, 'bold')
DIR_FONT = ('TkTextFont', 9)

FONT_COLOR = "black"
BG_COLOR = "white"
BG_COLOR2 = "#d0d1e6"
BTN_COLOR = "#73a9cf"

#BG_COLOR = "#2f3136"
#BG_COLOR2 = "#36393f"
#BG_COLOR3 = "#202225"

deck = {0: "2",
        1: "3",
        2: "4",
        3: "5",
        4: "6",
        5: "7",
        6: "8",
        7: "9",
        8: "T",
        9: "J",
        10: "Q",
        11: "K",
        12: "A"}
inv_deck = {v: k for k, v in deck.items()}

suits = {"c": "#00A318",
         "s": "#000000",
         "h": "#FF3333",
         "d": "#0093FB"}
             
lightsuits = {"c": "#BFFFC7",
              "s": "#DBDBDB",
              "h": "#FFCCCC",
              "d": "#CCEDFF"}

raiseColor = {100: '#67001f',
             95: '#7B032A',
             90: '#8F0735',
             85: '#A40A40',
             80: '#B80E4B',
             75: '#cc1156',
             70: '#D02268',
             65: '#D4327A',
             60: '#D7438C',
             55: '#DB539E',
             50: '#df64b0',
             45: '#DD75B8',
             40: '#DA86C0',
             35: '#D896C9',
             30: '#D5A7D1',
             25: '#d3b8d9',
             20: '#DCC6E1',
             15: '#E5D4E8',
             10: '#EDE3F0',
             5: '#F6F1F7',
             0: 'white'} 
   
callColor = {100: '#02385a',
             95: '#03436b',
             90: '#034E7c',
             85: '#04588d',
             80: '#04639e',
             75: '#056eaf',
             70: '#1B7AB5',
             65: '#3186BC',
             60: '#4791C2',
             55: '#5D9DC9',
             50: '#73a9cf',
             45: '#86B1D4',
             40: '#98B9D8',
             35: '#ABC1DD',
             30: '#BDC9E1',
             25: '#d0d1e6',
             20: '#D9DAEB',
             15: '#E3E3F0',
             10: '#ECEDF5',
             5: '#F6F6FA',
             0: 'white'} 
   
Scendict = {'R0': 'Open-',
            'R1': '3Bet-',
            'R2': '4Bet-',
            'R3': '5Bet-',
            'C0': 'Call-',
            'C1': 'Flat-',
            'C2': 'Call3Bet-',
            'C3': 'Call4Bet-'} 
      
# temporary variables
trainIdx = 4
myHand = "AsKs"
paintVal = 0
Correct = 0
Num = 0

# ---------------
# settings window    
# ---------------   

def gensettings():
    global parser
    global rangedir, RWEIGHT
    RWEIGHT = parser.getint('settings','RWEIGHT')
    rangedir = parser.get('settings','Range Package')
    
    def gensettingssave(flag):
        global rangedir, RWEIGHT
        RWEIGHT = int(entry1.get())
        rangedir = packOpt.get()
        
        if flag == 'close':
            popup.destroy()
            
        parser['settings']['Range Package'] = rangedir
        parser['settings']['RWEIGHT'] = str(RWEIGHT)

        with open('prefloptrain.ini','w') as configfile:
            parser.write(configfile)
            
        return
        
    popup = tk.Tk()  

    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Range Editor Settings")
    popup.configure(background=BG_COLOR)
    
    REditgroup = tk.LabelFrame(popup, text = 'Range Editor', padx=5, pady=5, background=BG_COLOR)
    
    label = tk.Label(REditgroup, text='Right-Click Increment (%):', font=DIR_FONT, background=BG_COLOR)
    label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry1 = tk.Entry(REditgroup, width=10, bd=0, highlightbackground="black", highlightthickness=1)
    entry1.insert(0, RWEIGHT)
    entry1.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    
    label = tk.Label(REditgroup, text='Range Pack:', font=DIR_FONT, background=BG_COLOR)
    label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
       
    root = fdir + '\\Range Packages'
    dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
    
    packOpt = ttk.Combobox(REditgroup, values=dirlist, width=30)
    packOpt.current(dirlist.index(rangedir))
    packOpt.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    
    REditgroup.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    
    windowCont = tk.Frame(popup, bd=0, highlightbackground="black", highlightcolor=BTN_COLOR, highlightthickness=0, background=BG_COLOR)
    B1border = tk.Frame(windowCont, bd=1, highlightbackground="black", highlightcolor=BTN_COLOR, highlightthickness=1) 
    B1 = tk.Button(B1border, text="    OK    ", font=DIR_FONT, bg='white', bd=0, highlightthickness=0, activebackground=BTN_COLOR, padx=8, pady=3, command = lambda: gensettingssave('close'))
    B1.pack(side = tk.LEFT)
    B1border.grid(row=0,column=0, padx=5, pady=5, sticky='e') 
    B1.bind('<Enter>', hoverButton)
    B1.bind('<Leave>', leaveButton)
    B2border = tk.Frame(windowCont, bd=1, highlightbackground="black" ,highlightcolor=BTN_COLOR, highlightthickness=1) 
    B2 = tk.Button(B2border, text="Cancel", font=DIR_FONT, bg='white', bd=0, highlightthickness=0, activebackground=BTN_COLOR, padx=8, pady=3, command = lambda: popup.destroy())
    B2.pack(side = tk.LEFT)
    B2border.grid(row=0,column=1, padx=5, pady=5, sticky='e') 
    B2.bind('<Enter>', hoverButton)
    B2.bind('<Leave>', leaveButton)    
    B3border = tk.Frame(windowCont, bd=1, highlightbackground="black", highlightcolor=BTN_COLOR, highlightthickness=1) 
    B3 = tk.Button(B3border, text=" Apply ", font=DIR_FONT, bg='white', bd=0, highlightthickness=0, activebackground=BTN_COLOR, padx=8, pady=3, command = lambda: gensettingssave('open'))
    B3.pack(side = tk.LEFT)
    B3border.grid(row=0,column=2, padx=5, pady=5, sticky='e') 
    B3.bind('<Enter>', hoverButton)
    B3.bind('<Leave>', leaveButton)
    windowCont.rowconfigure(0, weight=1)
    windowCont.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    
    popup.columnconfigure(0, weight=1)
    popup.rowconfigure(0, weight=3, uniform='x')
    popup.rowconfigure(1, weight=1, uniform='x')

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (420, 300, ws/4, hs/4))
    popup.mainloop()

# ---------------
# training settings window    
# ---------------   
 
def trainsettings():
    global parser, SHOWRANGES, TRAINTOL, SHOWHK, SHOWACC, AUDIO, SCEN1, SCEN2, SCEN3, SCEN4
    SHOWRANGES = parser.getint('settings','SHOWRANGES')
    TRAINTOL = parser.getint('settings','TRAINTOL')
    SHOWHK = parser.getint('settings','SHOWHK')
    SHOWACC = parser.getint('settings','SHOWACC')
    AUDIO = parser.getint('settings','AUDIO')
    SCEN1 = parser.getint('settings','SCEN1')
    SCEN2 = parser.getint('settings','SCEN2')
    SCEN3 = parser.getint('settings','SCEN3')
    SCEN4 = parser.getint('settings','SCEN4')
    
    def trainsettingssave(flag):
        global SHOWRANGES, TRAINTOL, SHOWHK, SHOWACC, AUDIO, SCEN1, SCEN2, SCEN3, SCEN4
        
        SHOWRANGES = int(showr.get())
        TRAINTOL = int(tolEntry.get())
        SHOWHK = int(hotvar.get())
        SHOWACC = int(accvar.get())
        AUDIO = int(audiovar.get())
        SCEN1 = int(scenvar1.get())
        SCEN2 = int(scenvar2.get())
        SCEN3 = int(scenvar3.get())
        SCEN4 = int(scenvar4.get())
        
        if flag == 'close':
            popup.destroy()
            
        parser['settings']['SHOWRANGES'] = str(SHOWRANGES)
        parser['settings']['TRAINTOL'] = str(TRAINTOL)
        parser['settings']['SHOWHK'] = str(SHOWHK)
        parser['settings']['SHOWACC'] = str(SHOWACC)
        parser['settings']['AUDIO'] = str(AUDIO)
        parser['settings']['SCEN1'] = str(SCEN1)
        parser['settings']['SCEN2'] = str(SCEN2)
        parser['settings']['SCEN3'] = str(SCEN3)
        parser['settings']['SCEN4'] = str(SCEN4)
        
        with open('prefloptrain.ini','w') as configfile:
            parser.write(configfile)
        
        return
    
    popup = tk.Tk()  
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Preflop Trainer Settings")
    popup.configure(background=BG_COLOR)
       
    Optgroup = tk.LabelFrame(popup, text = 'Range Popup', padx = 5, pady = 5, background=BG_COLOR)
    Optgroup.grid(row=0,column=0, padx = 5, pady = 5, sticky='nsew')
    
    showr = tk.IntVar(master = popup)
    showr.set(SHOWRANGES)
    
    showranges1 = tk.Radiobutton(Optgroup, text = "Range popup appears after every hand", value=0, variable=showr, background=BG_COLOR, activebackground=BG_COLOR2)
    showranges2 = tk.Radiobutton(Optgroup, text = "Range popup appears if an error is made", value=1, variable=showr, background=BG_COLOR, activebackground=BG_COLOR2)
    showranges3 = tk.Radiobutton(Optgroup, text = "Range popup disabled", value=2, variable=showr, background=BG_COLOR, activebackground=BG_COLOR2)
  
    if showr.get() == 0:
        showranges1.select()
    elif showr.get() == 1:
        showranges2.select()
    else:
        showranges3.select()
        
    showranges1.pack(anchor='w')
    showranges2.pack(anchor='w')
    showranges3.pack(anchor='w')       

    Tolgroup = tk.LabelFrame(popup, text = 'Tolerance', padx = 5, pady = 5, background=BG_COLOR)
    Tolgroup.grid(row=1,column=0, padx = 5, pady = 5, sticky='nsew')
    
    tolLabel = tk.Label(Tolgroup, text = 'Tolerance for correct answer (%):', background=BG_COLOR)
    tolLabel.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    tolEntry = tk.Entry(Tolgroup, width=10, bd=0, highlightbackground="black", highlightthickness=1)
    tolEntry.insert(0, TRAINTOL)
    tolEntry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
    
    Showgroup = tk.LabelFrame(popup, text = 'Toggle (Requires Program Restart)', padx = 5, pady = 5, background=BG_COLOR)
    Showgroup.grid(row=2,column=0, padx = 5, pady = 5, sticky='nsew')
    
    hotvar = tk.IntVar(master = popup)
    accvar = tk.IntVar(master = popup)

    hotkeyBtn = tk.Checkbutton(Showgroup, text = 'Hotkey Information', variable=hotvar, background=BG_COLOR)
    accuracyBtn = tk.Checkbutton(Showgroup, text = 'Accuracy Tracking', variable=accvar, background=BG_COLOR)
    hotkeyBtn.pack(anchor='w')
    accuracyBtn.pack(anchor='w')
    
    if SHOWHK:
        hotkeyBtn.select()
    else:
        hotkeyBtn.deselect()
    if SHOWACC:
        accuracyBtn.select()
    else:
        accuracyBtn.deselect()
        
    Audiogroup = tk.LabelFrame(popup, text = 'Audio', padx = 5, pady = 5, background = BG_COLOR)
    Audiogroup.grid(row = 3, column = 0, padx =  5, pady = 5, sticky = 'nsew')
    audiovar = tk.IntVar(master = popup)
    audioBtn = tk.Checkbutton(Audiogroup, text = 'Play dealer and right/wrong sounds', variable = audiovar, background = BG_COLOR)
    audioBtn.pack(anchor = 'w')
    
    if AUDIO:
        audioBtn.select()
    else:
        audioBtn.deselect()
    
    Scenariogroup = tk.LabelFrame(popup, text = 'Practice Scenarios', padx = 5, pady = 5, background = BG_COLOR)
    Scenariogroup.grid(row=4, column=0, padx = 5, pady = 5, sticky = 'nsew')
    scenvar1 = tk.IntVar(master = popup)
    scenvar2 = tk.IntVar(master = popup)
    scenvar3 = tk.IntVar(master = popup)
    scenvar4 = tk.IntVar(master = popup)
    scenBtn1 = tk.Checkbutton(Scenariogroup, text = 'Open', variable = scenvar1, background = BG_COLOR)
    scenBtn2 = tk.Checkbutton(Scenariogroup, text = 'Facing Open', variable = scenvar2, background = BG_COLOR)
    scenBtn3 = tk.Checkbutton(Scenariogroup, text = 'Facing 3Bet', variable = scenvar3, background = BG_COLOR)
    scenBtn4 = tk.Checkbutton(Scenariogroup, text = 'Facing 4Bet', variable = scenvar4, background = BG_COLOR)
    scenBtn1.pack(anchor = 'w')
    scenBtn2.pack(anchor = 'w')
    scenBtn3.pack(anchor = 'w')
    scenBtn4.pack(anchor = 'w')
    
    if SCEN1:
        scenBtn1.select()
    else:
        scenBtn1.deselect()
    if SCEN2:
        scenBtn2.select()
    else:
        scenBtn2.deselect() 
    if SCEN3:
        scenBtn3.select()
    else:
        scenBtn3.deselect()
    if SCEN4:
        scenBtn4.select()
    else:
        scenBtn4.deselect()
        
    windowCont = tk.Frame(popup, bd=0, highlightbackground="black", highlightcolor=BTN_COLOR, highlightthickness=0, background=BG_COLOR)
    B1border = tk.Frame(windowCont, bd=1, highlightbackground="black", highlightcolor=BTN_COLOR, highlightthickness=1) 
    B1 = tk.Button(B1border, text="    OK    ", font=DIR_FONT, bg='white',bd=0, highlightthickness=0, activebackground=BTN_COLOR, padx=8, pady=3, command = lambda: trainsettingssave('close'))
    B1.pack(side = tk.RIGHT)
    B1border.grid(row=0,column=0, padx=5, pady=5, sticky='e') 
    B1.bind('<Enter>', hoverButton)
    B1.bind('<Leave>', leaveButton)
    B2border = tk.Frame(windowCont, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1) 
    B2 = tk.Button(B2border, text="Cancel", font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=8, pady=3, command = lambda: popup.destroy())
    B2.pack(side = tk.RIGHT)
    B2border.grid(row=0,column=1, padx=5, pady=5, sticky='e') 
    B2.bind('<Enter>', hoverButton)
    B2.bind('<Leave>', leaveButton)    
    B3border = tk.Frame(windowCont, bd=1, highlightbackground="black", highlightcolor=BTN_COLOR, highlightthickness=1) 
    B3 = tk.Button(B3border, text=" Apply ", font=DIR_FONT, bg='white', bd=0, highlightthickness=0, activebackground=BTN_COLOR, padx=8, pady=3, command = lambda: trainsettingssave('open'))
    B3.pack(side = tk.RIGHT)
    B3border.grid(row=0,column=2, padx=5, pady=5, sticky='e') 
    B3.bind('<Enter>', hoverButton)
    B3.bind('<Leave>', leaveButton)
    windowCont.rowconfigure(0, weight=1)
    windowCont.grid(row=5, column=0, padx=5, pady=5, sticky='e')
      
    popup.columnconfigure(0, weight=1)
    popup.rowconfigure([0,1,2,3,4], weight=3)
    popup.rowconfigure(5 ,weight=1, uniform='x')
    
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (420, 620, ws/4, hs/4))
    popup.mainloop()

def createRangePack():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Add New Range Pack")
    popup.resizable(0,0)
    popup.configure(background=BG_COLOR)
    
    label = tk.Label(popup, text='Range package name:', font=DIR_FONT, background=BG_COLOR)
    label.grid(row=0, column=0, padx=5, pady=5)
    entry = tk.Entry(popup, width=60, bd=0, highlightbackground="black",highlightthickness=1)
    entry.insert(0,'')
    entry.grid(row=0, column=1, padx=5, pady=5)
    
    B2border = tk.Frame(popup, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
    B2 = tk.Button(B2border, text="Cancel", command = lambda: popup.destroy(), font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=10, pady=2)
    B2.pack(side=tk.RIGHT)
    B2border.grid(row=1, column=2, sticky='N', padx=10, pady=5)
    B2.bind('<Enter>', hoverButton)
    B2.bind('<Leave>', leaveButton)
    
    B1border = tk.Frame(popup, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
    B1 = tk.Button(B1border, text="  Create  ", command = lambda: createRP(popup, entry), font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=9, pady=2)
    B1.pack(side=tk.RIGHT)
    B1border.grid(row=0, column=2, sticky='N', padx=10, pady=5)
    B1.bind('<Enter>', hoverButton)
    B1.bind('<Leave>', leaveButton)
       
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (640, 90, ws/2 - 320, hs/2 - 45))
    
    popup.mainloop()
    
def createRP(popup, entry):
    global rangedir
    rangedir = entry.get()
    try:
        os.mkdir(fdir + '\\Range Packages\\' + rangedir)
    except OSError:
        print ("Creation of the directory %s failed" % rangedir)
    else:
        print ("Successfully created the directory %s " % rangedir)
    
    pos = ['BB','SB','BN','CO','MP','EP']   
    
    for idx, pidx in enumerate(pos):
        f = open('Range Packages\\' + rangedir + "\\Call-" + pidx + ".txt", "w+")
        f.close()
        f = open('Range Packages\\' + rangedir + "\\Open-" + pidx + ".txt", "w+")
        f.close()
        for idx2, pidx2 in enumerate(pos):
            if idx2 > idx:
                f = open('Range Packages\\' + rangedir + "\\Flat-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + rangedir + "\\3Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + rangedir + "\\Call4bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + rangedir + "\\5Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
            if idx2 < idx:
                f = open('Range Packages\\' + rangedir + "\\Call3bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + rangedir + "\\4Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()         
    
    parser['settings']['Range Package'] = rangedir
    
    popup.destroy()
    
def saveRangePack():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Save Range Pack As")
    popup.resizable(0,0)
    popup.configure(background=BG_COLOR)
    
    label = tk.Label(popup, text='Range package name:', font=DIR_FONT, background=BG_COLOR)
    label.grid(row=0,column=0, padx=10, pady=5)
    entry = tk.Entry(popup, width=60, bd=0, highlightbackground="black",highlightthickness=1)
    entry.insert(0,'')
    entry.grid(row=0,column=1, padx=10, pady=5)
    
    B2border = tk.Frame(popup, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
    B2 = tk.Button(B2border, text="Cancel", command = lambda: popup.destroy(), font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=10, pady=2)
    B2.pack(side=tk.RIGHT)
    B2border.grid(row=1,column=2,sticky='N',padx=10,pady=5)
    B2.bind('<Enter>', hoverButton)
    B2.bind('<Leave>', leaveButton)
    
    B1border = tk.Frame(popup, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
    B1 = tk.Button(B1border, text="   Save   ", command = lambda: saveRP(popup, entry), font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=9, pady=2)
    B1.pack(side=tk.RIGHT)
    B1border.grid(row=0,column=2,sticky='N',padx=10,pady=5)
    B1.bind('<Enter>', hoverButton)
    B1.bind('<Leave>', leaveButton)
    
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (640, 90, ws/2 - 320, hs/2 - 45))
    
    popup.mainloop()

def saveRP(popup, entry):
    global rangedir
    rangedir_future = entry.get()
    try:
        os.mkdir(fdir + '\\Range Packages\\' + rangedir_future)
    except OSError:
        print ("Creation of the directory %s failed" % rangedir_future)
    else:
        print ("Successfully created the directory %s " % rangedir_future)
    
    copy_tree(fdir +'\\Range Packages\\' + rangedir, '\\Range Packages\\' + rangedir_future)
                
    rangedir = rangedir_future           
    popup.destroy()
    
def importRangePack():  
    global rangedir
    filename = filedialog.askdirectory(title = "Select Folder to Import Ranges From")
    rangedir = os.path.basename(filename)
    try:
        os.mkdir(fdir + '\\Range Packages\\' + rangedir)
    except OSError:
        print ("Creation of the directory %s failed" % rangedir)
    else:
        print ("Successfully created the directory %s " % rangedir)
    
    pos = ['BB','SB','BN','CO','MP','EP']   
    try:
        for idx, pidx in enumerate(pos):
                f = open(filename + "\\Call-" + pidx + ".txt")
                f.close()
                f = open(filename + "\\Open-" + pidx + ".txt")
                f.close()
                for idx2, pidx2 in enumerate(pos):
                    if idx2 > idx:
                        f = open(filename + "\\Flat-" + pidx + "vs" + pidx2 + ".txt")
                        f.close()
                        f = open(filename + "\\3Bet-" + pidx + "vs" + pidx2 + ".txt")
                        f.close()
                        f = open(filename + "\\Call4bet-" + pidx + "vs" + pidx2 + ".txt")
                        f.close()
                        f = open(filename + "\\5Bet-" + pidx + "vs" + pidx2 + ".txt")
                        f.close()
                    if idx2 < idx:
                        f = open(filename + "\\Call3bet-" + pidx + "vs" + pidx2 + ".txt")
                        f.close()
                        f = open(filename + "\\4Bet-" + pidx + "vs" + pidx2 + ".txt")
                        f.close()
        copy_tree(filename, rangedir)
    except OSError:
        print ("Importing range pack failed")
    else:
        print ("Successfully imported the range pack")
                
    
def bugReport():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Report Bug")
    popup.resizable(0,0)
    popup.configure(background=BG_COLOR)
    
    label = tk.Label(popup, text='Please send bug reports to jejmcclu@protonmail.com', font=DIR_FONT, background=BG_COLOR)
    label.grid(row=0,column=0,sticky='NSEW', padx=15, pady=5)
    
    B1border = tk.Frame(popup, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
    B1 = tk.Button(B1border, text="  OK  ", command = lambda: popup.destroy(), font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=10, pady=2)
    B1.pack(side=tk.RIGHT)
    B1border.grid(row=1,column=0,sticky='N',padx=15,pady=5)
    B1.bind('<Enter>', hoverButton)
    B1.bind('<Leave>', leaveButton)
    
    popup.columnconfigure(0,weight=1, uniform='x')
    popup.rowconfigure(0,weight=1, uniform='x')
    popup.rowconfigure(1,weight=1, uniform='x')
 
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (ws/4, hs/10, 3*ws/8, 9*hs/20))
    
    popup.mainloop()
    
def docsReport():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Documentation")
    popup.configure(background=BG_COLOR)   
    
    # paned window
    panedwindow = tk.PanedWindow(popup, bd=4, bg='white', showhandle=False, relief="flat")
    panedwindow.grid(row=0,column=0,sticky='NSEW', pady=5, padx=15)
        
    fileEXP = tk.Frame(panedwindow,bd=0,bg="white",highlightbackground="black", highlightcolor="black", highlightthickness=0)
      
    fileTree = ttk.Treeview(fileEXP, selectmode='browse')
    vsb = tk.Scrollbar(fileEXP, orient="vertical", command=fileTree.yview)
    fileTree["columns"] = ("one")
    fileTree.column("#0", width=125, minwidth=100, stretch=0)
    fileTree.heading("#0", text="Topics", anchor=tk.W) 
    fileTree.insert("",0, "dir1",text="Preflop Trainer",values=(""))
    fileTree.insert("",1, "dir2",text="Range Editor",values=(""))
    fileTree.insert("",2, "dir3",text="Settings",values=(""))
    fileTree.insert("","end", "dir4",text="Range Packages",values=("")) 
    fileTree.insert("dir1", "end", 'A1', text="Topic1",tags = ("0","EP","BB"))
    fileTree.insert("dir1", "end", 'B1', text="Topic2",tags = ("0","MP","BB"))
    fileTree.insert("dir2", "end", 'A2', text="Topic1",tags = ("0","EP","BB"))
    fileTree.insert("dir2", "end", 'B2', text="Topic2",tags = ("0","MP","BB"))
    fileTree.insert("dir3", "end", 'A3', text="Topic1",tags = ("0","EP","BB"))
    fileTree.insert("dir3", "end", 'B3', text="Topic2",tags = ("0","MP","BB"))
    fileTree.insert("dir4", "end", 'A4', text="Topic1",tags = ("0","EP","BB"))
    fileTree.insert("dir4", "end", 'B4', text="Topic2",tags = ("0","MP","BB"))     
    fileTree.bind("<Double-1>", onDoubleClick_docs)
    fileTree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    fileTree.configure(yscrollcommand=vsb.set)
    fileEXP.columnconfigure(0,weight=1)
    fileEXP.columnconfigure(1,weight=1)
    fileEXP.rowconfigure(0,weight=1)
    
    panedwindow.add(fileEXP)
    
    docText = tk.Frame(panedwindow,padx=2,pady=2,bg="white")
    
    txt = tk.Text(docText,bd=0,bg="white",highlightbackground="black", highlightcolor="black", highlightthickness=1)
    txt.tag_configure('title', font=BOLD_FONT)
    txt.tag_configure('main', font=DIR_FONT)
    
    txt.insert(tk.INSERT,"Preflop Trainer\n",'title')
    txt.insert(tk.INSERT,"""\nThe preflop trainer randomly deals you into preflop practice scenarios, where you can choose to purely fold, purely call, or purely raise your hand, or input any mixed frequencies for the three actions. Your action is then compared to the currently actived range package in the range editor, and feedback is given on whether your action was correct. \n\nTo begin, press the "Start Training" button. A hand will be dealt to you, and your action needs to be input at the bottom of the screen, or you can skip the hand by pressing the "Deal Next Hand" button at the top of the screen. If your desired action is at 100% frequency, you can press one of the "Pure Raise", "Pure Call", or "Pure Fold" buttons. If a mixed frequency is desired, the mixed frequency slider must be used. To move the divider between the raise/call frequencies, click and drag with the left mouse button. To move the divider between the call/fold frequencies, click and drag with the right mouse button. After the desired frequencies have been specified, press the "Enter" button. \n\nAlternatively, instead of selecting the buttons with the mouse, the following pre-assigned hotkeys may be used. <spacebar> to deal the next hand, <r> to pure raise, <c> to pure call, and <f> to pure fold.""" ,'main')
    
    txt.config(state='disabled')
    txt.grid(row=0, column=0, sticky="nsew")
    scrollb = ttk.Scrollbar(docText, orient="vertical", command=txt.yview)
    scrollb.grid(row=0, column=1, sticky='ns')
    txt['yscrollcommand'] = scrollb.set
    docText.columnconfigure(0,weight=1)
    docText.columnconfigure(1,weight=1)
    docText.rowconfigure(0,weight=1)
    
    panedwindow.add(docText)
    
    B1border = tk.Frame(popup, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
    B1 = tk.Button(B1border, text="  OK  ", command = lambda: popup.destroy(), font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=10, pady=2)
    B1.pack(side=tk.RIGHT)
    B1border.grid(row=1,column=0,sticky='E',padx=15,pady=5)
    B1.bind('<Enter>', hoverButton)
    B1.bind('<Leave>', leaveButton)
    
    popup.columnconfigure(0,weight=1, uniform='x')
    popup.rowconfigure(0,weight=10, uniform='x')
    popup.rowconfigure(1,weight=1, uniform='x')
    
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (ws/2, hs/2, ws/4, hs/4))
    
    popup.mainloop()

def onDoubleClick_docs(event):
    return
        
def trainPos(val):
    global trainIdx
    trainIdx = val

def readRangefile(filename):
    range_array = [[0 for x in range(13)] for x in range(13)] 
    f = open(filename)
    split_contents = f.read().split(",") 
    for freq in split_contents:
        if freq:
            c1 = inv_deck[freq[0]] 
            c2 = inv_deck[freq[1]]
                
            if len(freq) < 4:
                if len(freq) == 3:
                    if freq[2] == "s":
                        range_array[12-c2][12-c1] = 100
                    if freq[2] == "o":
                        range_array[12-c1][12-c2] = 100
                else:
                    range_array[12-c2][12-c1] = 100
                    range_array[12-c1][12-c2] = 100
            else:
                if freq[2] == ":":
                    range_array[12-c2][12-c1] = int(float(freq[3:])*100)
                    range_array[12-c1][12-c2] = int(float(freq[3:])*100)
                elif freq[2] == "s":
                    range_array[12-c2][12-c1] = int(float(freq[4:])*100)
                elif freq[2] == "o":
                    range_array[12-c1][12-c2] = int(float(freq[4:])*100)
    f.close() 
    return range_array

def readRange(CR, myScen, myPos1, myPos2):
    global rangedir
    range_array = [[0 for x in range(13)] for x in range(13)] 
    
    if myScen == 0:
        f = open(fdir + '\\Range Packages\\' + rangedir + "\\" + Scendict[CR + str(myScen)] + myPos1 + ".txt")
    else:
        f = open(fdir + '\\Range Packages\\' + rangedir + "\\" + Scendict[CR + str(myScen)] + myPos1 + "vs" + myPos2 + ".txt")
           
    split_contents = f.read().split(",")             
 
    for freq in split_contents:
        if freq:
            c1 = inv_deck[freq[0]] 
            c2 = inv_deck[freq[1]]
                
            if len(freq) < 4:
                if len(freq) == 3:
                    if freq[2] == "s":
                        range_array[12-c2][12-c1] = 100
                    if freq[2] == "o":
                        range_array[12-c1][12-c2] = 100
                else:
                    range_array[12-c2][12-c1] = 100
                    range_array[12-c1][12-c2] = 100
            else:
                if freq[2] == ":":
                    range_array[12-c2][12-c1] = int(float(freq[3:])*100)
                    range_array[12-c1][12-c2] = int(float(freq[3:])*100)
                elif freq[2] == "s":
                    range_array[12-c2][12-c1] = int(float(freq[4:])*100)
                elif freq[2] == "o":
                    range_array[12-c1][12-c2] = int(float(freq[4:])*100)
    f.close()              
    return range_array

def writeRange(CR, myScen, myPos1, myPos2, range_array):
    global rangedir
    if myScen == 0:
        f = open(fdir + '\\Range Packages\\' + rangedir + "\\" + Scendict[CR + str(myScen)] + myPos1 + ".txt", "w+")
    else:
        f = open(fdir + '\\Range Packages\\' + rangedir + "\\" + Scendict[CR + str(myScen)] + myPos1 + "vs" + myPos2 + ".txt", "w+")

    fstart = ""
    
    for i in range(12,-1,-1):
        
        if range_array[12-i][12-i] == 100:
            f.write(fstart + deck[i] + deck[i])
            fstart = ","
        elif range_array[12-i][12-i] == 0:
            pass
        else:
            f.write(fstart + deck[i] + deck[i] + ":" + str(range_array[12-i][12-i]/100))
            fstart = ","
            
    for j in range(12,-1,-1):
        for i in range(12,-1,-1):     
            if i == j:
                pass
            elif range_array[12-i][12-j] == 100:
                if i > j:
                    f.write(fstart + deck[i] + deck[j] + "o")
                else:
                    f.write(fstart + deck[j] + deck[i] + "s")
                fstart = ","
            elif range_array[12-i][12-j] == 0:
                pass
            else:
                if i > j:
                    f.write(fstart + deck[i] + deck[j] + "o" + ":" + str(range_array[12-i][12-j]/100))
                else:
                    f.write(fstart + deck[j] + deck[i] + "s" + ":" + str(range_array[12-i][12-j]/100))
                fstart = ","    
    f.close()
    return

def hoverButton(event):
    event.widget.configure(bg=BG_COLOR2)
        
def leaveButton(event):
    event.widget.configure(bg=BG_COLOR)  
    
# ---------------
# splash window    
# ---------------   
    
class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.overrideredirect(True)  
        splashcanvas = tk.Canvas(self, width=480, height=480, bg="white", bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=0)
        splashimg = tk.PhotoImage(file = os.getcwd() + '\\Images\\splash_alt.png')
        splashcanvas.create_image(0, 0, anchor='nw', image=splashimg)
        splashcanvas.pack()
        loadlabel = tk.Label(self, text='Loading...', font=DIR_FONT, background=BG_COLOR, activebackground=BTN_COLOR, bd=0, fg=FONT_COLOR, justify="left")
        loadlabel.pack()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - ((480)/2)
        y = (hs/2) - ((480)/2)
        self.geometry("%dx%d+%d+%d" % (480, 480, x, y))
        self.title("Splash")
        self.lift()
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-alpha", 1)
        self.wm_attributes("-transparentcolor", "white")
        self.update()

# ---------------
# init window    
# ---------------   
        
class PreflopTrain(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.withdraw()
        splash = Splash(self)
        
        tk.Tk.iconbitmap(self, "icon.ico")
        tk.Tk.wm_title(self, "6-max Preflop Range Training")
        
        container = tk.Frame(self)     
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Create New Range Pack", command= lambda: createRangePack())
        filemenu.add_command(label="Save Range Pack As", command=lambda: saveRangePack())
        filemenu.add_command(label="Import Range Pack", command=lambda: importRangePack())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Preflop Trainer", command = lambda: trainsettings())
        settingsmenu.add_command(label="Ranger Editor", command = lambda: gensettings())
        menubar.add_cascade(label="Settings", menu=settingsmenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Documentation", command=lambda: docsReport())
        helpmenu.add_command(label="Report Bug", command=lambda: bugReport())
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        #optionmenu = tk.Menu(menubar, tearoff=0)
        #optionmenu.add_checkbutton(label="All", command = lambda: trainPos(4))
        #optionmenu.add_checkbutton(label="Open Ranges", command = lambda: trainPos(0))
        #optionmenu.add_checkbutton(label="Facing Open Ranges", command = lambda: trainPos(1))
        #optionmenu.add_checkbutton(label="Facing 3bet Ranges", command = lambda: trainPos(2))
        #optionmenu.add_checkbutton(label="Facing 4bet Ranges", command = lambda: trainPos(3))
        #menubar.add_cascade(label="Training Positions", menu=optionmenu)
        
        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        
        for F in (StartPage, RangeEdit):
            
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
        
        time.sleep(1)
        splash.destroy()
        self.deiconify()
          
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
    def onExit(self):
        self.quit()
        self.destroy()
        
# ---------------
# training window    
# ---------------  
         
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        global rangedir, SHOWHK, SHOWACC, SCEN1, SCEN2, SCEN3, SCEN4, AUDIO
        tk.Frame.__init__(self, parent)
        self.configure(bg=BG_COLOR)
        
        # *** Tab Navigation ***
        self.switchframe = tk.Frame(self, bd=0, bg=BG_COLOR, highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0)
        self.labelborder = tk.Frame(self.switchframe, bd=0, highlightbackground=BG_COLOR, highlightcolor=BTN_COLOR, highlightthickness=1)    
        label = tk.Button(self.labelborder, text=' Preflop Trainer ', font=DIR_FONT, background=BG_COLOR, activebackground=BTN_COLOR, bd=0, fg=FONT_COLOR)
        label.pack(side = tk.LEFT)
        self.labelborder.pack(side=tk.LEFT) 
        switchbutton = tk.Button(self.switchframe, text=' Range Editor ', font=DIR_FONT, background=BG_COLOR, activebackground = BTN_COLOR, command=lambda: controller.show_frame(RangeEdit), fg=FONT_COLOR,anchor='w',relief='sunken')
        switchbutton.pack(side = tk.LEFT)
        switchbutton.bind('<Enter>', self.hoverButton)
        switchbutton.bind('<Leave>', self.leaveButton)
        self.switchframe.grid(row=0,column=0,sticky='NEW')
        
        # *** Text and Accuracy *** #
        textframe = tk.Frame(self, bd=0, bg=BG_COLOR, highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0)
        hotkeytext = tk.Label(textframe,text='Press "f" to pure fold\nPress "c" to pure call\nPress "r" to pure raise\nPress "spacebar" to deal new hand',font=DIR_FONT, background=BG_COLOR, activebackground=BTN_COLOR, bd=0, fg=FONT_COLOR, justify="left")
        hotkeytext.grid(row=0,column=0,padx=5,pady=5,sticky='W')
        if SHOWHK == 0:
            hotkeytext.grid_forget()
        
        self.dealhandtext = tk.StringVar()
        self.dealhandtext.set("  Start Training  ")
        self.button_1border = tk.Frame(textframe, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        self.button_1 = tk.Button(self.button_1border, textvariable=self.dealhandtext, command=self.start_train, font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5)
        self.button_1.pack()
        self.button_1border.grid(row=0,column=1,padx=5,pady=5) 
        self.button_1.bind('<Enter>', self.hoverButton)
        self.button_1.bind('<Leave>', self.leaveButton)
        
        accframe = tk.Frame(textframe, bd=0, bg=BG_COLOR, highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0)
        self.accout = tk.StringVar()
        self.accout.set('undef\n (0/0)')
        accuracyvalue = tk.Label(accframe,textvariable=self.accout,font=DIR_FONT, background=BG_COLOR, activebackground=BTN_COLOR, bd=0, fg=FONT_COLOR)
        accuracyvalue.grid(row=0,column=1,sticky='W')
        accuracytext = tk.Label(accframe,text='Accuracy:\n',font=DIR_FONT, background=BG_COLOR, activebackground=BTN_COLOR, bd=0, fg=FONT_COLOR)
        accuracytext.grid(row=0,column=0,sticky='E')
        accframe.grid(row=0,column=2,padx=5,pady=5,sticky='E')
        
        if SHOWACC == 0:
            accframe.grid_forget()
            
        textframe.rowconfigure(0,weight=1)
        textframe.columnconfigure([0,1,2],weight=1,uniform='x')
        textframe.grid(row=1,column=0,sticky='NEW')
        
        # *** Table Canvas ***
        plotframe = tk.Frame(self, bd=0, bg=BG_COLOR, highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0) 
        self.tablereplayer = TableReplay(plotframe,'CO','EP',3,'AdAs')
        self.tablereplayer.grid(row=0, column=1,sticky='NSEW')
        plotframe.rowconfigure(0,weight=2)
        plotframe.grid(row=2,column=0,padx=5,pady=5)
        
        # *** Button Controls ***
        self.trainingInterface = tk.Frame(self,bd=0,bg=BG_COLOR,highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0)
        
        self.sgraph = sliderGraphical(self.trainingInterface)
        self.sgraph.grid(row=0,column=0,columnspan=3,padx=0,pady=1)
        self.sgraph.grid_remove()
        
        self.inp_raise = tk.StringVar(self)
        self.inp_raise.set("0")
        self.inp_call = tk.StringVar(self)
        self.inp_call.set("0")
        self.inp_fold = tk.StringVar(self)
        self.inp_fold.set("0")
        
        self.okayBtnborder = tk.Frame(self.trainingInterface, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        self.okayBtn = tk.Button(self.okayBtnborder, text="Enter", command=self.getOptions, font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=15, pady=1)
        self.okayBtn.pack(side=tk.RIGHT)
        self.okayBtnborder.grid(row=0,column=3, padx=5, pady=1, sticky='S')
        self.okayBtn.bind('<Enter>', self.hoverButton)
        self.okayBtn.bind('<Leave>', self.leaveButton)
        self.okayBtnborder.grid_remove()
        
        self.rButton_brd = tk.Frame(self.trainingInterface, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR, bg='white',highlightthickness=1)
        self.cButton_brd = tk.Frame(self.trainingInterface, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR, bg='white',highlightthickness=1)
        self.fButton_brd = tk.Frame(self.trainingInterface, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR, bg='white',highlightthickness=1)
        self.rButton = tk.Button(self.rButton_brd, text='         Pure Raise         ', font=DIR_FONT, bg='white', fg='black', bd=0,highlightthickness=0, padx=8, pady=0, command=lambda: self.pureraise(self))
        self.cButton = tk.Button(self.cButton_brd, text='         Pure Call         ', font=DIR_FONT, bg='white', fg='black', bd=0,highlightthickness=0, padx=8, pady=0, command=lambda: self.purecall(self))
        self.fButton = tk.Button(self.fButton_brd, text='         Pure Fold         ', font=DIR_FONT, bg='white', fg='black', bd=0,highlightthickness=0, padx=8, pady=0, command=lambda: self.purefold(self))
        self.rButton.pack()
        self.cButton.pack()
        self.fButton.pack()
        self.rButton_brd.grid(row=1,column=0,padx=1,pady=0)
        self.cButton_brd.grid(row=1,column=1,padx=1,pady=0)
        self.fButton_brd.grid(row=1,column=2,padx=1,pady=0)
        self.rButton.bind('<Enter>', self.hoverButton)
        self.rButton.bind('<Leave>', self.leaveButton)
        self.cButton.bind('<Enter>', self.hoverButton)
        self.cButton.bind('<Leave>', self.leaveButton)
        self.fButton.bind('<Enter>', self.hoverButton)
        self.fButton.bind('<Leave>', self.leaveButton)
        self.rButton_brd.grid_remove()
        self.cButton_brd.grid_remove()
        self.fButton_brd.grid_remove()
        
        self.trainingInterface.grid(row=3,column=0,sticky='N')
        
        # *** Status Bar ***
        self.statusvar = tk.StringVar()
        self.statusvar.set('Status Idle')
        self.statuslabel = tk.Label(self, textvariable=self.statusvar, bd=1, relief='sunken', anchor='w')
        self.statuslabel.grid(row=3,column=0,sticky='SEW')
        
        # *** grid configure ***
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1, uniform='x')
        self.rowconfigure(1, weight=2, uniform='x')
        self.rowconfigure(2, weight=10, uniform='x')
        self.rowconfigure(3, weight=3, uniform='x')
        
        # ** key binds ***
        self.bind_all("f", self.purefold)
        self.bind_all("c", self.purecall)
        self.bind_all("r", self.pureraise)
        self.bind_all("<space>", self.newhand)
    
    # training functions
    def purefold(self,event):
        self.sgraph.rfreq = 0
        self.sgraph.cfreq = 0
        self.getOptions()
        
    def purecall(self,event):
        self.sgraph.rfreq = 0
        self.sgraph.cfreq = 100
        self.getOptions()
        
    def pureraise(self,event):
        self.sgraph.rfreq = 100
        self.sgraph.cfreq = 0
        self.getOptions()
        
    def newhand(self,event):
        self.start_train() 
    
    def hoverButton(self, event):
        event.widget.configure(bg=BG_COLOR2)
        
    def leaveButton(self, event):
        event.widget.configure(bg=BG_COLOR)
        
    def getOptions(self):
        global rangedir, SHOWRANGES, TRAINTOL
        self.inp_fold.set("Fold: " + str(100 - int(self.inp_call.get()) - int(self.inp_raise.get())))
        
        global trueraise
        global save_inp_raise
        global save_inp_call
        global myHand_s
        global Correct, Num
        
        save_inp_raise = int(self.sgraph.rfreq)
        save_inp_call = int(self.sgraph.cfreq)
               
        if myHand[1] == myHand[3]:
            myHand_s = myHand[0] + myHand[2] + "s"
        else:
            myHand_s = myHand[0] + myHand[2]
        
        # convert range strings to array data
        raise_freq = readRange("R", myPos_idx, myPos_p1, myPos_p2)
        call_freq = readRange("C", myPos_idx, myPos_p1, myPos_p2) 
        
        if myHand[1] == myHand[3]:
            hand_j = 12-inv_deck[myHand[2]]
            hand_i = 12-inv_deck[myHand[0]]
        else:
            hand_j = 12-inv_deck[myHand[0]]
            hand_i = 12-inv_deck[myHand[2]]
         
        trueraise = raise_freq[hand_j][hand_i]
        truecall = call_freq[hand_j][hand_i]
        
        # compare and determine right/wrong
        if abs(int(trueraise) - int(save_inp_raise)) <= TRAINTOL and abs(int(truecall) - int(save_inp_call)) <= TRAINTOL:
            self.statusvar.set("Correct!")
            if AUDIO:
                playsound('Audio\\sfx_correct.wav')
            Correct += 1
            Num += 1 
            Acc = 100*Correct/Num
            self.accout.set(f'{Acc:.1f}' + '%\n' + '(' + str(Correct) + '/' + str(Num) + ')')
            if SHOWRANGES == 0:
                self.rangepopup(raise_freq, call_freq, hand_i, hand_j)  
            self.start_train()
        else:
            self.statusvar.set("Wrong! Raise: " + str(trueraise) + "%  and Call: " + str(truecall) + "%")
            if AUDIO:
                playsound('Audio\\sfx_error.wav')
            Num += 1 
            Acc = 100*Correct/Num
            self.accout.set(f'{Acc:.1f}' + '%\n' + '(' + str(Correct) + '/' + str(Num) + ')')
            if SHOWRANGES < 2:
                self.rangepopup(raise_freq, call_freq, hand_i, hand_j) 
            else:
                self.start_train()
    
    def start_train(self):    
        global myPos_idx, fdir, myPos_p1, myPos_p2, myHand, deck, inv_deck, rangedir, SCEN1, SCEN2, SCEN3, SCEN4
            
        self.dealhandtext.set("Deal Next Hand")
        
        # Bring in graphical slider options
        self.rButton_brd.grid()
        self.cButton_brd.grid()
        self.fButton_brd.grid()
        self.okayBtnborder.grid()
        self.sgraph.grid()
        
        # Randomly determine positions and deal hands within range
        scen_check = [SCEN1, SCEN2, SCEN3, SCEN4]
        
        if scen_check == [0,0,0,0]:
            self.statusvar.set('All training scenarios have been deselected, and no hand dealt')
            return
        [myPos_idx, myPos_p1, myPos_p2, myPos_p3] = DealPos() 
        while scen_check[myPos_idx] == 0:
            [myPos_idx, myPos_p1, myPos_p2, myPos_p3] = DealPos() 
        
        myHand = DealHand()
            
        # check if hand is within proper range given situation or redeal
        if myPos_idx == 2:
            f = open(fdir + "\\Range Packages\\" + rangedir + "\\" + "Open-" + myPos_p1 + ".txt")
            contents = f.read()
            flag = InRange(myHand, contents)
            while not flag:
                myHand = DealHand()
                flag = InRange(myHand, contents)
             
        elif myPos_idx == 3:
            f = open(fdir + "\\Range Packages\\" + rangedir + "\\3Bet-" + myPos_p1 + "vs" + myPos_p2 + ".txt")
            contents = f.read()
            flag = InRange(myHand, contents)
            while not flag:
                myHand = DealHand()
                flag = InRange(myHand, contents)

        # update table replayer
        self.tablereplayer.herocards = myHand
        self.tablereplayer.heropos = myPos_p1
        self.tablereplayer.vilpos = myPos_p2
        self.tablereplayer.situation_index = myPos_idx
        self.tablereplayer.update()
        
        # update text training label
        if myPos_idx == 0:
            self.statusvar.set('Dealt ' + myHand + ' in ' + myPos_p1 + ' - Open?')
        elif myPos_idx == 1:
            self.statusvar.set('Dealt ' + myHand + ' in ' + myPos_p1 + ' - ' + myPos_p3 + ' from ' + myPos_p2)
        elif myPos_idx == 2:
            self.statusvar.set('Dealt ' + myHand + ' in ' + myPos_p1 + ' - ' + myPos_p3 + ' from ' + myPos_p2)
        elif myPos_idx == 3:
            self.statusvar.set('Dealt ' + myHand + ' in ' + myPos_p1 + ' - ' + myPos_p3 + ' from ' + myPos_p2)
        if AUDIO:
            playsound('Audio\\deal.wav')
        
    def rangepopup(self, raise_freq, call_freq, hi, hj):
        self.rpopup = tk.Toplevel()  
        tk.Tk.iconbitmap(self.rpopup, "icon.ico")
        
        if myPos_idx == 0:
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Open')
        elif myPos_idx == 1:  
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Facing Open from ' + myPos_p2)
        elif myPos_idx == 2:
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Facing 3Bet from ' + myPos_p2)
        elif myPos_idx == 3:
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Facing 4Bet from ' + myPos_p2)
        
        self.rpopup.configure(background=BG_COLOR) 
        self.raiseExp = RaiseViewer(self.rpopup)
        self.callExp = CallViewer(self.rpopup)
        self.callExp.lock = True
        self.raiseExp.lock = True
        self.raiseExp.grid(row=1,column=0,sticky='NSEW',padx=15,pady=5)
        self.callExp.grid(row=1,column=1,sticky='NSEW',padx=15,pady=5) 
        raiselabel = tk.Label(self.rpopup,text='Raise Range',font=DIR_FONT, background='white',activebackground=BTN_COLOR,bd=0)
        raiselabel.grid(row=0,column=0,sticky='W',padx=15,pady=5)
        calllabel = tk.Label(self.rpopup,text='Call Range',font=DIR_FONT, background='white',activebackground=BTN_COLOR,bd=0)
        calllabel.grid(row=0,column=1,sticky='W',padx=15,pady=5)
        
        self.raiseExp.weights = raise_freq
        self.callExp.weights = call_freq
        self.raiseExp.update()
        self.callExp.update()
        self.raiseExp.handgrid[hj][hi].configure(bd=3)
        self.callExp.handgrid[hj][hi].configure(bd=3)
           
        B1border = tk.Frame(self.rpopup, bd=1, highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        B1 = tk.Button(B1border, text="  OK  ", command = lambda: self.popupexit(self.rpopup), font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=10, pady=2)
        B1.pack(side=tk.RIGHT)
        B1border.grid(row=2,column=1,sticky='E',padx=15,pady=5)
        B1.bind('<Enter>', self.hoverButton)
        B1.bind('<Leave>', self.leaveButton)
        
        self.rpopup.columnconfigure([0,1],weight=1, uniform='x')
        self.rpopup.rowconfigure(0,weight=1, uniform='x')
        self.rpopup.rowconfigure(1,weight=20, uniform='x')
        self.rpopup.rowconfigure(2,weight=2, uniform='x')

        ws = self.rpopup.winfo_screenwidth()
        hs = self.rpopup.winfo_screenheight()

        self.rpopup.geometry('%dx%d+%d+%d' % (ws/2+ws/16, hs/2+hs/16, ws/4-ws/32, hs/4-hs/32))
        self.rpopup.mainloop()
    
    def popupexit(self, popup):
        popup.destroy()
        self.start_train()
    
        
# -------------------
# range editor window    
# -------------------
         
class RangeEdit(tk.Frame):
    
    def __init__(self, parent, controller):
        global rangedir, RWEIGHT
        tk.Frame.__init__(self, parent)
        self.configure(bg="white")
        
        self.switchframe = tk.Frame(self,bd=0,bg="white",highlightbackground="white", highlightcolor="white", highlightthickness=0)
        
        switchbutton = tk.Button(self.switchframe, text=' Preflop Trainer ', font=DIR_FONT, background='white', activebackground = BTN_COLOR, command=lambda: controller.show_frame(StartPage),anchor='w',relief='sunken')
        switchbutton.pack(side = tk.LEFT)
        switchbutton.bind('<Enter>', self.hoverButton)
        switchbutton.bind('<Leave>', self.leaveButton)
        self.labelborder = tk.Frame(self.switchframe, bd=0,highlightbackground="white",highlightcolor=BTN_COLOR, highlightthickness=0)    
        label = tk.Button(self.labelborder, text=' Range Editor ', font=DIR_FONT, background='white', activebackground=BTN_COLOR, bd=0)
        label.pack(side = tk.LEFT)
        self.labelborder.pack(side=tk.LEFT) 
        self.switchframe.grid(row=0,column=0,sticky='NW',columnspan=2)
        
        # paned window
        panedwindow = tk.PanedWindow(self, bd=4, bg='white', showhandle=False, relief="flat")
        panedwindow.grid(row=1,column=0,sticky='NSEW', pady=5, padx=5)
        
        self.fileEXP = tk.Frame(panedwindow,bd=0,bg="white",highlightbackground="black", highlightcolor="black", highlightthickness=0)
      
        self.fileTree = ttk.Treeview(self.fileEXP, selectmode='browse')
        self.vsb = tk.Scrollbar(self.fileEXP, orient="vertical", command=self.fileTree.yview)
        
        self.fileTree["columns"] = ("one")
        self.fileTree.column("#0", width=125, minwidth=100, stretch=0)
        self.fileTree.column("one", width=125, minwidth=100, stretch=0)
        self.fileTree.heading("#0", text="Positions", anchor=tk.W)
        self.fileTree.heading("one", text="Date Modified", anchor=tk.W)
        
        self.fileTree.insert("",0, "dir1",text="Open",values=(""))
        self.fileTree.insert("",1, "dir2",text="Facing Open",values=(""))
        self.fileTree.insert("",2, "dir3",text="Facing 3Bet",values=(""))
        self.fileTree.insert("","end", "dir4",text="Facing 4Bet",values=(""))
        
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Open-EP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call-EP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'A', text="EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","EP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Open-MP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call-MP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'B', text="MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","MP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Open-CO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call-CO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'C', text="CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","CO","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Open-BN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call-BN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'D', text="BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","BN","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Open-SB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call-SB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'E', text="SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","SB","BB"))
        
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-MPvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-MPvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'A1', text="MP vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","MP","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-COvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-COvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'B1', text="CO vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","CO","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-COvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-COvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'C1', text="CO vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","CO","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BNvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BNvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'D1', text="BN vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BN","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BNvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BNvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'E1', text="BN vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BN","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BNvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BNvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'F1', text="BN vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BN","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-SBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-SBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'G1', text="SB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-SBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-SBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'H1', text="SB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-SBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-SBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'I1', text="SB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-SBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-SBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'J1', text="SB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","BN")) 
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'K1', text="BB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'L1', text="BB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'M1', text="BB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'N1', text="BB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","BN"))    
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\3Bet-BBvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Flat-BBvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'O1', text="BB vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","SB"))  
 
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-EPvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-EPvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'A2', text="EP vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-EPvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-EPvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'B2', text="EP vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-EPvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-EPvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'C2', text="EP vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-EPvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-EPvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'D2', text="EP vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-EPvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-EPvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'E2', text="EP vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-MPvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-MPvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'F2', text="MP vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-MPvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-MPvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'G2', text="MP vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-MPvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-MPvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'H2', text="MP vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-MPvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-MPvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'I2', text="MP vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-COvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-COvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'J2', text="CO vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","CO","BN")) 
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-COvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-COvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'K2', text="CO vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","CO","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-COvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-COvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'L2', text="CO vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","CO","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-BNvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-BNvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'M2', text="BN vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","BN","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-BNvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-BNvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'N2', text="BN vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","BN","BB"))   
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\4Bet-SBvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call3bet-SBvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'O2', text="SB vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","SB","BB")) 
        
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-MPvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-MPvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'A3', text="MP vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","MP","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-COvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-COvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'B3', text="CO vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","CO","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-COvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-COvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'C3', text="CO vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","CO","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BNvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BNvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'D3', text="BN vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BN","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BNvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BNvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'E3', text="BN vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BN","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BNvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BNvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'F3', text="BN vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BN","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-SBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-SBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'G3', text="SB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-SBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-SBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'H3', text="SB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-SBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-SBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'I3', text="SB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-SBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-SBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'J3', text="SB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","BN")) 
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'K3', text="BB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'L3', text="BB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'M3', text="BB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'N3', text="BB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","BN"))   
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\5Bet-BBvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + rangedir + '\\Call4bet-BBvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'O3', text="BB vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","SB"))      
        
        self.fileTree.bind("<Double-1>", self.OnDoubleClick)
        
        self.fileTree.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        self.fileTree.configure(yscrollcommand=self.vsb.set)
        panedwindow.add(self.fileEXP)
        
        rangeExplorer = tk.Frame(panedwindow,padx=5,pady=5,bg="white", width = 1200, height = 600) 
        rangeExplorer.grid_propagate(False)
            
        self.raiseExp = RaiseViewer(rangeExplorer)
        self.callExp = CallViewer(rangeExplorer)
        self.callExp.grid(row=1,column=1,sticky='NSEW',padx=5,pady=5) 
        self.raiseExp.grid(row=1,column=0,sticky='NSEW',padx=5,pady=5)
        self.callExp.lock = True
        self.raiseExp.lock = True
        self.callExp.increment = RWEIGHT
        self.raiseExp.increment = RWEIGHT
        
        raiselabel = tk.Label(rangeExplorer,text='Raise Range',font=DIR_FONT, background='white',activebackground=BTN_COLOR,bd=0)
        raiselabel.grid(row=0,column=0,sticky='W',padx=5,pady=5)
        raiseclearborder = tk.Frame(rangeExplorer, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        raiseclearbtn = tk.Button(raiseclearborder, text='Clear Range', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command=self.raiseExp.clear)
        raiseclearbtn.pack(side = tk.LEFT)
        raiseclearborder.grid(row=0,column=0, padx=5, pady=5) 
        raiseclearbtn.bind('<Enter>', self.hoverButton)
        raiseclearbtn.bind('<Leave>', self.leaveButton)
        raiseselectborder = tk.Frame(rangeExplorer, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        raiseselectbtn = tk.Button(raiseselectborder, text='Select All', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command=self.raiseExp.selectall)
        raiseselectbtn.pack(side = tk.LEFT)
        raiseselectborder.grid(row=0,column=0,sticky='E', padx=5, pady=5) 
        raiseselectbtn.bind('<Enter>', self.hoverButton)
        raiseselectbtn.bind('<Leave>', self.leaveButton)
        calllabel = tk.Label(rangeExplorer,text='Call Range',font=DIR_FONT, background='white',activebackground=BTN_COLOR,bd=0)
        calllabel.grid(row=0,column=1,sticky='W',padx=5,pady=5)
        callclearborder = tk.Frame(rangeExplorer, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        callclearbtn = tk.Button(callclearborder, text='Clear Range', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command=self.callExp.clear)
        callclearbtn.pack(side = tk.LEFT)
        callclearborder.grid(row=0,column=1, padx=5, pady=5) 
        callclearbtn.bind('<Enter>', self.hoverButton)
        callclearbtn.bind('<Leave>', self.leaveButton)
        callselectborder = tk.Frame(rangeExplorer, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        callselectbtn = tk.Button(callselectborder, text='Select All', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command=self.callExp.selectall)
        callselectbtn.pack(side = tk.LEFT)
        callselectborder.grid(row=0,column=1,sticky='E', padx=5, pady=5) 
        callselectbtn.bind('<Enter>', self.hoverButton)
        callselectbtn.bind('<Leave>', self.leaveButton)
             
        rangeOptions1 = tk.Frame(rangeExplorer,padx=0,pady=0,bg="white")
        label1border = tk.Frame(rangeOptions1, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        label = tk.Button(label1border, text='Load Range', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command= lambda: self.loadRange('R'))
        label.pack(side = tk.LEFT)
        label.bind('<Enter>', self.hoverButton)
        label.bind('<Leave>', self.leaveButton)
        label1border.pack(side = tk.LEFT, padx=5, pady=5) 
        label2border = tk.Frame(rangeOptions1, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        label = tk.Button(label2border, text='Save Range', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command= lambda: self.saveRange('R'))
        label.pack(side = tk.LEFT)
        label.bind('<Enter>', self.hoverButton)
        label.bind('<Leave>', self.leaveButton)
        label2border.pack(side = tk.LEFT, padx=5, pady=5) 
        rangeOptions1.grid(row=2,column=0,sticky='E', padx=5, pady=5)
        
        rangeOptions2 = tk.Frame(rangeExplorer,padx=0,pady=0,bg="white")
        label1border = tk.Frame(rangeOptions2, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        label = tk.Button(label1border, text='Load Range', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command= lambda: self.loadRange('C'))
        label.pack(side = tk.LEFT)
        label.bind('<Enter>', self.hoverButton)
        label.bind('<Leave>', self.leaveButton)
        label1border.pack(side = tk.LEFT, padx=5, pady=5)  
        label2border = tk.Frame(rangeOptions2, bd=1,highlightbackground="black",highlightcolor=BTN_COLOR,highlightthickness=1)    
        label = tk.Button(label2border, text='Save Range', font=DIR_FONT, bg='white',bd=0,highlightthickness=0,activebackground=BTN_COLOR, padx=5, pady=5, command= lambda: self.saveRange('C'))
        label.pack(side = tk.LEFT)
        label.bind('<Enter>', self.hoverButton)
        label.bind('<Leave>', self.leaveButton)
        label2border.pack(side = tk.LEFT, padx=5, pady=5) 
        rangeOptions2.grid(row=2,column=1,sticky='E', padx=5, pady=5)
        
        rangeExplorer.columnconfigure([0,1],weight=1,uniform='x')
        rangeExplorer.rowconfigure(1,weight=10,uniform='x')
        rangeExplorer.rowconfigure(0,weight=1,uniform='x')
        rangeExplorer.rowconfigure(2,weight=1,uniform='x')
        panedwindow.add(rangeExplorer)
        
        # *** Status Bar ***
        self.statusvar = tk.StringVar()
        self.statusvar.set('Status Idle')
        self.status = tk.Label(self, textvariable=self.statusvar, bd=1, relief='sunken', anchor='w')
        self.status.grid(row=3,column=0,sticky='SEW')
       
        # *** grid configure ***
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1) 
    
    # range editor functions
    def hoverButton(self, event):
        event.widget.configure(bg=BG_COLOR2)
        
    def leaveButton(self, event):
        event.widget.configure(bg=BG_COLOR)   
                                
    def saveRange(self,param):
        if param == 'C':
            writeRange("C", g_myScen, g_myPos1, g_myPos2, self.callExp.weights)
        else:
            writeRange("R", g_myScen, g_myPos1, g_myPos2, self.raiseExp.weights)
        
        if g_myScen == 0:
            flocation = fdir + '\\Range Packages\\' + rangedir + "\\" + Scendict[param + str(g_myScen)] + g_myPos1 + ".txt"
        else:
            flocation = fdir + '\\Range Packages\\' + rangedir + "\\" + Scendict[param + str(g_myScen)] + g_myPos1 + "vs" + g_myPos2 + ".txt"  
        date = dt.datetime.fromtimestamp(os.path.getmtime(flocation))
        format_date = f"{date:%Y-%m-%d %H:%M}"
        self.fileTree.item(item,values=(str(format_date)))
        self.statusvar.set('Range Saved Successfully') 
        return   
    
    def loadRange(self,param):
        filename = filedialog.askopenfilename(title = "Select Range in PIO .txt format",filetypes = (("txt files","*.txt"),("all files","*.*")))
        rangeselect = readRangefile(filename)
        if param == 'C':
            self.callExp.weights = rangeselect
            self.callExp.update()
        else:
            self.raiseExp.weights = rangeselect
            self.raiseExp.update()
        self.statusvar.set('Range Loaded Successfully')  
        
    def OnDoubleClick(self,event):
        global g_myScen, g_myPos1, g_myPos2, treeIdx, item, RWEIGHT
        self.callExp.lock = False
        self.raiseExp.lock = False
        self.callExp.increment = RWEIGHT
        self.raiseExp.increment = RWEIGHT
        item = self.fileTree.identify('item', event.x, event.y)   
        treeText = self.fileTree.item(item, "tags")
        if len(treeText) > 0:
            g_myScen = int(treeText[0])
            g_myPos1, g_myPos2 = treeText[1], treeText[2]
            self.raiseExp.weights = readRange("R", g_myScen, g_myPos1, g_myPos2)
            self.callExp.weights = readRange("C", g_myScen, g_myPos1, g_myPos2)
            self.raiseExp.update()
            self.callExp.update()
            
if __name__ == "__main__":        
    app = PreflopTrain()

    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()
    app.geometry('%dx%d+%d+%d' % (3*ws/4, 3*hs/4, 1*ws/8, 1*hs/8))
    
    app.mainloop()