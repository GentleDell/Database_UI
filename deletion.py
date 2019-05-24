# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:41:17 2019

@author: Gentle Deng
"""
import cx_Oracle
import tkinter as tk
from tkinter.messagebox import showinfo, askyesno
from tkinter import IntVar, Label, Entry, Button, W

from constants import TABEL_LIST, COLUNM_LIST, TYPE_LIST

# In[]
def upload_query(query, bind_var):
    if askyesno('Attention', 'Really Delete the tuples from the table?'):
        showinfo('Yes', 'Deleting the data')
        
        # connect to the server
        dsn_tns = cx_Oracle.makedsn('HOST', 'PORT', service_name='TOBEFILLED')
        conn = cx_Oracle.connect(user=r'USER_NAME', password='PASSWORDS', dsn=dsn_tns)
                                 
        c = conn.cursor()
        c.execute(query, bind_var)
        conn.commit()
        conn.close()        
    
# In[]
# search values
def delete_tuples(button_ind, list_of_attributes, list_of_entries):
    
    query = "delete from " + TABEL_LIST[button_ind] + ' where '
    vars_dict = {}
        
    for ind, attr in enumerate(list_of_attributes):
        if len(list_of_entries[ind].get()) != 0:
            query = query + attr + ' = :' + attr
            if TYPE_LIST[button_ind][ind] == 'str':
                vars_dict[attr] = list_of_entries[ind].get()
            elif TYPE_LIST[button_ind][ind] == 'int':
                vars_dict[attr] = int(list_of_entries[ind].get())
            elif TYPE_LIST[button_ind][ind] == 'float':
                vars_dict[attr] = float(list_of_entries[ind].get())
            else:
                raise ValueError('Unsupported data type')
                
    upload_query(query = query, bind_var=vars_dict)
    
        
# In[]
def Delete_Handler(button_ind):
    
    available_col = COLUNM_LIST[button_ind]
    
    master = tk.Tk()
    master.title('Delete tuples containing specific values')
    
    list_of_entries  = []
    
    for ind, attr in enumerate(available_col):
        Label(master, text=attr).grid(row=ind+1)
        entry = Entry(master)
        entry.grid(row=ind+1, column=1)
        list_of_entries.append(entry)
       
    Button( master, text='Delete',
            command=lambda: delete_tuples(button_ind, available_col, list_of_entries))     \
    .grid(row=len(available_col)+1, column=0, sticky=W, pady=4)   
    
    master.mainloop()

# In[]
# basic window

def Deletion(event):                           
    # create a new window
    Delete = tk.Tk() 
    
    # define the variable to get the button
    TABEL_Ind = IntVar(Delete)
    TABEL_Ind.set(0)
    
    # create labels                        
    tk.Label(Delete, 
             text='Choose the tabel to be changed',
             justify = tk.CENTER,
             padx = 20).pack()

    for val, tabel in enumerate(TABEL_LIST):
        tk.Radiobutton(Delete, 
                      text=tabel,
                      indicatoron = 0,
                      width = 20,
                      padx = 20, 
                      variable=TABEL_Ind, 
                      command=lambda: Delete_Handler(TABEL_Ind.get()),
                      value = val
                      ).pack(anchor=tk.W)
    Delete.mainloop()