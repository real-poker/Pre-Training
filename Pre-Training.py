"""
# Preflop Hold'em Trainer
"""
import pygame
import tkinter as tk
import os
import time
import shutil
import datetime as dt
from tkinter import filedialog
from tkinter import ttk
from configparser import ConfigParser
from holdem_utils import deal_hand, deal_pos, in_range
from tkinter_utils import cButton, tabButton
from RangeViewer import CallViewer, RaiseViewer
from SliderGraphical import SliderGraphical
from TableReplay import TableReplay

pygame.init()

# directories
fdir = os.path.dirname(os.path.abspath("Pre-Training.py"))

# load in saved user settings
parser = ConfigParser()
parser.read('prefloptrain.ini')
range_dir = parser.get('settings','Range Package')
theme_set = parser.get('settings','Colour Theme')
show_ranges = parser.getint('settings','show_ranges')
training_tolerance = parser.getint('settings','training_tolerance')
show_hotkeys = parser.getint('settings','show_hotkeys')
show_accuracy = parser.getint('settings','show_accuracy')
rclick_weight = parser.getint('settings','rclick_weight')
toggle_sound = parser.getint('settings', 'toggle_sound')
open_scenario = parser.getint('settings', 'open_scenario')
facingopen_scenario = parser.getint('settings', 'facingopen_scenario')
facing3bet_scenario = parser.getint('settings', 'facing3bet_scenario')
facing4bet_scenario = parser.getint('settings', 'facing4bet_scenario')

# font and color theme
theme = lambda: None
theme.bfont = ('TkTextFont', 12, 'bold')
theme.dirfont = ('TkDefaultFont', 9)

if theme_set == 'dark':
    theme.fcolor = "#FFFFFF"
    theme.bgcolor = "#191919"
    theme.bgcolor2 = "#46515C"
    theme.bgcolor3 = "#333130"
    theme.btncolor = "#2F546E"
else:
    theme.fcolor = "#000000"
    theme.bgcolor = "#FFFFFF"
    theme.bgcolor2 = "#E5F1FD"
    theme.bgcolor3 = "#F1F5FF"
    theme.btncolor = "#73A9CF"

# dictionaries
idx_to_card = {0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8", 7: "9", 8: "T", 9: "J", 10: "Q", 11: "K", 12: "A"}
card_to_idx = {v: k for k, v in idx_to_card.items()}
range_to_label = {'R0': 'Open-', 'R1': '3Bet-', 'R2': '4Bet-', 'R3': '5Bet-', 'C0': 'Call-', 'C1': 'Flat-', 'C2': 'Call3Bet-', 'C3': 'Call4Bet-'}

# ---------------
# splash window
# ---------------

class Splash(tk.Toplevel):

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        splash_canvas = tk.Canvas(self, width=480, height=480, bg="white", bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=0)
        splash_img = tk.PhotoImage(file = os.getcwd() + '\\Images\\splash.png')
        splash_canvas.create_image(0, 0, anchor='nw', image=splash_img)
        splash_canvas.pack()

        self.overrideredirect(True)
        self.geometry("%dx%d+%d+%d" % (480, 480, self.winfo_screenwidth()/2 - 240, self.winfo_screenheight()/2 - 240))
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
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (3*ws/4, 3*hs/4, 1*ws/8, 1*hs/8))
        self.withdraw()

        splash = Splash(self)
        time.sleep(1)
        splash.destroy()

        tk.Tk.iconbitmap(self, "icon.ico")
        tk.Tk.wm_title(self, "6-max Preflop Range Training")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu_bar = tk.Menu(container)
        tk.Tk.config(self, menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Create New Range Directory...", command=lambda: create_range_pack())
        file_menu.add_command(label="Save Range Directory As...", command=lambda: save_range_pack())
        file_menu.add_command(label="Import Range Directory...", command=lambda: import_range_pack())
        file_menu.add_command(label="Delete Range Directory", command=lambda: delete_range_pack())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Preflop Trainer", command=lambda: train_settings())
        settings_menu.add_command(label="Ranger Editor", command=lambda: popup_general_settings())
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=lambda: docs_report())
        help_menu.add_command(label="Report Bug", command=lambda: bug_report())
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.frames = {}
        for F in (StartPage, RangeEdit):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
        self.deiconify()
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update()

    def on_exit(self):
        self.quit()
        self.destroy()

