# -*- coding: utf-8 -*-
"""
TableReplay class for texas hold'em.

Class displays 6-max table and 


"""

import tkinter as tk
import os
class TableReplay(tk.Canvas):
    
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
    pos_str = ['BN','SB','BB','EP','MP','CO']
    suits = {"c": "#00A318",
             "s": "#000000",
             "h": "#FF3333",
             "d": "#0093FB"}
             
    # coordinates for placing objects on table
    chippos_x = [205,360,500,505,350,198]
    chippos_y = [140,110,142,235,265,240]
    btn_x = [155,315,575,559,415,179]
    btn_y = [160,105,160,285,309,289]
    labelpos_x = [162,447,629,634,343,161]
    labelpos_y = [143,75,143,304,397,304]
        
    def __init__(self, parent, heropos, vilpos, situation_index, herocards, **kwargs):
        tk.Canvas.__init__(self, parent, width=765, height=440, bg="white", highlightbackground="white", highlightcolor="white", highlightthickness=0)
        
        # defines the preflop situation/positions
        self.heropos = heropos
        self.vilpos = vilpos
        self.situation_index = situation_index
        self.herocards = herocards
        
        # image locations
        self.ptable = tk.PhotoImage(file = os.getcwd() + '\\Images\\handreplayer_table_med.png')
        self.bn_marker = tk.PhotoImage(file = os.getcwd() + '\\Images\\bn_marker.png')
        self.chips_sb = tk.PhotoImage(file = os.getcwd() + '\\Images\\chips_sb.png')
        self.chips_bb = tk.PhotoImage(file = os.getcwd() + '\\Images\\chips_bb.png')
        self.chips_2p5bb = tk.PhotoImage(file = os.getcwd() + '\\Images\\chips_2p5bb.png')
        self.chips_8bb = tk.PhotoImage(file = os.getcwd() + '\\Images\\chips_8bb.png')
        self.chips_22bb = tk.PhotoImage(file = os.getcwd() + '\\Images\\chips_22bb.png')
        self.suit_h = tk.PhotoImage(file = os.getcwd() + '\\Images\\suit_h.png')
        self.suit_d = tk.PhotoImage(file = os.getcwd() + '\\Images\\suit_d.png')
        self.suit_c = tk.PhotoImage(file = os.getcwd() + '\\Images\\suit_c.png')
        self.suit_s = tk.PhotoImage(file = os.getcwd() + '\\Images\\suit_s.png')
        self.blank = tk.PhotoImage(file = os.getcwd() + '\\Images\\blank.png')
        
        # draw table template
        self.grid(row=0, column=0, sticky = 'w')
        self.create_image(10, 10, anchor='nw', image=self.ptable)
        
        # draw position labels
        heropos_idx = TableReplay.pos_str.index(self.heropos)
        self.poslabels = [0,0,0,0,0,0]
        for i in range(6):
            strdraw_idx = (heropos_idx + 2 + i) % 6
            self.poslabels[i] = self.create_text(TableReplay.labelpos_x[i], TableReplay.labelpos_y[i], text=TableReplay.pos_str[strdraw_idx], anchor='e', font=("Helvetica", 16, 'bold'), fill='white')
        
        # post sb and bb and btn marker
        strdraw_idx = (5 - heropos_idx) % 6
        self.sb_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_sb)
        strdraw_idx = (6 - heropos_idx) % 6
        self.bb_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_bb)
        strdraw_idx = (4 - heropos_idx) % 6
        self.btn_img = self.create_image(TableReplay.btn_x[strdraw_idx], TableReplay.btn_y[strdraw_idx], anchor = 'nw', image=self.bn_marker)
        
        self.itemconfigure(self.sb_img, state='hidden')
        self.itemconfigure(self.bb_img, state='hidden')
        self.itemconfigure(self.btn_img, state='hidden')
        
        # place bet amounts depending on preflop situation
        vilpos_idx = TableReplay.pos_str.index(self.vilpos)
        if self.situation_index == 0:
            pass
        elif self.situation_index == 1:
            strdraw_idx = (vilpos_idx + 4 - heropos_idx) % 6
            self.vilchips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_2p5bb)
        elif self.situation_index == 2:
            strdraw_idx = 4
            self.herochips_img =self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_2p5bb)
            strdraw_idx = (vilpos_idx + 4 - heropos_idx) % 6
            self.vilchips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_8bb)
        else:
            strdraw_idx = 4
            self.herochips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_8bb)
            strdraw_idx = (vilpos_idx + 4 - heropos_idx) % 6
            self.vilchips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_22bb) 
        
        self.itemconfigure(self.vilchips_img, state='hidden')
        self.itemconfigure(self.herochips_img, state='hidden')
        
        # draw hand
        self.hand1crd_img = self.create_text(351, 347, text='', anchor='e', font=("Consolas", 20, 'bold'), fill=TableReplay.suits[self.herocards[1]])
        self.hand2crd_img = self.create_text(402, 347, text='', anchor='e', font=("Consolas", 20, 'bold'), fill=TableReplay.suits[self.herocards[3]]) 
        self.hand1suit_img = self.create_image(337, 358, anchor='nw', image=self.blank)
        self.hand2suit_img = self.create_image(388, 358, anchor='nw', image=self.blank)
            
    def update(self):
        heropos_idx = TableReplay.pos_str.index(self.heropos)
        vilpos_idx = TableReplay.pos_str.index(self.vilpos)
        
        # update position labels
        for i in range(6):
            strdraw_idx = (heropos_idx + 2 + i) % 6
            self.itemconfig(self.poslabels[i], text=TableReplay.pos_str[strdraw_idx])
            
        # update sb and bb and btn marker
        self.delete(self.sb_img)
        self.delete(self.bb_img)
        self.delete(self.btn_img)
        strdraw_idx = (5 - heropos_idx) % 6
        self.sb_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_sb)
        strdraw_idx = (6 - heropos_idx) % 6
        self.bb_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_bb)
        strdraw_idx = (4 - heropos_idx) % 6
        self.btn_img = self.create_image(TableReplay.btn_x[strdraw_idx], TableReplay.btn_y[strdraw_idx], anchor = 'nw', image=self.bn_marker)
        
        # update raise and open chips, and delete overlapping images
        if self.vilchips_img:
            self.delete(self.vilchips_img)
        if self.herochips_img:
            self.delete(self.herochips_img)
            
        if self.situation_index == 0:
            pass
        
        elif self.situation_index == 1:
            strdraw_idx = (vilpos_idx + 4 - heropos_idx) % 6
            self.vilchips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_2p5bb)
            if vilpos_idx == 1:
                self.delete(self.sb_img)
                
        elif self.situation_index == 2:
            strdraw_idx = 4
            self.herochips_img =self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_2p5bb)
            strdraw_idx = (vilpos_idx + 4 - heropos_idx) % 6
            self.vilchips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_8bb)
            if heropos_idx == 1:
                self.delete(self.sb_img)
            if vilpos_idx == 1:
                self.delete(self.sb_img)
            if vilpos_idx == 2:
                self.delete(self.bb_img)
            
        else:
            strdraw_idx = 4
            self.herochips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_8bb)
            strdraw_idx = (vilpos_idx + 4 - heropos_idx) % 6
            self.vilchips_img = self.create_image(TableReplay.chippos_x[strdraw_idx], TableReplay.chippos_y[strdraw_idx], anchor = 'nw', image=self.chips_22bb)
            if heropos_idx == 1:
                self.delete(self.sb_img)
            if heropos_idx == 2:
                self.delete(self.bb_img)  
            if vilpos_idx == 1:
                self.delete(self.sb_img)
            
        # update dealt hand
        if self.hand1crd_img:
            self.delete(self.hand1crd_img)
            self.delete(self.hand2crd_img)
            self.delete(self.hand1suit_img)
            self.delete(self.hand2suit_img)
            
            self.hand1crd_img = self.create_text(351, 347, text=self.herocards[0], anchor='e', font=("Consolas", 20, 'bold'), fill=TableReplay.suits[self.herocards[1]])
            self.hand2crd_img = self.create_text(402, 347, text=self.herocards[2], anchor='e', font=("Consolas", 20, 'bold'), fill=TableReplay.suits[self.herocards[3]]) 
            
            if self.herocards[1] == 'h':
                self.hand1suit_img = self.create_image(337, 358, anchor='nw', image=self.suit_h)
            elif self.herocards[1] == 'c':
                self.hand1suit_img = self.create_image(337, 358, anchor='nw', image=self.suit_c)
            elif self.herocards[1] == 'd':
                self.hand1suit_img = self.create_image(337, 358, anchor='nw', image=self.suit_d)
            elif self.herocards[1] == 's':
                self.hand1suit_img = self.create_image(337, 358, anchor='nw', image=self.suit_s)
                
            if self.herocards[3] == 'h':
                self.hand2suit_img = self.create_image(388, 358, anchor='nw', image=self.suit_h)
            if self.herocards[3] == 'c':
                self.hand2suit_img = self.create_image(388, 358, anchor='nw', image=self.suit_c)
            if self.herocards[3] == 'd':
                self.hand2suit_img = self.create_image(388, 358, anchor='nw', image=self.suit_d)
            if self.herocards[3] == 's':
                self.hand2suit_img = self.create_image(388, 358, anchor='nw', image=self.suit_s)
        