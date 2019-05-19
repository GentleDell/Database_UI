# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:41:17 2019

@author: Gentle Deng
"""
import cx_Oracle
import pandas as pd
import pandastable as pt
import tkinter as tk
from tkinter.messagebox import showinfo, askyesno
from tkinter import IntVar, Label, Entry, Button, W

TABEL_LIST = ['Amenities', 'Attributes',  'Avg_price',  'Calendar' ,
             'Capacity' , 'Hosts'     ,  'Listing'  ,  'Locations',
             'Obtain'   , 'Provide'   ,  'Requirements','Reviews' ,
             'Scores'   , 'Verifications', 'Verify'      ]

COLUNM_LIST = [['ame_id', 'amenities'],
               ['attr_id', 'property_type', 'room_type', 'accomodates', 
                'bathrooms', 'bedrooms', 'beds', 'bed_type', 'square_feet',
                'is_business_travel_ready'],
               ['avg_p_id', 'price', 'weekly_price', 'monthly_price', 
                'security_deposit', 'cleaning_fee'],
               ['list_id', 'date_', 'price'],
               ['cap_id', 'guests_included', 'extra_people',  
                'minimum_nights', 'maximum_nights'],
               ['host_id', 'host_url', 'host_name',  'host_since', 
                'host_response_time','host_response_rate','host_thumbnail_url',
                'host_picture_url', 'host_neighbourhood', 'host_about'],
               ['list_id', 'host_id', 'loc_id', 'cap_id', 'attr_id', 'req_id', 
                'avg_p_id', 'list_url', 'list_name',  'picture_url', 'latitude', 
                'longitude','dsummary','dspace', 'description', 'neighborhood_overview', 
                'notes', 'transit','daccess','interaction', 'house_rules'],
               ['loc_Id', 'country', 'country_code',  'city', 'city_name'],
               ['list_id', 'scor_id'],
               ['list_id', 'ame_id'],
               ['req_id', 'cancellation_policy', 'REQUIRE_GUEST_PROFILE_PICTURE', 'REQUIRE_GUEST_PHONE_VERIFICATION'],
               ['list_id', 'rev_id', 'date_',  'reviewer_id', 
                    'reviewer_name','comments'],
               ['scor_id', 'review_scores_rating', 'review_scores_accuracy',
                'review_scores_cleanliness'      , 'review_scores_checkin' , 
                'review_scores_communication'    , 'review_scores_location',
                'review_scores_value'],
               ['ver_id', 'verifications'],
               ['host_id', 'ver_id']]
               
TYPE_LIST = [# amenity
             ['int', 'str'],  
             # attribute
             ['int', 'str', 'str', 'int', 
              'int', 'int', 'int', 'str', 'float', 'str'],
             # avg_price
             ['int', 'str', 'str', 'str', 'str', 'str'],
             # calendar
             ['int', 'str', 'str'],
             # capacity
             ['int', 'int', 'str', 'int', 'int'],
             # host
              ['int', 'str', 'str',  'str', 'str','str','str','str', 'str', 'str'],
             # listing
             ['int', 'int', 'int', 'int', 'int', 'int', 'int', 'str', 'str',  'str', 'float', 
              'float','str','str', 'str', 'str', 'str', 'str','str','str', 'str'],
             # location
             ['int', 'str', 'str',  'str', 'str'],
             # obtain
             ['int', 'int'],
             # provide
             ['int', 'int'],
             # requirment
             ['int', 'str', 'str', 'str'],
             # review 
             ['int', 'int', 'str', 'int', 'str','str'],
             # score
             ['int', 'float', 'float', 'float', 'float' , 
              'float', 'float', 'float'],
             # verifications
             ['int', 'str'],
             # verify
             ['int', 'int']]

# In[]
def upload_query(query, bind_var):
    if askyesno('Attention', 'Really search for the value?'):
        showinfo('Yes', 'Searching the data')
        
        # connect to the server
        dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', service_name='ORCLCDB')
        conn = cx_Oracle.connect(user=r'C##DB2019_G19', password='DB2019_G19', dsn=dsn_tns)
                                 
        c = conn.cursor()
        c.execute(query, bind_var)
        results = c.fetchall()
        conn.close()        

        return results
        
    else:
        showinfo('No', 'Uploading has been cancelled')
        return -1

# In[]
def show_table(tabel):
    
    master_search = tk.Toplevel()
    master_search.title('Searching results')
    
    vis_table = pt.Table(parent = master_search, dataframe = tabel, showtoolbar=True, showstatusbar=True)
    vis_table.show()
    master_search.mainloop()
    
# In[]
# search values
def search_values(button_ind, list_of_attributes, list_of_entries):
    
    query = "select * from " + TABEL_LIST[button_ind] + ' where '
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
                
    tabel =  upload_query(query = query, bind_var=vars_dict)
    tabel = pd.DataFrame(tabel, columns = COLUNM_LIST[button_ind])
    show_table(tabel)
    
        
# In[]
def Search_Handler(button_ind):
    
    available_col = COLUNM_LIST[button_ind]
    
    master = tk.Tk()
    master.title('Search values in table {:s}'.format(TABEL_LIST[button_ind]))
    
    list_of_entries  = []
    
    for ind, attr in enumerate(available_col):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
       
    Button( master, text='Search',
            command=lambda: search_values(button_ind, available_col, list_of_entries))     \
    .grid(row=len(available_col), column=0, sticky=W, pady=4)   
    
    master.mainloop()

# In[]
# basic window

def Search(event):                           
    # create a new window
    Insert = tk.Tk() 
    
    # define the variable to get the button
    TABEL_Ind = IntVar(Insert)
    TABEL_Ind.set(0)
    
    # create labels                        
    tk.Label(Insert, 
             text='Choose the tabel conduct searching',
             justify = tk.CENTER,
             padx = 20).pack()

    for val, tabel in enumerate(TABEL_LIST):
        tk.Radiobutton(Insert, 
                      text=tabel,
                      indicatoron = 0,
                      width = 20,
                      padx = 20, 
                      variable=TABEL_Ind, 
                      command=lambda: Search_Handler(TABEL_Ind.get()),
                      value = val
                      ).pack(anchor=tk.W)
    Insert.mainloop()