# ---------------
# training window
# ---------------

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=theme.bgcolor)

        # *** tab navigation ***
        switchframe = tk.Frame(self, bd=0, bg=theme.bgcolor, highlightbackground=theme.bgcolor, highlightcolor=theme.bgcolor, highlightthickness=0)

        pageBtn = tabButton(switchframe, ' Preflop Trainer ', lambda: controller.show_frame(StartPage), theme, 'on')
        navBtn = tabButton(switchframe, ' Range Editor ', lambda: controller.show_frame(RangeEdit), theme, 'off')
        pageBtn.pack(side=tk.LEFT)
        navBtn.pack(side=tk.LEFT)

        switchframe.grid(row=0, column=0, sticky='NEW')

        # *** text and accuracy ***
        textframe = tk.Frame(self, bd=0, bg=theme.bgcolor, highlightbackground=theme.bgcolor, highlightcolor=theme.bgcolor, highlightthickness=0)

        self.hotkeytext = tk.Label(textframe, text='Hotkeys:\nPress "f" to pure fold\nPress "c" to pure call\nPress "r" to pure raise\nPress "spacebar" to deal new hand', font=theme.dirfont, bg=theme.bgcolor, activebackground=theme.btncolor, bd=0, fg=theme.fcolor, justify="left")
        self.dealhandtext = tk.StringVar(self, "  Start Training  ")
        self.startBtn = cButton(textframe, self.dealhandtext, self.start_train, theme)
        self.accout = tk.StringVar(self, 'Accuracy:\nundef\n (0/0)')
        self.acctext = tk.Label(textframe, textvariable=self.accout, bd=0, bg=theme.bgcolor, fg=theme.fcolor, font=theme.dirfont, highlightbackground=theme.bgcolor, highlightcolor=theme.bgcolor, highlightthickness=0)

        self.hotkeytext.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        self.startBtn.grid(row=0, column=1, padx=5, pady=5, sticky = 'N')
        self.acctext.grid(row=0, column=2, padx=5, pady=5, sticky='E')
        self.hotkeytext.grid_remove()
        self.acctext.grid_remove()

        textframe.rowconfigure(0, weight=1)
        textframe.columnconfigure([0,1,2], weight=1, uniform='x')
        textframe.grid(row=1, column=0, sticky='NEW')

        # *** table canvas ***
        plotframe = tk.Frame(self, bd=0, bg=theme.bgcolor, highlightbackground=theme.fcolor, highlightcolor=theme.fcolor, highlightthickness=0)
        self.tablereplayer = TableReplay(plotframe, 'CO', 'EP', 3, 'AdAs', theme)
        self.tablereplayer.pack()
        plotframe.rowconfigure(0, weight=2)
        plotframe.grid(row=2, column=0, padx=5, pady=5)

        # *** slider button controls ***
        trainingInterface = tk.Frame(self, bd=0, bg=theme.bgcolor, highlightbackground=theme.bgcolor, highlightcolor=theme.bgcolor, highlightthickness=0)

        self.sgraph = SliderGraphical(trainingInterface, theme)
        self.okayBtn = cButton(trainingInterface, "Enter", self.get_options, theme)
        self.raiseBtn = cButton(trainingInterface, '         Pure Raise         ', lambda: self.pureraise(self), theme)
        self.callBtn = cButton(trainingInterface, '         Pure Call         ', lambda: self.purecall(self), theme)
        self.foldBtn = cButton(trainingInterface, '         Pure Fold         ', lambda: self.purefold(self), theme)
        self.sgraph.grid(row=0, column=0, columnspan=3, padx=0, pady=1)
        self.okayBtn.grid(row=0, column=3, padx=5, pady=2, sticky='S')
        self.raiseBtn.grid(row=1, column=0, padx=3, pady=2)
        self.callBtn.grid(row=1, column=1, padx=3, pady=2)
        self.foldBtn.grid(row=1, column=2, padx=3, pady=2)
        self.sgraph.grid_remove()
        self.okayBtn.grid_remove()
        self.raiseBtn.grid_remove()
        self.callBtn.grid_remove()
        self.foldBtn.grid_remove()

        trainingInterface.grid(row=3, column=0, sticky='N')

        # *** status bar ***
        self.statusvar = tk.StringVar(self, 'Status Idle')
        self.statuslabel = tk.Label(self, textvariable=self.statusvar, bd=1, relief='sunken', anchor='w')
        self.statuslabel.grid(row=3, column=0, sticky='SEW')

        # *** grid configure ***
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1, uniform='x')
        self.rowconfigure(1, weight=2, uniform='x')
        self.rowconfigure(2, weight=10, uniform='x')
        self.rowconfigure(3, weight=3, uniform='x')

        # *** key binds ***
        self.bind_all("f", self.purefold)
        self.bind_all("c", self.purecall)
        self.bind_all("r", self.pureraise)
        self.bind_all("<space>", self.start_train)

        # *** init variables ***
        self.correct = 0
        self.num = 0
        self.my_hand = "AsKs"

    # training functions
    def purefold(self, event):
        self.sgraph.rfreq = 0
        self.sgraph.cfreq = 0
        self.get_options()

    def purecall(self, event):
        self.sgraph.rfreq = 0
        self.sgraph.cfreq = 100
        self.get_options()

    def pureraise(self, event):
        self.sgraph.rfreq = 100
        self.sgraph.cfreq = 0
        self.get_options()

    def get_options(self):
        save_inp_raise = int(self.sgraph.rfreq)
        save_inp_call = int(self.sgraph.cfreq)

        # convert range strings to array data
        raise_freq = readRange("R", myPos_idx, myPos_p1, myPos_p2)
        call_freq = readRange("C", myPos_idx, myPos_p1, myPos_p2)

        if self.my_hand[1] == self.my_hand[3]:
            hand_j = 12 - card_to_idx[self.my_hand[2]]
            hand_i = 12 - card_to_idx[self.my_hand[0]]
        else:
            hand_j = 12 - card_to_idx[self.my_hand[0]]
            hand_i = 12 - card_to_idx[self.my_hand[2]]

        trueraise = raise_freq[hand_j][hand_i]
        truecall = call_freq[hand_j][hand_i]

        # compare and determine right/wrong
        if abs(int(trueraise) - int(save_inp_raise)) <= training_tolerance and abs(int(truecall) - int(save_inp_call)) <= training_tolerance:
            self.statusvar.set("Correct!")
            self.correct += 1
            self.num += 1
            self.accout.set(f'Accuracy:\n{100*self.correct/self.num:.1f}%\n({self.correct}/{self.num})')
            if toggle_sound:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.getcwd() + '\\Audio\\sfx_correct.mp3'))
            if show_ranges == 0:
                self.rangepopup(raise_freq, call_freq, hand_i, hand_j)
            else:
                self.start_train()
        else:
            self.statusvar.set("Wrong! Raise: " + str(trueraise) + "%  and Call: " + str(truecall) + "%")
            self.num += 1
            self.accout.set(f'Accuracy:\n{100*self.correct/self.num:.1f}%\n({self.correct}/{self.num})')
            if toggle_sound:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.getcwd() + '\\Audio\\sfx_error.mp3'))
            if show_ranges < 2:
                self.rangepopup(raise_freq, call_freq, hand_i, hand_j)
            else:
                self.start_train()

    def start_train(self, *args):
        global myPos_idx, fdir, myPos_p1, myPos_p2, range_dir, open_scenario, facingopen_scenario, facing3bet_scenario, facing4bet_scenario

        # Bring in graphical slider options
        self.dealhandtext.set("Deal Next Hand")
        self.raiseBtn.grid()
        self.callBtn.grid()
        self.foldBtn.grid()
        self.okayBtn.grid()
        self.sgraph.grid()
        if show_hotkeys:
            self.hotkeytext.grid()
        if show_accuracy:
            self.acctext.grid()

        # Randomly determine positions and deal hands within range
        scen_check = [open_scenario, facingopen_scenario, facing3bet_scenario, facing4bet_scenario]

        if scen_check == [0,0,0,0]:
            self.statusvar.set('All training scenarios have been deselected, and no hand dealt')
            return
        [myPos_idx, myPos_p1, myPos_p2, myPos_p3] = deal_pos()
        while scen_check[myPos_idx] == 0:
            [myPos_idx, myPos_p1, myPos_p2, myPos_p3] = deal_pos()

        self.my_hand = deal_hand()

        # check if hand is within proper range given situation or redeal
        if myPos_idx == 2 or myPos_idx == 3:
            if myPos_idx == 2:
                f = open(fdir + "\\Range Packages\\" + range_dir + "\\" + "Open-" + myPos_p1 + ".txt")
            else:
                f = open(fdir + "\\Range Packages\\" + range_dir + "\\3Bet-" + myPos_p1 + "vs" + myPos_p2 + ".txt")

            contents = f.read()
            if contents:
                flag = in_range(self.my_hand, contents)
                while not flag:
                    self.my_hand = deal_hand()
                    flag = in_range(self.my_hand, contents)
            f.close()

        # update table replayer
        self.tablereplayer.herocards = self.my_hand
        self.tablereplayer.heropos = myPos_p1
        self.tablereplayer.vilpos = myPos_p2
        self.tablereplayer.situation_index = myPos_idx
        self.tablereplayer.update()

        # update text training label
        if myPos_idx == 0:
            self.statusvar.set('Dealt ' + self.my_hand + ' in ' + myPos_p1 + ' - Open?')
        elif myPos_idx == 1:
            self.statusvar.set('Dealt ' + self.my_hand + ' in ' + myPos_p1 + ' - ' + myPos_p3 + ' from ' + myPos_p2)
        elif myPos_idx == 2:
            self.statusvar.set('Dealt ' + self.my_hand + ' in ' + myPos_p1 + ' - ' + myPos_p3 + ' from ' + myPos_p2)
        elif myPos_idx == 3:
            self.statusvar.set('Dealt ' + self.my_hand + ' in ' + myPos_p1 + ' - ' + myPos_p3 + ' from ' + myPos_p2)
        if toggle_sound:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Audio\\deal.mp3'))

    def rangepopup(self, raise_freq, call_freq, hi, hj):
        self.rpopup = tk.Toplevel()
        tk.Tk.iconbitmap(self.rpopup, "icon.ico")
        ws = self.rpopup.winfo_screenwidth()
        hs = self.rpopup.winfo_screenheight()
        self.rpopup.geometry('%dx%d+%d+%d' % (ws/2, hs/2, ws/4, hs/4))
        
        if myPos_idx == 0:
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Open')
        elif myPos_idx == 1:
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Facing Open from ' + myPos_p2)
        elif myPos_idx == 2:
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Facing 3Bet from ' + myPos_p2)
        elif myPos_idx == 3:
            self.rpopup.wm_title('Range Viewer: ' + myPos_p1 + ' - Facing 4Bet from ' + myPos_p2)

        self.rpopup.configure(bg=theme.bgcolor)

        raiselabel = tk.Label(self.rpopup, text='Raise Range', font=theme.dirfont, bg=theme.bgcolor, activebackground=theme.btncolor, bd=0, fg=theme.fcolor)
        calllabel = tk.Label(self.rpopup, text='Call Range', font=theme.dirfont, bg=theme.bgcolor, activebackground=theme.btncolor, bd=0, fg=theme.fcolor)
       
        raiseExp = RaiseViewer(self.rpopup, theme)
        callExp = CallViewer(self.rpopup, theme)
        raiseExp.weights = raise_freq
        callExp.weights = call_freq
        raiseExp.range_canvas.itemconfig(raiseExp.rectgrid[hj][hi], width=3)
        callExp.range_canvas.itemconfig(callExp.rectgrid[hj][hi], width=3)
        raiseExp.lock = True
        callExp.lock = True

        okBtn = cButton(self.rpopup, "    OK    ", lambda: self.popupexit(self.rpopup), theme)

        raiselabel.grid(row=0, column=0, sticky='W', padx=5, pady=5)
        calllabel.grid(row=0, column=1, sticky='W', padx=5, pady=5)
        raiseExp.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        callExp.grid(row=1, column=1, sticky='NSEW', padx=5, pady=5)
        okBtn.grid(row=2, column=1, sticky='NE', padx=3, pady=5)
        
        raiseExp.update()
        callExp.update()      
        
        self.rpopup.rowconfigure(1 ,weight=10, uniform='x')
        self.rpopup.rowconfigure([0,2], weight=1, uniform='x')
        self.rpopup.columnconfigure([0,1], weight=1, uniform='x')

        self.rpopup.mainloop()

    def popupexit(self, popup):
        popup.destroy()
        self.start_train()


