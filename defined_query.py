# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:42:24 2019

@author: Gentle Deng
"""
import cx_Oracle
import pandastable as pt
import tkinter as tk
from tkinter.messagebox import showinfo, askyesno
from tkinter import IntVar

import pandas as pd
from constants import QUERY_LIST

NUM_QUERIES = 12
    

def show_table(tabel):
    
    master_search = tk.Toplevel()
    master_search.title('Outputs of predefined qurey')
    
    vis_table = pt.Table(parent = master_search, dataframe = tabel, showtoolbar=True, showstatusbar=True,  )
    vis_table.show()
    master_search.mainloop()

def upload_queries(index: int):
    if askyesno('Attention', 'Really upload?'):
        showinfo('Yes', 'Uploading the data')
        
        statement = QUERY_LIST[index][0]
        
        print('>>>> The query to be uploaded is:\n{:s}'.format(statement))
        
        # connect to the server
        dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', service_name='ORCLCDB')
        conn = cx_Oracle.connect(user=r'C##DB2019_G19', password='DB2019_G19', dsn=dsn_tns)
        
        c = conn.cursor()
        c.execute(statement)
        results = c.fetchall()
        conn.close()        
        
        results = pd.DataFrame(results)
        show_table(results)
        
    else:
        showinfo('No', 'Uploading has been cancelled')


def Def_Query(event):
    # create a new window
    Insert = tk.Tk()
    
    # define the variable to get the button
    TABEL_Ind = IntVar(Insert)
    TABEL_Ind.set(0)
    
    TABEL_LIST =[]
    for cnt in range(NUM_QUERIES):
        TABEL_LIST.append('Question{:d}'.format(cnt+1))
    
    # create labels                        
    tk.Label(Insert, 
             text='Choose the tabel you want to change',
             justify = tk.CENTER,
             padx = 20).pack()

    for val, tabel in enumerate(TABEL_LIST):
        tk.Radiobutton(Insert, 
                      text=tabel,
                      indicatoron = 0,
                      width = 20,
                      padx = 20, 
                      variable=TABEL_Ind, 
                      command=lambda: upload_queries(TABEL_Ind.get()),
                      value = val
                      ).pack(anchor=tk.W)
    Insert.mainloop()