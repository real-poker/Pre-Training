# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 03:33:42 2020

@author: Jeffrey McClure
"""
import tkinter as tk
from tkinter import font
class sliderGraphical(tk.Frame): 
   
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")
        self.increment = 5
        self.callcolors = {100: '#02385a',
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
    
        self.raisecolors = {100: '#67001f',
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
        
        # set font variable
        self.font_text = font.Font(self, family='TkTextFont', size = 9) 
        self.Sthickness = 25
        self.Swidth = 402
        
        # Labels showing raise/call/fold percentages
        self.rLabelout = tk.StringVar()
        self.cLabelout = tk.StringVar()
        self.fLabelout = tk.StringVar()
        self.rLabelout.set('Raise: 25%')
        self.cLabelout.set('Call: 25%')
        self.fLabelout.set('Fold: 50%')
        rLabel = tk.Label(self, textvariable=self.rLabelout, font=self.font_text, bg='white', fg='black', padx=1, pady=1)
        cLabel = tk.Label(self, textvariable=self.cLabelout, font=self.font_text, bg='white', fg='black', padx=1, pady=1)
        fLabel = tk.Label(self, textvariable=self.fLabelout, font=self.font_text, bg='white', fg='black', padx=1, pady=1)
        rLabel.grid(row=0,column=0,padx=0,pady=0,sticky='NSEW')
        cLabel.grid(row=0,column=1,padx=0,pady=0,sticky='NSEW')
        fLabel.grid(row=0,column=2,padx=0,pady=0,sticky='NSEW')
        
        # Canvas slider
        self.cSlider = tk.Canvas(self, width=self.Swidth, height=self.Sthickness, bg="white", highlightbackground="black", highlightcolor="black", highlightthickness=0)
        self.robj = self.cSlider.create_rectangle(1, 1, 25*self.Swidth/100, self.Sthickness-1, fill='#8F0735', width=1)
        self.cobj = self.cSlider.create_rectangle(25*self.Swidth/100, 1, round(self.Swidth/2), self.Sthickness-1, fill='#73a9cf', width=1)
        self.fobj = self.cSlider.create_rectangle(50*self.Swidth/100, 1, self.Swidth-1, self.Sthickness-1, fill="white", width=1)
        self.cSlider.grid(row=1,column=0,columnspan=3,padx=0,pady=0,sticky='NSEW')
        
        self.cSlider.bind('<B1-Motion>', self.colorset)
        self.cSlider.bind('<Button-1>', self.colorsetclick)
        self.cSlider.bind('<B3-Motion>', self.colorset2)
        self.cSlider.bind('<Button-3>', self.colorsetclick2)
        
        # initialize frequencies
        self.rfreq = 25
        self.cfreq = 25
        self.ffreq = 50    
               
    def colorset(self, event):
        self.rfreq = min(max(self.increment*round(100*(self.winfo_pointerx() - self.winfo_rootx()) / (self.winfo_width()*self.increment)), 0),100)
        self.cfreq = min(max(100 - self.rfreq - self.ffreq, 0),100)
        self.ffreq = min(max(100 - self.rfreq - self.cfreq, 0),100)
        self.cSlider.coords(self.robj, 1, 1, self.rfreq*self.Swidth/100, self.Sthickness-1)
        self.cSlider.coords(self.cobj, self.rfreq*self.Swidth/100, 1, self.rfreq*self.Swidth/100 + (100 - self.rfreq - self.ffreq)*self.Swidth/100, self.Sthickness-1)
        self.cSlider.coords(self.fobj, (self.rfreq + self.cfreq)*self.Swidth/100, 1, self.Swidth-1, self.Sthickness-1)
        self.rLabelout.set('Raise: ' + str(self.rfreq) + '%')
        self.cLabelout.set('Call: ' + str(self.cfreq) + '%') 
        self.fLabelout.set('Fold: ' + str(self.ffreq) + '%') 
        
    def colorsetclick(self, event):
        self.rfreq = min(max(self.increment*round(100*(self.winfo_pointerx() - self.winfo_rootx()) / (self.winfo_width()*self.increment)), 0),100)
        self.cfreq = min(max(100 - self.rfreq - self.ffreq, 0),100)
        self.ffreq = min(max(100 - self.rfreq - self.cfreq, 0),100)
        self.cSlider.coords(self.robj, 1, 1, self.rfreq*self.Swidth/100, self.Sthickness-1)
        self.cSlider.coords(self.cobj, self.rfreq*self.Swidth/100, 1, self.rfreq*self.Swidth/100 + (100 - self.rfreq - self.ffreq)*self.Swidth/100, self.Sthickness-1)
        self.cSlider.coords(self.fobj, (self.rfreq + self.cfreq)*self.Swidth/100, 1, self.Swidth-1, self.Sthickness-1)
        self.rLabelout.set('Raise: ' + str(self.rfreq) + '%')
        self.cLabelout.set('Call: ' + str(self.cfreq) + '%') 
        self.fLabelout.set('Fold: ' + str(self.ffreq) + '%') 
        
    def colorset2(self, event):
        self.ffreq = min(max(100 - self.increment*round(100*(self.winfo_pointerx() - self.winfo_rootx()) / (self.winfo_width()*self.increment)), 0),100)
        self.cfreq = min(max(100 - self.rfreq - self.ffreq, 0),100)
        self.rfreq = min(max(100 - self.cfreq - self.ffreq, 0),100)
        self.cSlider.coords(self.cobj, self.rfreq*self.Swidth/100, 1, self.rfreq*self.Swidth/100 + (100 - self.rfreq - self.ffreq)*self.Swidth/100, self.Sthickness-1)
        self.cSlider.coords(self.fobj, (self.rfreq + self.cfreq)*self.Swidth/100, 1, self.Swidth-1, self.Sthickness-1)
        self.rLabelout.set('Raise: ' + str(self.rfreq) + '%')
        self.cLabelout.set('Call: ' + str(self.cfreq) + '%') 
        self.fLabelout.set('Fold: ' + str(self.ffreq) + '%') 
        
    def colorsetclick2(self, event):
        self.ffreq = min(max(100 - self.increment*round(100*(self.winfo_pointerx() - self.winfo_rootx()) / (self.winfo_width()*self.increment)), 0),100)
        self.cfreq = min(max(100 - self.rfreq - self.ffreq, 0),100)
        self.rfreq = min(max(100 - self.cfreq - self.ffreq, 0),100)
        self.cSlider.coords(self.cobj, self.rfreq*self.Swidth/100, 1, self.rfreq*self.Swidth/100 + (100 - self.rfreq - self.ffreq)*self.Swidth/100, self.Sthickness-1)
        self.cSlider.coords(self.fobj, (self.rfreq + self.cfreq)*self.Swidth/100, 1, self.Swidth-1, self.Sthickness-1)
        self.rLabelout.set('Raise: ' + str(self.rfreq) + '%')
        self.cLabelout.set('Call: ' + str(self.cfreq) + '%') 
        self.fLabelout.set('Fold: ' + str(self.ffreq) + '%') 