# -------------------
# range editor window
# -------------------

class RangeEdit(tk.Frame):

    def __init__(self, parent, controller):
        global range_dir, rclick_weight, g_myScen
        g_myScen =  1337

        tk.Frame.__init__(self, parent)
        self.configure(bg=theme.bgcolor)

        # *** tab navigation ***
        switchframe = tk.Frame(self, bd=0, bg=theme.bgcolor, highlightbackground=theme.bgcolor, highlightcolor=theme.bgcolor, highlightthickness=0)

        pageBtn = tabButton(switchframe, ' Preflop Trainer ', lambda: controller.show_frame(StartPage), theme, 'off')
        navBtn = tabButton(switchframe, ' Range Editor ', lambda: controller.show_frame(RangeEdit), theme, 'on')
        pageBtn.pack(side = tk.LEFT)
        navBtn.pack(side = tk.LEFT)

        switchframe.grid(row=0, column=0, sticky='NW', columnspan=2)

        # paned window
        panedwindow = tk.PanedWindow(self, bd=4, bg=theme.bgcolor, showhandle=False, relief="flat")
        panedwindow.grid(row=1,column=0,sticky='NSEW', pady=5, padx=5)

        self.fileEXP = tk.Frame(panedwindow, bd=0, bg=theme.bgcolor, highlightbackground="black", highlightcolor="black", highlightthickness=0)

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

        if not range_dir:
            create_rp_name('default')
        if not os.path.isdir('Range Packages\\' + range_dir):
            create_rp_name(range_dir)

        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Open-EP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call-EP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'A', text="EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","EP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Open-MP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call-MP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'B', text="MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","MP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Open-CO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call-CO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'C', text="CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","CO","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Open-BN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call-BN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'D', text="BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","BN","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Open-SB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call-SB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir1", "end", 'E', text="SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("0","SB","BB"))

        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-MPvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-MPvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'A1', text="MP vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","MP","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-COvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-COvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'B1', text="CO vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","CO","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-COvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-COvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'C1', text="CO vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","CO","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BNvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BNvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'D1', text="BN vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BN","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BNvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BNvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'E1', text="BN vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BN","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BNvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BNvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'F1', text="BN vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BN","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-SBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-SBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'G1', text="SB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-SBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-SBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'H1', text="SB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-SBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-SBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'I1', text="SB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-SBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-SBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'J1', text="SB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","SB","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'K1', text="BB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'L1', text="BB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'M1', text="BB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'N1', text="BB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\3Bet-BBvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Flat-BBvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir2", "end", 'O1', text="BB vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("1","BB","SB"))

        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-EPvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-EPvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'A2', text="EP vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-EPvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-EPvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'B2', text="EP vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-EPvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-EPvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'C2', text="EP vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-EPvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-EPvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'D2', text="EP vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-EPvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-EPvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'E2', text="EP vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","EP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-MPvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-MPvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'F2', text="MP vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-MPvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-MPvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'G2', text="MP vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-MPvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-MPvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'H2', text="MP vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-MPvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-MPvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'I2', text="MP vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","MP","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-COvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-COvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'J2', text="CO vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","CO","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-COvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-COvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'K2', text="CO vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","CO","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-COvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-COvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'L2', text="CO vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","CO","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-BNvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-BNvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'M2', text="BN vs SB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","BN","SB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-BNvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-BNvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'N2', text="BN vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","BN","BB"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\4Bet-SBvsBB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call3bet-SBvsBB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir3", "end", 'O2', text="SB vs BB",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("2","SB","BB"))

        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-MPvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-MPvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'A3', text="MP vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","MP","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-COvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-COvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'B3', text="CO vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","CO","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-COvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-COvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'C3', text="CO vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","CO","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BNvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BNvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'D3', text="BN vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BN","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BNvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BNvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'E3', text="BN vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BN","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BNvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BNvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'F3', text="BN vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BN","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-SBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-SBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'G3', text="SB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-SBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-SBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'H3', text="SB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-SBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-SBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'I3', text="SB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-SBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-SBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'J3', text="SB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","SB","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BBvsEP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BBvsEP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'K3', text="BB vs EP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","EP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BBvsMP.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BBvsMP.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'L3', text="BB vs MP",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","MP"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BBvsCO.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BBvsCO.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'M3', text="BB vs CO",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","CO"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BBvsBN.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BBvsBN.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'N3', text="BB vs BN",values=(f"{date:%Y-%m-%d %H:%M}"),tags = ("3","BB","BN"))
        date1 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\5Bet-BBvsSB.txt'))
        date2 = dt.datetime.fromtimestamp(os.path.getmtime('Range Packages\\' + range_dir + '\\Call4bet-BBvsSB.txt'))
        date = max(date1,date2)
        self.fileTree.insert("dir4", "end", 'O3', text="BB vs SB", values=(f"{date:%Y-%m-%d %H:%M}"), tags = ("3","BB","SB"))

        self.fileTree.bind("<Double-1>", self.OnDoubleClick)

        self.vsb.pack(side="right", fill="y")
        self.fileTree.pack(side="left", fill="both", expand=True)

        self.fileTree.configure(yscrollcommand=self.vsb.set)
        panedwindow.add(self.fileEXP)

        rangeExplorer = tk.Frame(panedwindow, padx=5, pady=5, bg=theme.bgcolor, width=1200, height=600)
        rangeExplorer.grid_propagate(False)

        self.raiseExp = RaiseViewer(rangeExplorer, theme)
        self.callExp = CallViewer(rangeExplorer, theme)
        self.callExp.grid(row=1, column=1, sticky='NSEW', padx=5, pady=5)
        self.raiseExp.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        self.callExp.lock = True
        self.raiseExp.lock = True
        self.callExp.increment = rclick_weight
        self.raiseExp.increment = rclick_weight

        raiselabel = tk.Label(rangeExplorer, text='Raise Range', font=theme.dirfont, bg=theme.bgcolor, activebackground=theme.btncolor, bd=0, fg=theme.fcolor)
        raiselabel.grid(row=0, column=0, sticky='W', padx=5, pady=5)
        calllabel = tk.Label(rangeExplorer,text='Call Range',font=theme.dirfont, bg=theme.bgcolor,activebackground=theme.btncolor,bd=0, fg=theme.fcolor)
        calllabel.grid(row=0,column=1,sticky='W',padx=5,pady=5)

        rclearBtn = cButton(rangeExplorer, 'Clear Range', self.raiseExp.clear, theme)
        rinvertBtn = cButton(rangeExplorer, 'Inverse Range', lambda: self.raiseExp.invert_weights(self.callExp.weights), theme)
        rselectBtn = cButton(rangeExplorer, 'Select All', self.raiseExp.selectall, theme)
        cclearBtn = cButton(rangeExplorer, 'Clear Range', self.callExp.clear, theme)
        cinvertBtn = cButton(rangeExplorer, 'Inverse Range', lambda: self.callExp.invert_weights(self.raiseExp.weights), theme)
        cselectBtn = cButton(rangeExplorer, 'Select All', self.callExp.selectall, theme)
        rclearBtn.grid(row=0, column=0, sticky='W', padx=3, pady=5)
        rinvertBtn.grid(row=0, column=0, padx=3, pady=5)
        rselectBtn.grid(row=0, column=0, sticky='E', padx=3, pady=5)
        cclearBtn.grid(row=0,column=1, sticky='W', padx=3, pady=5)
        cinvertBtn.grid(row=0, column=1, padx=5, pady=3)
        cselectBtn.grid(row=0,column=1,sticky='E', padx=3, pady=5)

        rloadBtn = cButton(rangeExplorer, 'Load Range', lambda: self.loadRange('R'), theme)
        rsaveBtn = cButton(rangeExplorer, 'Save Range', lambda: self.saveRange('R'), theme)
        rloadBtn.grid(row=2, column=0, sticky='W', padx=3, pady=5)
        rsaveBtn.grid(row=2, column=0, sticky='E', padx=3, pady=5)

        cloadBtn = cButton(rangeExplorer, 'Load Range', lambda: self.loadRange('C'), theme)
        csaveBtn = cButton(rangeExplorer, 'Save Range', lambda: self.saveRange('C'), theme)
        cloadBtn.grid(row=2, column=1, sticky='W', padx=3, pady=5)
        csaveBtn.grid(row=2, column=1, sticky='E', padx=3, pady=5)

        rangeExplorer.columnconfigure([0,1],weight=1,uniform='x')
        rangeExplorer.rowconfigure(1,weight=10,uniform='x')
        rangeExplorer.rowconfigure(0,weight=1,uniform='x')
        rangeExplorer.rowconfigure(2,weight=1,uniform='x')
        panedwindow.add(rangeExplorer)

        # *** Status Bar ***
        self.statusvar = tk.StringVar(self, 'Status Idle')
        self.status = tk.Label(self, textvariable=self.statusvar, bd=1, relief='sunken', anchor='w')
        self.status.grid(row=3,column=0,sticky='SEW')

        # *** grid configure ***
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def saveRange(self,param):
        global g_myScen
        if g_myScen == 1337:
            return
        if param == 'C':
            writeRange("C", g_myScen, g_myPos1, g_myPos2, self.callExp.weights)
        else:
            writeRange("R", g_myScen, g_myPos1, g_myPos2, self.raiseExp.weights)

        if g_myScen == 0:
            flocation = fdir + '\\Range Packages\\' + range_dir + "\\" + range_to_label[param + str(g_myScen)] + g_myPos1 + ".txt"
        else:
            flocation = fdir + '\\Range Packages\\' + range_dir + "\\" + range_to_label[param + str(g_myScen)] + g_myPos1 + "vs" + g_myPos2 + ".txt"
        date = dt.datetime.fromtimestamp(os.path.getmtime(flocation))
        format_date = f"{date:%Y-%m-%d %H:%M}"
        self.fileTree.item(item,values=(str(format_date)))
        self.statusvar.set('Range Saved Successfully')
        return

    def loadRange(self,param):
        global g_myScen
        if g_myScen == 1337:
            return
        filename = filedialog.askopenfilename(title = "Select Range in PIO .txt format",filetypes = (("txt files","*.txt"),("all files","*.*")))
        if not filename: return
        rangeselect = readRangefile(filename)
        if param == 'C':
            self.callExp.weights = rangeselect
            self.callExp.update()
        else:
            self.raiseExp.weights = rangeselect
            self.raiseExp.update()
        self.statusvar.set('Range Loaded Successfully')
        return

    def OnDoubleClick(self,event):
        global g_myScen, g_myPos1, g_myPos2, treeIdx, item, rclick_weight
        self.callExp.lock = False
        self.raiseExp.lock = False
        self.callExp.increment = rclick_weight
        self.raiseExp.increment = rclick_weight
        item = self.fileTree.identify('item', event.x, event.y)
        treeText = self.fileTree.item(item, "tags")
        if len(treeText) > 0:
            g_myScen = int(treeText[0])
            g_myPos1, g_myPos2 = treeText[1], treeText[2]
            self.raiseExp.weights = readRange("R", g_myScen, g_myPos1, g_myPos2)
            self.callExp.weights = readRange("C", g_myScen, g_myPos1, g_myPos2)
            self.raiseExp.update()
            self.callExp.update()

