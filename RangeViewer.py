# -*- coding: utf-8 -*-
"""
RangeViewer class for texas hold'em.

Class displays 13 x 13 grid containing hold'em hands. Mouse clicks change % values of hands according to weight input.

Inputs: weight (int)
Attributes: matrix of weights (array of ints)

"""

import tkinter as tk
from tkinter import font
class RangeViewer(tk.Frame):
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

    erasemode = False
    weightsave = 0

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")
        self.colors = {100: '#fcf803',
             95: '#FDF90F',
             90: '#FDFA1A',
             85: '#FEFA26',
             80: '#FEFB31',
             75: '#FFFC3D',
             70: '#FFFC49',
             65: '#FFFC55',
             60: '#FFFD62',
             55: '#FFFD6E',
             50: '#FFFD7A',
             45: '#FFFD87',
             40: '#FFFD94',
             35: '#FFFEA0',
             30: '#FFFEAD',
             25: '#FFFEBA',
             20: '#FFFEC8',
             15: '#FFFED6',
             10: '#FFFFE3',
             5: '#FFFFF1',
             0: 'white'}  
        self.increment = 25
        self.lock = False
        
        viewframe = tk.Frame(self, bg="white") 
        reportframe = tk.Frame(self, bg="white") 
        
        # initialize range with zero weights
        self.weights = [[0 for x in range(13)] for x in range(13)] 
        self.weightStrs = [[tk.StringVar() for x in range(13)] for x in range(13)] 
        for j in range(0, 13):
            for i in range(0, 13):
                if j > i:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+"s"+'\n0')
                elif j < i:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+"o"+'\n0')
                else:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+'\n0')
                    
        # labels for viewing range weights
        self.handgrid = [[0 for x in range(13)] for x in range(13)] 
        self.handtext = [[0 for x in range(13)] for x in range(13)] 
        self.handweight = [[0 for x in range(13)] for x in range(13)] 
        
        for i in range(0, 13):       
            viewframe.rowconfigure(i, weight=1)
            viewframe.columnconfigure(i, weight=1)
        
        # set font variable
        self.font_text = font.Font(self, family='Consolas', size = 10) 
        
        for j in range(0, 13):
            for i in range(0, 13):
                self.handgrid[j][i] = tk.Label(viewframe, background = 'white', textvariable=self.weightStrs[j][i], borderwidth = 1, highlightthickness=1, highlightbackground = 'black', font = self.font_text, relief="solid")   
                self.handgrid[j][i].grid(row=i, column=j, sticky='NSEW')
                self.handgrid[j][i].bind('<B1-Motion>', self.colorset)
                self.handgrid[j][i].bind('<Button-1>', self.colorsetclick)
                self.handgrid[j][i].bind('<B3-Motion>', self.colorset3)
                self.handgrid[j][i].bind('<Button-3>', self.colorset3click)
        
        viewframe.pack(expand=True,fill='both')
        self.percent = tk.StringVar()
        self.percent.set('0.00%')
        perclabel = tk.Label(reportframe,textvariable=self.percent,font=self.font_text, background='white',bd=0)
        perclabel.grid(row=0,column=0,sticky='W',padx=5,pady=5)
        reportframe.pack(side=tk.LEFT,expand=True,fill='both')
        reportframe.rowconfigure(0,weight=1)
        
        self.rowconfigure(0,weight=30,uniform='x')
        self.rowconfigure(1,weight=1,uniform='x')
        self.columnconfigure(0,weight=1)
        # resize fonts on frame size change
        #self.bind('<Configure>', self.resize)
            
    def resize(self, event):
        height = self.winfo_height()
        width = self.winfo_width()
        if height < 300 or width < 300:
            self.font_text['size'] = 7
        elif height < 450 or width < 450:
            self.font_text['size'] = 10
        elif height < 700 or width < 700:
            self.font_text['size'] = 12
        else:
            self.font_text['size'] = 16 
            
    def colorset(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                if not RangeViewer.erasemode:
                    self.weights[idx_x][idx_y]= 100
                    self.handgrid[idx_x][idx_y].config(background = self.colors[100])
                    if idx_x > idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_y]+RangeViewer.deck[12-idx_x]+"s"+'\n100')
                    elif idx_x < idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+"o"+'\n100')
                    else:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+'\n100')
                else:
                    self.weights[idx_x][idx_y]= 0
                    self.handgrid[idx_x][idx_y].config(background = 'white')
                    if idx_x > idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_y]+RangeViewer.deck[12-idx_x]+"s"+'\n0')
                    elif idx_x < idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+"o"+'\n0')
                    else:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+'\n0')                  
        self.percent.set(f'{RangeViewer.getPercentage(self):.2f}' + '%')
        
    def colorsetclick(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                if self.weights[idx_x][idx_y] == 0:
                    RangeViewer.erasemode = False
                else:
                    RangeViewer.erasemode = True
                if not RangeViewer.erasemode:
                    self.weights[idx_x][idx_y]= 100
                    self.handgrid[idx_x][idx_y].config(background = self.colors[100])
                    if idx_x > idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_y]+RangeViewer.deck[12-idx_x]+"s"+'\n100')
                    elif idx_x < idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+"o"+'\n100')
                    else:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+'\n100')
                else:
                    self.weights[idx_x][idx_y]= 0
                    self.handgrid[idx_x][idx_y].config(background = 'white')
                    if idx_x > idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_y]+RangeViewer.deck[12-idx_x]+"s"+'\n0')
                    elif idx_x < idx_y:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+"o"+'\n0')
                    else:
                        self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+'\n0')
        self.percent.set(f'{RangeViewer.getPercentage(self):.2f}' + '%')
                
    def colorset3(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                self.weights[idx_x][idx_y] = RangeViewer.weightsave
                self.handgrid[idx_x][idx_y].config(background = self.colors[RangeViewer.weightsave])
                if idx_x > idx_y:
                    self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_y]+RangeViewer.deck[12-idx_x]+"s"+'\n'+str(RangeViewer.weightsave))
                elif idx_x < idx_y:
                    self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+"o"+'\n'+str(RangeViewer.weightsave))
                else:
                    self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+'\n'+str(RangeViewer.weightsave))
        self.percent.set(f'{RangeViewer.getPercentage(self):.2f}' + '%')
       
    def colorset3click(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                self.weights[idx_x][idx_y] = min(self.weights[idx_x][idx_y] + self.increment, 100)
                RangeViewer.weightsave = self.weights[idx_x][idx_y]
                self.handgrid[idx_x][idx_y].config(background = self.colors[RangeViewer.weightsave])
                if idx_x > idx_y:
                    self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_y]+RangeViewer.deck[12-idx_x]+"s"+'\n'+str(RangeViewer.weightsave))
                elif idx_x < idx_y:
                    self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+"o"+'\n'+str(RangeViewer.weightsave))
                else:
                    self.weightStrs[idx_x][idx_y].set(RangeViewer.deck[12-idx_x]+RangeViewer.deck[12-idx_y]+'\n'+str(RangeViewer.weightsave))
        self.percent.set(f'{RangeViewer.getPercentage(self):.2f}' + '%')
            
    def update(self):
        for j in range(0, 13):
            for i in range(0, 13):
                if j > i:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+"s"+'\n'+str(self.weights[j][i]))
                elif j < i:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+"o"+'\n'+str(self.weights[j][i]))
                else:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+'\n'+str(self.weights[j][i]))
                self.handgrid[j][i].config(background = self.colors[self.weights[j][i]])
        self.percent.set(f'{RangeViewer.getPercentage(self):.2f}' + '%')
                
    def clear(self):
        if not self.lock:
            self.weights = [[0 for x in range(13)] for x in range(13)] 
            for j in range(0, 13):
                for i in range(0, 13):
                    if j > i:
                        self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+"s"+'\n0')
                    elif j < i:
                        self.weightStrs[j][i].set(RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+"o"+'\n0')
                    else:
                        self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+'\n0')  
                    self.handgrid[j][i].config(background = self.colors[self.weights[j][i]])    
        self.percent.set(f'{RangeViewer.getPercentage(self):.2f}' + '%')
                
    def selectall(self):
        if not self.lock:
            self.weights = [[100 for x in range(13)] for x in range(13)] 
            for j in range(0, 13):
                for i in range(0, 13):
                    if j > i:
                        self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+"s"+'\n100')
                    elif j < i:
                        self.weightStrs[j][i].set(RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+"o"+'\n100')
                    else:
                        self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+'\n100')
                    self.handgrid[j][i].config(background = self.colors[self.weights[j][i]])   
        self.percent.set(f'{RangeViewer.getPercentage(self):.2f}' + '%')
                   
    def getPercentage(self):
        summation = 0
        for j in range(0, 13):
            for i in range(0, 13):
                if i > j:
                    summation += 12*self.weights[j][i]
                elif i < j:
                    summation += 4*self.weights[j][i]
                else:
                    summation += 6*self.weights[j][i]
        percentage = summation/1326
        return percentage
    
    @property
    def weightlist(self):
        return self.weights
    
    @weightlist.setter
    def weightlist(self, weights):
        self.weights = weights
        for j in range(0, 13):
            for i in range(0, 13):
                if j > i:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+"s"+'\n'+str(self.weights[j][i]))
                elif j < i:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+"o"+'\n'+str(self.weights[j][i]))
                else:
                    self.weightStrs[j][i].set(RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+'\n'+str(self.weights[j][i]))
                self.handgrid[j][i].config(background = self.colors[self.weights[j][i]])
        self.percent.set(str(RangeViewer.getPercentage(self))+'%')
                
                    
class CallViewer(RangeViewer):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.colors = {100: '#02385a',
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
    
class RaiseViewer(RangeViewer):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)       
        self.colors = {100: '#67001f',
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