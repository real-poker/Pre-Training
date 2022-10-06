"""
# GUI for selecting raise/call/fold frequencies for the range training module
"""
import tkinter as tk
from tkinter import font

class SliderGraphical(tk.Frame): 
    
    def __init__(self, parent, theme):
        tk.Frame.__init__(self, parent)
        
        # Config
        self.bg_color = theme.bgcolor
        self.font_color = theme.fcolor        
        self.increment = 5
        self.configure(background=self.bg_color)    
        self.font_text = font.Font(self, family='TkTextFont', size = 9) 
        self.Sthickness = 25
        self.Swidth = 452
        
        # Labels showing raise/call/fold percentages
        self.rLabelout = tk.StringVar(self, 'Raise: 25%')
        self.cLabelout = tk.StringVar(self, 'Call: 25%')
        self.fLabelout = tk.StringVar(self, 'Fold: 50%')
        rLabel = tk.Label(self, textvariable=self.rLabelout, font=self.font_text, bg=self.bg_color, fg=self.font_color, padx=1, pady=1)
        cLabel = tk.Label(self, textvariable=self.cLabelout, font=self.font_text, bg=self.bg_color, fg=self.font_color, padx=1, pady=1)
        fLabel = tk.Label(self, textvariable=self.fLabelout, font=self.font_text, bg=self.bg_color, fg=self.font_color, padx=1, pady=1)
        rLabel.grid(row=0,column=0,padx=0,pady=0,sticky='NSEW')
        cLabel.grid(row=0,column=1,padx=0,pady=0,sticky='NSEW')
        fLabel.grid(row=0,column=2,padx=0,pady=0,sticky='NSEW')
        
        # Canvas slider canvas object
        self.cSlider = tk.Canvas(self, width=self.Swidth, height=self.Sthickness, bg=self.bg_color, highlightbackground=self.font_color, highlightcolor=self.font_color, highlightthickness=0)
        self.robj = self.cSlider.create_rectangle(1, 1, 25*self.Swidth/100, self.Sthickness-1, fill='#8F0735', width=1, outline=self.font_color)
        self.cobj = self.cSlider.create_rectangle(25*self.Swidth/100, 1, round(self.Swidth/2), self.Sthickness-1, fill='#73a9cf', width=1, outline=self.font_color)
        self.fobj = self.cSlider.create_rectangle(50*self.Swidth/100, 1, self.Swidth-1, self.Sthickness-1, fill=self.bg_color, width=1, outline=self.font_color)
        self.cSlider.grid(row=1,column=0,columnspan=3,padx=0,pady=0,sticky='NSEW')
        
        self.cSlider.bind('<B1-Motion>', self.colorset)
        self.cSlider.bind('<Button-1>', self.colorsetclick)
        self.cSlider.bind('<B3-Motion>', self.colorset2)
        self.cSlider.bind('<Button-3>', self.colorsetclick2)
        
        # Initialize frequencies
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