# ---------------
# settings windows
# ---------------

def popup_general_settings():
    global parser, range_dir, rclick_weight

    rclick_weight = parser.getint('settings','rclick_weight')
    range_dir = parser.get('settings','Range Package')

    def save_general_settings(flag):
        global range_dir, rclick_weight

        rclick_weight = int(entry1.get())
        range_dir = packOpt.get()

        if flag == 'close':
            popup.destroy()

        parser['settings']['Range Package'] = range_dir
        parser['settings']['rclick_weight'] = str(rclick_weight)

        with open('prefloptrain.ini','w') as configfile:
            parser.write(configfile)

        return

    popup = tk.Tk()

    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Range Editor Settings")
    popup.configure(bg=theme.bgcolor)

    REditgroup = tk.LabelFrame(popup, text='Range Editor', font=theme.dirfont, padx=5, pady=5, bg=theme.bgcolor, fg=theme.fcolor)

    label = tk.Label(REditgroup, text='Right-Click Increment (%):', font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor)
    label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry1 = tk.Entry(REditgroup, width=10, bd=0, bg=theme.bgcolor2, highlightbackground=theme.fcolor, highlightthickness=1, fg=theme.fcolor)
    entry1.insert(0, rclick_weight)
    entry1.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    label = tk.Label(REditgroup, text='Range Pack:', font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor)
    label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    root = fdir + '\\Range Packages'
    dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]

    style = ttk.Style(REditgroup)
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground=theme.bgcolor2, bg=theme.bgcolor2, foreground=theme.fcolor)

    packOpt = ttk.Combobox(REditgroup, values=dirlist, width=30)
    packOpt.current(dirlist.index(range_dir))
    packOpt.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    REditgroup.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    windowCont = tk.Frame(popup, bd=0, highlightbackground="black", highlightcolor=theme.btncolor, highlightthickness=0, bg=theme.bgcolor)

    okBtn = cButton(windowCont, "    OK    ", lambda: save_general_settings('close'), theme)
    cancelBtn = cButton(windowCont, "Cancel", lambda: popup.destroy(), theme)
    applyBtn = cButton(windowCont, " Apply ", lambda: save_general_settings('open'), theme)
    okBtn.grid(row=0,column=0, padx=3, pady=5, sticky='e')
    cancelBtn.grid(row=0,column=1, padx=3, pady=5, sticky='e')
    applyBtn.grid(row=0,column=2, padx=3, pady=5, sticky='e')

    windowCont.rowconfigure(0, weight=1)
    windowCont.grid(row=1, column=0, padx=5, pady=5, sticky='e')

    popup.columnconfigure(0, weight=1)
    popup.rowconfigure(0, weight=3, uniform='x')
    popup.rowconfigure(1, weight=1, uniform='x')

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (420, 300, ws/4, hs/4))
    popup.mainloop()

