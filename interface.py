# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:32:12 2019

@author: Gentle Deng
"""
import tkinter as tk
from tkinter import Button
from tkinter.messagebox import showinfo, showwarning, askyesno

from Insertion import Insertion
from deletion import Deletion
from searching import Search
from defined_query import Def_Query


def Quit(event):
    if askyesno('Warning', 'Really quit?'):
        showwarning('Yes', 'Not yet implemented')
    else:
        showinfo('No', 'Quit has been cancelled')


top_interface = tk.Tk()
top_interface.geometry("400x200+50+50") 
top_interface.title('Project for Database 2019')

Ins_Del_BT = Button(top_interface, text='Insertion', width=25)
Ins_Del_BT.bind('<Button-1>', Insertion)
Ins_Del_BT.grid(row=0, column=0)

Quit_BT = Button(top_interface, text='Deletion', width=25)
Quit_BT.bind('<Button-1>', Deletion) 
Quit_BT.grid(row=0, column=1)

Search_BT = Button(top_interface, text='Searching', width=25)
Search_BT.bind('<Button-1>', Search)
Search_BT.grid(row=1, column=0)

Query_BT = Button(top_interface, text='Predefined Queries', width=25)
Query_BT.bind('<Button-1>', Def_Query)
Query_BT.grid(row=1, column=1)

Quit_BT = Button(top_interface, text='Quit', width=25)
Quit_BT.bind('<Button-1>', Quit) 
Quit_BT.grid(row=4, column=0)

top_interface.mainloop()