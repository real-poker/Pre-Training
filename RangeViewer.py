"""
# RangeViewer class.
# Handles a tk.Frame object that displays a 13x13 grid containing hold'em hands. Mouse clicks change % values of hands according to weight input.
# Inputs: weight (int)
# Attributes: matrix of weights (array of ints)
"""

import tkinter as tk
from tkinter import font
from tkinter_utils import color_gradient

class RangeViewer(tk.Frame):
    deck = {0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8", 7: "9", 8: "T", 9: "J", 10: "Q", 11: "K", 12: "A"}

    def __init__(self, parent, theme):
        tk.Frame.__init__(self, parent)
        self.bg_color = theme.bgcolor
        self.font_color = theme.fcolor 
        self.colors = color_gradient(self.bg_color, '#fcf803')
        self.erasemode = False
        self.weightsave = 0
        self.configure(background=self.bg_color)
        self.hand_text = font.Font(self, family='Consolas', size = 9) 
        self.weight_text = font.Font(self, family='Consolas', size = 7) 
        self.increment = 25
        self.lock = False
        
        self.viewframe = tk.Frame(self, bg=self.bg_color) 
        
        # initialize range with zero weights
        self.weights = [[0 for x in range(13)] for x in range(13)] 
        self.weightStrs = [['' for x in range(13)] for x in range(13)] 
        for j in range(0, 13):
            for i in range(0, 13):
                if j > i:
                    self.weightStrs[j][i] = RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+"s"+'\n0'
                elif j < i:
                    self.weightStrs[j][i] = RangeViewer.deck[12-j]+RangeViewer.deck[12-i]+"o"+'\n0'
                else:
                    self.weightStrs[j][i] = RangeViewer.deck[12-i]+RangeViewer.deck[12-j]+'\n0'

        self.range_canvas = tk.Canvas(self.viewframe, width=540, height=511, bg=self.bg_color, borderwidth=0, highlightbackground="black", highlightcolor="black", highlightthickness=0, bd=0)
        self.range_canvas.bind('<B1-Motion>', self.colorset)
        self.range_canvas.bind('<Button-1>', self.colorsetclick)
        self.range_canvas.bind('<B3-Motion>', self.colorset3)
        self.range_canvas.bind('<Button-3>', self.colorset3click)
        
        self.handgrid = [[0 for x in range(13)] for x in range(13)] 
        self.textgrid = [[0 for x in range(13)] for x in range(13)] 
        self.rectgrid = [[0 for x in range(13)] for x in range(13)] 
        
        w = int(self.range_canvas['width']) - 1
        h = int(self.range_canvas['height']) - 1
        for j in range(0, 13):
            for i in range(0, 13):
                self.rectgrid[j][i] = self.range_canvas.create_rectangle(j*w/13, i*h/13, (j+1)*w/13, (i+1)*h/13, fill=self.bg_color, width=1, outline=self.font_color)
                self.textgrid[j][i] = self.range_canvas.create_text((j+0.1)*(w/13), (i+0.1)*(h/13), font=self.hand_text, text=self.weightStrs[j][i].split('\n')[0], anchor=tk.NW, fill=self.font_color)
                self.handgrid[j][i] = self.range_canvas.create_text((j+0.9)*(w/13), (i+0.9)*(h/13), font=self.weight_text, text=self.weightStrs[j][i].split('\n')[1], anchor=tk.SE, fill=self.font_color)
        self.hand_text['size'] = min(11, int(0.021*min(w,h)))
        self.weight_text['size'] = min(9, int(0.016*min(w,h)))
        
        self.percent = tk.StringVar(self, '0.0%')
        self.perclabel = tk.Label(self.viewframe, bg=self.bg_color, textvariable=self.percent, borderwidth=0, highlightthickness=0, highlightbackground='black', font=self.hand_text, relief="solid", fg=self.font_color)
        
        self.range_canvas.grid(row=0, column=0, sticky='NSEW', padx=0, pady=0)
        self.perclabel.grid(row=1, column=0, sticky='W')

        self.viewframe.rowconfigure(0, weight=10, uniform='x')
        self.viewframe.rowconfigure(1, weight=1, uniform='x')
        self.viewframe.columnconfigure(0, weight=1, uniform='x')
        self.viewframe.pack(expand=True, fill='both')
        
        # resize fonts on frame size change
        self.bind('<Configure>', self.resize)

            
    def resize(self, event):  
        self.range_canvas.update()
        w = int(self.range_canvas.winfo_width()) - 1
        h = int(self.range_canvas.winfo_height()) - 1
        if w > 0:
            self.hand_text['size'] = min(11, int(0.021*min(w,h)))
            self.weight_text['size'] = min(9, int(0.016*min(w,h)))
            for j in range(0, 13):
                for i in range(0, 13):
                    self.range_canvas.coords(self.rectgrid[j][i], j*w/13, i*h/13, (j+1)*w/13, (i+1)*h/13)
                    self.range_canvas.coords(self.textgrid[j][i], (j+0.1)*(w/13), (i+0.1)*(h/13))
                    self.range_canvas.coords(self.handgrid[j][i], (j+0.9)*(w/13), (i+0.9)*(h/13))

    def colorset(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.range_canvas.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.range_canvas.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                if not self.erasemode:
                    self.weights[idx_x][idx_y] = 100
                    self.range_canvas.itemconfig(self.rectgrid[idx_x][idx_y], fill=self.colors[100])
                    self.weightStrs[idx_x][idx_y] = self.weightStrs[idx_x][idx_y].split('\n')[0] + '\n100'
                    self.range_canvas.itemconfig(self.handgrid[idx_x][idx_y], text=self.weightStrs[idx_x][idx_y].split('\n')[1])
                else:
                    self.weights[idx_x][idx_y] = 0
                    self.range_canvas.itemconfig(self.rectgrid[idx_x][idx_y], fill=self.bg_color)
                    self.weightStrs[idx_x][idx_y] = self.weightStrs[idx_x][idx_y].split('\n')[0] + '\n0'   
                    self.range_canvas.itemconfig(self.handgrid[idx_x][idx_y], text=self.weightStrs[idx_x][idx_y].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
        
    def colorsetclick(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.range_canvas.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.range_canvas.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                if self.weights[idx_x][idx_y] == 0:
                    self.erasemode = False
                else:
                    self.erasemode = True
                if not self.erasemode:
                    self.weights[idx_x][idx_y] = 100
                    self.range_canvas.itemconfig(self.rectgrid[idx_x][idx_y], fill=self.colors[100])
                    self.weightStrs[idx_x][idx_y] = self.weightStrs[idx_x][idx_y].split('\n')[0] + '\n100'
                    self.range_canvas.itemconfig(self.handgrid[idx_x][idx_y], text=self.weightStrs[idx_x][idx_y].split('\n')[1])
                else:
                    self.weights[idx_x][idx_y] = 0
                    self.range_canvas.itemconfig(self.rectgrid[idx_x][idx_y], fill=self.bg_color)
                    self.weightStrs[idx_x][idx_y] = self.weightStrs[idx_x][idx_y].split('\n')[0] + '\n0'
                    self.range_canvas.itemconfig(self.handgrid[idx_x][idx_y], text=self.weightStrs[idx_x][idx_y].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
                
    def colorset3(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.range_canvas.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.range_canvas.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                self.weights[idx_x][idx_y] = self.weightsave
                self.range_canvas.itemconfig(self.rectgrid[idx_x][idx_y], fill=self.colors[self.weightsave])
                self.weightStrs[idx_x][idx_y] = self.weightStrs[idx_x][idx_y].split('\n')[0] + '\n' + str(self.weightsave)
                self.range_canvas.itemconfig(self.handgrid[idx_x][idx_y], text=self.weightStrs[idx_x][idx_y].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
       
    def colorset3click(self, event):
        if not self.lock:
            idx_x = 13*(self.winfo_pointerx() - self.winfo_rootx()) // self.range_canvas.winfo_width()
            idx_y = 13*(self.winfo_pointery() - self.winfo_rooty()) // self.range_canvas.winfo_height()
            if idx_x in range(0,13) and idx_y in range(0,13):
                self.weights[idx_x][idx_y] = min(self.weights[idx_x][idx_y] + self.increment, 100)
                self.weightsave = self.weights[idx_x][idx_y]
                self.range_canvas.itemconfig(self.rectgrid[idx_x][idx_y], fill=self.colors[self.weightsave])
                self.weightStrs[idx_x][idx_y] = self.weightStrs[idx_x][idx_y].split('\n')[0] + '\n' + str(self.weightsave)
                self.range_canvas.itemconfig(self.handgrid[idx_x][idx_y], text=self.weightStrs[idx_x][idx_y].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
            
    def update(self):
        self.range_canvas.update()
        for j in range(0, 13):
            for i in range(0, 13):
                self.weightStrs[j][i] = self.weightStrs[j][i].split('\n')[0] + '\n' + str(self.weights[j][i])
                self.range_canvas.itemconfig(self.rectgrid[j][i], fill=self.colors[self.weights[j][i]])
                self.range_canvas.itemconfig(self.handgrid[j][i], text=self.weightStrs[j][i].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
                
    def clear(self):
        if not self.lock:
            self.weights = [[0 for x in range(13)] for x in range(13)] 
            for j in range(0, 13):
                for i in range(0, 13):
                    self.weightStrs[j][i] = self.weightStrs[j][i].split('\n')[0] + '\n0'
                    self.range_canvas.itemconfig(self.rectgrid[j][i], fill=self.colors[self.weights[j][i]]) 
                    self.range_canvas.itemconfig(self.handgrid[j][i], text=self.weightStrs[j][i].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
                
    def selectall(self):
        if not self.lock:
            self.weights = [[100 for x in range(13)] for x in range(13)] 
            for j in range(0, 13):
                for i in range(0, 13):
                    self.weightStrs[j][i] = self.weightStrs[j][i].split('\n')[0] + '\n100'
                    self.range_canvas.itemconfig(self.rectgrid[j][i], fill=self.colors[self.weights[j][i]])
                    self.range_canvas.itemconfig(self.handgrid[j][i], text=self.weightStrs[j][i].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
                   
    def get_percentage(self):
        summation = 0
        for j in range(0, 13):
            for i in range(0, 13):
                if i > j:
                    summation += 12*self.weights[j][i]
                elif i < j:
                    summation += 4*self.weights[j][i]
                else:
                    summation += 6*self.weights[j][i]
        return summation/1326
    
    def invert_weights(self, inv_weights):
        for j in range(0, 13):
            for i in range(0, 13):
                self.weights[j][i] = 100 - inv_weights[j][i]
                self.weightStrs[j][i] = self.weightStrs[j][i].split('\n')[0] + '\n' + str(self.weights[j][i])
                self.range_canvas.itemconfig(self.rectgrid[j][i], fill=self.colors[self.weights[j][i]])
                self.range_canvas.itemconfig(self.handgrid[j][i], text=self.weightStrs[j][i].split('\n')[1])
        self.percent.set(f'{RangeViewer.get_percentage(self):.1f}' + '%')
        self.range_canvas.update()        
    
    @property
    def weightlist(self):
        return self.weights
    
    @weightlist.setter
    def weightlist(self, weights):
        self.weights = weights
        for j in range(0, 13):
            for i in range(0, 13):
                self.weightStrs[j][i] = self.weightStrs[j][i].split('\n')[0] + '\n' + str(self.weights[j][i])
                self.range_canvas.itemconfig(self.rectgrid[j][i], fill=self.colors[self.weights[j][i]])
                self.range_canvas.itemconfig(self.handgrid[j][i], text=self.weightStrs[j][i].split('\n')[1])
        self.percent.set(str(RangeViewer.get_percentage(self))+'%')
                
                    
class CallViewer(RangeViewer):
    def __init__(self, parent, theme):
        super().__init__(parent, theme)
        self.colors = color_gradient(self.bg_color, '#008080')
    
class RaiseViewer(RangeViewer):
    def __init__(self, parent, theme):
        super().__init__(parent, theme) 
        self.colors = color_gradient(self.bg_color, '#FF0000')