def train_settings():
    global parser, show_ranges, training_tolerance, show_hotkeys, show_accuracy, toggle_sound, open_scenario, facingopen_scenario, facing3bet_scenario, facing4bet_scenario
    show_ranges = parser.getint('settings','show_ranges')
    training_tolerance = parser.getint('settings','training_tolerance')
    show_hotkeys = parser.getint('settings','show_hotkeys')
    show_accuracy = parser.getint('settings','show_accuracy')
    toggle_sound = parser.getint('settings','toggle_sound')
    open_scenario = parser.getint('settings','open_scenario')
    facingopen_scenario = parser.getint('settings','facingopen_scenario')
    facing3bet_scenario = parser.getint('settings','facing3bet_scenario')
    facing4bet_scenario = parser.getint('settings','facing4bet_scenario')

    def save_train_settings(flag):
        global show_ranges, training_tolerance, show_hotkeys, show_accuracy, toggle_sound, open_scenario, facingopen_scenario, facing3bet_scenario, facing4bet_scenario

        show_ranges = int(showr.get())
        training_tolerance = int(tolEntry.get())
        show_hotkeys = int(hotvar.get())
        show_accuracy = int(accvar.get())
        toggle_sound = int(audiovar.get())
        open_scenario = int(scenvar1.get())
        facingopen_scenario = int(scenvar2.get())
        facing3bet_scenario = int(scenvar3.get())
        facing4bet_scenario = int(scenvar4.get())

        if flag == 'close':
            popup.destroy()

        parser['settings']['show_ranges'] = str(show_ranges)
        parser['settings']['training_tolerance'] = str(training_tolerance)
        parser['settings']['show_hotkeys'] = str(show_hotkeys)
        parser['settings']['show_accuracy'] = str(show_accuracy)
        parser['settings']['toggle_sound'] = str(toggle_sound)
        parser['settings']['open_scenario'] = str(open_scenario)
        parser['settings']['facingopen_scenario'] = str(facingopen_scenario)
        parser['settings']['facing3bet_scenario'] = str(facing3bet_scenario)
        parser['settings']['facing4bet_scenario'] = str(facing4bet_scenario)

        with open('prefloptrain.ini','w') as configfile:
            parser.write(configfile)

        return

    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Preflop Trainer Settings")
    popup.configure(bg=theme.bgcolor)

    Optgroup = tk.LabelFrame(popup, text='Range Popup', font=theme.dirfont, padx=5, pady=5, bg=theme.bgcolor, fg=theme.fcolor)
    Optgroup.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    showr = tk.IntVar(master = popup)
    showr.set(show_ranges)

    showranges1 = tk.Radiobutton(Optgroup, text = "Range popup appears after every hand", value=0, variable=showr, bg=theme.bgcolor, activebackground=theme.bgcolor2, fg=theme.fcolor, selectcolor=theme.bgcolor)
    showranges2 = tk.Radiobutton(Optgroup, text = "Range popup appears if an error is made", value=1, variable=showr, bg=theme.bgcolor, activebackground=theme.bgcolor2, fg=theme.fcolor, selectcolor=theme.bgcolor)
    showranges3 = tk.Radiobutton(Optgroup, text = "Range popup disabled", value=2, variable=showr, bg=theme.bgcolor, activebackground=theme.bgcolor2, fg=theme.fcolor, selectcolor=theme.bgcolor)

    if showr.get() == 0:
        showranges1.select()
    elif showr.get() == 1:
        showranges2.select()
    else:
        showranges3.select()

    showranges1.pack(anchor='w')
    showranges2.pack(anchor='w')
    showranges3.pack(anchor='w')

    Tolgroup = tk.LabelFrame(popup, text = 'Tolerance', padx = 5, pady = 5, bg=theme.bgcolor, fg=theme.fcolor)
    Tolgroup.grid(row=1,column=0, padx = 5, pady = 5, sticky='nsew')

    tolLabel = tk.Label(Tolgroup, text = 'Tolerance for correct answer (%):', bg=theme.bgcolor, fg=theme.fcolor)
    tolLabel.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    tolEntry = tk.Entry(Tolgroup, width=10, bd=0, highlightbackground="black", highlightthickness=1, bg=theme.bgcolor2, fg=theme.fcolor)
    tolEntry.insert(0, training_tolerance)
    tolEntry.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    Showgroup = tk.LabelFrame(popup, text='Toggle (Requires Program Restart)', padx=5, pady=5, bg=theme.bgcolor, fg=theme.fcolor)
    Showgroup.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    hotvar = tk.IntVar(master = popup)
    accvar = tk.IntVar(master = popup)

    hotkeyBtn = tk.Checkbutton(Showgroup, text = 'Hotkey Information', variable=hotvar, bg=theme.bgcolor, fg=theme.fcolor, selectcolor=theme.bgcolor)
    accuracyBtn = tk.Checkbutton(Showgroup, text = 'Accuracy Tracking', variable=accvar, bg=theme.bgcolor, fg=theme.fcolor, selectcolor=theme.bgcolor)
    hotkeyBtn.pack(anchor='w')
    accuracyBtn.pack(anchor='w')

    if show_hotkeys:
        hotkeyBtn.select()
    else:
        hotkeyBtn.deselect()
    if show_accuracy:
        accuracyBtn.select()
    else:
        accuracyBtn.deselect()

    Audiogroup = tk.LabelFrame(popup, text='Audio', padx=5, pady=5, bg=theme.bgcolor, fg=theme.fcolor)
    Audiogroup.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
    audiovar = tk.IntVar(master = popup)
    audioBtn = tk.Checkbutton(Audiogroup, text='Play dealer and right/wrong sounds', variable=audiovar, bg=theme.bgcolor, fg=theme.fcolor, selectcolor=theme.bgcolor)
    audioBtn.pack(anchor = 'w')

    if toggle_sound:
        audioBtn.select()
    else:
        audioBtn.deselect()

    Scenariogroup = tk.LabelFrame(popup, text='Practice Scenarios', padx=5, pady=5, bg=theme.bgcolor, fg=theme.fcolor)
    Scenariogroup.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
    scenvar1 = tk.IntVar(master = popup)
    scenvar2 = tk.IntVar(master = popup)
    scenvar3 = tk.IntVar(master = popup)
    scenvar4 = tk.IntVar(master = popup)
    scenBtn1 = tk.Checkbutton(Scenariogroup, text='Open', variable=scenvar1, bg=theme.bgcolor, fg=theme.fcolor, selectcolor=theme.bgcolor)
    scenBtn2 = tk.Checkbutton(Scenariogroup, text='Facing Open', variable=scenvar2, bg=theme.bgcolor, fg=theme.fcolor, selectcolor=theme.bgcolor)
    scenBtn3 = tk.Checkbutton(Scenariogroup, text='Facing 3Bet', variable=scenvar3, bg=theme.bgcolor, fg=theme.fcolor, selectcolor=theme.bgcolor)
    scenBtn4 = tk.Checkbutton(Scenariogroup, text='Facing 4Bet', variable=scenvar4, bg=theme.bgcolor, fg=theme.fcolor, selectcolor=theme.bgcolor)
    scenBtn1.pack(anchor = 'w')
    scenBtn2.pack(anchor = 'w')
    scenBtn3.pack(anchor = 'w')
    scenBtn4.pack(anchor = 'w')

    if open_scenario:
        scenBtn1.select()
    else:
        scenBtn1.deselect()
    if facingopen_scenario:
        scenBtn2.select()
    else:
        scenBtn2.deselect()
    if facing3bet_scenario:
        scenBtn3.select()
    else:
        scenBtn3.deselect()
    if facing4bet_scenario:
        scenBtn4.select()
    else:
        scenBtn4.deselect()

    windowCont = tk.Frame(popup, bd=0, highlightbackground="black", highlightcolor=theme.btncolor, highlightthickness=0, bg=theme.bgcolor)

    okBtn = cButton(windowCont, "    OK    ", lambda: save_train_settings('close'), theme)
    cancelBtn = cButton(windowCont, "Cancel", lambda: popup.destroy(), theme)
    applyBtn = cButton(windowCont, " Apply ", lambda: save_train_settings('open'), theme)
    okBtn.grid(row=0,column=0, padx=3, pady=5, sticky='e')
    cancelBtn.grid(row=0,column=1, padx=3, pady=5, sticky='e')
    applyBtn.grid(row=0,column=2, padx=3, pady=5, sticky='e')

    windowCont.rowconfigure(0, weight=1)
    windowCont.grid(row=5, column=0, padx=5, pady=5, sticky='e')

    popup.columnconfigure(0, weight=1)
    popup.rowconfigure([0,1,2,3,4], weight=3)
    popup.rowconfigure(5 ,weight=1, uniform='x')

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (420, 620, ws/4, hs/4))
    popup.mainloop()

