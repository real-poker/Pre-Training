"""
# Custom classes for tkinter GUI
"""

import tkinter as tk

# Control button
class cButton(tk.Frame):
    
    def __init__(self, parent, btn_label, btn_command, theme, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.theme = theme
        self['highlightthickness'] = 1

        if type(btn_label) == str:
            self.Button = tk.Button(self, text=btn_label, command=btn_command, font=theme.dirfont, bg=theme.bgcolor3, fg=theme.fcolor, bd=1, highlightthickness=0, activebackground=theme.btncolor, padx=15, pady=0, relief='flat')
        else:
            self.Button = tk.Button(self, textvariable=btn_label, command=btn_command, font=theme.dirfont, bg=theme.bgcolor3, fg=theme.fcolor, bd=1, highlightthickness=0, activebackground=theme.btncolor, padx=15, pady=0, relief='flat') 
        self.Button.pack(side=tk.RIGHT)
        self.Button.bind('<Enter>', self.hoverButton)
        self.Button.bind('<Leave>', self.leaveButton)
    
    def hoverButton(self, event):
        event.widget.configure(bg=self.theme.bgcolor2, relief='sunken')
        
    def leaveButton(self, event):
        event.widget.configure(bg=self.theme.bgcolor3, relief='flat')  
        
# Tab explorer button        
class tabButton(tk.Frame):
    
    def __init__(self, parent, btn_label, btn_command, theme, mode, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.theme = theme
        if mode == 'on':
            self.bw = 0
            self.relief = 'raised'
        else:
            self.bw = 1 
            self.relief = 'sunken'
        if type(btn_label) == str:
            self.Button = tk.Button(self, text=btn_label, command=btn_command, font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor, activebackground=theme.btncolor, anchor='w', relief=self.relief, bd=self.bw)
        else:
            self.Button = tk.Button(self, textvariable=btn_label, command=btn_command, font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor, activebackground=theme.btncolor, anchor='w', relief=self.relief, bd=self.bw)
        self.Button.pack(side=tk.LEFT)
        self.Button.bind('<Enter>', self.hoverButton)
        self.Button.bind('<Leave>', self.leaveButton)
         
    def hoverButton(self, event):
        event.widget.configure(bg=self.theme.bgcolor2, relief='raised')
         
    def leaveButton(self, event):
        event.widget.configure(bg=self.theme.bgcolor, relief='sunken')     

# Hex color code to RGB color code
def hex_to_rgb(hex_input):
    hex_stripped = hex_input.lstrip('#')
    return tuple(int(hex_stripped[i:i+2], 16) for i in (0, 2, 4))

# RGB color code to Hex color code
def rgb_to_hex(rgb_input):
    return '#%02x%02x%02x' %  rgb_input

# Create dictionary containing color gradient
def color_gradient(start_hex, end_hex):
    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    color_dict = {}
    for i in range(0, 21):
        interp_rgb = (int(start_rgb[0]*(20-i)/20 + end_rgb[0]*i/20), int(start_rgb[1]*(20-i)/20 + end_rgb[1]*i/20), int(start_rgb[2]*(20-i)/20 + end_rgb[2]*i/20))
        color_dict[5*i] = rgb_to_hex(interp_rgb)   
    return color_dict
    
    
    
    
    