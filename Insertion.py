# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:35:19 2019

@author: Gentle Deng
"""
import cx_Oracle
import tkinter as tk
from tkinter.messagebox import showinfo, askyesno
from tkinter import IntVar, Label, Entry, Button, Text, END, W

# In[]
def upload_query(tabel_name ,attributes, entries):
    
    if askyesno('Attention', 'Really upload?'):
        showinfo('Yes', 'Uploading the data')
        
        # connect to the server
        dsn_tns = cx_Oracle.makedsn('cs322-db.epfl.ch', '1521', service_name='ORCLCDB')
        conn = cx_Oracle.connect(user=r'C##DB2019_G19', password='DB2019_G19', dsn=dsn_tns)
                                 
        c = conn.cursor()
        
        statement = 'insert into {:s}('.format(tabel_name)
        for attr in attributes:
            statement = statement + attr + ','
        statement = statement[:-1]
        statement = statement + ') values ('
        for ct in range(len(entries)):
            statement = statement + ':{:d},'.format(ct + 2)
        statement = statement[:-1] + ')'
        
        c.execute(statement, tuple([item for item in entries]))
        conn.commit()
        conn.close()        
    else:
        showinfo('No', 'Uploading has been cancelled')


# In[insert tuples]
def intert_tuple(tabel_name: str, list_of_attributes: list, 
                 list_of_entries: list, list_of_text: list = [], 
                 int_index: list = [], float_ind: list = [], vis_text_ind: int = -1 ):
    
    entries = []
    
    # for separating text data
    if vis_text_ind == -1:
        vis_text_ind = len(list_of_attributes)
        
    for ct in range(len(list_of_attributes)):
        if ct < vis_text_ind:
            print(list_of_attributes[ct], 'is :', list_of_entries[ct].get())
        else:
            print(list_of_attributes[ct], 'is :', list_of_text[ct-vis_text_ind].get("1.0", 'end -1c'))
        
        if ct < len(list_of_entries):
            is_not_empty = len(list_of_entries[ct].get()) != 0
        else:
            is_not_empty = len(list_of_text[ct-vis_text_ind].get("1.0", 'end -1c')) != 0
        
        if ct in int_index and is_not_empty:
            entries.append(int(list_of_entries[ct].get()))
        elif ct in float_ind and is_not_empty:
            entries.append(float(list_of_entries[ct].get()))
        elif is_not_empty:
            if ct < vis_text_ind:
                entries.append(list_of_entries[ct].get())
            else:
                entries.append(list_of_text[ct - vis_text_ind].get("1.0", 'end -1c'))
        else:
            entries.append(None)
        
    upload_query(tabel_name, list_of_attributes, entries)
        
    for entry in list_of_entries:
        entry.delete(0,END)
    for text in list_of_text:
        text.delete('1.0',END)

# In[Amenities]
def Ins_amenities_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "amenities"')
    
    list_of_attr = ['ame_id', 'amenities']
    
    list_of_entries = [] 
    
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
        
    list_of_entries[0].insert(10,'0')
    list_of_entries[1].insert(10,'TV')
            
    num_index = [0]
    
    Button( master, text='Upload',
            command=lambda: intert_tuple(tabel_name='amenities',  
                                         list_of_attributes=list_of_attr, 
                                         list_of_entries=list_of_entries, 
                                         int_index=num_index) )     \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    
    master.mainloop()

# In[Attributes]
def Ins_attributes_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "attributes"')
    
    list_of_attr = ['attr_id', 'property_type', 'room_type', 'accomodates', 
                    'bathrooms', 'bedrooms', 'beds', 'bed_type', 'square_feet',
                    'is_business_travel_ready']
    
    list_of_entries = [] 
    
    for ind, attr in enumerate(list_of_attr):
            Label(master, text=attr).grid(row=ind)
            entry = Entry(master)
            entry.grid(row=ind, column=1)
            list_of_entries.append(entry)
            
    int_index = [0,3,4,5,6]
    float_ind = [8]
            
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='attributes', 
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index,
                                        float_ind=float_ind) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Avg_price]
def Ins_avg_price_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "avg_price"')
    
    list_of_attr = ['avg_p_id', 'price', 'weekly_price', 'monthly_price', 
                    'security_deposit', 'cleaning_fee']
    
    list_of_entries = [] 
    
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
    
    list_of_entries[0].insert(10,'16961')
    list_of_entries[1].insert(10,'$29.00')
    list_of_entries[2].insert(10,'$240.00')
    list_of_entries[3].insert(10,'$675.00')
    list_of_entries[4].insert(10,'$85.00')
    list_of_entries[5].insert(10,'$0.00')
    
    int_index = [0]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='avg_price', 
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Calendar]
def Ins_calendar_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "calendar"')
    
    list_of_attr = ['list_id', 'date_', 'price']
    
    list_of_entries = [] 
    
    for ind, attr in enumerate(list_of_attr):
            Label(master, text=attr).grid(row=ind)
            entry = Entry(master)
            entry.grid(row=ind, column=1)
            list_of_entries.append(entry)
            
    list_of_entries[0].insert(10,'259249')
    list_of_entries[1].insert(10,'2019-06-29')
    list_of_entries[2].insert(10,'$50.00')
            
    int_index = [0]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='calendar',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)
    master.mainloop()

# In[Capacity]
def Ins_capacity_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "capacity"')
    
    list_of_attr = ['cap_id', 'guests_included', 'extra_people',  
                    'minimum_nights', 'maximum_nights']
    
    list_of_entries = [] 
    
    for ind, attr in enumerate(list_of_attr):
            Label(master, text=attr).grid(row=ind)
            entry = Entry(master)
            entry.grid(row=ind, column=1)
            list_of_entries.append(entry)
        
    list_of_entries[0].insert(10,'1154')
    list_of_entries[1].insert(10,'1')
    list_of_entries[2].insert(10,'$0.00')
    list_of_entries[3].insert(10,'28')
    list_of_entries[4].insert(10,'1124')
            
    int_index = [0,1,3,4]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='capacity',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Hosts]
def Ins_host_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "hosts"')
    
    list_of_attr = ['host_id', 'host_url', 'host_name',  'host_since', 
                    'host_response_time','host_response_rate','host_thumbnail_url',
                    'host_picture_url', 'host_neighbourhood', 'host_about']
    
    list_of_entries = []
    list_of_text = []   
    
    int_index = [0,1,3,4]
    vis_text_ind = 9
    
    for ind, attr in enumerate(list_of_attr):
        if ind < vis_text_ind:
            Label(master, text=attr).grid(row=ind)
            entry = Entry(master)
            entry.grid(row=ind, column=1)
            list_of_entries.append(entry)
        else:
            Label(master, text=attr).grid(row=ind, column = 1)
            text = Text(master, width=35, height=5)
            text.grid(row=ind, column=1)
            list_of_text.append(text)
        
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='hosts',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        list_of_text=list_of_text,
                                        int_index=int_index,
                                        vis_text_ind=vis_text_ind) )\
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Listing]  
def Ins_listing_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "listing"')
    
    list_of_attr = ['list_id', 'host_id', 'loc_id', 'cap_id', 'attr_id', 'req_id', 
                    'avg_p_id', 'list_url', 'list_name',  'picture_url', 'latitude', 
                    'longitude','dsummary','dspace', 'description', 'neighborhood_overview', 
                    'notes', 'transit','daccess','interaction', 'house_rules']
    
    list_of_entries = []
    list_of_text = []   
    vis_text_ind = 12
    
    for ind, attr in enumerate(list_of_attr):
        if ind < vis_text_ind:
            Label(master, text=attr).grid(row=ind)
            entry = Entry(master)
            entry.grid(row=ind, column=1)
            list_of_entries.append(entry)
        else:
            Label(master, text=attr).grid(row=ind-vis_text_ind, column = 2)
            text = Text(master, width=35, height=4)
            text.grid(row=ind - vis_text_ind, column=3)
            list_of_text.append(text)
          
    int_index = [0,1,2,3,4,5,6]
    float_ind = [10,11]  
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name = 'listing',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        list_of_text=list_of_text,
                                        int_index=int_index,
                                        float_ind=float_ind,
                                        vis_text_ind=vis_text_ind) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Location]
def Ins_Locations_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "locations"')
    
    list_of_attr = ['loc_Id', 'country', 'country_code',  'city', 'city_name']
    
    list_of_entries = []   
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
          
    list_of_entries[0].insert(10,'1')
    list_of_entries[1].insert(10,'Spain')
    list_of_entries[2].insert(10,'ES')
    list_of_entries[3].insert(10,'chiva')
    list_of_entries[4].insert(10,'madrid')
    
    int_index = [0]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='locations',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index)) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Obtain]
def Ins_Obtain_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "obtain"')
    
    list_of_attr = ['list_id', 'scor_id']
    
    list_of_entries = []   
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
    
    list_of_entries[0].insert(10,'7059846')
    list_of_entries[1].insert(10,'24')

    int_index = [0,1]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='obtain',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index)) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Provide]
def Ins_Provide_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "provide"')
    
    list_of_attr = ['list_id', 'ame_id']
    
    list_of_entries = []   
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
    
    list_of_entries[0].insert(10,'282715')
    list_of_entries[1].insert(10,'74')

    int_index = [0,1]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='provide',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Requirements]  
def Ins_Requirements_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "requirements"')
    
    list_of_attr = ['req_id', 'cancellation_policy', 'REQUIRE_GUEST_PROFILE_PICTURE', 'REQUIRE_GUEST_PHONE_VERIFICATION']
    
    list_of_entries = []   
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
    
    list_of_entries[0].insert(10,'0')
    list_of_entries[1].insert(10,'strict_14_with_grace_period')
    list_of_entries[2].insert(10,'f')
    list_of_entries[3].insert(10,'f')
       
    int_index = [0]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='requirements',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()    

# In[Reviews]
def Ins_Review_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "reviews"')
    
    list_of_attr = ['list_id', 'rev_id', 'date_',  'reviewer_id', 
                    'reviewer_name','comments']
    
    int_index = [0,1,3]    
    vis_text_ind = 5
    list_of_entries = []
    list_of_text = []   
    
    for ind, attr in enumerate(list_of_attr):
        if ind < vis_text_ind:
            Label(master, text=attr).grid(row=ind)
            entry = Entry(master)
            entry.grid(row=ind, column=1)
            list_of_entries.append(entry)
        else:
            Label(master, text=attr).grid(row=ind, column = 1)
            text = Text(master, width=50, height=20)
            text.grid(row=ind, column=1)
            list_of_text.append(text)
            
    list_of_entries[0].insert(10,'8719352')
    list_of_entries[1].insert(10,'54151832')
    list_of_entries[2].insert(10,'2015-11-16')
    list_of_entries[3].insert(10,'6007606')
    list_of_entries[4].insert(10,'Jan')
    list_of_text[0].insert(END,'Marta"s home was just as described and perfect for our stay.\
The location is exactly what you want for Madrid and close to San Miguel market which\
is a fabulous place to eat tapas and mingle with locals and tourists. Easy arrival on\
the subway as well.Marta was very helpful and pleasant.A great host.')
          
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name = 'reviews',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        list_of_text=list_of_text,
                                        int_index=int_index,
                                        vis_text_ind=vis_text_ind) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()

# In[Score]  
def Ins_Score_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "scores"')
    
    list_of_attr = ['scor_id', 'review_scores_rating', 'review_scores_accuracy',
                    'review_scores_cleanliness'      , 'review_scores_checkin' , 
                    'review_scores_communication'    , 'review_scores_location',
                    'review_scores_value']
    
    int_index = [0]
    float_ind = [1,2,3,4,5,6,7]
    list_of_entries = []   
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
    
    list_of_entries[0].insert(10,'0')
    list_of_entries[1].insert(10,'90')
    list_of_entries[2].insert(10,'9')
    list_of_entries[3].insert(10,'9')
    list_of_entries[4].insert(10,'9')
    list_of_entries[5].insert(10,'9')
    list_of_entries[6].insert(10,'10')
    list_of_entries[7].insert(10,'9')
          
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='scores',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index,
                                        float_ind=float_ind) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()    

# In[Verification]
def Ins_Verifications_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "verifications"')
    
    list_of_attr = ['ver_id', 'verifications']
    
    list_of_entries = []   
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
    
    list_of_entries[0].insert(10,'0')
    list_of_entries[1].insert(10,'email')
        
    int_index = [0]
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='verifications',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()
    
# In[verify]
def Ins_Verify_Handler():
    master = tk.Tk()
    master.title('Insert a tuple into "verify"')
    
    list_of_attr = ['host_id', 'ver_id']
    
    list_of_entries = []   
    for ind, attr in enumerate(list_of_attr):
        Label(master, text=attr).grid(row=ind)
        entry = Entry(master)
        entry.grid(row=ind, column=1)
        list_of_entries.append(entry)
    
    list_of_entries[0].insert(10,'1331093')
    list_of_entries[1].insert(10,'0')
    
    int_index = [0,1]    
    
    Button(master, text='Upload', 
           command=lambda: intert_tuple(tabel_name='verify',
                                        list_of_attributes=list_of_attr, 
                                        list_of_entries=list_of_entries,
                                        int_index=int_index) ) \
    .grid(row=len(list_of_attr), column=0, sticky=W, pady=4)   
    master.mainloop()
    
# In[]
# basic window
    
TABEL_LIST =['Amenities', 'Attributes',  'Avg_price',  'Calendar' ,
             'Capacity' , 'Hosts'     ,  'Listing'  ,  'Locations',
             'Obtain'   , 'Provide'   ,  'Requirements','Reviews' ,
             'Scores'   , 'Verifications', 'Verify'      ]

Ins_Handler = [Ins_amenities_Handler,  Ins_attributes_Handler,  Ins_avg_price_Handler,
               Ins_calendar_Handler ,  Ins_capacity_Handler  ,  Ins_host_Handler     ,
               Ins_listing_Handler  ,  Ins_Locations_Handler ,  Ins_Obtain_Handler   ,
               Ins_Provide_Handler  ,  Ins_Requirements_Handler,Ins_Review_Handler   , 
               Ins_Score_Handler    ,  Ins_Verifications_Handler,Ins_Verify_Handler  ]
    
def Insertion(event):
    # create a new window
    Insert = tk.Tk()
    
    # define the variable to get the button
    TABEL_Ind = IntVar(Insert)
    TABEL_Ind.set(0)
    
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
                      command=lambda: Ins_Handler[TABEL_Ind.get()](),
                      value = val
                      ).pack(anchor=tk.W)
    Insert.mainloop()