# ---------------
# functions
# ---------------

def create_range_pack():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Add New Range Directory")
    popup.resizable(0,0)
    popup.configure(bg=theme.bgcolor)

    label = tk.Label(popup, text='Range directory name:', font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor)
    label.grid(row=0, column=0, padx=5, pady=5)
    entry = tk.Entry(popup, width=60, bd=0, bg=theme.bgcolor2, highlightbackground="black", highlightthickness=1, fg=theme.fcolor)
    entry.insert(0,'')
    entry.grid(row=0, column=1, padx=5, pady=5)

    createBtn = cButton(popup, " Create ", lambda: createRP(popup, entry), theme)
    cancelBtn = cButton(popup, "Cancel", lambda: popup.destroy(), theme)
    createBtn.grid(row=0, column=2, sticky='N', padx=3, pady=5)
    cancelBtn.grid(row=1, column=2, sticky='N', padx=3, pady=5)

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (640, 90, ws/2 - 320, hs/2 - 45))
    popup.mainloop()

def createRP(popup, entry):
    global range_dir
    range_dir = entry.get()
    try:
        os.mkdir(fdir + '\\Range Packages\\' + range_dir)
    except OSError:
        print ("Creation of the directory %s failed" % range_dir)
    else:
        print ("Successfully created the directory %s " % range_dir)

    pos = ['BB','SB','BN','CO','MP','EP']

    for idx, pidx in enumerate(pos):
        f = open('Range Packages\\' + range_dir + "\\Call-" + pidx + ".txt", "w+")
        f.close()
        f = open('Range Packages\\' + range_dir + "\\Open-" + pidx + ".txt", "w+")
        f.close()
        for idx2, pidx2 in enumerate(pos):
            if idx2 > idx:
                f = open('Range Packages\\' + range_dir + "\\Flat-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\3Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\Call4bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\5Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
            if idx2 < idx:
                f = open('Range Packages\\' + range_dir + "\\Call3bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\4Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()

    parser['settings']['Range Package'] = range_dir
    with open('prefloptrain.ini','w') as configfile:
        parser.write(configfile)
    popup.destroy()

def create_rp_name(name):
    global range_dir
    range_dir = name

    if not os.path.isdir(fdir + '\\Range Packages'):
        os.mkdir(f'{fdir}\\Range Packages')
    try:
        os.mkdir(f'{fdir}\\Range Packages\\{range_dir}')
    except OSError:
        print ("Creation of the directory %s failed" % range_dir)
    else:
        print ("Successfully created the directory %s " % range_dir)

    pos = ['BB','SB','BN','CO','MP','EP']

    for idx, pidx in enumerate(pos):
        f = open('Range Packages\\' + range_dir + "\\Call-" + pidx + ".txt", "w+")
        f.close()
        f = open('Range Packages\\' + range_dir + "\\Open-" + pidx + ".txt", "w+")
        f.close()
        for idx2, pidx2 in enumerate(pos):
            if idx2 > idx:
                f = open('Range Packages\\' + range_dir + "\\Flat-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\3Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\Call4bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\5Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
            if idx2 < idx:
                f = open('Range Packages\\' + range_dir + "\\Call3bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()
                f = open('Range Packages\\' + range_dir + "\\4Bet-" + pidx + "vs" + pidx2 + ".txt", "w+")
                f.close()

    parser['settings']['Range Package'] = range_dir
    with open('prefloptrain.ini','w') as configfile:
        parser.write(configfile)

def save_range_pack():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Save Range Directory As")
    popup.resizable(0,0)
    popup.configure(bg=theme.bgcolor)

    label = tk.Label(popup, text='Range directory name:', font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor)
    label.grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(popup, width=60, bd=0, bg=theme.bgcolor2, highlightbackground="black",highlightthickness=1, fg=theme.fcolor)
    entry.insert(0,'')
    entry.grid(row=0, column=1, padx=10, pady=5)

    saveBtn = cButton(popup, "   Save   ", lambda: saveRP(popup, entry), theme)
    cancelBtn = cButton(popup, "Cancel", lambda: popup.destroy(), theme)
    saveBtn.grid(row=0, column=2, sticky='N', padx=3, pady=5)
    cancelBtn.grid(row=1, column=2, sticky='N', padx=3, pady=5)

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (640, 90, ws/2 - 320, hs/2 - 45))

    popup.mainloop()

def delete_range_pack():
    global range_dir

    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Delete Range Directory")
    popup.resizable(0,0)
    popup.configure(bg=theme.bgcolor)
    label = tk.Label(popup, text= "Delete the range directory \"" + range_dir + "\" permanently?", font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor)
    label.grid(row=0, column=0, sticky='NSEW', padx=15, pady=5)

    yesBtn = cButton(popup, "  Yes  ", lambda: delete_confirm(popup), theme)
    noBtn = cButton(popup, "   No   ", lambda: popup.destroy(), theme)
    yesBtn.grid(row=0, column=1, sticky='E', padx=3, pady=5)
    noBtn.grid(row=1, column=1, sticky='E', padx=3, pady=5)

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (500, 80, 3*ws/8, 9*hs/20))

    popup.mainloop()

def delete_confirm(popup):
    global range_dir

    popup.destroy()
    shutil.rmtree(fdir + '\\Range Packages\\' + range_dir)
    if next(os.walk(fdir + '\\Range Packages\\'))[1]:
        range_dir = next(os.walk(fdir + '\\Range Packages\\'))[1][0]
    else:
        create_rp_name('empty')
        range_dir = 'empty'

    parser['settings']['Range Package'] = range_dir
    with open('prefloptrain.ini','w') as configfile:
        parser.write(configfile)

def saveRP(popup, entry):
    global range_dir
    range_dir_future = entry.get()

    try:
        os.mkdir(fdir + '\\Range Packages\\' + range_dir_future)
    except OSError:
        print ("Creation of the directory %s failed" % range_dir_future)
    else:
        print ("Successfully created the directory %s " % range_dir_future)

    src = fdir +'\\Range Packages\\' + range_dir
    dst = fdir +'\\Range Packages\\' + range_dir_future

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

    range_dir = range_dir_future
    parser['settings']['Range Package'] = range_dir
    with open('prefloptrain.ini','w') as configfile:
        parser.write(configfile)

    popup.destroy()

def import_range_pack():
    global range_dir
    filename = filedialog.askdirectory(title = "Select Directory to Import Ranges From")
    range_dir_temp = os.path.basename(filename)
    try:
        os.mkdir(fdir + '\\Range Packages\\' + range_dir_temp)
    except OSError:
        return

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

        src = filename
        dst = fdir +'\\Range Packages\\' + range_dir_temp

        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)

    except OSError:
        shutil.rmtree(fdir + '\\Range Packages\\' + range_dir_temp)
        error_popup("Importing range directory failed, ensure text files are complete and formatted properly.")
        return

    range_dir = range_dir_temp
    parser['settings']['Range Package'] = range_dir
    with open('prefloptrain.ini','w') as configfile:
        parser.write(configfile)

def error_popup(message):
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Error")
    popup.resizable(0,0)
    popup.configure(bg=theme.bgcolor)
    label = tk.Label(popup, text=message, font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor)
    label.grid(row=0,column=0,sticky='NSEW', padx=15, pady=5)

    okBtn = cButton(popup, "    OK    ", lambda: popup.destroy(), theme)
    okBtn.grid(row=1, column=0, sticky='N', padx=3, pady=5)

    popup.columnconfigure(0,weight=1, uniform='x')
    popup.rowconfigure(0,weight=1, uniform='x')
    popup.rowconfigure(1,weight=1, uniform='x')

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (400, 80, 3*ws/8, 9*hs/20))

    popup.mainloop()

def bug_report():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Report Bug")
    popup.resizable(0,0)
    popup.configure(bg=theme.bgcolor)

    label = tk.Label(popup, text='Please send bug reports to jejmcclu@protonmail.com', font=theme.dirfont, bg=theme.bgcolor, fg=theme.fcolor)
    label.grid(row=0,column=0,sticky='NSEW', padx=15, pady=5)

    okBtn = cButton(popup, "    OK    ", lambda: popup.destroy(), theme)
    okBtn.grid(row=1, column=0, sticky='N', padx=3, pady=5)

    popup.columnconfigure(0, weight=1, uniform='x')
    popup.rowconfigure(0, weight=1, uniform='x')
    popup.rowconfigure(1, weight=1, uniform='x')

    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (400, 80, 3*ws/8, 9*hs/20))

    popup.mainloop()

def docs_report():
    popup = tk.Tk()
    tk.Tk.iconbitmap(popup, "icon.ico")
    popup.wm_title("Help Files")
    popup.configure(bg=theme.bgcolor)

    def onDoubleClick_docs(event):
        item = fileTree.identify('item', event.x, event.y)
        treeText = fileTree.item(item, "tags")
        if treeText[0] == '0':
            txt.pack_forget()
            txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        print(treeText[0])
        return

    # paned window
    panedwindow = tk.PanedWindow(popup, bd=4, bg=theme.bgcolor, showhandle=False, relief="flat")
    panedwindow.grid(row=0, column=0, sticky='NSEW', pady=5, padx=15)

    # file explorer
    fileEXP = tk.Frame(panedwindow, bd=0, bg=theme.bgcolor, highlightbackground="black", highlightcolor="black", highlightthickness=0)
    fileTree = ttk.Treeview(fileEXP, selectmode='browse')
    vsb = tk.Scrollbar(fileEXP, orient="vertical", command=fileTree.yview)
    fileTree["columns"] = ("one")
    fileTree.column("#0", width=125, minwidth=100, stretch=0)
    fileTree.heading("#0", text="Topics", anchor=tk.W)
    fileTree.insert("",0, "dir1", text="Preflop Trainer", values=(""), tags = ("0"))
    fileTree.insert("",1, "dir2", text="Range Editor", values=(""), tags = ("1"))
    fileTree.insert("",2, "dir3", text="Range Packages", values=(""), tags = ("2"))
    fileTree.insert("dir1", "end", 'A1', text="Settings", tags = ("P0"))
    fileTree.insert("dir2", "end", 'A2', text="Settings", tags = ("P1"))
    fileTree.insert("dir3", "end", 'A3', text="Topic1", tags = ("P2"))
    fileTree.insert("dir3", "end", 'B3', text="Topic2", tags = ("P3"))
    vsb.pack(side="right", fill="y")
    fileTree.pack(side="left", fill="both", expand=True)
    fileTree.configure(yscrollcommand=vsb.set)
    fileTree.bind("<Double-1>", onDoubleClick_docs)

    panedwindow.add(fileEXP)

    # text explorer
    docText = tk.Frame(panedwindow, padx=2, pady=2, bg=theme.bgcolor)

    txt = tk.Text(docText, bd=0, bg=theme.bgcolor, highlightbackground="black", highlightcolor="black", highlightthickness=1, fg=theme.fcolor)
    txt.tag_configure('title', font=theme.bfont)
    txt.tag_configure('main', font=theme.dirfont)
    txt.insert(tk.INSERT, "Preflop Trainer\n", 'title')
    txt.insert(tk.INSERT, """\nThe preflop trainer randomly deals you into preflop practice scenarios, where you can choose to purely fold, purely call, or purely raise your hand, or input any mixed frequencies for the three actions. Your action is then compared to the currently actived range package in the range editor, and feedback is given on whether your action was correct. \n\nTo begin, press the "Start Training" button. A hand will be dealt to you, and your action needs to be input at the bottom of the screen, or you can skip the hand by pressing the "Deal Next Hand" button at the top of the screen. If your desired action is at 100% frequency, you can press one of the "Pure Raise", "Pure Call", or "Pure Fold" buttons. If a mixed frequency is desired, the mixed frequency slider must be used. To move the divider between the raise/call frequencies, click and drag with the left mouse button. To move the divider between the call/fold frequencies, click and drag with the right mouse button. After the desired frequencies have been specified, press the "Enter" button. \n\nAlternatively, instead of selecting the buttons with the mouse, the following pre-assigned hotkeys may be used. <spacebar> to deal the next hand, <r> to pure raise, <c> to pure call, and <f> to pure fold. \n\n Once you have selected an action, a popup may appear showing you the correct raising and calling ranges in the position (depending on your settings this popup may appear always, only after a mistake, or never). To continue with training, press the "OK" button on the popup.""" ,'main')
    txt.config(state='disabled')

    txt2 = tk.Text(docText, bd=0, bg=theme.bgcolor, highlightbackground="black", highlightcolor="black", highlightthickness=1, fg=theme.fcolor)
    txt2.tag_configure('title', font=theme.bfont)
    txt2.tag_configure('main', font=theme.dirfont)
    txt2.insert(tk.INSERT, "Settings\n", 'title')
    txt2.insert(tk.INSERT, "test", 'main')
    txt2.config(state='disabled')

    scrollb = ttk.Scrollbar(docText, orient="vertical", command=txt.yview)
    scrollb.pack(side=tk.RIGHT, fill=tk.Y)
    txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    txt['yscrollcommand'] = scrollb.set

    panedwindow.add(docText)
    panedwindow.columnconfigure(0, weight=1)
    panedwindow.columnconfigure(1, weight=1)
    panedwindow.rowconfigure(0, weight=1)

    # button controls
    okBtn = cButton(popup, "    OK    ", lambda: popup.destroy(), theme)
    okBtn.grid(row=1, column=0, sticky='E', padx=3, pady=5)

    # configure format
    popup.columnconfigure(0, weight=1)
    popup.rowconfigure(0, weight=10, uniform='x')
    popup.rowconfigure(1, weight=1, uniform='x')
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    popup.geometry('%dx%d+%d+%d' % (ws/2, hs/2, ws/4, hs/4))
    popup.mainloop()

def readRangefile(filename):
    range_array = [[0 for x in range(13)] for x in range(13)]
    f = open(filename)
    split_contents = f.read().split(",")
    f.close()

    if not split_contents:
        return

    for freq in split_contents:
        if freq:
            c1 = card_to_idx[freq[0]]
            c2 = card_to_idx[freq[1]]

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

    return range_array

def readRange(CR, myScen, myPos1, myPos2):
    global range_dir
    range_array = [[0 for x in range(13)] for x in range(13)]

    if myScen == 0:
        f = open(fdir + '\\Range Packages\\' + range_dir + "\\" + range_to_label[CR + str(myScen)] + myPos1 + ".txt")
    else:
        f = open(fdir + '\\Range Packages\\' + range_dir + "\\" + range_to_label[CR + str(myScen)] + myPos1 + "vs" + myPos2 + ".txt")
    split_contents = f.read().split(",")
    f.close()

    if not split_contents:
        return

    for freq in split_contents:
        if freq:
            c1 = card_to_idx[freq[0]]
            c2 = card_to_idx[freq[1]]

            if len(freq) < 4:
                if len(freq) == 2:
                    range_array[12-c2][12-c1] = 100
                    range_array[12-c1][12-c2] = 100
                else:
                    if freq[2] == "s":
                        range_array[12-c2][12-c1] = 100
                    if freq[2] == "o":
                        range_array[12-c1][12-c2] = 100

            else:
                if freq[2] == ":":
                    range_array[12-c2][12-c1] = int(float(freq[3:])*100)
                    range_array[12-c1][12-c2] = int(float(freq[3:])*100)
                elif freq[2] == "s":
                    range_array[12-c2][12-c1] = int(float(freq[4:])*100)
                elif freq[2] == "o":
                    range_array[12-c1][12-c2] = int(float(freq[4:])*100)

    return range_array

def writeRange(CR, myScen, myPos1, myPos2, range_array):
    global range_dir
    if myScen == 0:
        f = open(fdir + '\\Range Packages\\' + range_dir + "\\" + range_to_label[CR + str(myScen)] + myPos1 + ".txt", "w+")
    else:
        f = open(fdir + '\\Range Packages\\' + range_dir + "\\" + range_to_label[CR + str(myScen)] + myPos1 + "vs" + myPos2 + ".txt", "w+")

    fstart = ""

    for i in range(12,-1,-1):
        if range_array[12-i][12-i] == 100:
            f.write(fstart + idx_to_card[i] + idx_to_card[i])
            fstart = ","
        elif range_array[12-i][12-i] == 0:
            pass
        else:
            f.write(fstart + idx_to_card[i] + idx_to_card[i] + ":" + str(range_array[12-i][12-i]/100))
            fstart = ","

    for j in range(12,-1,-1):
        for i in range(12,-1,-1):
            if i == j:
                pass
            elif range_array[12-i][12-j] == 100:
                if i > j:
                    f.write(fstart + idx_to_card[i] + idx_to_card[j] + "o")
                else:
                    f.write(fstart + idx_to_card[j] + idx_to_card[i] + "s")
                fstart = ","
            elif range_array[12-i][12-j] == 0:
                pass
            else:
                if i > j:
                    f.write(fstart + idx_to_card[i] + idx_to_card[j] + "o" + ":" + str(range_array[12-i][12-j]/100))
                else:
                    f.write(fstart + idx_to_card[j] + idx_to_card[i] + "s" + ":" + str(range_array[12-i][12-j]/100))
                fstart = ","
    f.close()
    return

if __name__ == "__main__":
    app = PreflopTrain()
    app.mainloop()
